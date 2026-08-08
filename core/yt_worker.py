"""
Tropical Downloader - Core yt-dlp Download Worker
Features 100% yt-dlp option parsing via official yt_dlp.parse_options,
robust Anti-429 Rate Limit Avoidance, and default comment/description saving.
"""
import os
import shlex
import yt_dlp
from PySide6.QtCore import QThread, Signal
from core.config import config_manager
from core.cookie_manager import get_cookie_options
from core.history_manager import history_manager


# ── Logger ────────────────────────────────────────────────────────────────────
class YtDlpLogger:
    def __init__(self, cb, task_id: str):
        self._cb = cb
        self._tid = task_id

    def debug(self, msg):
        self._cb(self._tid, msg)

    def info(self, msg):
        self._cb(self._tid, msg)

    def warning(self, msg):
        self._cb(self._tid, f"[경고] {msg}")

    def error(self, msg):
        self._cb(self._tid, f"[오류] {msg}")


# ── Worker ────────────────────────────────────────────────────────────────────
class DownloadWorker(QThread):
    # (task_id, percent, speed_str, eta_str, downloaded_bytes, total_bytes, status)
    progress_signal = Signal(str, float, str, str, int, int, str)
    log_signal      = Signal(str, str)       # task_id, line
    finished_signal = Signal(str, str, str)  # task_id, filepath, title
    error_signal    = Signal(str, str)       # task_id, message

    def __init__(self, task_id: str, url: str,
                 options_override: dict = None, custom_args: str = ""):
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.options_override = options_override or {}
        self.custom_args = custom_args
        self._canceled = False

    def cancel(self):
        self._canceled = True

    # ── Main run ──────────────────────────────────────────────────────────────
    def run(self):
        try:
            ydl_opts = self._build_opts()
            self.log_signal.emit(self.task_id, f"[정보] 다운로드 진행 중: {self.url}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)

            if self._canceled:
                self.error_signal.emit(self.task_id, "사용자가 취소했습니다.")
                return

            title = "Downloaded Media"
            filepath = ""
            if info:
                title = info.get("title", title)
                if info.get("requested_downloads"):
                    filepath = info["requested_downloads"][0].get("filepath", "") or \
                               info["requested_downloads"][0].get("_filename", "")
                if not filepath:
                    try:
                        filepath = ydl.prepare_filename(info)
                    except Exception:
                        filepath = ydl_opts.get("outtmpl", "")

            size_str = "?"
            if filepath and os.path.exists(filepath):
                size_str = f"{os.path.getsize(filepath) / 1048576:.1f} MB"

            history_manager.add_entry(
                title=title,
                url=self.url,
                format_str=str(ydl_opts.get("format", "")),
                file_path=filepath,
                file_size=size_str,
            )

            self.progress_signal.emit(self.task_id, 100.0, "완료", "00:00", 0, 0, "FINISHED")
            self.finished_signal.emit(self.task_id, filepath, title)

        except Exception as exc:
            if not self._canceled:
                self.error_signal.emit(self.task_id, str(exc))

    # ── Option builder ────────────────────────────────────────────────────────
    def _build_opts(self) -> dict:
        ov = self.options_override.copy()
        cfg = config_manager

        # 1. Advanced tab options if passed
        adv_opts: dict = ov.pop("_adv_opts", {}) or {}
        opts = dict(adv_opts)

        # 2. Output path
        dl_dir = ov.get("download_path") or cfg.get("download_path",
                        os.path.join(os.path.expanduser("~"), "Downloads", "Tropical"))
        os.makedirs(dl_dir, exist_ok=True)

        tmpl = (ov.get("output_template")
                or opts.get("outtmpl")
                or cfg.get("filename_template", "%(title)s [%(id)s].%(ext)s"))
        if isinstance(tmpl, dict):
            opts["outtmpl"] = tmpl
        else:
            opts["outtmpl"] = os.path.join(dl_dir, tmpl)

        # 3. Format / quality
        if ov.get("extract_audio"):
            audio_fmt = ov.get("audio_format", "mp3")
            audio_q   = ov.get("audio_quality", "320")
            opts["format"] = "bestaudio/best"
            pp = opts.get("postprocessors", [])
            pp.insert(0, {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_fmt,
                "preferredquality": audio_q,
            })
            opts["postprocessors"] = pp
        elif ov.get("format"):
            opts["format"] = ov["format"]
        else:
            opts.setdefault("format", "bestvideo+bestaudio/best")

        # 4. Merge container
        if not ov.get("extract_audio"):
            opts.setdefault("merge_output_format", cfg.get("merge_output_format", "mkv"))

        # 5. Metadata, Thumbnail, Description, Info-JSON, Comments (Default enabled)
        pp = opts.get("postprocessors", [])
        pp_keys = {p.get("key") for p in pp if isinstance(p, dict)}

        if ov.get("embed_metadata", cfg.get("embed_metadata", True)):
            if "FFmpegMetadata" not in pp_keys:
                pp.append({"key": "FFmpegMetadata"})

        if ov.get("embed_thumbnail", cfg.get("embed_thumbnail", True)):
            if "EmbedThumbnail" not in pp_keys:
                pp.append({"key": "EmbedThumbnail"})
            opts["writethumbnail"] = True

        opts["postprocessors"] = pp

        # 기본 댓글 / 설명 / info.json 저장 설정
        opts["getcomments"] = ov.get("write_comments", cfg.get("write_comments", True))
        opts["writedescription"] = ov.get("write_description", cfg.get("write_description", True))
        opts["writeinfojson"] = ov.get("write_info_json", cfg.get("write_info_json", True))

        # 6. Subtitles
        if ov.get("embed_subs", cfg.get("embed_subs", True)):
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            sub_langs_str = cfg.get("sub_langs", "ko,en.*")
            opts["subtitleslangs"] = sub_langs_str.split(",") if isinstance(sub_langs_str, str) else sub_langs_str

        # 7. Playlist items / range
        if ov.get("playlist_range"):
            opts["playlist_items"] = ov["playlist_range"]
        elif ov.get("playlist_items"):
            opts["playlist_items"] = ov["playlist_items"]

        # 8. Cookies & Authentication
        browser = ov.get("cookie_browser") or cfg.get("cookie_browser", "")
        cfile   = ov.get("cookies_file")   or cfg.get("cookies_file", "")
        opts.update(get_cookie_options(browser, cfile))

        if ov.get("username") or cfg.get("username"):
            opts["username"] = ov.get("username") or cfg.get("username")
        if ov.get("password") or cfg.get("password"):
            opts["password"] = ov.get("password") or cfg.get("password")

        # 9. Anti-429 Rate Limit Avoidance & Anti-Bot protection
        sleep_min = cfg.get("sleep_interval", 1)
        sleep_max = cfg.get("max_sleep_interval", 3)
        opts["sleep_interval"] = float(sleep_min)
        opts["max_sleep_interval"] = float(sleep_max)
        opts["sleep_interval_subtitles"] = 1.0

        opts["retries"] = cfg.get("retries", 10)
        opts["fragment_retries"] = 10
        opts["file_access_retries"] = 3
        opts["extractor_retries"] = 3

        # YouTube Player Clients fallbacks
        player_clients = cfg.get("player_clients", "android,ios,web,mweb,tv")
        client_list = [c.strip() for c in player_clients.split(",") if c.strip()]
        if "extractor_args" not in opts:
            opts["extractor_args"] = {}
        if "youtube" not in opts["extractor_args"]:
            opts["extractor_args"]["youtube"] = {}
        opts["extractor_args"]["youtube"]["player_client"] = client_list

        proxy = ov.get("proxy") or cfg.get("proxy", "")
        if proxy:
            opts["proxy"] = proxy

        rate = cfg.get("rate_limit", "")
        if rate:
            opts["ratelimit"] = rate

        opts.setdefault("socket_timeout", cfg.get("socket_timeout", 30))
        opts.setdefault("geo_bypass", cfg.get("geo_bypass", True))

        # 10. FFmpeg location
        ffmpeg = cfg.get("ffmpeg_path", "")
        if ffmpeg and os.path.exists(ffmpeg):
            opts["ffmpeg_location"] = ffmpeg

        # 11. General
        opts.update({
            "progress_hooks":    [self._progress_hook],
            "logger":            YtDlpLogger(self.log_signal.emit, self.task_id),
            "nocheckcertificate": True,
            "ignoreerrors":       "only_download",
        })
        opts.setdefault("nooverwrites", cfg.get("no_overwrites", True))

        # 12. Parse 100% full yt-dlp CLI arguments via official parse_options
        cli_args = self.custom_args or cfg.get("custom_cli_args", "")
        if cli_args:
            self._parse_and_apply_official_cli(opts, cli_args)

        return opts

    def _parse_and_apply_official_cli(self, opts: dict, cli_args_str: str):
        """Uses yt_dlp.parse_options to achieve 100% yt-dlp CLI feature compatibility."""
        try:
            tokens = shlex.split(cli_args_str)
            parsed = yt_dlp.parse_options(tokens)
            cli_opts = parsed.ydl_opts
            
            # Merge non-default/explicitly passed options into opts
            for key, val in cli_opts.items():
                if val is not None and key not in ("outtmpl", "progress_hooks", "logger"):
                    opts[key] = val
            self.log_signal.emit(self.task_id, f"[CLI 파서] 사용자 커스텀 인자 {len(tokens)}개 100% 적용 완료")
        except Exception as e:
            self.log_signal.emit(self.task_id, f"[CLI 경고] 사용자 인자 파싱 오류: {e}")

    # ── Progress hook ─────────────────────────────────────────────────────────
    def _progress_hook(self, d: dict):
        if self._canceled:
            raise Exception("Download Canceled")

        status = d.get("status", "")
        if status == "downloading":
            dl   = d.get("downloaded_bytes", 0) or 0
            tot  = d.get("total_bytes") or d.get("total_bytes_estimate", 0) or 0
            pct  = (dl / tot * 100.0) if tot else 0.0
            spd  = d.get("speed") or 0
            eta  = d.get("eta") or 0
            spd_s = f"{spd/1048576:.2f} MB/s" if spd else "-- MB/s"
            eta_s = f"{eta//60:02d}:{eta%60:02d}" if eta else "--:--"
            self.progress_signal.emit(
                self.task_id, pct, spd_s, eta_s, dl, tot, "DOWNLOADING")
        elif status == "finished":
            self.progress_signal.emit(
                self.task_id, 99.0, "처리 중…", "00:00", 0, 0, "PROCESSING")
