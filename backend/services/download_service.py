"""
Tropical Downloader - Download Service
Async-compatible multi-task download engine.
Ports core yt_worker.py logic from PySide6 QThread to ThreadPoolExecutor.
Supports: pause/resume/cancel/retry, disk safety check, RAM buffer fallback,
          node_modules purge, SponsorBlock, cookies, custom CLI args.
"""

import os
import shlex
import shutil
import tempfile
import uuid
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, Any, Optional, Callable, List

import yt_dlp

from backend.services.cookie_service import cookie_service
from backend.services.config_service import config_service
from backend.services.file_service import file_service
from backend.services.history_service import history_service

# Shared executor for all download tasks (limit concurrent)
_executor = ThreadPoolExecutor(max_workers=4)


class DownloadTask:
    def __init__(self, task_id: str, url: str, options: Dict[str, Any]):
        self.task_id = task_id
        self.url = url
        self.options = options
        self.status = "pending"          # pending / downloading / paused / finished / error / canceled
        self.progress_percent = 0.0
        self.speed_str = "0 KB/s"
        self.eta_str = "--:--"
        self.downloaded_bytes = 0
        self.total_bytes = 0
        self.title = ""
        self.filename = ""
        self.filepath = ""
        self.error_msg = ""
        self._cancel_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Not paused initially

    def pause(self):
        self._pause_event.clear()
        self.status = "paused"

    def resume(self):
        self._pause_event.set()
        self.status = "downloading"

    def cancel(self):
        self._cancel_event.set()
        self._pause_event.set()  # unblock if paused
        self.status = "canceled"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "url": self.url,
            "title": self.title,
            "status": self.status,
            "progress_percent": round(self.progress_percent, 1),
            "speed_str": self.speed_str,
            "eta_str": self.eta_str,
            "downloaded_bytes": self.downloaded_bytes,
            "total_bytes": self.total_bytes,
            "filename": self.filename,
            "filepath": self.filepath,
            "error_msg": self.error_msg
        }


