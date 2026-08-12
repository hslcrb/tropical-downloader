"""
Tropical Downloader - FastAPI API Router
All REST API endpoints for the Electron frontend.
"""

import os
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse

from backend.models.schemas import (
    AnalyzeRequest, DownloadRequest, PlaylistDownloadRequest,
    ChannelBackupRequest, ConfigModel
)
from backend.services.info_service import info_fetcher_service
from backend.services.download_service import download_service
from backend.services.channel_backup_service import channel_backup_service
from backend.services.history_service import history_service
from backend.services.config_service import config_service
from backend.services.cookie_service import cookie_service
from backend.services.file_service import file_service
from backend.services.websocket_service import ws_service

router = APIRouter()

# ─── WebSocket ────────────────────────────────────────────────────────────────
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_service.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        ws_service.disconnect(websocket)


# ─── Media Analysis ───────────────────────────────────────────────────────────
@router.post("/api/analyze")
async def analyze_media(req: AnalyzeRequest):
    """Analyze a YouTube URL and return metadata + available formats."""
    try:
        logs = []
        info = info_fetcher_service.fetch(
            url=req.url,
            browser_cookies=req.browser_cookies or "chrome",
            custom_args=req.custom_args or "",
            log_callback=logs.append
        )
        return {"success": True, "data": info, "logs": logs}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# ─── Download Control ─────────────────────────────────────────────────────────
@router.post("/api/download")
async def start_download(req: DownloadRequest):
    """Start a new download task."""
    opts = req.dict()
    task_id = download_service.start_download(req.url, opts)
    return {"success": True, "task_id": task_id}


@router.get("/api/download/{task_id}")
async def get_task_status(task_id: str):
    """Get the status of a download task."""
    task = download_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "data": task.to_dict()}


@router.post("/api/download/{task_id}/pause")
async def pause_download(task_id: str):
    ok = download_service.pause_task(task_id)
    return {"success": ok}


@router.post("/api/download/{task_id}/resume")
async def resume_download(task_id: str):
    ok = download_service.resume_task(task_id)
    return {"success": ok}


@router.post("/api/download/{task_id}/cancel")
async def cancel_download(task_id: str):
    ok = download_service.cancel_task(task_id)
    return {"success": ok}


@router.post("/api/download/{task_id}/retry")
async def retry_download(task_id: str):
    new_id = download_service.retry_task(task_id)
    if not new_id:
        raise HTTPException(status_code=400, detail="Task cannot be retried in its current state")
    return {"success": True, "task_id": new_id}


@router.get("/api/tasks")
async def get_all_tasks():
    """Get all active download tasks."""
    return {"success": True, "data": download_service.get_all_tasks()}


# ─── Playlist Download ────────────────────────────────────────────────────────
@router.post("/api/playlist/download")
async def download_playlist(req: PlaylistDownloadRequest):
    """Start a batch playlist download."""
    opts = req.dict()
    if req.filename_template:
        opts["filename_template"] = req.filename_template

    # Handle range: "1-10", "all"
    if req.range_str and req.range_str.lower() != "all":
        opts["playlist_items"] = req.range_str

    task_id = download_service.start_download(req.url, opts)
    return {"success": True, "task_id": task_id}


# ─── Channel Backup ───────────────────────────────────────────────────────────
@router.post("/api/channel-backup")
async def start_channel_backup(req: ChannelBackupRequest):
    """Start a full channel/account backup."""
    opts = req.dict()
    backup_id = channel_backup_service.start_backup(req.channel_url, opts)
    return {"success": True, "backup_id": backup_id}


@router.get("/api/channel-backup/{backup_id}")
async def get_backup_status(backup_id: str):
    task = channel_backup_service.get_task(backup_id)
    if not task:
        raise HTTPException(status_code=404, detail="Backup task not found")
    return {"success": True, "data": task.to_dict()}


@router.post("/api/channel-backup/{backup_id}/cancel")
async def cancel_backup(backup_id: str):
    ok = channel_backup_service.cancel_backup(backup_id)
    return {"success": ok}


@router.get("/api/channel-backup")
async def get_all_backups():
    return {"success": True, "data": channel_backup_service.get_all_tasks()}


# ─── History ──────────────────────────────────────────────────────────────────
@router.get("/api/history")
async def get_history(q: Optional[str] = Query(None)):
    items = history_service.get_history(search_query=q)
    return {"success": True, "data": items}


@router.delete("/api/history")
async def clear_history():
    history_service.clear_history()
    return {"success": True, "message": "History cleared"}


# ─── Files ────────────────────────────────────────────────────────────────────
@router.get("/api/files")
async def list_files():
    dl_dir = config_service.get("download_path")
    files = file_service.list_files(dl_dir)
    return {"success": True, "data": files}


@router.delete("/api/files")
async def delete_file(path: str = Query(...)):
    if not os.path.isabs(path):
        raise HTTPException(status_code=400, detail="Invalid path")
    ok = file_service.delete_file(path)
    return {"success": ok}


@router.get("/api/disk-space")
async def get_disk_space():
    dl_dir = config_service.get("download_path")
    try:
        import shutil
        usage = shutil.disk_usage(dl_dir if os.path.exists(dl_dir) else os.path.expanduser("~"))
        return {
            "success": True,
            "data": {
                "total": usage.total,
                "used": usage.used,
                "free": usage.free,
                "free_gb": round(usage.free / (1024**3), 2)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ─── Config ───────────────────────────────────────────────────────────────────
@router.get("/api/config")
async def get_config():
    return {"success": True, "data": config_service.get_all()}


@router.put("/api/config")
async def update_config(updates: dict):
    updated = config_service.update(updates)
    return {"success": True, "data": updated}


# ─── Browsers ────────────────────────────────────────────────────────────────
@router.get("/api/browsers")
async def get_browsers():
    browsers = cookie_service.detect_browsers()
    return {"success": True, "data": [b.model_dump() for b in browsers]}
