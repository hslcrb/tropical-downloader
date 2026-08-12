"""
Tropical Downloader - Cookie Service
Detects installed browsers and builds yt-dlp cookie extraction options.
"""

import os
from typing import List, Dict, Any
from backend.models.schemas import BrowserCookieOption


class CookieService:
    def __init__(self):
        self.browser_paths = {
            "chrome": [
                os.path.expanduser("~/AppData/Local/Google/Chrome/User Data"),
                os.path.expanduser("~/Library/Application Support/Google/Chrome"),
                os.path.expanduser("~/.config/google-chrome"),
            ],
            "edge": [
                os.path.expanduser("~/AppData/Local/Microsoft/Edge/User Data"),
                os.path.expanduser("~/Library/Application Support/Microsoft Edge"),
            ],
            "firefox": [
                os.path.expanduser("~/AppData/Roaming/Mozilla/Firefox"),
                os.path.expanduser("~/Library/Application Support/Firefox"),
                os.path.expanduser("~/.mozilla/firefox"),
            ],
            "brave": [
                os.path.expanduser("~/AppData/Local/BraveSoftware/Brave-Browser/User Data"),
                os.path.expanduser("~/Library/Application Support/BraveSoftware/Brave-Browser"),
            ],
            "opera": [
                os.path.expanduser("~/AppData/Roaming/Opera Software/Opera Stable"),
                os.path.expanduser("~/Library/Application Support/com.operasoftware.Opera"),
            ],
            "vivaldi": [
                os.path.expanduser("~/AppData/Local/Vivaldi/User Data"),
                os.path.expanduser("~/Library/Application Support/Vivaldi"),
            ],
        }

    def detect_browsers(self) -> List[BrowserCookieOption]:
        result = [
            BrowserCookieOption(name="Auto (자동 감지)", key="auto", installed=True)
        ]
        
        display_names = {
            "chrome": "Google Chrome",
            "edge": "Microsoft Edge",
            "firefox": "Mozilla Firefox",
            "brave": "Brave Browser",
            "opera": "Opera",
            "vivaldi": "Vivaldi",
        }

        for key, paths in self.browser_paths.items():
            installed = any(os.path.exists(p) for p in paths)
            result.append(BrowserCookieOption(
                name=display_names.get(key, key.capitalize()),
                key=key,
                installed=installed
            ))

        result.append(BrowserCookieOption(name="None (비활성화)", key="none", installed=True))
        return result

    def get_best_browser(self) -> str:
        for key, paths in self.browser_paths.items():
            if any(os.path.exists(p) for p in paths):
                return key
        return "chrome"

    def get_cookie_options(self, browser_code: str, cookies_file_path: str = "") -> Dict[str, Any]:
        opts = {}
        if cookies_file_path and cookies_file_path.strip() and os.path.exists(cookies_file_path.strip()):
            opts["cookiefile"] = cookies_file_path.strip()
        else:
            code = (browser_code or "auto").strip().lower()
            if code == "auto":
                code = self.get_best_browser()
            if code and code != "none":
                opts["cookiesfrombrowser"] = (code,)
        return opts


cookie_service = CookieService()
