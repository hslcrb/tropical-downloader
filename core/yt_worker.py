"""
Tropical Downloader - Core yt-dlp Download Worker Thread
"""
import os
import re
import shlex
import yt_dlp
from PySide6.QtCore import QThread, Signal
from core.config import config_manager
from core.cookie_manager import get_cookie_options
from core.history_manager import history_manager

class YtDlpLogger:
    def __init__(self, callback, task_id):
        self.callback = callback
        self.task_id = task_id

    def debug(self, msg):
        if msg.startswith('[debug] '):
            self.callback(self.task_id, msg)

    def info(self, msg):
        self.callback(self.task_id, msg)

    def warning(self, msg):
        self.callback(self.task_id, f"[WARNING] {msg}")

    def error(self, msg):
        self.callback(self.task_id, f"[ERROR] {msg}")

class DownloadWorker(QThread):
    progress_signal = Signal(str, float, str, str, int, int, str) # task_id, percent, speed, eta, downloaded, total, status
    log_signal = Signal(str, str)                                 # task_id, log_line
    finished_signal = Signal(str, str, str)                      # task_id, output_path, title
    error_signal = Signal(str, str)                                # task_id, error_message

    def __init__(self, task_id: str, url: str, options_override: dict = None, custom_args: str = ""):
        super().__init__()
        self.task_id = task_id
        self.url = url
        self.options_override = options_override or {}
        self.custom_args = custom_args
        self._is_canceled = False

    def cancel(self):
        self._is_canceled = True

    def run(self):
        try:
            self.log_signal.emit(self.task_id, f"Initializing download for task [{self.task_id}]: {self.url}")
            
            # Base download options
            download_dir = self.options_override.get("download_path") or config_manager.get("download_path")
            os.makedirs(download_dir, exist_ok=True)
            
            out_template = self.options_override.get("filename_template") or config_manager.get("filename_template")
            ydl_opts = {
                'outtmpl': out_tmpl_full,
                'progress_hooks': [self._progress_hook],
                'logger': YtDlpLogger(self.log_signal.emit, self.task_id),
                'nocheckcertificate': True,
                'ignoreerrors': False,
                'geo_bypass': True,
                'geo_bypass_country': 'US',
                'extractor_args': {'youtube': {'player_client': ['android', 'ios', 'web']}},
            }
            ffmpeg_path = config_manager.get("ffmpeg_path")
            if ffmpeg_path and os.path.exists(ffmpeg_path):
                ydl_opts['ffmpeg_location'] = ffmpeg_path

            # Playlist & Channel Range options
            if self.options_override.get("playlist_range"):
                ydl_opts['playlist_items'] = self.options_override.get("playlist_range")

            # Quality / Format specification
            fmt = self.options_override.get("format", "bestvideo+bestaudio/best")
            ydl_opts['format'] = fmt

            # Audio extraction mode
            if self.options_override.get("extract_audio", False):
                audio_fmt = self.options_override.get("audio_format", "mp3")
                audio_quality = self.options_override.get("audio_quality", "320")
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_fmt,
                    'preferredquality': audio_quality,
                }]

            # Metadata & Thumbnail embedding
            postprocessors = ydl_opts.get('postprocessors', [])
            if self.options_override.get("embed_metadata", config_manager.get("embed_metadata")):
                postprocessors.append({'key': 'FFmpegMetadata'})

            if self.options_override.get("embed_thumbnail", config_manager.get("embed_thumbnail")):
                postprocessors.append({'key': 'EmbedThumbnail'})
                ydl_opts['writethumbnail'] = True

            ydl_opts['postprocessors'] = postprocessors

            # Subtitles
            if self.options_override.get("embed_subs", config_manager.get("embed_subs")):
                ydl_opts['writesubtitles'] = True
                ydl_opts['writeautomaticsub'] = True
                ydl_opts['subtitleslangs'] = config_manager.get("sub_langs", "ko,en.*").split(',')

            # Cookies & Proxy
            browser = self.options_override.get("cookie_browser") or config_manager.get("cookie_browser")
            cookie_file = self.options_override.get("cookies_file") or config_manager.get("cookies_file")
            ydl_opts.update(get_cookie_options(browser, cookie_file))

            proxy = self.options_override.get("proxy") or config_manager.get("proxy")
            if proxy:
                ydl_opts['proxy'] = proxy

            rate_limit = config_manager.get("rate_limit")
            if rate_limit:
                ydl_opts['ratelimit'] = rate_limit

            # Parse custom CLI flags pass-through if provided
            if self.custom_args:
                self._apply_custom_cli_args(ydl_opts, self.custom_args)

            # Perform Download
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=True)
                
                if self._is_canceled:
                    self.error_signal.emit(self.task_id, "Download canceled by user.")
                    return

                title = info.get("title", "Downloaded Media") if info else "Downloaded Media"
                
                # Determine output filename
                filepath = ""
                if info:
                    if 'requested_downloads' in info and info['requested_downloads']:
                        filepath = info['requested_downloads'][0].get('_filename', '')
                    else:
                        filepath = ydl.prepare_filename(info)

                # Format file size for history
                filesize_str = "Unknown Size"
                if filepath and os.path.exists(filepath):
                    size_bytes = os.path.getsize(filepath)
                    filesize_str = f"{size_bytes / (1024 * 1024):.2f} MB"

                # Record in history
                history_manager.add_entry(
                    title=title,
                    url=self.url,
                    format_str=fmt,
                    file_path=filepath,
                    file_size=filesize_str
                )

                self.progress_signal.emit(self.task_id, 100.0, "Completed", "00:00", 0, 0, "FINISHED")
                self.finished_signal.emit(self.task_id, filepath, title)

        except Exception as e:
            if not self._is_canceled:
                self.error_signal.emit(self.task_id, str(e))

    def _progress_hook(self, d: dict):
        if self._is_canceled:
            raise Exception("Download Canceled")

        status = d.get('status', '')
        if status == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            
            percent = 0.0
            if total > 0:
                percent = (downloaded / total) * 100.0
            
            speed = d.get('speed', 0)
            speed_str = f"{speed / (1024 * 1024):.2f} MB/s" if speed else "-- MB/s"
            
            eta = d.get('eta', 0)
            eta_str = f"{eta // 60:02d}:{eta % 60:02d}" if eta is not None else "--:--"

            self.progress_signal.emit(
                self.task_id,
                percent,
                speed_str,
                eta_str,
                downloaded,
                total,
                "DOWNLOADING"
            )
        elif status == 'finished':
            self.progress_signal.emit(
                self.task_id,
                99.0,
                "Processing...",
                "00:00",
                0,
                0,
                "PROCESSING"
            )

    def _apply_custom_cli_args(self, opts: dict, args_str: str):
        """Simple CLI args parser for custom options"""
        try:
            tokens = shlex.split(args_str)
            i = 0
            while i < len(tokens):
                t = tokens[i]
                if t == '--write-comments':
                    opts['getcomments'] = True
                elif t == '--write-description':
                    opts['writedescription'] = True
                elif t == '--write-info-json':
                    opts['writeinfojson'] = True
                elif t == '--sponsorblock-remove' and i + 1 < len(tokens):
                    opts['sponsorblock_remove'] = tokens[i+1].split(',')
                    i += 1
                elif t == '--concurrent-fragments' and i + 1 < len(tokens):
                    opts['concurrent_fragment_downloads'] = int(tokens[i+1])
                    i += 1
                elif t == '--user-agent' and i + 1 < len(tokens):
                    opts['user_agent'] = tokens[i+1]
                    i += 1
                elif t == '--geo-bypass':
                    opts['geo_bypass'] = True
                i += 1
        except Exception as e:
            self.log_signal.emit(self.task_id, f"[Warning] Could not parse custom args: {e}")
