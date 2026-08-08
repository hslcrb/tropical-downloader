"""
Tropical Downloader - Core yt-dlp Download Worker
Merges all settings from AdvancedTab.get_ydl_opts() with per-job overrides.
Custom CLI args cover any option not otherwise exposed.
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
        self._cb(self._tid, f"[WARNING] {msg}")

    def error(self, msg):
        self._cb(self._tid, f"[ERROR] {msg}")


# ── Worker ────────────────────────────────────────────────────────────────────
class DownloadWorker(QThread):
    # (task_id, percent, speed_str, eta_str, downloaded_bytes, total_bytes, status)
    progress_signal = Signal(str, float, str, str, int, int, str)
    log_signal      = Signal(str, str)   # task_id, line
    finished_signal = Signal(str, str, str)  # task_id, filepath, title
    error_signal    = Signal(str, str)   # task_id, message

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
            self.log_signal.emit(self.task_id, f"[INFO] 다운로드 시작: {self.url}")

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
                    filepath = ydl_opts.get("outtmpl", "")

            size_str = "?"
            if filepath and os.path.exists(filepath):
                size_str = f"{os.path.getsize(filepath) / 1048576:.1f} MB"

            history_manager.add_entry(
                title=title,
                url=self.url,
                format_str=ydl_opts.get("format", ""),
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
        ov = self.options_override
        cfg = config_manager

        # ── 1. Start from advanced tab settings if available ──────────────────
        # (AdvancedTab.get_ydl_opts() is called lazily from main window)
        adv_opts: dict = ov.pop("_adv_opts", {}) or {}
        opts = dict(adv_opts)   # copy

        # ── 2. Output path ────────────────────────────────────────────────────
        dl_dir = ov.get("download_path") or cfg.get("download_path",
                        os.path.join(os.path.expanduser("~"), "Downloads"))
        os.makedirs(dl_dir, exist_ok=True)

        tmpl = (ov.get("output_template")
                or opts.get("outtmpl")
                or cfg.get("output_template", "%(title)s.%(ext)s"))
        opts["outtmpl"] = os.path.join(dl_dir, tmpl)

        # ── 3. Format / quality ───────────────────────────────────────────────
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

        # ── 4. Merge container ────────────────────────────────────────────────
        if not ov.get("extract_audio"):
            opts.setdefault("merge_output_format",
                            cfg.get("merge_output_format", "mkv"))

        # ── 5. Postprocessors (metadata / thumbnail) ──────────────────────────
        pp = opts.get("postprocessors", [])
        pp_keys = {p["key"] for p in pp}

        if ov.get("embed_metadata", cfg.get("embed_metadata", True)):
            if "FFmpegMetadata" not in pp_keys:
                pp.append({"key": "FFmpegMetadata"})

        if ov.get("embed_thumbnail", cfg.get("embed_thumbnail", True)):
            if "EmbedThumbnail" not in pp_keys:
                pp.append({"key": "EmbedThumbnail"})
            opts["writethumbnail"] = True

        opts["postprocessors"] = pp

        # ── 6. Subtitles ──────────────────────────────────────────────────────
        if ov.get("embed_subs", cfg.get("embed_subs", False)):
            opts["writesubtitles"]  = True
            opts["writeautomaticsub"] = True
            opts.setdefault("subtitleslangs",
                            cfg.get("sub_langs", "ko,en.*").split(","))

        # ── 7. Playlist range (from override — playlist tab) ──────────────────
        if ov.get("playlist_range"):
            opts["playlist_items"] = ov["playlist_range"]
        elif ov.get("playlist_items"):
            opts["playlist_items"] = ov["playlist_items"]

        # ── 8. Cookies & auth ─────────────────────────────────────────────────
        browser = ov.get("cookie_browser") or cfg.get("cookie_browser", "")
        cfile   = ov.get("cookies_file")   or cfg.get("cookies_file", "")
        opts.update(get_cookie_options(browser, cfile))

        if ov.get("username") or cfg.get("username"):
            opts["username"] = ov.get("username") or cfg.get("username")
        if ov.get("password") or cfg.get("password"):
            opts["password"] = ov.get("password") or cfg.get("password")

        # ── 9. Network ────────────────────────────────────────────────────────
        proxy = ov.get("proxy") or cfg.get("proxy", "")
        if proxy:
            opts["proxy"] = proxy

        rate = cfg.get("rate_limit", "")
        if rate:
            opts["ratelimit"] = rate

        opts.setdefault("retries", cfg.get("retries", 10))
        opts.setdefault("socket_timeout", cfg.get("socket_timeout", 30))

        # ── 10. Geo-bypass (default on for convenience) ───────────────────────
        opts.setdefault("geo_bypass", cfg.get("geo_bypass", True))

        # ── 11. FFmpeg location ───────────────────────────────────────────────
        ffmpeg = cfg.get("ffmpeg_path", "")
        if ffmpeg and os.path.exists(ffmpeg):
            opts["ffmpeg_location"] = ffmpeg

        # ── 12. General ───────────────────────────────────────────────────────
        opts.update({
            "progress_hooks":    [self._progress_hook],
            "logger":            YtDlpLogger(self.log_signal.emit, self.task_id),
            "nocheckcertificate": True,
            "extractor_args": {
                "youtube": {
                    "player_client": ["android", "ios", "web"]
                }
            },
        })
        opts.setdefault("nooverwrites", cfg.get("no_overwrites", True))

        # ── 13. Custom CLI pass-through ───────────────────────────────────────
        cli = self.custom_args or cfg.get("custom_cli_args", "")
        if cli:
            self._apply_cli(opts, cli)

        return opts

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

    # ── CLI arg parser ────────────────────────────────────────────────────────
    # Maps common CLI flags → ydl_opts keys.
    # Unknown flags are silently skipped to avoid crashing.
    _CLI_MAP = {
        "--write-comments":       ("getcomments",       True),
        "--write-description":    ("writedescription",  True),
        "--write-info-json":      ("writeinfojson",     True),
        "--write-thumbnail":      ("writethumbnail",    True),
        "--write-subs":           ("writesubtitles",    True),
        "--write-auto-subs":      ("writeautomaticsub", True),
        "--embed-subs":           ("embedsubtitles",    True),
        "--embed-thumbnail":      ("embedthumbnail",    True),
        "--add-metadata":         ("addmetadata",       True),
        "--geo-bypass":           ("geo_bypass",        True),
        "--no-playlist":          ("noplaylist",        True),
        "--no-overwrites":        ("nooverwrites",      True),
        "--restrict-filenames":   ("restrictfilenames", True),
    }
    _CLI_VALUE_MAP = {
        "--proxy":                  "proxy",
        "--rate-limit":             "ratelimit",
        "--user-agent":             "user_agent",
        "--referer":                "referer",
        "--sleep-interval":         "sleep_interval",
        "--max-sleep-interval":     "max_sleep_interval",
        "--concurrent-fragments":   "concurrent_fragment_downloads",
        "--sponsorblock-remove":    "sponsorblock_remove",
        "--subtitles-langs":        "subtitleslangs",
        "--merge-output-format":    "merge_output_format",
        "--remux-video":            "remuxvideo",
        "--recode-video":           "recodevideo",
        "--format":                 "format",
        "--output":                 "outtmpl",
        "-o":                       "outtmpl",
        "-f":                       "format",
        "--playlist-items":         "playlist_items",
        "--playlist-start":         "playliststart",
        "--playlist-end":           "playlistend",
        "--age-limit":              "age_limit",
        "--download-archive":       "download_archive",
        "--geo-bypass-country":     "geo_bypass_country",
        "--netrc-location":         "netrc_location",
        "--username":               "username",
        "--password":               "password",
        "--retries":                "retries",
        "--socket-timeout":         "socket_timeout",
    }

    def _apply_cli(self, opts: dict, args_str: str):
        try:
            tokens = shlex.split(args_str)
        except Exception:
            return
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok in self._CLI_MAP:
                key, val = self._CLI_MAP[tok]
                opts[key] = val
            elif tok in self._CLI_VALUE_MAP and i + 1 < len(tokens):
                key = self._CLI_VALUE_MAP[tok]
                raw = tokens[i + 1]
                # type coercion
                if key in ("concurrent_fragment_downloads", "age_limit",
                           "retries", "socket_timeout", "playliststart", "playlistend"):
                    try:
                        raw = int(raw)
                    except ValueError:
                        pass
                elif key == "sponsorblock_remove":
                    raw = raw.split(",")
                elif key == "subtitleslangs":
                    raw = raw.split(",")
                opts[key] = raw
                i += 1
            else:
                self.log_signal.emit(
                    self.task_id, f"[CLI] 미지원 인자 무시됨: {tok}")
            i += 1
