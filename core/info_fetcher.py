"""
Tropical Downloader - Asynchronous Media Information Fetcher Thread
Robust handling for DPAPI cookie decryption failures with automatic fallback.
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
        self.log_emitted.emit(f"Analyzing media URL: {self.url}...")
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'extract_flat': False,
            'nocheckcertificate': True,
        }

        # Add cookie settings
        browser = config_manager.get("cookie_browser")
        cookie_file = config_manager.get("cookies_file")
        ydl_opts.update(get_cookie_options(browser, cookie_file))

        # Add proxy settings
        proxy = config_manager.get("proxy")
        if proxy:
            ydl_opts['proxy'] = proxy

        info = None
        # Primary attempt with cookies
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
        except Exception as primary_exc:
            err_msg = str(primary_exc)
            # If cookie DPAPI decryption error occurs, retry without cookies
            if "DPAPI" in err_msg or "cookie" in err_msg.lower() or "cookies" in err_msg.lower():
                self.log_emitted.emit("[쿠키 경고] 브라우저 DPAPI 쿠키 복호화 불가. 공개 세션으로 분석을 재시도합니다.")
                ydl_opts.pop('cookiesfrombrowser', None)
                ydl_opts.pop('cookiefile', None)
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as fallback_ydl:
                        info = fallback_ydl.extract_info(self.url, download=False)
                except Exception as fallback_exc:
                    self.error_occurred.emit(str(fallback_exc))
                    return
            else:
                self.error_occurred.emit(err_msg)
                return

        if not info:
            self.error_occurred.emit("미디어 정보를 가져올 수 없습니다.")
            return

        processed_info = self._process_info(info)
        self.finished_info.emit(processed_info)

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
