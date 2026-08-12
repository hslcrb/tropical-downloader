"""
Tropical Downloader - WebSocket Service
Manages connected WebSocket clients and broadcasts real-time download events.
"""

import json
from typing import Set, Any, Dict
from fastapi import WebSocket


class WebSocketService:
    def __init__(self):
        self.connections: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.connections.add(ws)

    def disconnect(self, ws: WebSocket):
        self.connections.discard(ws)

    async def _broadcast(self, data: Dict[str, Any]):
        dead = set()
        msg = json.dumps(data, ensure_ascii=False)
        for ws in self.connections:
            try:
                await ws.send_text(msg)
            except Exception:
                dead.add(ws)
        self.connections -= dead

    async def broadcast_progress(
        self,
        task_id: str,
        percent: float,
        speed: str,
        eta: str,
        downloaded: int,
        total: int,
        status: str = "downloading"
    ):
        await self._broadcast({
            "type": "progress",
            "task_id": task_id,
            "percent": round(percent, 1),
            "speed": speed,
            "eta": eta,
            "downloaded": downloaded,
            "total": total,
            "status": status
        })

    async def broadcast_log(self, task_id: str, message: str):
        await self._broadcast({
            "type": "log",
            "task_id": task_id,
            "message": message
        })

    async def broadcast_task_complete(self, task_id: str, title: str, filepath: str):
        await self._broadcast({
            "type": "task_complete",
            "task_id": task_id,
            "title": title,
            "filepath": filepath
        })

    async def broadcast_task_error(self, task_id: str, error: str):
        await self._broadcast({
            "type": "task_error",
            "task_id": task_id,
            "error": error
        })

    async def broadcast_channel_progress(self, backup_id: str, current: int, total: int, title: str):
        await self._broadcast({
            "type": "channel_progress",
            "backup_id": backup_id,
            "current": current,
            "total": total,
            "title": title
        })


ws_service = WebSocketService()
