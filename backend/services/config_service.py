"""
Tropical Downloader - Config Service
Manages JSON persistent user configuration without PySide6 dependencies.
"""

import os
import json
from typing import Dict, Any

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".tropical_downloader")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
DEFAULT_DOWNLOAD_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "Tropical")

DEFAULT_CONFIG: Dict[str, Any] = {
    "download_path": DEFAULT_DOWNLOAD_PATH,
    "theme": "tropical",
    "ffmpeg_path": "",
    "default_format": "bestvideo+bestaudio/best",
    "browser_cookies": "chrome",
    "proxy": "",
    "rate_limit": "",
    "sponsorblock": False,
    "embed_subs": True,
    "embed_thumbnail": True,
    "auto_purge_node_modules": True,
    "concurrent_downloads": 2,
    "filename_template": "%(title)s [%(id)s].%(ext)s",
    "custom_cli_args": ""
}


class ConfigService:
    def __init__(self):
        self.config = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    saved = json.load(f)
                    self.config = {**DEFAULT_CONFIG, **saved}
            except Exception as e:
                print(f"[ConfigService] Load error: {e}")

    def save(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[ConfigService] Save error: {e}")

    def get_all(self) -> Dict[str, Any]:
        return self.config

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

    def update(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        self.config.update(updates)
        self.save()
        return self.config


config_service = ConfigService()
