"""
Tropical Downloader - Core yt-dlp Download Worker
Integrates 100% yt-dlp parsing, Anti-429 protection, +10% Disk space safety check,
RAM buffering, auto-purge node_modules on low disk space, and 10s auto-detect waiting signal.
"""
import os
import shlex
import tempfile
import shutil
import yt_dlp
from PySide6.QtCore import QThread, Signal
from core.config import config_manager
from core.cookie_manager import get_cookie_options
from core.history_manager import history_manager
from core.disk_manager import has_sufficient_space, purge_node_modules


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
    progress_signal = Signal(str, float, str, str, int, int, str)
    log_signal      = Signal(str, str)
    finished_signal = Signal(str, str, str)
    error_signal    = Signal(str, str)
    # Signal emitted when disk space is low and user action / wait is required
    disk_space_required_signal = Signal(str, str, int)  # task_id, dl_dir, required_bytes

    def __init__(self, task_id: str, url: str,
                 options_override: dict = None, custom_args: str = ""):
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.options_override = options_override or {}
        self.custom_args = custom_args
        self._canceled = False
        self._disk_wait_event_handled = False

    def cancel(self):
        self._canceled = True

    def notify_space_freed(self):
        self._disk_wait_event_handled = True

    def run(self):
        try:
            ydl_opts = self._build_opts()
            dl_dir = self.options_override.get("download_path") or config_manager.get("download_path")
            os.makedirs(dl_dir, exist_ok=True)

            self.log_signal.emit(self.task_id, f"[정보] 미디어 분석 및 저장공간 확인 중: {self.url}")

            # 1. Estimate file size & check disk space with +10% margin
            with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'nocheckcertificate': True}) as info_ydl:
                try:
                    meta = info_ydl.extract_info(self.url, download=False) or {}
                    est_bytes = meta.get('filesize') or meta.get('filesize_approx') or (100 * 1024 * 1024)
                except Exception:
                    est_bytes = 100 * 1024 * 1024

            has_space, free_b, req_b = has_sufficient_space(dl_dir, est_bytes, safety_margin=0.10)

            # 2. Low disk space handling
            if not has_space:
                self.log_signal.emit(
                    self.task_id,
                    f"[저장공간 경고] 필요 공간(+10% 여유분 포함): {req_b / 1048576:.1f} MB, "
                    f"현재 잔여 디스크: {free_b / 1048576:.1f} MB"
                )

                # Auto-purge node_modules if enabled in settings
                if config_manager.get("auto_purge_node_modules", True):
                    self.log_signal.emit(self.task_id, "[저장공간 확보] node_modules 자동 영구 삭제를 병렬 실행합니다.")
                    freed = purge_node_modules(log_callback=lambda msg: self.log_signal.emit(self.task_id, msg))
                    self.log_signal.emit(self.task_id, f"[저장공간 확보 결과] 총 {freed / 1048576:.1f} MB 확보 완료")
                    has_space, free_b, req_b = has_sufficient_space(dl_dir, est_bytes, safety_margin=0.10)

                # If still low, fallback to RAM / temp buffer
                if not has_space:
                    self.log_signal.emit(self.task_id, "[RAM 보관 모드] 디스크 용량이 부족하여 RAM/임시 메모리 버퍼로 다운로드를 수신합니다.")
                    ram_tmp_dir = tempfile.mkdtemp(prefix="tropical_ram_")
                    orig_outtmpl = ydl_opts["outtmpl"]
                    if isinstance(orig_outtmpl, str):
                        ydl_opts["outtmpl"] = os.path.join(ram_tmp_dir, os.path.basename(orig_outtmpl))

            # 3. Perform Download
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

            # 4. Post-download final disk check & space freed dialog wait if needed
            if filepath and os.path.exists(filepath):
                file_size = os.path.getsize(filepath)
                has_space, free_b, req_b = has_sufficient_space(dl_dir, file_size, safety_margin=0.10)

                if not has_space:
                    self.log_signal.emit(self.task_id, "[저장공간 비움 대기] 완료된 미디어를 저장하기 위해 사용자 저장공간 비움 대기 알림창을 표출합니다.")
                    self.disk_space_required_signal.emit(self.task_id, dl_dir, req_b)
                    
                    # Wait until user or 10-second timer frees space
                    while not self._disk_wait_event_handled and not self._canceled:
                        self.msleep(500)
                        has_space_now, _, _ = has_sufficient_space(dl_dir, file_size, safety_margin=0.10)
                        if has_space_now:
                            break

                # If download was buffered in RAM temp dir, move to final download dir
                if "ram_tmp_dir" in locals() and os.path.exists(ram_tmp_dir):
                    final_dest = os.path.join(dl_dir, os.path.basename(filepath))
                    shutil.move(filepath, final_dest)
                    filepath = final_dest
                    shutil.rmtree(ram_tmp_dir, ignore_errors=True)

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

        adv_opts: dict = ov.pop("_adv_opts", {}) or {}
        opts = dict(adv_opts)

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

        if not ov.get("extract_audio"):
            opts.setdefault("merge_output_format", cfg.get("merge_output_format", "mkv"))

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

        opts["getcomments"] = ov.get("write_comments", cfg.get("write_comments", True))
        opts["writedescription"] = ov.get("write_description", cfg.get("write_description", True))
        opts["writeinfojson"] = ov.get("write_info_json", cfg.get("write_info_json", True))

        if ov.get("embed_subs", cfg.get("embed_subs", True)):
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            sub_langs_str = cfg.get("sub_langs", "ko,en.*")
            opts["subtitleslangs"] = sub_langs_str.split(",") if isinstance(sub_langs_str, str) else sub_langs_str

        if ov.get("playlist_range"):
            opts["playlist_items"] = ov["playlist_range"]
        elif ov.get("playlist_items"):
            opts["playlist_items"] = ov["playlist_items"]

        # Automatic Cookies Detection & Integration
        browser = ov.get("cookie_browser") or cfg.get("cookie_browser", "auto")
        cfile   = ov.get("cookies_file")   or cfg.get("cookies_file", "")
        opts.update(get_cookie_options(browser, cfile))

        if ov.get("username") or cfg.get("username"):
            opts["username"] = ov.get("username") or cfg.get("username")
        if ov.get("password") or cfg.get("password"):
            opts["password"] = ov.get("password") or cfg.get("password")

        # Anti-429 Rate Limit Avoidance & Anti-Bot protection
        sleep_min = cfg.get("sleep_interval", 1)
        sleep_max = cfg.get("max_sleep_interval", 3)
        opts["sleep_interval"] = float(sleep_min)
        opts["max_sleep_interval"] = float(sleep_max)
        opts["sleep_interval_subtitles"] = 1.0

        opts["retries"] = cfg.get("retries", 10)
        opts["fragment_retries"] = 10
        opts["file_access_retries"] = 3
        opts["extractor_retries"] = 3

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

        ffmpeg = cfg.get("ffmpeg_path", "")
        if ffmpeg and os.path.exists(ffmpeg):
            opts["ffmpeg_location"] = ffmpeg

        opts.update({
            "progress_hooks":    [self._progress_hook],
            "logger":            YtDlpLogger(self.log_signal.emit, self.task_id),
            "nocheckcertificate": True,
            "ignoreerrors":       "only_download",
        })
        opts.setdefault("nooverwrites", cfg.get("no_overwrites", True))

        cli_args = self.custom_args or cfg.get("custom_cli_args", "")
        if cli_args:
            self._parse_and_apply_official_cli(opts, cli_args)

        return opts

    def _parse_and_apply_official_cli(self, opts: dict, cli_args_str: str):
        try:
            tokens = shlex.split(cli_args_str)
            parsed = yt_dlp.parse_options(tokens)
            cli_opts = parsed.ydl_opts
            for key, val in cli_opts.items():
                if val is not None and key not in ("outtmpl", "progress_hooks", "logger"):
                    opts[key] = val
        except Exception as e:
            self.log_signal.emit(self.task_id, f"[CLI 경고] 사용자 인자 파싱 오류: {e}")

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
