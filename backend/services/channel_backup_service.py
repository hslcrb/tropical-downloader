"""
Tropical Downloader - YouTube Channel & Account Full Backup Service
Permanently archives entire channels, accounts, and playlists for information preservation.
Mission: Support democratic citizens in censored nations to preserve free information.
"""

import os
import uuid
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional, Callable, List

import yt_dlp

from backend.services.cookie_service import cookie_service
from backend.services.config_service import config_service
from backend.services.history_service import history_service

_backup_executor = ThreadPoolExecutor(max_workers=2)


class ChannelBackupTask:
    def __init__(self, backup_id: str, channel_url: str, options: Dict[str, Any]):
        self.backup_id = backup_id
        self.channel_url = channel_url
        self.options = options
        self.status = "pending"        # pending / indexing / downloading / finished / error
        self.total_items = 0
        self.completed_items = 0
        self.current_title = ""
        self.error_msg = ""
        self._cancel_event = threading.Event()

    def cancel(self):
        self._cancel_event.set()
        self.status = "canceled"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "backup_id": self.backup_id,
            "channel_url": self.channel_url,
            "status": self.status,
            "total_items": self.total_items,
            "completed_items": self.completed_items,
            "current_title": self.current_title,
            "progress_percent": round(
                (self.completed_items / self.total_items * 100.0) if self.total_items else 0.0, 1
            ),
            "error_msg": self.error_msg
        }


