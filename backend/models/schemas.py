"""
Tropical Downloader - Pydantic Schemas for API Requests & Responses
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class AnalyzeRequest(BaseModel):
    url: str = Field(..., description="Target media, playlist, or channel URL")
    browser_cookies: Optional[str] = Field("chrome", description="Browser to extract cookies from")
    custom_args: Optional[str] = Field("", description="Additional custom yt-dlp arguments")


class StreamFormat(BaseModel):
    format_id: str
    ext: str
    resolution: Optional[str] = "N/A"
    vcodec: Optional[str] = "none"
    acodec: Optional[str] = "none"
    filesize_approx: Optional[int] = 0
    tbr: Optional[float] = 0.0
    fps: Optional[float] = 0.0
    format_note: Optional[str] = ""


class MediaMetadataResponse(BaseModel):
    id: str
    title: str
    url: str
    uploader: Optional[str] = "Unknown"
    duration: Optional[int] = 0
    duration_string: Optional[str] = "00:00"
    thumbnail: Optional[str] = ""
    description: Optional[str] = ""
    view_count: Optional[int] = 0
    like_count: Optional[int] = 0
    upload_date: Optional[str] = ""
    is_playlist: bool = False
    playlist_count: Optional[int] = 0
    playlist_title: Optional[str] = ""
    is_channel: bool = False
    formats: List[StreamFormat] = []
    playlist_items: Optional[List[Dict[str, Any]]] = []


class DownloadRequest(BaseModel):
    url: str
    format_id: Optional[str] = "bestvideo+bestaudio/best"
    container: Optional[str] = "mp4"
    audio_only: bool = False
    audio_format: Optional[str] = "mp3"
    download_path: Optional[str] = None
    embed_subtitles: bool = True
    embed_thumbnail: bool = True
    sponsorblock: bool = False
    rate_limit: Optional[str] = None
    proxy: Optional[str] = None
    sub_langs: Optional[str] = "ko,en"
    browser_cookies: Optional[str] = "chrome"
    custom_args: Optional[str] = ""


class PlaylistDownloadRequest(BaseModel):
    url: str
    range_str: Optional[str] = "all"  # e.g., "1-10" or "all"
    format_id: Optional[str] = "bestvideo+bestaudio/best"
    audio_only: bool = False
    filename_template: Optional[str] = "%(playlist_index)s - %(title)s.%(ext)s"
    browser_cookies: Optional[str] = "chrome"
    custom_args: Optional[str] = ""


class ChannelBackupRequest(BaseModel):
    channel_url: str = Field(..., description="YouTube Channel or User Account URL")
    backup_path: Optional[str] = None
    download_videos: bool = True
    download_shorts: bool = True
    download_audio_only: bool = False
    download_subtitles: bool = True
    download_thumbnails: bool = True
    download_metadata_json: bool = True
    download_comments: bool = False
    browser_cookies: Optional[str] = "chrome"
    custom_args: Optional[str] = ""


class TaskStatusResponse(BaseModel):
    task_id: str
    url: str
    title: str
    status: str  # pending, downloading, paused, finished, error, canceled
    progress_percent: float = 0.0
    speed_str: str = "0 KB/s"
    eta_str: str = "00:00"
    downloaded_bytes: int = 0
    total_bytes: int = 0
    filename: str = ""
    filepath: str = ""
    error_msg: Optional[str] = None


class ConfigModel(BaseModel):
    download_path: str
    ffmpeg_path: str = ""
    default_format: str = "bestvideo+bestaudio/best"
    auto_purge_node_modules: bool = True
    theme: str = "tropical"
    sponsorblock: bool = False
    browser_cookies: str = "chrome"


class HistoryItemModel(BaseModel):
    task_id: str
    url: str
    title: str
    timestamp: str
    filepath: str
    filesize: int = 0
    status: str = "finished"


class BrowserCookieOption(BaseModel):
    name: str
    key: str
    installed: bool
