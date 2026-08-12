# Implementation Plan - PySide6 to Electron + Python FastAPI Migration & Channel Backup System

This plan outlines the complete implementation for migrating **Tropical Downloader ("트로피컬 다운로더")** from PySide6 to an **Electron + Python (FastAPI) backend architecture**, featuring a **Frutiger Aero / Tropical Y2K design system** and **YouTube Account & Channel Full Archive/Backup capabilities** for permanent information preservation.

---

## User Review Required

> [!IMPORTANT]
> **Key Architecture Decisions**
> 1. **Backend**: Python FastAPI service running on `http://127.0.0.1:8765` providing REST API endpoints + WebSockets for real-time download progress, logs, and state updates.
> 2. **Frontend**: Electron Desktop Application running a Frutiger Aero styled web frontend (Aqua Gel buttons, Glassmorphic panels, Wave progress bars, Emerald Lagoon themes).
> 3. **Process Life-Cycle**: Electron Main process automatically spawns and manages the Python FastAPI backend process on startup and gracefully terminates it on app exit.
> 4. **Democracy & Freedom Archive Mission**: Includes full YouTube Channel Backup mode (all videos, shorts, audio, metadata JSON, thumbnails, subtitles, comments, and playlists) to ensure complete anti-censorship preservation.

> [!NOTE]
> **Git Rule Compliance**
> - All git commits will use English prefixes with Korean descriptive messages (e.g. `feat: 백엔드 채널 백업 API 구현`).
> - No `git merge` or PR will be performed without explicit user commands. When explicitly commanded, `git merge --no-ff <branch-name>` will be used.

---

## Open Questions

None at this time. All requirements from `chat-kiro.Clean State.md` and `.kiro/specs/electron-python-migration` have been incorporated into this plan.

---

## Proposed Changes

### 1. Python FastAPI Backend Service (`backend/`)

#### [NEW] [backend/requirements.txt](file:///d:/tropical-downloader/backend/requirements.txt)
- Dependencies: `fastapi`, `uvicorn[standard]`, `yt-dlp`, `pydantic`, `websockets`, `python-multipart`, `pytest`, `hypothesis`.

#### [MODIFY] [backend/main.py](file:///d:/tropical-downloader/backend/main.py)
- Integrate API Routers (`/api/analyze`, `/api/download`, `/api/tasks`, `/api/playlist`, `/api/channel-backup`, `/api/history`, `/api/files`, `/api/config`, `/api/browsers`).
- Integrate WebSocket route (`/ws`) for real-time progress, speed, ETA, and console logs streaming.
- Global exception handlers & CORS middleware for Electron host.

#### [NEW] [backend/models/schemas.py](file:///d:/tropical-downloader/backend/models/schemas.py)
- Pydantic models: `AnalyzeRequest`, `DownloadRequest`, `ChannelBackupRequest`, `TaskStatusResponse`, `MediaMetadataResponse`, `ConfigModel`, `HistoryItemModel`.

#### [NEW] [backend/services/info_service.py](file:///d:/tropical-downloader/backend/services/info_service.py)
- Metadata extraction using `yt-dlp`. Support for single video, playlist, and full channel indexing. Automatic browser cookie loading and DPAPI fallback.

#### [NEW] [backend/services/download_service.py](file:///d:/tropical-downloader/backend/services/download_service.py)
- Multi-threaded download task engine. Support pause, resume, cancel, retry, custom CLI arguments pass-through, low disk space auto-purge & RAM buffering.

#### [NEW] [backend/services/websocket_service.py](file:///d:/tropical-downloader/backend/services/websocket_service.py)
- Manager for client WebSocket connections. Broadcasts `progress`, `log`, `task_complete`, and `task_error` events.

#### [NEW] [backend/services/channel_backup_service.py](file:///d:/tropical-downloader/backend/services/channel_backup_service.py)
- Dedicated engine for full Youtube Channel & Account archive downloads (video/audio, metadata JSON, thumbnails, subtitles, comments, playlist files).

#### [NEW] [backend/services/history_service.py](file:///d:/tropical-downloader/backend/services/history_service.py)
- Persistent JSON history store with search filtering and clear functionality.

#### [NEW] [backend/services/config_service.py](file:///d:/tropical-downloader/backend/services/config_service.py)
- App configuration manager (download directory, FFmpeg path, SponsorBlock, auto-purge options, default formats).

#### [NEW] [backend/services/cookie_service.py](file:///d:/tropical-downloader/backend/services/cookie_service.py)
- Browser cookie auto-detector (Chrome, Edge, Firefox, Brave, Safari).

#### [NEW] [backend/services/file_service.py](file:///d:/tropical-downloader/backend/services/file_service.py)
- Disk space check, file manager, node_modules emergency purge worker.

#### [NEW] [backend/routes/api_router.py](file:///d:/tropical-downloader/backend/routes/api_router.py)
- FastAPI router binding services to HTTP endpoints.

#### [NEW] [backend/tests/test_backend_api.py](file:///d:/tropical-downloader/backend/tests/test_backend_api.py)
- Unit and integration tests for API endpoints using FastAPI `TestClient`.