class ChannelBackupService:
    def __init__(self):
        self.backup_tasks: Dict[str, ChannelBackupTask] = {}
        self._ws_service = None

    def set_ws_service(self, ws_service):
        self._ws_service = ws_service

    def _get_event_loop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            return None

    def _emit_ws(self, coro):
        if self._ws_service and coro:
            loop = self._get_event_loop()
            if loop and loop.is_running():
                asyncio.run_coroutine_threadsafe(coro, loop)

    def start_backup(self, channel_url: str, options: Dict[str, Any]) -> str:
        backup_id = str(uuid.uuid4())[:8]
        task = ChannelBackupTask(backup_id, channel_url, options)
        self.backup_tasks[backup_id] = task
        _backup_executor.submit(self._run_backup, task)
        return backup_id

    def get_task(self, backup_id: str) -> Optional[ChannelBackupTask]:
        return self.backup_tasks.get(backup_id)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self.backup_tasks.values()]

    def cancel_backup(self, backup_id: str) -> bool:
        task = self.backup_tasks.get(backup_id)
        if task:
            task.cancel()
            return True
        return False

    def _build_opts(self, task: ChannelBackupTask) -> Dict[str, Any]:
        opts = task.options.copy()
        cfg = config_service

        channel_name = task.channel_url.rstrip("/").split("/")[-1].lstrip("@")
        default_backup_path = os.path.join(
            cfg.get("download_path", os.path.expanduser("~/Downloads/Tropical")),
            "ChannelBackup",
            channel_name
        )
        backup_path = opts.get("backup_path") or default_backup_path
        os.makedirs(backup_path, exist_ok=True)

        # Output template: organized by upload date and title
        opts["outtmpl"] = os.path.join(
            backup_path, "%(upload_date)s - %(title)s [%(id)s].%(ext)s"
        )

        # Format selection
        if opts.get("download_audio_only"):
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320"
            }]
        else:
            opts["format"] = "bestvideo+bestaudio/best"
            opts["merge_output_format"] = "mp4"

        pp = opts.setdefault("postprocessors", [])
        pp_keys = {p.get("key") for p in pp if isinstance(p, dict)}

        if "FFmpegMetadata" not in pp_keys:
            pp.append({"key": "FFmpegMetadata"})

        # Thumbnail embedding
        if opts.get("download_thumbnails", True) and "EmbedThumbnail" not in pp_keys:
            opts["writethumbnail"] = True
            pp.append({"key": "EmbedThumbnail"})

        # Subtitles
        if opts.get("download_subtitles", True):
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            opts["subtitleslangs"] = ["ko", "en"]

        # Metadata JSON
        if opts.get("download_metadata_json", True):
            opts["writeinfojson"] = True

        # Comments
        if opts.get("download_comments", False):
            opts["getcomments"] = True

        # Shorts & videos inclusion
        # By default yt-dlp fetches all uploads; we handle shorts separately if needed.
        if not opts.get("download_shorts", True):
            # Filter out YouTube Shorts by duration (< 60s)
            opts["match_filter"] = "duration > 60"

        # Cookies
        browser = opts.get("browser_cookies") or cfg.get("browser_cookies", "chrome")
        cookies_file = opts.get("cookies_file", "")
        cookie_opts = cookie_service.get_cookie_options(browser, cookies_file)
        opts.update(cookie_opts)

        # FFmpeg
        ffmpeg = cfg.get("ffmpeg_path", "")
        if ffmpeg and os.path.exists(ffmpeg):
            opts["ffmpeg_location"] = ffmpeg

        # Anti-rate-limit settings
        opts.setdefault("sleep_interval", 2.0)
        opts.setdefault("max_sleep_interval", 5.0)
        opts.setdefault("retries", 10)
        opts.setdefault("fragment_retries", 10)
        opts.setdefault("nocheckcertificate", True)
        opts.setdefault("ignoreerrors", "only_download")
        opts.setdefault("nooverwrites", True)

        # Progress hook & logger
        opts["progress_hooks"] = [lambda d, t=task: self._progress_hook(d, t)]

        # Custom CLI args pass-through
        custom_args = opts.get("custom_args") or cfg.get("custom_cli_args", "")
        if custom_args:
            import shlex
            try:
                tokens = shlex.split(custom_args)
                parsed = yt_dlp.parse_options(tokens)
                for k, v in parsed.ydl_opts.items():
                    if v is not None and k not in ("outtmpl", "progress_hooks", "logger"):
                        opts[k] = v
            except Exception as e:
                print(f"[ChannelBackupService] Custom CLI parse error: {e}")

        return opts

    def _progress_hook(self, d: Dict[str, Any], task: ChannelBackupTask):
        if task._cancel_event.is_set():
            raise Exception("Backup canceled by user")

        if d.get("status") == "finished":
            task.completed_items += 1
            title = d.get("info_dict", {}).get("title", "Unknown")
            task.current_title = title
            if self._ws_service:
                self._emit_ws(self._ws_service.broadcast_channel_progress(
                    task.backup_id, task.completed_items, task.total_items, title
                ))

    def _run_backup(self, task: ChannelBackupTask):
        """
        Phase 1: Index channel to count total items.
        Phase 2: Download all content with full archive options.
        """
        task.status = "indexing"

        try:
            # Phase 1: Index channel
            index_opts = {
                "quiet": True,
                "extract_flat": True,
                "nocheckcertificate": True
            }
            browser = task.options.get("browser_cookies", "chrome")
            index_opts.update(cookie_service.get_cookie_options(browser))

            with yt_dlp.YoutubeDL(index_opts) as ydl:
                self._emit_ws(
                    self._ws_service.broadcast_log(task.backup_id, f"[채널 백업] 채널 인덱싱 중: {task.channel_url}") if self._ws_service else None
                )
                info = ydl.extract_info(task.channel_url, download=False)
                entries = info.get("entries", []) if info else []
                task.total_items = len(entries)

            if task._cancel_event.is_set():
                return

            task.status = "downloading"
            self._emit_ws(
                self._ws_service.broadcast_log(task.backup_id, f"[채널 백업] 총 {task.total_items}개 영상 다운로드 시작") if self._ws_service else None
            )

            # Phase 2: Download all
            opts = self._build_opts(task)
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([task.channel_url])

            task.status = "finished"
            self._emit_ws(
                self._ws_service.broadcast_channel_progress(
                    task.backup_id, task.total_items, task.total_items, "완료"
                ) if self._ws_service else None
            )

        except Exception as e:
            if not task._cancel_event.is_set():
                task.status = "error"
                task.error_msg = str(e)
                if self._ws_service:
                    self._emit_ws(self._ws_service.broadcast_task_error(task.backup_id, str(e)))


channel_backup_service = ChannelBackupService()
