"""
Tropical Downloader - Download History Manager
"""
import os
import json
from datetime import datetime

HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".tropical_downloader", "history.json")

class HistoryManager:
    def __init__(self):
        self.history = []
        self.load()

    def load(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            except Exception as e:
                print(f"[HistoryManager] Load error: {e}")
                self.history = []

    def save(self):
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        try:
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[HistoryManager] Save error: {e}")

    def add_entry(self, title: str, url: str, format_str: str, file_path: str, file_size: str):
        entry = {
            "id": str(len(self.history) + 1),
            "title": title,
            "url": url,
            "format": format_str,
            "path": file_path,
            "size": file_size,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.history.insert(0, entry)  # Newest first
        self.save()
        return entry

    def clear(self):
        self.history = []
        self.save()

history_manager = HistoryManager()
