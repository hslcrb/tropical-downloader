"""
Tropical Downloader - Asynchronous Media Information Fetcher Thread
"""
import yt_dlp
from PySide6.QtCore import QThread, Signal
from core.config import config_manager
from core.cookie_manager import get_cookie_options

class MediaInfoWorker(QThread):
    finished_info = Signal(dict)
    error_occurred = Signal(str)
    log_emitted = Signal(str)

    def __init__(self, url: str):
        super().__init__()
        self.url = url.strip()

    def run(self):
        try:
            self.log_emitted.emit(f"Analyzing media URL: {self.url}...")
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'extract_flat': False,
            }

            # Add cookie settings
            browser = config_manager.get("cookie_browser")
            cookie_file = config_manager.get("cookies_file")
            ydl_opts.update(get_cookie_options(browser, cookie_file))

            # Add proxy settings
            proxy = config_manager.get("proxy")
            if proxy:
                ydl_opts['proxy'] = proxy

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                if not info:
                    self.error_occurred.emit("Failed to extract media information.")
                    return

                # Normalize info dict
                processed_info = self._process_info(info)
                self.finished_info.emit(processed_info)

        except Exception as e:
            self.error_occurred.emit(str(e))

    def _process_info(self, info: dict) -> dict:
        is_playlist = 'entries' in info or info.get('_type') == 'playlist'
        
        result = {
            "is_playlist": is_playlist,
            "title": info.get("title", "Unknown Title"),
            "uploader": info.get("uploader") or info.get("channel") or info.get("uploader_id") or "Unknown Uploader",
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail", ""),
            "description": info.get("description", ""),
            "url": self.url,
            "formats": [],
            "playlist_entries": []
        }

        if is_playlist:
            entries = info.get("entries", [])
            for idx, entry in enumerate(entries):
                if entry:
                    result["playlist_entries"].append({
                        "index": idx + 1,
                        "id": entry.get("id", ""),
                        "title": entry.get("title", f"Track {idx + 1}"),
                        "duration": entry.get("duration", 0),
                        "uploader": entry.get("uploader", ""),
                        "url": entry.get("url") or entry.get("webpage_url") or f"https://www.youtube.com/watch?v={entry.get('id')}"
                    })
        else:
            formats = info.get("formats", [])
            for fmt in formats:
                fmt_id = fmt.get("format_id", "")
                ext = fmt.get("ext", "")
                resolution = fmt.get("resolution") or (f"{fmt.get('width')}x{fmt.get('height')}" if fmt.get('width') else "audio only")
                vcodec = fmt.get("vcodec", "none")
                acodec = fmt.get("acodec", "none")
                filesize = fmt.get("filesize") or fmt.get("filesize_approx") or 0
                fps = fmt.get("fps", 0)
                tbr = fmt.get("tbr", 0)

                # Classify stream type
                is_video = vcodec != "none"
                is_audio = acodec != "none"

                result["formats"].append({
                    "format_id": fmt_id,
                    "ext": ext,
                    "resolution": resolution,
                    "vcodec": vcodec,
                    "acodec": acodec,
                    "filesize": filesize,
                    "fps": fps,
                    "tbr": tbr,
                    "is_video": is_video,
                    "is_audio": is_audio,
                    "format_note": fmt.get("format_note", "")
                })

        return result
