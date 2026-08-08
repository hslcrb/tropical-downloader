"""
Tropical Downloader - Browser Cookies Integrator
"""

SUPPORTED_BROWSERS = [
    ("None (Public Access)", ""),
    ("Google Chrome", "chrome"),
    ("Microsoft Edge", "edge"),
    ("Mozilla Firefox", "firefox"),
    ("Brave Browser", "brave"),
    ("Opera", "opera"),
    ("Vivaldi", "vivaldi"),
    ("Safari (macOS)", "safari"),
]

def get_cookie_options(browser_code: str, cookies_file_path: str = "") -> dict:
    """Returns yt-dlp cookie options dict based on user selection"""
    opts = {}
    if cookies_file_path and cookies_file_path.strip():
        opts['cookiefile'] = cookies_file_path.strip()
    elif browser_code and browser_code.strip():
        opts['cookiesfrombrowser'] = (browser_code.strip(),)
    return opts
