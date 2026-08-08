"""
Tropical Downloader - Configuration & Settings Management
"""
import os
import json

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".tropical_downloader")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "Tropical")

DEFAULT_CONFIG = {
    "download_path": DEFAULT_DOWNLOAD_PATH,
    "ffmpeg_path": "",
    "default_quality": "best",
    "cookie_browser": "",
    "cookies_file": "",
    "proxy": "",
    "rate_limit": "",
    "sponsorblock": False,
    "embed_subs": True,
    "sub_langs": "ko,en.*",
    "embed_thumbnail": True,
    "embed_metadata": True,
    "concurrent_downloads": 2,
    "filename_template": "%(title)s [%(id)s].%(ext)s",
    "custom_cli_args": ""
}

class ConfigManager:
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, exist_ok=True)
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    self.config.update(saved)
            except Exception as e:
                print(f"[ConfigManager] Error loading config: {e}")

    def save(self):
        if not os.path.exists(CONFIG_DIR):
            os.makedirs(CONFIG_DIR, exist_ok=True)
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ConfigManager] Error saving config: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default if default is not None else DEFAULT_CONFIG.get(key))

    def set(self, key, value):
        self.config[key] = value
        self.save()

# Global config singleton instance
config_manager = ConfigManager()