---

### 2. Electron Application & Process Management (`electron/` & `package.json`)

#### [NEW] [package.json](file:///d:/tropical-downloader/package.json)
- Electron setup, scripts (`npm start`, `npm run dev`, `npm run build`), dependencies (`electron`, `ws`).

#### [NEW] [electron/main.js](file:///d:/tropical-downloader/electron/main.js)
- Main process script:
  - Spawns Python FastAPI backend process on startup (`python -m uvicorn backend.main:app`).
  - Manages `BrowserWindow` with custom Frutiger Aero window frame.
  - IPC handlers for folder dialogs, opening files, system notifications.
  - Graceful backend process kill on window close.

#### [NEW] [electron/preload.js](file:///d:/tropical-downloader/electron/preload.js)
- Secure `contextBridge` exposing `window.api` (IPC methods and backend port configuration).

---

### 3. Frutiger Aero Web Frontend (`src/`)

#### [NEW] [src/index.html](file:///d:/tropical-downloader/src/index.html)
- Main HTML file loading Frutiger Aero CSS design system and modular component scripts.

#### [NEW] [src/styles/frutiger_aero.css](file:///d:/tropical-downloader/src/styles/frutiger_aero.css)
- Modern CSS tokens for Frutiger Aero / Tropical Y2K aesthetics:
  - Aqua Gel Buttons (gradient highlights & gloss sheen)
  - Glassmorphism Cards & Panels (backdrop blur, subtle borders)
  - Wave Progress Bars (animated shimmer gradient)
  - Tropical Emerald Lagoon Palette (`#00E5FF`, `#0077B6`, `#06D6A0`, `#FFD166`, `#FF6B6B`)

#### [NEW] [src/app.js](file:///d:/tropical-downloader/src/app.js)
- Main application shell: tab router, WebSocket listener for real-time progress update, backend status indicator.

#### [NEW] [src/components/QuickDownloadTab.js](file:///d:/tropical-downloader/src/components/QuickDownloadTab.js)
- Quick Download UI with automatic clipboard paste, instant media preview card, and one-click quality presets (4K, 1080p, 720p, MP3, FLAC).

#### [NEW] [src/components/FormatInspectorTab.js](file:///d:/tropical-downloader/src/components/FormatInspectorTab.js)
- Detailed format inspector with stream resolution table, codec info, audio/video stream selection, container selector (MP4, MKV, WEBM), and subtitle/thumbnail embedding checkboxes.

#### [NEW] [src/components/PlaylistChannelTab.js](file:///d:/tropical-downloader/src/components/PlaylistChannelTab.js)
- **Playlist & Full Channel Archive UI**: URL analysis, item selection range ("1-50"), subtitle/metadata/comment backup options, archive structure template settings.

#### [NEW] [src/components/QueueTab.js](file:///d:/tropical-downloader/src/components/QueueTab.js)
- Download Queue manager with real-time wave progress bars, speed (MB/s), ETA, Pause/Resume/Cancel/Retry controls, and direct Open File / Open Folder buttons.

#### [NEW] [src/components/AdvancedTab.js](file:///d:/tropical-downloader/src/components/AdvancedTab.js)
- Advanced yt-dlp settings: Browser cookies selector, SponsorBlock filter toggles, proxy settings, speed limit input, subtitle languages, and direct custom CLI argument pass-through.

#### [NEW] [src/components/HistoryLogsTab.js](file:///d:/tropical-downloader/src/components/HistoryLogsTab.js)
- Download history table with search filtering and live streaming yt-dlp console logs output.

#### [NEW] [src/components/MediaPlayerTab.js](file:///d:/tropical-downloader/src/components/MediaPlayerTab.js)
- Built-in media player with HTML5 video/audio controls, playback rate options, auto subtitle detection, and downloaded media file browser.

#### [NEW] [src/components/SettingsTab.js](file:///d:/tropical-downloader/src/components/SettingsTab.js)
- Settings UI for download location (with Electron native folder picker), FFmpeg executable path, auto purge node_modules toggle, and theme switching.

---

## Verification Plan

### Automated Tests
1. **Python Backend Unit & API Tests**:
   - Command: `python -m pytest backend/tests/`
   - Checks: API endpoint validation, schema correctness, route responses, WebSocket broadcast capabilities.
2. **Backend Syntax & Import Verification**:
   - Command: `python -m py_compile backend/main.py backend/services/*.py backend/routes/*.py backend/models/*.py`

### Manual Verification
1. **Backend Server Launch**:
   - Run `python backend/main.py` and inspect `GET http://127.0.0.1:8765/` to confirm running status.
2. **Media Analysis & Download Flow**:
   - Test analyzing a YouTube URL (`/api/analyze`), triggering download (`/api/download`), and receiving real-time WebSocket progress updates.
3. **Channel Backup Feature**:
   - Verify channel backup metadata indexing and complete download of channel playlists & video metadata.
4. **Electron Desktop Application Launch**:
   - Run `npx electron .` to verify Electron window, Frutiger Aero design rendering, IPC folder selection, and automatic Python process lifecycle management.
