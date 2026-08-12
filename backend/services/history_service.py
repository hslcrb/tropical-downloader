"""
Tropical Downloader - History Service
Manages download history persistence and search querying.
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

HISTORY_FILE = os.path.join(os.path.expanduser("~"), ".tropical_downloader", "history.json")


class HistoryService:
    def __init__(self):
        self.items: List[Dict[str, Any]] = []
        self.load()

    def load(self):
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                    self.items = json.load(f)
            except Exception as e:
                print(f"[HistoryService] Load error: {e}")
                self.items = []

    def save(self):
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        try:
            with open(HISTORY_FILE, "w", encoding="utf-8") as f:
                json.dump(self.items, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[HistoryService] Save error: {e}")

    def add_entry(
        self,
        task_id: str,
        url: str,
        title: str,
        filepath: str,
        filesize: int = 0,
        status: str = "finished"
    ) -> Dict[str, Any]:
        entry = {
            "task_id": task_id,
            "url": url,
            "title": title,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "filepath": filepath,
            "filesize": filesize,
            "status": status
        }
        self.items.insert(0, entry)
        self.save()
        return entry

    def get_history(self, search_query: Optional[str] = None) -> List[Dict[str, Any]]:
        if not search_query:
            return self.items
        q = search_query.lower()
        return [
            item for item in self.items
            if q in item.get("title", "").lower() or q in item.get("url", "").lower()
        ]

    def clear_history(self):
        self.items = []
        self.save()


history_service = HistoryService()
