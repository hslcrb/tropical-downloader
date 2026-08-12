"""
Tropical Downloader - Info Fetcher Service
Async-compatible yt-dlp metadata extraction.
Handles single video, playlist, and channel info extraction.
DPAPI cookie failures are automatically retried without cookies.
"""

import yt_dlp
from typing import Dict, Any, Optional, List, Callable

from backend.services.cookie_service import cookie_service
from backend.services.config_service import config_service


class InfoFetcherService:
    def fetch(
        self,
        url: str,
        browser_cookies: str = "chrome",
        cookies_file: str = "",
        custom_args: str = "",
        log_callback: Optional[Callable[[str], None]] = None
    ) -> Dict[str, Any]:
        """Extract media metadata from a URL (video, playlist, or channel)."""
        def _log(msg: str):
            if log_callback:
                log_callback(msg)

        proxy = config_service.get("proxy", "")

        ydl_opts: Dict[str, Any] = {
            "quiet": True,
            "no_warnings": True,
            "skip_download": True,
            "extract_flat": "in_playlist",  # fast playlist indexing
            "nocheckcertificate": True,
        }

        if proxy:
            ydl_opts["proxy"] = proxy

        # Apply cookie options
        cookie_opts = cookie_service.get_cookie_options(browser_cookies, cookies_file)
        ydl_opts.update(cookie_opts)

        info = None

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                _log(f"[분석 중] {url}")
                raw = ydl.extract_info(url, download=False)
                # Get full format info for single video
                if raw and raw.get("_type") != "playlist" and "entries" not in raw:
                    full_opts = dict(ydl_opts)
                    full_opts["extract_flat"] = False
                    with yt_dlp.YoutubeDL(full_opts) as full_ydl:
                        info = full_ydl.extract_info(url, download=False)
                else:
                    info = raw
        except Exception as e:
            err = str(e)
            if "DPAPI" in err or "cookie" in err.lower():
                _log("[쿠키 경고] 브라우저 DPAPI 쿠키 복호화 실패 → 공개 세션으로 재시도합니다.")
                ydl_opts.pop("cookiesfrombrowser", None)
                ydl_opts.pop("cookiefile", None)
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                        raw = ydl2.extract_info(url, download=False)
                        if raw and raw.get("_type") != "playlist" and "entries" not in raw:
                            fallback_full = dict(ydl_opts)
                            fallback_full["extract_flat"] = False
                            with yt_dlp.YoutubeDL(fallback_full) as ydl3:
                                info = ydl3.extract_info(url, download=False)
                        else:
                            info = raw
                except Exception as e2:
                    raise RuntimeError(f"미디어 분석 실패: {e2}")
            else:
                raise RuntimeError(f"미디어 분석 실패: {e}")

        if not info:
            raise RuntimeError("미디어 정보를 가져올 수 없습니다.")

        return self._process_info(info, url)

    def _process_info(self, info: Dict[str, Any], url: str) -> Dict[str, Any]:
        is_playlist = "entries" in info or info.get("_type") == "playlist"
        is_channel = info.get("_type") == "playlist" and bool(info.get("uploader_id") or info.get("channel_id"))

        def _dur_str(secs: int) -> str:
            if not secs:
                return "00:00"
            h, r = divmod(int(secs), 3600)
            m, s = divmod(r, 60)
            return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"

        result: Dict[str, Any] = {
            "id": info.get("id", ""),
            "title": info.get("title", "Unknown Title"),
            "url": info.get("webpage_url") or url,
            "uploader": info.get("uploader") or info.get("channel") or "Unknown",
            "duration": info.get("duration", 0),
            "duration_string": _dur_str(info.get("duration", 0)),
            "thumbnail": info.get("thumbnail", ""),
            "description": (info.get("description") or "")[:300],
            "view_count": info.get("view_count", 0),
            "like_count": info.get("like_count", 0),
            "upload_date": info.get("upload_date", ""),
            "is_playlist": is_playlist,
            "is_channel": is_channel,
            "playlist_count": info.get("playlist_count") or len(info.get("entries", [])),
            "playlist_title": info.get("title") if is_playlist else "",
            "formats": [],
            "playlist_items": []
        }

        if is_playlist:
            entries = info.get("entries") or []
            result["playlist_items"] = [
                {
                    "index": i + 1,
                    "id": e.get("id", ""),
                    "title": e.get("title", f"Track {i + 1}"),
                    "duration": e.get("duration", 0),
                    "url": e.get("url") or e.get("webpage_url") or f"https://www.youtube.com/watch?v={e.get('id', '')}"
                }
                for i, e in enumerate(entries)
                if e
            ]
        else:
            formats: List[Dict] = info.get("formats") or []
            result["formats"] = [
                {
                    "format_id": f.get("format_id", ""),
                    "ext": f.get("ext", ""),
                    "resolution": f.get("resolution") or (
                        f"{f.get('width')}x{f.get('height')}" if f.get("width") else "audio only"
                    ),
                    "vcodec": f.get("vcodec", "none"),
                    "acodec": f.get("acodec", "none"),
                    "filesize_approx": f.get("filesize") or f.get("filesize_approx") or 0,
                    "tbr": f.get("tbr") or 0.0,
                    "fps": f.get("fps") or 0.0,
                    "format_note": f.get("format_note", "")
                }
                for f in formats
            ]

        return result


info_fetcher_service = InfoFetcherService()
