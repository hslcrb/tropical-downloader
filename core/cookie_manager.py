"""
Tropical Downloader - Browser Cookies Auto-Detector
Automatically detects installed and active web browsers on Windows/macOS/Linux
"""
import os
import shutil
import subprocess

SUPPORTED_BROWSERS = [
    ("Auto (자동 감지)", "auto"),
    ("Google Chrome", "chrome"),
    ("Microsoft Edge", "edge"),
    ("Mozilla Firefox", "firefox"),
    ("Brave Browser", "brave"),
    ("Opera", "opera"),
    ("Vivaldi", "vivaldi"),
    ("Safari (macOS)", "safari"),
    ("비활성화 (공개 접근)", "none"),
]

def detect_available_browsers() -> list[tuple[str, str]]:
    """Detects installed browsers on the system by checking standard profile paths"""
    detected = [("Auto (자동 감지)", "auto")]
    home = os.path.expanduser("~")
    
    # Path mappings for Windows & cross-platform checks
    browser_paths = {
        "chrome": [
            os.path.join(home, "AppData", "Local", "Google", "Chrome", "User Data"),
            os.path.join(home, "Library", "Application Support", "Google", "Chrome"),
            os.path.join(home, ".config", "google-chrome"),
        ],
        "edge": [
            os.path.join(home, "AppData", "Local", "Microsoft", "Edge", "User Data"),
            os.path.join(home, "Library", "Application Support", "Microsoft Edge"),
        ],
        "firefox": [
            os.path.join(home, "AppData", "Roaming", "Mozilla", "Firefox"),
            os.path.join(home, "Library", "Application Support", "Firefox"),
            os.path.join(home, ".mozilla", "firefox"),
        ],
        "brave": [
            os.path.join(home, "AppData", "Local", "BraveSoftware", "Brave-Browser", "User Data"),
            os.path.join(home, "Library", "Application Support", "BraveSoftware", "Brave-Browser"),
        ],
        "opera": [
            os.path.join(home, "AppData", "Roaming", "Opera Software", "Opera Stable"),
            os.path.join(home, "Library", "Application Support", "com.operasoftware.Opera"),
        ],
        "vivaldi": [
            os.path.join(home, "AppData", "Local", "Vivaldi", "User Data"),
            os.path.join(home, "Library", "Application Support", "Vivaldi"),
        ],
    }

    for b_code, paths in browser_paths.items():
        for p in paths:
            if os.path.exists(p):
                name_dict = {
                    "chrome": "Google Chrome",
                    "edge": "Microsoft Edge",
                    "firefox": "Mozilla Firefox",
                    "brave": "Brave Browser",
                    "opera": "Opera",
                    "vivaldi": "Vivaldi",
                }
                detected.append((f"{name_dict.get(b_code, b_code)} (감지됨)", b_code))
                break

    detected.append(("비활성화 (공개 접근)", "none"))
    return detected

def get_best_autodetected_browser() -> str:
    """Returns the first detected browser or 'chrome' / 'edge' as fallback"""
    detected = detect_available_browsers()
    for name, code in detected:
        if code not in ("auto", "none"):
            return code
    return "chrome"

def get_cookie_options(browser_code: str, cookies_file_path: str = "") -> dict:
    """Returns yt-dlp cookie options dict based on user selection"""
    opts = {}
    if cookies_file_path and cookies_file_path.strip() and os.path.exists(cookies_file_path.strip()):
        opts['cookiefile'] = cookies_file_path.strip()
    else:
        target_b = browser_code.strip() if browser_code else "auto"
        if target_b == "auto":
            target_b = get_best_autodetected_browser()
        
        if target_b and target_b != "none":
            opts['cookiesfrombrowser'] = (target_b,)
            
    return opts