class DownloadService:
    def __init__(self):
        self.tasks: Dict[str, DownloadTask] = {}
        self._ws_service = None

    def set_ws_service(self, ws_service):
        self._ws_service = ws_service

    def _get_event_loop(self):
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            return None

    def _emit_ws(self, coro):
        if self._ws_service:
            loop = self._get_event_loop()
            if loop and loop.is_running():
                asyncio.run_coroutine_threadsafe(coro, loop)

    def start_download(self, url: str, options: Dict[str, Any]) -> str:
        task_id = str(uuid.uuid4())[:8]
        task = DownloadTask(task_id, url, options)
        self.tasks[task_id] = task
        _executor.submit(self._run_download, task)
        return task_id

    def get_task(self, task_id: str) -> Optional[DownloadTask]:
        return self.tasks.get(task_id)

    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return [t.to_dict() for t in self.tasks.values()]

    def pause_task(self, task_id: str) -> bool:
        task = self.tasks.get(task_id)
        if task and task.status == "downloading":
            task.pause()
            return True
        return False

    def resume_task(self, task_id: str) -> bool:
        task = self.tasks.get(task_id)
        if task and task.status == "paused":
            task.resume()
            return True
        return False

    def cancel_task(self, task_id: str) -> bool:
        task = self.tasks.get(task_id)
        if task and task.status in ("downloading", "paused", "pending"):
            task.cancel()
            return True
        return False

    def retry_task(self, task_id: str) -> Optional[str]:
        task = self.tasks.get(task_id)
        if task and task.status in ("error", "canceled"):
            return self.start_download(task.url, task.options)
        return None

    def _build_opts(self, task: DownloadTask) -> Dict[str, Any]:
        opts = task.options.copy()
        cfg = config_service

        dl_dir = opts.get("download_path") or cfg.get("download_path",
            os.path.join(os.path.expanduser("~"), "Downloads", "Tropical"))
        os.makedirs(dl_dir, exist_ok=True)

        tmpl = opts.get("filename_template") or cfg.get("filename_template", "%(title)s [%(id)s].%(ext)s")
        opts["outtmpl"] = os.path.join(dl_dir, tmpl)

        # Format
        if opts.get("audio_only"):
            audio_fmt = opts.get("audio_format", "mp3")
            opts["format"] = "bestaudio/best"
            opts["postprocessors"] = [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_fmt,
                "preferredquality": "320"
            }]
        else:
            opts["format"] = opts.get("format_id") or "bestvideo+bestaudio/best"
            opts["merge_output_format"] = opts.get("container", "mp4")

        pp = opts.setdefault("postprocessors", [])
        pp_keys = {p.get("key") for p in pp if isinstance(p, dict)}

        # Embed thumbnail & metadata
        if opts.get("embed_thumbnail", True) and "EmbedThumbnail" not in pp_keys:
            opts["writethumbnail"] = True
            pp.append({"key": "EmbedThumbnail"})
        if "FFmpegMetadata" not in pp_keys:
            pp.append({"key": "FFmpegMetadata"})

        # Subtitles
        if opts.get("embed_subtitles", True):
            opts["writesubtitles"] = True
            opts["writeautomaticsub"] = True
            sub_langs = opts.get("sub_langs") or cfg.get("sub_langs", "ko,en")
            opts["subtitleslangs"] = [s.strip() for s in sub_langs.split(",") if s.strip()]

        # SponsorBlock
        if opts.get("sponsorblock", cfg.get("sponsorblock", False)):
            opts["sponsorblock_remove"] = ["sponsor", "intro", "outro", "selfpromo"]

        # Cookies
        browser = opts.get("browser_cookies") or cfg.get("browser_cookies", "chrome")
        cookies_file = opts.get("cookies_file", "")
        cookie_opts = cookie_service.get_cookie_options(browser, cookies_file)
        opts.update(cookie_opts)

        # Proxy / Rate limit
        proxy = opts.get("proxy") or cfg.get("proxy", "")
        if proxy:
            opts["proxy"] = proxy
        rate = opts.get("rate_limit") or cfg.get("rate_limit", "")
        if rate:
            opts["ratelimit"] = rate

        # FFmpeg path
        ffmpeg = opts.get("ffmpeg_path") or cfg.get("ffmpeg_path", "")
        if ffmpeg and os.path.exists(ffmpeg):
            opts["ffmpeg_location"] = ffmpeg

        # Anti-429
        opts.setdefault("sleep_interval", 1.0)
        opts.setdefault("max_sleep_interval", 3.0)
        opts.setdefault("retries", 10)
        opts.setdefault("fragment_retries", 10)
        opts.setdefault("nocheckcertificate", True)
        opts.setdefault("ignoreerrors", "only_download")
        opts.setdefault("nooverwrites", True)

        # Custom CLI args
        custom_args = opts.get("custom_args") or cfg.get("custom_cli_args", "")
        if custom_args:
            try:
                tokens = shlex.split(custom_args)
                parsed = yt_dlp.parse_options(tokens)
                for k, v in parsed.ydl_opts.items():
                    if v is not None and k not in ("outtmpl", "progress_hooks", "logger"):
                        opts[k] = v
            except Exception as e:
                print(f"[DownloadService] Custom CLI parse error: {e}")

        # Progress hook & logger
        opts["progress_hooks"] = [lambda d, t=task: self._progress_hook(d, t)]
        opts["logger"] = self._make_logger(task)

        return opts

    def _make_logger(self, task: DownloadTask):
        svc = self

        class _Logger:
            def debug(self, msg):
                svc._emit_ws(svc._ws_service.broadcast_log(task.task_id, msg) if svc._ws_service else None)

            def info(self, msg):
                svc._emit_ws(svc._ws_service.broadcast_log(task.task_id, msg) if svc._ws_service else None)

            def warning(self, msg):
                svc._emit_ws(svc._ws_service.broadcast_log(task.task_id, f"[경고] {msg}") if svc._ws_service else None)

            def error(self, msg):
                svc._emit_ws(svc._ws_service.broadcast_log(task.task_id, f"[오류] {msg}") if svc._ws_service else None)

        return _Logger()

    def _progress_hook(self, d: Dict[str, Any], task: DownloadTask):
        # Pause support - block in hook if paused
        task._pause_event.wait()

        if task._cancel_event.is_set():
            raise Exception("Download canceled by user")

        status = d.get("status", "")
        if status == "downloading":
            dl = d.get("downloaded_bytes", 0) or 0
            tot = d.get("total_bytes") or d.get("total_bytes_estimate", 0) or 0
            pct = (dl / tot * 100.0) if tot else 0.0
            spd = d.get("speed") or 0
            eta = d.get("eta") or 0
            task.progress_percent = pct
            task.speed_str = f"{spd/1048576:.2f} MB/s" if spd else "-- MB/s"
            task.eta_str = f"{eta//60:02d}:{eta%60:02d}" if eta else "--:--"
            task.downloaded_bytes = dl
            task.total_bytes = tot
            task.status = "downloading"

            if self._ws_service:
                self._emit_ws(self._ws_service.broadcast_progress(
                    task.task_id, pct, task.speed_str, task.eta_str, dl, tot
                ))
        elif status == "finished":
            task.progress_percent = 99.0
            task.speed_str = "처리 중…"

    def _run_download(self, task: DownloadTask):
        task.status = "downloading"
        ram_tmp_dir = None

        try:
            opts = self._build_opts(task)
            dl_dir = config_service.get("download_path",
                os.path.join(os.path.expanduser("~"), "Downloads", "Tropical"))
            os.makedirs(dl_dir, exist_ok=True)

            # Disk space check (+10% safety margin)
            with yt_dlp.YoutubeDL({"quiet": True, "extract_flat": True}) as ydl:
                try:
                    meta = ydl.extract_info(task.url, download=False) or {}
                    est = meta.get("filesize") or meta.get("filesize_approx") or (200 * 1024 * 1024)
                except Exception:
                    est = 200 * 1024 * 1024  # 200MB default estimate

            has_space, free_b, req_b = file_service.has_sufficient_space(dl_dir, est, 0.10)

            if not has_space:
                if config_service.get("auto_purge_node_modules", True):
                    def _log(msg):
                        if self._ws_service:
                            self._emit_ws(self._ws_service.broadcast_log(task.task_id, msg))
                    file_service.purge_node_modules(log_callback=_log)
                    has_space, free_b, req_b = file_service.has_sufficient_space(dl_dir, est, 0.10)

                if not has_space:
                    # RAM buffer fallback
                    ram_tmp_dir = tempfile.mkdtemp(prefix="tropical_ram_")
                    orig = opts.get("outtmpl", "")
                    if isinstance(orig, str):
                        opts["outtmpl"] = os.path.join(ram_tmp_dir, os.path.basename(orig))

            # Execute download
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(task.url, download=True)

            if task._cancel_event.is_set():
                task.status = "canceled"
                return

            # Extract final path & title
            title = "Downloaded Media"
            filepath = ""
            if info:
                title = info.get("title", title)
                reqs = info.get("requested_downloads")
                if reqs:
                    filepath = reqs[0].get("filepath", "") or reqs[0].get("_filename", "")

            task.title = title
            task.filepath = filepath
            task.filename = os.path.basename(filepath) if filepath else ""

            # Move from RAM buffer to final dir
            if ram_tmp_dir and filepath and os.path.exists(filepath):
                final = os.path.join(dl_dir, os.path.basename(filepath))
                shutil.move(filepath, final)
                filepath = final
                task.filepath = filepath
                shutil.rmtree(ram_tmp_dir, ignore_errors=True)
                ram_tmp_dir = None

            fsize = os.path.getsize(filepath) if filepath and os.path.exists(filepath) else 0

            # Save history
            history_service.add_entry(
                task_id=task.task_id,
                url=task.url,
                title=title,
                filepath=filepath,
                filesize=fsize,
                status="finished"
            )

            task.status = "finished"
            task.progress_percent = 100.0
            task.speed_str = "완료"
            task.eta_str = "00:00"

            if self._ws_service:
                self._emit_ws(self._ws_service.broadcast_task_complete(task.task_id, title, filepath))

        except Exception as e:
            if ram_tmp_dir:
                shutil.rmtree(ram_tmp_dir, ignore_errors=True)
            if not task._cancel_event.is_set():
                task.status = "error"
                task.error_msg = str(e)
                if self._ws_service:
                    self._emit_ws(self._ws_service.broadcast_task_error(task.task_id, str(e)))


download_service = DownloadService()
