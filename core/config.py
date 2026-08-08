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
    "theme_mode": "system",       # 기본 시스템 설정을 따름 ("system" | "light" | "dark")
    "ffmpeg_path": "",
    "default_quality": "best",
    "cookie_browser": "auto",     # 기본 자동 탐지
    "auto_cookie_detect": True,   # 기본 자동 탐지 켬
    "cookies_file": "",
    "proxy": "",
    "rate_limit": "",
    "sponsorblock": False,
    "embed_subs": True,
    "write_subs": True,
    "sub_langs": "ko,en.*",
    "embed_thumbnail": True,
    "embed_metadata": True,
    "write_comments": True,       # 기본 댓글 저장
    "write_description": True,    # 기본 동영상 설명 저장
    "write_info_json": True,      # 기본 info.json 저장
    "sleep_interval": 1,          # 429 차단 방지 지연
    "max_sleep_interval": 3,
    "player_clients": "android,ios,web,mweb,tv",
    "disk_safety_margin": True,   # +10% 용량 검사 기본 켬
    "ram_buffering": True,        # 저장공간 부족 시 RAM 보관 후 알림 기본 켬
    "auto_purge_node_modules": True, # 저장공간 부족 시 node_modules 자동 영구 삭제 기본 켬
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
                    merged = DEFAULT_CONFIG.copy()
                    merged.update(saved)
                    self.config = merged
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
