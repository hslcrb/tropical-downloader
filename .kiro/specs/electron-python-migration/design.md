# Technical Design Document

## Overview

이 문서는 Tropical Downloader를 PySide6 기반 데스크톱 애플리케이션에서 **Electron 프론트엔드 + Python FastAPI 백엔드** 아키텍처로 완전히 재구축하는 마이그레이션 프로젝트의 기술 설계를 정의합니다.

### 핵심 목표

1. **아키텍처 혁신**: 모놀리식 PySide6 UI를 완전히 제거하고, Electron + React/Vue 웹 기술 스택으로 교체
2. **명확한 분리**: 프론트엔드(Electron)와 백엔드(Python FastAPI) 완전 분리
3. **기능 보존**: 모든 기존 기능(빠른 다운로드, 포맷 분석, 플레이리스트, 고급 옵션, 큐 관리, 히스토리, 인앱 플레이어) 유지
4. **UX 개선**: Frutiger Aero 디자인 시스템을 웹 기술로 재구현하여 더 부드럽고 현대적인 사용자 경험 제공
5. **안정성 강화**: 독재 국가의 민주 시민이 사용하는 사명있는 프로젝트로서, 유튜브 계정 전체 백업, 채널 완전 백업, 플레이리스트 보존, 검열 콘텐츠 아카이브, 오프라인 접근 보장

### 프로젝트 사명

이 프로젝트는 **탄압받는 독재 국가의 민주 시민세력**이 정보의 자유를 보전하고 영구 보존하기 위한 도구입니다. 따라서 다음 기능이 핵심입니다:

- **유튜브 계정 데이터 전체 백업**: 사용자의 모든 미디어 데이터 완전 백업
- **채널 전체 백업**: 모든 영상, 자막, 메타데이터 완전 보존
- **플레이리스트 완전 보존**: 재생목록 구조 및 순서 유지
- **검열될 수 있는 콘텐츠의 안전한 아카이브**: 정치적으로 민감한 콘텐츠 보호
- **오프라인 접근 가능한 완전한 백업**: 인터넷 차단 상황에서도 접근 가능

### 기술 스택

**프론트엔드 (Electron)**
- Electron 최신 버전 (v28+)
- React 18+ 또는 Vue 3+ (컴포넌트 기반 UI)
- TypeScript (타입 안정성)
- Vite 또는 Webpack (번들링)
- TailwindCSS 또는 Emotion (스타일링)
- WebSocket Client (실시간 진행상황)

**백엔드 (Python)**
- Python 3.11+
- FastAPI (비동기 REST API 프레임워크)
- Uvicorn (ASGI 서버)
- yt-dlp (최신 버전, 미디어 다운로드 엔진)
- python-socketio 또는 WebSocket (실시간 통신)
- Pydantic (데이터 검증)

**빌드 & 배포**
- electron-builder 또는 electron-forge (앱 패키징)
- PyInstaller 또는 Nuitka (Python 백엔드 번들링)

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Electron Desktop Application                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Electron Main Process                         │  │
│  │  - Lifecycle Management (시작/종료)                        │  │
│  │  - Python Backend Process 관리                            │  │
│  │  - Window Management                                       │  │
│  │  - IPC Bridge (Renderer ↔ Main)                          │  │
│  │  - Native API Access (파일 시스템, 알림 등)               │  │
│  └───────────────┬────────────────────────────────────────────┘  │
│                  │ IPC                                            │
│  ┌───────────────▼────────────────────────────────────────────┐  │
│  │           Electron Renderer Process                        │  │
│  │  ┌──────────────────────────────────────────────────────┐  │  │
│  │  │         React/Vue Frontend UI                        │  │  │
│  │  │  - Quick Download Tab                                │  │  │
│  │  │  - Format Inspector Tab                              │  │  │
│  │  │  - Playlist Tab                                      │  │  │
│  │  │  - Advanced Options Tab                              │  │  │
│  │  │  - Queue Management Tab                              │  │  │
│  │  │  - History & Logs Tab                                │  │  │
│  │  │  - Media Player Tab                                  │  │  │
│  │  │  - Settings Tab                                      │  │  │
│  │  │  - Frutiger Aero Design System Components           │  │  │
│  │  └──────────────────────────────────────────────────────┘  │  │
│  └───────────────┬────────────────────────────────────────────┘  │
└──────────────────┼─────────────────────────────────────────────┘
                   │ HTTP REST API + WebSocket
┌──────────────────▼─────────────────────────────────────────────┐
│                  Python FastAPI Backend                         │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                FastAPI Application                        │  │
│  │  - REST API Routes (/analyze, /download, /queue, etc.)  │  │
│  │  - WebSocket Server (실시간 진행상황 스트리밍)            │  │
│  │  - Request/Response 검증 (Pydantic Models)               │  │
│  │  - CORS Configuration (localhost 허용)                   │  │
│  │  - Error Handling & Logging                              │  │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│  ┌───────────────▼──────────────────────────────────────────┐  │
│  │             Core Service Layer                           │  │
│  │  ┌────────────────┐  ┌─────────────────┐               │  │
│  │  │  Download      │  │  Info Fetcher   │               │  │
│  │  │  Service       │  │  Service        │               │  │
│  │  │  - Task Queue  │  │  - Metadata     │               │  │
│  │  │  - Progress    │  │  - Format List  │               │  │
│  │  │  - Cancel/Pause│  │  - Playlist     │               │  │
│  │  └────────────────┘  └─────────────────┘               │  │
│  │  ┌────────────────┐  ┌─────────────────┐               │  │
│  │  │  Cookie        │  │  History        │               │  │
│  │  │  Manager       │  │  Manager        │               │  │
│  │  │  - Browser     │  │  - DB Storage   │               │  │
│  │  │  - Detection   │  │  - Search       │               │  │
│  │  └────────────────┘  └─────────────────┘               │  │
│  │  ┌────────────────┐  ┌─────────────────┐               │  │
│  │  │  Disk          │  │  Config         │               │  │
│  │  │  Manager       │  │  Manager        │               │  │
│  │  │  - Space Check │  │  - Settings     │               │  │
│  │  │  - File Ops    │  │  - Persistence  │               │  │
│  │  └────────────────┘  └─────────────────┘               │  │
│  └───────────────┬──────────────────────────────────────────┘  │
│                  │                                              │
│  ┌───────────────▼──────────────────────────────────────────┐  │
│  │                  yt-dlp Engine                           │  │
│  │  - extract_info() - 메타데이터 추출                      │  │
│  │  - download() - 다운로드 실행                            │  │
│  │  - Progress Hooks - 진행상황 콜백                        │  │
│  │  - Logger - 로그 캡처                                    │  │
│  │  - Options - 고급 옵션 적용                              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 통신 흐름

1. **Electron 시작 → Python 백엔드 자동 시작**
   ```
   Electron Main Process → spawn Python Backend → 포트 8765 대기
   ```

2. **프론트엔드 요청 → 백엔드 처리**
   ```
   React/Vue Component → fetch/axios HTTP Request → FastAPI Route → Service Layer → yt-dlp → Response
   ```

3. **실시간 진행상황 스트리밍**
   ```
   FastAPI WebSocket Server → Progress Updates → Frontend WebSocket Client → UI Update
   ```

4. **Electron 종료 → Python 백엔드 자동 종료**
   ```
   Electron Main Process → SIGTERM to Python Process → Graceful Shutdown
   ```

---

## Components and Interfaces

### 1. Electron Main Process

**책임:**
- Electron 앱 생명주기 관리
- Python 백엔드 프로세스 생성 및 종료
- BrowserWindow 생성 및 관리
- IPC 통신 처리 (Renderer ↔ Main)
- 네이티브 OS 기능 접근 (파일 다이얼로그, 알림, 시스템 트레이)

**주요 인터페이스:**

```typescript
// main/index.ts

interface BackendProcessConfig {
  pythonExecutable: string;      // Python 실행 파일 경로 (번들된 또는 시스템)
  backendScript: string;          // FastAPI 진입점 스크립트
  port: number;                   // 백엔드 포트 (기본 8765)
  logFile: string;                // 백엔드 로그 파일 경로
}

class BackendProcessManager {
  private process: ChildProcess | null;
  
  start(config: BackendProcessConfig): Promise<void>;
  stop(): Promise<void>;
  isRunning(): boolean;
  getPort(): number;
  onExit(callback: (code: number) => void): void;
  onError(callback: (error: Error) => void): void;
}

interface ElectronMainAPI {
  // IPC 핸들러
  selectFolder(): Promise<string>;          // 폴더 선택 대화상자
  openPath(path: string): Promise<void>;    // 파일/폴더 열기
  showNotification(title: string, body: string): void;  // 알림 표시
  getBackendStatus(): Promise<{ running: boolean; port: number }>;
}
```

### 2. Electron Renderer Process (React/Vue Frontend)

**책임:**
- 사용자 인터페이스 렌더링
- 사용자 입력 처리
- Python 백엔드 API 호출
- WebSocket을 통한 실시간 진행상황 수신
- 상태 관리 (Redux/Zustand/Pinia)

**주요 컴포넌트 구조 (React 예시):**

```typescript
// renderer/src/components/

// Tabs
- QuickDownloadTab.tsx          // 빠른 다운로드
- FormatInspectorTab.tsx         // 상세 포맷 분석
- PlaylistTab.tsx                // 플레이리스트
- AdvancedOptionsTab.tsx         // 고급 옵션
- QueueTab.tsx                   // 다운로드 큐
- HistoryTab.tsx                 // 히스토리
- PlayerTab.tsx                  // 인앱 플레이어
- SettingsTab.tsx                // 설정

// Shared Components
- MediaCard.tsx                  // 미디어 정보 카드
- FormatTable.tsx                // 포맷 테이블
- ProgressBar.tsx                // 진행률 바
- AquaGelButton.tsx              // Aqua Gel 버튼
- GlassmorphismCard.tsx          // 유리 형태 카드
- TropicalIcon.tsx               // 트로피컬 아이콘

// Services
- apiClient.ts                   // API 클라이언트 (axios)
- websocketClient.ts             // WebSocket 클라이언트
```

**API 클라이언트 인터페이스:**

```typescript
// renderer/src/services/apiClient.ts

interface MediaMetadata {
  is_playlist: boolean;
  title: string;
  uploader: string;
  duration: number;
  thumbnail: string;
  description: string;
  url: string;
  formats: Format[];
  playlist_entries: PlaylistEntry[];
}

interface Format {
  format_id: string;
  ext: string;
  resolution: string;
  vcodec: string;
  acodec: string;
  filesize: number;
  fps: number;
  tbr: number;
  is_video: boolean;
  is_audio: boolean;
  format_note: string;
}

interface DownloadTask {
  task_id: string;
  url: string;
  title: string;
  status: 'queued' | 'downloading' | 'paused' | 'completed' | 'failed';
  progress: number;
  speed: string;
  eta: string;
  downloaded_bytes: number;
  total_bytes: number;
  file_path?: string;
  error?: string;
}

class APIClient {
  private baseURL: string = 'http://localhost:8765';
  
  // Media Analysis
  analyzeMedia(url: string): Promise<MediaMetadata>;
  
  // Download Management
  startDownload(request: DownloadRequest): Promise<{ task_id: string }>;
  pauseDownload(taskId: string): Promise<void>;
  resumeDownload(taskId: string): Promise<void>;
  cancelDownload(taskId: string): Promise<void>;
  retryDownload(taskId: string): Promise<{ task_id: string }>;
  getDownloadStatus(taskId: string): Promise<DownloadTask>;
  listActiveTasks(): Promise<DownloadTask[]>;
  
  // Playlist
  downloadPlaylist(request: PlaylistDownloadRequest): Promise<{ task_ids: string[] }>;
  
  // History
  getHistory(limit?: number, search?: string): Promise<HistoryEntry[]>;
  clearHistory(): Promise<void>;
  
  // Configuration
  getConfig(): Promise<Config>;
  updateConfig(config: Partial<Config>): Promise<void>;
  
  // File System
  listDownloadedFiles(): Promise<FileInfo[]>;
  deleteFile(path: string): Promise<void>;
  getDiskSpace(path: string): Promise<DiskSpaceInfo>;
  
  // Cookies
  detectBrowsers(): Promise<BrowserInfo[]>;
}
```

**WebSocket 클라이언트:**

```typescript
// renderer/src/services/websocketClient.ts

interface ProgressUpdate {
  task_id: string;
  progress: number;
  speed: string;
  eta: string;
  downloaded_bytes: number;
  total_bytes: number;
  status: string;
}

interface LogMessage {
  task_id: string;
  level: 'info' | 'warning' | 'error';
  message: string;
  timestamp: string;
}

class WebSocketClient {
  private socket: WebSocket;
  
  connect(url: string): Promise<void>;
  disconnect(): void;
  
  onProgress(callback: (update: ProgressUpdate) => void): void;
  onLog(callback: (log: LogMessage) => void): void;
  onTaskComplete(callback: (taskId: string, filePath: string) => void): void;
  onTaskError(callback: (taskId: string, error: string) => void): void;
}
```

### 3. Python FastAPI Backend

**책임:**
- REST API 엔드포인트 제공
- WebSocket 서버 운영 (실시간 진행상황)
- yt-dlp 엔진 통합 및 관리
- 다운로드 작업 큐 관리
- 파일 시스템 작업
- 설정 및 히스토리 저장

**API 엔드포인트 설계:**

```python
# backend/main.py

from fastapi import FastAPI, WebSocket, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import Optional, List
import uvicorn

app = FastAPI(title="Tropical Downloader API", version="2.0.0")

# CORS 설정 (Electron localhost 허용)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:*", "file://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Pydantic Models
# ============================================================================

class AnalyzeRequest(BaseModel):
    url: HttpUrl

class MediaMetadataResponse(BaseModel):
    is_playlist: bool
    title: str
    uploader: str
    duration: int
    thumbnail: str
    description: str
    url: str
    formats: List[FormatInfo]
    playlist_entries: List[PlaylistEntry]

class DownloadRequest(BaseModel):
    url: HttpUrl
    format_id: Optional[str] = None
    extract_audio: bool = False
    audio_format: str = "mp3"
    audio_quality: str = "320"
    merge_output_format: str = "mkv"
    embed_thumbnail: bool = True
    embed_metadata: bool = True
    embed_subs: bool = True
    download_path: Optional[str] = None
    output_template: Optional[str] = None
    cookie_browser: str = "auto"
    cookies_file: Optional[str] = None
    proxy: Optional[str] = None
    rate_limit: Optional[str] = None
    sponsorblock_options: List[str] = []
    custom_args: str = ""
    playlist_range: Optional[str] = None

class TaskResponse(BaseModel):
    task_id: str

class TaskStatusResponse(BaseModel):
    task_id: str
    url: str
    title: str
    status: str
    progress: float
    speed: str
    eta: str
    downloaded_bytes: int
    total_bytes: int
    file_path: Optional[str] = None
    error: Optional[str] = None

# ============================================================================
# API Routes
# ============================================================================

@app.get("/")
async def root():
    return {"message": "Tropical Downloader API v2.0", "status": "running"}

@app.post("/api/analyze", response_model=MediaMetadataResponse)
async def analyze_media(request: AnalyzeRequest):
    """
    미디어 URL 분석 및 메타데이터 반환
    """
    from services.info_fetcher_service import InfoFetcherService
    service = InfoFetcherService()
    metadata = await service.fetch_info(str(request.url))
    return metadata

@app.post("/api/download", response_model=TaskResponse)
async def start_download(request: DownloadRequest):
    """
    다운로드 작업 시작
    """
    from services.download_service import DownloadService
    service = DownloadService()
    task_id = await service.start_download(request.dict())
    return {"task_id": task_id}

@app.post("/api/download/{task_id}/pause")
async def pause_download(task_id: str):
    """
    다운로드 일시정지
    """
    from services.download_service import DownloadService
    service = DownloadService()
    await service.pause_download(task_id)
    return {"message": "Paused"}

@app.post("/api/download/{task_id}/resume")
async def resume_download(task_id: str):
    """
    다운로드 재개
    """
    from services.download_service import DownloadService
    service = DownloadService()
    await service.resume_download(task_id)
    return {"message": "Resumed"}

@app.post("/api/download/{task_id}/cancel")
async def cancel_download(task_id: str):
    """
    다운로드 취소
    """
    from services.download_service import DownloadService
    service = DownloadService()
    await service.cancel_download(task_id)
    return {"message": "Cancelled"}

@app.post("/api/download/{task_id}/retry", response_model=TaskResponse)
async def retry_download(task_id: str):
    """
    실패한 다운로드 재시도
    """
    from services.download_service import DownloadService
    service = DownloadService()
    new_task_id = await service.retry_download(task_id)
    return {"task_id": new_task_id}

@app.get("/api/download/{task_id}", response_model=TaskStatusResponse)
async def get_download_status(task_id: str):
    """
    다운로드 작업 상태 조회
    """
    from services.download_service import DownloadService
    service = DownloadService()
    status = await service.get_task_status(task_id)
    return status

@app.get("/api/tasks", response_model=List[TaskStatusResponse])
async def list_active_tasks():
    """
    모든 활성 작업 목록
    """
    from services.download_service import DownloadService
    service = DownloadService()
    tasks = await service.list_active_tasks()
    return tasks

@app.post("/api/playlist/download")
async def download_playlist(request: PlaylistDownloadRequest):
    """
    플레이리스트 일괄 다운로드
    """
    from services.download_service import DownloadService
    service = DownloadService()
    task_ids = await service.download_playlist(request.dict())
    return {"task_ids": task_ids}

@app.get("/api/history")
async def get_history(limit: int = 100, search: Optional[str] = None):
    """
    다운로드 히스토리 조회
    """
    from services.history_service import HistoryService
    service = HistoryService()
    entries = await service.get_history(limit=limit, search=search)
    return entries

@app.delete("/api/history")
async def clear_history():
    """
    히스토리 전체 삭제
    """
    from services.history_service import HistoryService
    service = HistoryService()
    await service.clear()
    return {"message": "History cleared"}

@app.get("/api/config")
async def get_config():
    """
    현재 설정 조회
    """
    from services.config_service import ConfigService
    service = ConfigService()
    config = await service.get_config()
    return config

@app.put("/api/config")
async def update_config(config: dict):
    """
    설정 업데이트
    """
    from services.config_service import ConfigService
    service = ConfigService()
    await service.update_config(config)
    return {"message": "Config updated"}

@app.get("/api/files")
async def list_downloaded_files(path: Optional[str] = None):
    """
    다운로드 폴더 파일 목록
    """
    from services.file_service import FileService
    service = FileService()
    files = await service.list_files(path)
    return files

@app.delete("/api/files")
async def delete_file(path: str):
    """
    파일 삭제
    """
    from services.file_service import FileService
    service = FileService()
    await service.delete_file(path)
    return {"message": "File deleted"}

@app.get("/api/disk-space")
async def get_disk_space(path: str):
    """
    디스크 공간 조회
    """
    from services.file_service import FileService
    service = FileService()
    space = await service.get_disk_space(path)
    return space

@app.get("/api/browsers")
async def detect_browsers():
    """
    설치된 브라우저 감지
    """
    from services.cookie_service import CookieService
    service = CookieService()
    browsers = await service.detect_browsers()
    return browsers

# ============================================================================
# WebSocket Endpoint
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    실시간 진행상황 스트리밍
    """
    await websocket.accept()
    from services.websocket_service import WebSocketService
    service = WebSocketService()
    await service.handle_connection(websocket)

# ============================================================================
# Startup & Shutdown
# ============================================================================

@app.on_event("startup")
async def startup_event():
    print("[Backend] Tropical Downloader API starting...")
    # Initialize services, load config, etc.

@app.on_event("shutdown")
async def shutdown_event():
    print("[Backend] Tropical Downloader API shutting down...")
    # Cleanup: cancel active downloads, close connections, etc.

# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8765,
        log_level="info",
        reload=False  # Production mode
    )
```

### 4. Service Layer

각 서비스는 독립적인 비즈니스 로직을 담당하며, FastAPI 라우트와 yt-dlp 엔진 사이의 중간 레이어 역할을 합니다.

#### 4.1 DownloadService

```python
# backend/services/download_service.py

import asyncio
import uuid
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import yt_dlp

class DownloadService:
    def __init__(self):
        self.active_tasks: Dict[str, DownloadTask] = {}
        self.executor = ThreadPoolExecutor(max_workers=5)
        
    async def start_download(self, request: dict) -> str:
        """다운로드 작업 시작"""
        task_id = str(uuid.uuid4())
        task = DownloadTask(
            task_id=task_id,
            url=request['url'],
            options=request
        )
        self.active_tasks[task_id] = task
        
        # 비동기로 다운로드 실행
        asyncio.create_task(self._execute_download(task))
        
        return task_id
    
    async def _execute_download(self, task: DownloadTask):
        """실제 다운로드 실행 (별도 스레드에서 yt-dlp 호출)"""
        loop = asyncio.get_event_loop()
        try:
            await loop.run_in_executor(
                self.executor,
                self._download_worker,
                task
            )
        except Exception as e:
            task.status = 'failed'
            task.error = str(e)
    
    def _download_worker(self, task: DownloadTask):
        """yt-dlp 다운로드 워커 (블로킹 I/O)"""
        ydl_opts = self._build_ydl_opts(task.options)
        ydl_opts['progress_hooks'] = [lambda d: self._progress_hook(task, d)]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(task.url, download=True)
            task.title = info.get('title', 'Unknown')
            if info.get('requested_downloads'):
                task.file_path = info['requested_downloads'][0].get('filepath')
            task.status = 'completed'
    
    def _progress_hook(self, task: DownloadTask, d: dict):
        """진행상황 콜백"""
        if d['status'] == 'downloading':
            task.progress = (d.get('downloaded_bytes', 0) / d.get('total_bytes', 1)) * 100
            task.speed = f"{d.get('speed', 0) / 1048576:.2f} MB/s"
            task.eta = f"{d.get('eta', 0) // 60:02d}:{d.get('eta', 0) % 60:02d}"
            task.downloaded_bytes = d.get('downloaded_bytes', 0)
            task.total_bytes = d.get('total_bytes', 0)
            
            # WebSocket으로 진행상황 브로드캐스트
            from services.websocket_service import broadcast_progress
            asyncio.run(broadcast_progress(task.to_dict()))
    
    async def pause_download(self, task_id: str):
        """다운로드 일시정지"""
        # yt-dlp는 네이티브 pause를 지원하지 않으므로, cancel 후 resume 시 --continue 사용
        task = self.active_tasks.get(task_id)
        if task:
            task.paused = True
            # 실제 구현에서는 프로세스 시그널 전송
    
    async def resume_download(self, task_id: str):
        """다운로드 재개"""
        task = self.active_tasks.get(task_id)
        if task and task.paused:
            task.paused = False
            # 실제 구현에서는 --continue 옵션으로 재시작
    
    async def cancel_download(self, task_id: str):
        """다운로드 취소"""
        task = self.active_tasks.get(task_id)
        if task:
            task.cancelled = True
            task.status = 'cancelled'
            # 실제 구현에서는 프로세스 강제 종료 및 임시 파일 삭제
```

#### 4.2 InfoFetcherService

```python
# backend/services/info_fetcher_service.py

import yt_dlp
from typing import Dict

class InfoFetcherService:
    async def fetch_info(self, url: str) -> Dict:
        """미디어 메타데이터 추출"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'skip_download': True,
            'extract_flat': False,
            'nocheckcertificate': True,
        }
        
        # 브라우저 쿠키 자동 감지
        from core.cookie_manager import get_cookie_options
        from core.config import config_manager
        browser = config_manager.get("cookie_browser", "auto")
        ydl_opts.update(get_cookie_options(browser, ""))
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
            return self._process_info(info, url)
        except Exception as e:
            # DPAPI 쿠키 오류 시 쿠키 없이 재시도
            if "DPAPI" in str(e) or "cookie" in str(e).lower():
                ydl_opts.pop('cookiesfrombrowser', None)
                ydl_opts.pop('cookiefile', None)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                return self._process_info(info, url)
            raise
    
    def _process_info(self, info: dict, url: str) -> dict:
        """정보 가공"""
        is_playlist = 'entries' in info or info.get('_type') == 'playlist'
        
        result = {
            "is_playlist": is_playlist,
            "title": info.get("title", "Unknown"),
            "uploader": info.get("uploader", "Unknown"),
            "duration": info.get("duration", 0),
            "thumbnail": info.get("thumbnail", ""),
            "description": info.get("description", ""),
            "url": url,
            "formats": [],
            "playlist_entries": []
        }
        
        if is_playlist:
            for idx, entry in enumerate(info.get("entries", [])):
                if entry:
                    result["playlist_entries"].append({
                        "index": idx + 1,
                        "id": entry.get("id", ""),
                        "title": entry.get("title", f"Track {idx + 1}"),
                        "duration": entry.get("duration", 0),
                        "url": entry.get("webpage_url", "")
                    })
        else:
            for fmt in info.get("formats", []):
                result["formats"].append({
                    "format_id": fmt.get("format_id", ""),
                    "ext": fmt.get("ext", ""),
                    "resolution": fmt.get("resolution", "audio only"),
                    "vcodec": fmt.get("vcodec", "none"),
                    "acodec": fmt.get("acodec", "none"),
                    "filesize": fmt.get("filesize") or fmt.get("filesize_approx") or 0,
                    "fps": fmt.get("fps", 0),
                    "tbr": fmt.get("tbr", 0),
                    "is_video": fmt.get("vcodec") != "none",
                    "is_audio": fmt.get("acodec") != "none",
                    "format_note": fmt.get("format_note", "")
                })
        
        return result
```

### 5. WebSocket Service

```python
# backend/services/websocket_service.py

from fastapi import WebSocket
from typing import List, Dict
import asyncio
import json

class WebSocketService:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def handle_connection(self, websocket: WebSocket):
        """WebSocket 연결 처리"""
        self.active_connections.append(websocket)
        try:
            while True:
                # Keep-alive
                await asyncio.sleep(1)
        except Exception:
            self.active_connections.remove(websocket)
    
    async def broadcast_progress(self, update: Dict):
        """진행상황 브로드캐스트"""
        message = json.dumps({
            "type": "progress",
            "data": update
        })
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass
    
    async def broadcast_log(self, log: Dict):
        """로그 브로드캐스트"""
        message = json.dumps({
            "type": "log",
            "data": log
        })
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                pass

# 전역 인스턴스
_ws_service = WebSocketService()

async def broadcast_progress(update: Dict):
    await _ws_service.broadcast_progress(update)

async def broadcast_log(log: Dict):
    await _ws_service.broadcast_log(log)
```

---

## Data Models

### Frontend TypeScript Models

```typescript
// renderer/src/types/models.ts

export interface MediaMetadata {
  is_playlist: boolean;
  title: string;
  uploader: string;
  duration: number;
  thumbnail: string;
  description: string;
  url: string;
  formats: Format[];
  playlist_entries: PlaylistEntry[];
}

export interface Format {
  format_id: string;
  ext: string;
  resolution: string;
  vcodec: string;
  acodec: string;
  filesize: number;
  fps: number;
  tbr: number;
  is_video: boolean;
  is_audio: boolean;
  format_note: string;
}

export interface PlaylistEntry {
  index: number;
  id: string;
  title: string;
  duration: number;
  url: string;
}

export interface DownloadRequest {
  url: string;
  format_id?: string;
  extract_audio?: boolean;
  audio_format?: string;
  audio_quality?: string;
  merge_output_format?: string;
  embed_thumbnail?: boolean;
  embed_metadata?: boolean;
  embed_subs?: boolean;
  download_path?: string;
  output_template?: string;
  cookie_browser?: string;
  cookies_file?: string;
  proxy?: string;
  rate_limit?: string;
  sponsorblock_options?: string[];
  custom_args?: string;
  playlist_range?: string;
}

export interface DownloadTask {
  task_id: string;
  url: string;
  title: string;
  status: 'queued' | 'downloading' | 'paused' | 'completed' | 'failed' | 'cancelled';
  progress: number;
  speed: string;
  eta: string;
  downloaded_bytes: number;
  total_bytes: number;
  file_path?: string;
  error?: string;
  created_at: string;
}

export interface HistoryEntry {
  id: string;
  title: string;
  url: string;
  format: string;
  path: string;
  size: string;
  timestamp: string;
}

export interface Config {
  download_path: string;
  filename_template: string;
  merge_output_format: string;
  embed_metadata: boolean;
  embed_thumbnail: boolean;
  embed_subs: boolean;
  sub_langs: string;
  cookie_browser: string;
  cookies_file: string;
  ffmpeg_path: string;
  rate_limit: string;
  proxy: string;
  custom_cli_args: string;
  theme: 'light' | 'dark' | 'system';
  notifications_enabled: boolean;
}

export interface DiskSpaceInfo {
  total: number;
  used: number;
  free: number;
  percent: number;
}

export interface FileInfo {
  name: string;
  path: string;
  size: number;
  modified: string;
  is_video: boolean;
  is_audio: boolean;
}
```

### Backend Python Models

```python
# backend/models/schemas.py

from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List
from datetime import datetime

class FormatInfo(BaseModel):
    format_id: str
    ext: str
    resolution: str
    vcodec: str
    acodec: str
    filesize: int
    fps: int
    tbr: float
    is_video: bool
    is_audio: bool
    format_note: str

class PlaylistEntry(BaseModel):
    index: int
    id: str
    title: str
    duration: int
    url: str

class MediaMetadataResponse(BaseModel):
    is_playlist: bool
    title: str
    uploader: str
    duration: int
    thumbnail: str
    description: str
    url: str
    formats: List[FormatInfo]
    playlist_entries: List[PlaylistEntry]

class DownloadRequest(BaseModel):
    url: HttpUrl
    format_id: Optional[str] = None
    extract_audio: bool = False
    audio_format: str = "mp3"
    audio_quality: str = "320"
    merge_output_format: str = "mkv"
    embed_thumbnail: bool = True
    embed_metadata: bool = True
    embed_subs: bool = True
    download_path: Optional[str] = None
    output_template: Optional[str] = None
    cookie_browser: str = "auto"
    cookies_file: Optional[str] = None
    proxy: Optional[str] = None
    rate_limit: Optional[str] = None
    sponsorblock_options: List[str] = Field(default_factory=list)
    custom_args: str = ""
    playlist_range: Optional[str] = None

class TaskStatusResponse(BaseModel):
    task_id: str
    url: str
    title: str
    status: str
    progress: float
    speed: str
    eta: str
    downloaded_bytes: int
    total_bytes: int
    file_path: Optional[str] = None
    error: Optional[str] = None
    created_at: datetime

class HistoryEntry(BaseModel):
    id: str
    title: str
    url: str
    format: str
    path: str
    size: str
    timestamp: str

class Config(BaseModel):
    download_path: str
    filename_template: str = "%(title)s [%(id)s].%(ext)s"
    merge_output_format: str = "mkv"
    embed_metadata: bool = True
    embed_thumbnail: bool = True
    embed_subs: bool = True
    sub_langs: str = "ko,en.*"
    cookie_browser: str = "auto"
    cookies_file: str = ""
    ffmpeg_path: str = ""
    rate_limit: str = ""
    proxy: str = ""
    custom_cli_args: str = ""
    theme: str = "system"
    notifications_enabled: bool = True
```

---


## Error Handling

### Frontend Error Handling Strategy

**1. API 호출 에러 처리**

```typescript
// renderer/src/services/errorHandler.ts

export class APIError extends Error {
  constructor(
    message: string,
    public statusCode: number,
    public details?: any
  ) {
    super(message);
    this.name = 'APIError';
  }
}

export async function handleAPICall<T>(
  apiCall: () => Promise<T>,
  userFriendlyMessage: string
): Promise<T> {
  try {
    return await apiCall();
  } catch (error) {
    if (error instanceof APIError) {
      // HTTP 에러 처리
      switch (error.statusCode) {
        case 404:
          throw new Error(`${userFriendlyMessage}: 리소스를 찾을 수 없습니다.`);
        case 500:
          throw new Error(`${userFriendlyMessage}: 서버 내부 오류가 발생했습니다.`);
        case 503:
          throw new Error(`${userFriendlyMessage}: 백엔드 서버에 연결할 수 없습니다.`);
        default:
          throw new Error(`${userFriendlyMessage}: ${error.message}`);
      }
    } else if (error instanceof Error) {
      // 네트워크 에러
      if (error.message.includes('ECONNREFUSED') || error.message.includes('Network Error')) {
        throw new Error('백엔드 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요.');
      }
      throw new Error(`${userFriendlyMessage}: ${error.message}`);
    }
    throw error;
  }
}
```

**2. WebSocket 재연결 로직**

```typescript
// renderer/src/services/websocketClient.ts

class WebSocketClient {
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000;
  
  connect(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      this.socket = new WebSocket(url);
      
      this.socket.onopen = () => {
        this.reconnectAttempts = 0;
        resolve();
      };
      
      this.socket.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
      this.socket.onclose = () => {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
          this.reconnectAttempts++;
          const delay = this.reconnectDelay * Math.pow(2, this.reconnectAttempts - 1);
          console.log(`WebSocket 재연결 시도 ${this.reconnectAttempts}/${this.maxReconnectAttempts} (${delay}ms 후)`);
          setTimeout(() => this.connect(url), delay);
        } else {
          reject(new Error('WebSocket 연결 실패: 최대 재연결 시도 횟수 초과'));
        }
      };
    });
  }
}
```

**3. 전역 에러 바운더리 (React)**

```typescript
// renderer/src/components/ErrorBoundary.tsx

import React from 'react';

interface Props {
  children: React.ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends React.Component<Props, State> {
  state: State = { hasError: false };
  
  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }
  
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Uncaught error:', error, errorInfo);
    // 에러 로깅 서비스로 전송 (선택적)
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h1>앗, 문제가 발생했습니다!</h1>
          <p>{this.state.error?.message}</p>
          <button onClick={() => window.location.reload()}>
            앱 새로고침
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}
```

### Backend Error Handling Strategy

**1. 전역 예외 핸들러**

```python
# backend/main.py

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import traceback

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Pydantic 검증 오류 처리"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "details": exc.errors(),
            "message": "요청 데이터가 올바르지 않습니다."
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """일반 예외 처리"""
    error_trace = traceback.format_exc()
    print(f"[ERROR] {error_trace}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "type": type(exc).__name__
        }
    )

class DownloadError(Exception):
    """다운로드 관련 에러"""
    pass

class MetadataExtractionError(Exception):
    """메타데이터 추출 에러"""
    pass

class InsufficientDiskSpaceError(Exception):
    """디스크 공간 부족 에러"""
    pass
```

**2. 서비스 레이어 에러 처리**

```python
# backend/services/download_service.py

from fastapi import HTTPException, status

class DownloadService:
    async def start_download(self, request: dict) -> str:
        try:
            # 디스크 공간 체크
            from services.file_service import FileService
            file_service = FileService()
            space = await file_service.get_disk_space(request.get('download_path'))
            
            if space['free'] < 100 * 1024 * 1024:  # 100MB 미만
                raise HTTPException(
                    status_code=status.HTTP_507_INSUFFICIENT_STORAGE,
                    detail={
                        "message": "디스크 공간이 부족합니다.",
                        "free_space": space['free'],
                        "required_space": 100 * 1024 * 1024
                    }
                )
            
            # 다운로드 시작
            task_id = str(uuid.uuid4())
            # ... 다운로드 로직
            
            return task_id
            
        except yt_dlp.utils.DownloadError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "다운로드 중 오류가 발생했습니다.",
                    "error": str(e)
                }
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={
                    "message": "예기치 않은 오류가 발생했습니다.",
                    "error": str(e)
                }
            )
```

**3. 로깅 시스템**

```python
# backend/utils/logger.py

import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logger(name: str, log_file: str, level=logging.INFO):
    """로거 설정"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # 파일 핸들러 (10MB 크기, 5개 백업)
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding='utf-8'
    )
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)
    
    logger.addHandler(handler)
    
    # 콘솔 핸들러
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

# 전역 로거
app_logger = setup_logger(
    'tropical_downloader',
    os.path.join(os.path.expanduser('~'), '.tropical_downloader', 'app.log')
)
```

---

## Testing Strategy

### Unit Testing

**Frontend Unit Tests (Jest + React Testing Library)**

```typescript
// renderer/src/components/__tests__/MediaCard.test.tsx

import { render, screen } from '@testing-library/react';
import { MediaCard } from '../MediaCard';

describe('MediaCard', () => {
  const mockMetadata = {
    title: 'Test Video',
    uploader: 'Test Channel',
    duration: 300,
    thumbnail: 'https://example.com/thumb.jpg'
  };
  
  test('renders media information correctly', () => {
    render(<MediaCard metadata={mockMetadata} />);
    
    expect(screen.getByText('Test Video')).toBeInTheDocument();
    expect(screen.getByText('Test Channel')).toBeInTheDocument();
    expect(screen.getByText('5:00')).toBeInTheDocument();  // duration formatting
  });
  
  test('displays thumbnail image', () => {
    render(<MediaCard metadata={mockMetadata} />);
    
    const img = screen.getByRole('img');
    expect(img).toHaveAttribute('src', mockMetadata.thumbnail);
  });
});
```

**Backend Unit Tests (pytest)**

```python
# backend/tests/test_info_fetcher_service.py

import pytest
from services.info_fetcher_service import InfoFetcherService

@pytest.mark.asyncio
async def test_fetch_info_single_video():
    """단일 비디오 정보 추출 테스트"""
    service = InfoFetcherService()
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Mock yt-dlp extract_info
    with patch('yt_dlp.YoutubeDL.extract_info') as mock_extract:
        mock_extract.return_value = {
            'title': 'Test Video',
            'uploader': 'Test Channel',
            'duration': 300,
            'formats': []
        }
        
        result = await service.fetch_info(url)
        
        assert result['is_playlist'] == False
        assert result['title'] == 'Test Video'
        assert result['uploader'] == 'Test Channel'
        assert result['duration'] == 300

@pytest.mark.asyncio
async def test_fetch_info_handles_cookie_error():
    """쿠키 오류 처리 테스트"""
    service = InfoFetcherService()
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    with patch('yt_dlp.YoutubeDL.extract_info') as mock_extract:
        # 첫 시도: DPAPI 오류
        mock_extract.side_effect = [
            Exception("DPAPI decryption failed"),
            {'title': 'Test Video', 'formats': []}  # 재시도 성공
        ]
        
        result = await service.fetch_info(url)
        
        assert result['title'] == 'Test Video'
        assert mock_extract.call_count == 2  # 재시도 확인
```

### Integration Testing

**API Endpoint Tests**

```python
# backend/tests/test_api_endpoints.py

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """루트 엔드포인트 테스트"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "running"

def test_analyze_endpoint():
    """분석 엔드포인트 테스트"""
    response = client.post(
        "/api/analyze",
        json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "formats" in data

def test_download_endpoint():
    """다운로드 엔드포인트 테스트"""
    response = client.post(
        "/api/download",
        json={
            "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "format_id": "22",
            "extract_audio": False
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert isinstance(data["task_id"], str)

def test_invalid_url_returns_error():
    """잘못된 URL 에러 테스트"""
    response = client.post(
        "/api/analyze",
        json={"url": "not_a_valid_url"}
    )
    assert response.status_code == 422  # Validation Error
```

### End-to-End Testing

**Electron E2E Tests (Playwright)**

```typescript
// e2e/tests/download-workflow.spec.ts

import { test, expect, _electron as electron } from '@playwright/test';

test.describe('Download Workflow', () => {
  test('complete download workflow from URL input to completion', async () => {
    // Electron 앱 시작
    const app = await electron.launch({
      args: ['./dist/main.js']
    });
    
    const window = await app.firstWindow();
    
    // URL 입력
    await window.fill('input[name="url"]', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ');
    await window.click('button:has-text("분석")');
    
    // 메타데이터 로딩 대기
    await window.waitForSelector('.media-card');
    
    // 미디어 정보 확인
    const title = await window.textContent('.media-title');
    expect(title).toBeTruthy();
    
    // 다운로드 시작
    await window.click('button:has-text("최고화질 다운로드")');
    
    // 큐 탭으로 이동
    await window.click('button:has-text("다운로드 큐")');
    
    // 진행상황 확인
    await window.waitForSelector('.download-task');
    const progress = await window.textContent('.progress-percentage');
    expect(progress).toMatch(/\d+%/);
    
    // 완료 대기 (타임아웃 설정)
    await window.waitForSelector('.task-status:has-text("완료")', { timeout: 60000 });
    
    // 앱 종료
    await app.close();
  });
});
```

### Performance Testing

**다운로드 동시성 테스트**

```python
# backend/tests/test_performance.py

import pytest
import asyncio
from services.download_service import DownloadService

@pytest.mark.asyncio
async def test_concurrent_downloads():
    """동시 다운로드 성능 테스트"""
    service = DownloadService()
    
    urls = [
        "https://www.youtube.com/watch?v=test1",
        "https://www.youtube.com/watch?v=test2",
        "https://www.youtube.com/watch?v=test3",
        "https://www.youtube.com/watch?v=test4",
        "https://www.youtube.com/watch?v=test5",
    ]
    
    # 동시 다운로드 시작
    tasks = [
        service.start_download({"url": url, "format_id": "22"})
        for url in urls
    ]
    
    task_ids = await asyncio.gather(*tasks)
    
    # 모든 작업이 생성되었는지 확인
    assert len(task_ids) == 5
    assert all(isinstance(tid, str) for tid in task_ids)
    
    # 활성 작업 확인
    active_tasks = await service.list_active_tasks()
    assert len(active_tasks) >= 5
```

---

## Frutiger Aero Design System Implementation

### CSS 변수 정의

```css
/* renderer/src/styles/tropical-theme.css */

:root {
  /* Tropical Color Palette */
  --color-lagoon-cyan: #00E5FF;
  --color-tropical-emerald: #06D6A0;
  --color-sunshine-yellow: #FFD166;
  --color-sunset-coral: #FF6B6B;
  --color-sky-blue: #4EC3FF;
  --color-ocean-deep: #0077B6;
  --color-palm-green: #2A9D8F;
  
  /* Neutrals */
  --color-white: #FFFFFF;
  --color-gray-50: #F8FAFC;
  --color-gray-100: #F1F5F9;
  --color-gray-200: #E2E8F0;
  --color-gray-700: #334155;
  --color-gray-900: #0F172A;
  
  /* Glassmorphism */
  --glass-bg: rgba(255, 255, 255, 0.7);
  --glass-border: rgba(255, 255, 255, 0.3);
  --glass-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
  --glass-blur: blur(10px);
  
  /* Aqua Gel Button */
  --aqua-gradient-start: var(--color-lagoon-cyan);
  --aqua-gradient-end: var(--color-sky-blue);
  --aqua-highlight: rgba(255, 255, 255, 0.4);
  --aqua-shadow: 0 4px 15px rgba(0, 229, 255, 0.3);
  
  /* Animations */
  --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  --transition-bounce: all 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
}

/* Dark Theme */
[data-theme="dark"] {
  --glass-bg: rgba(15, 23, 42, 0.7);
  --glass-border: rgba(255, 255, 255, 0.1);
  --color-gray-50: #1E293B;
  --color-gray-100: #334155;
}
```

### Aqua Gel Button Component

```tsx
// renderer/src/components/design-system/AquaGelButton.tsx

import React from 'react';
import styled from '@emotion/styled';

interface AquaGelButtonProps {
  children: React.ReactNode;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
}

const StyledButton = styled.button<{ variant: string; size: string }>`
  position: relative;
  padding: ${props => {
    switch (props.size) {
      case 'sm': return '8px 16px';
      case 'lg': return '16px 32px';
      default: return '12px 24px';
    }
  }};
  font-size: ${props => {
    switch (props.size) {
      case 'sm': return '14px';
      case 'lg': return '18px';
      default: return '16px';
    }
  }};
  font-weight: 600;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  transition: var(--transition-smooth);
  
  /* Gradient Background */
  background: ${props => {
    switch (props.variant) {
      case 'success':
        return 'linear-gradient(135deg, var(--color-tropical-emerald), var(--color-palm-green))';
      case 'danger':
        return 'linear-gradient(135deg, var(--color-sunset-coral), #EF4444)';
      case 'secondary':
        return 'linear-gradient(135deg, var(--color-gray-200), var(--color-gray-100))';
      default:
        return 'linear-gradient(135deg, var(--color-lagoon-cyan), var(--color-sky-blue))';
    }
  }};
  
  color: ${props => props.variant === 'secondary' ? 'var(--color-gray-900)' : 'white'};
  
  /* Glossy Top Highlight */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.4), transparent);
    border-radius: 12px 12px 0 0;
    pointer-events: none;
  }
  
  /* Shadow */
  box-shadow: ${props => {
    switch (props.variant) {
      case 'success':
        return '0 4px 15px rgba(6, 214, 160, 0.3)';
      case 'danger':
        return '0 4px 15px rgba(255, 107, 107, 0.3)';
      default:
        return 'var(--aqua-shadow)';
    }
  }};
  
  /* Hover Effect */
  &:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: ${props => {
      switch (props.variant) {
        case 'success':
          return '0 6px 20px rgba(6, 214, 160, 0.4)';
        case 'danger':
          return '0 6px 20px rgba(255, 107, 107, 0.4)';
        default:
          return '0 6px 20px rgba(0, 229, 255, 0.4)';
      }
    }};
  }
  
  /* Active Effect */
  &:active:not(:disabled) {
    transform: translateY(0);
  }
  
  /* Disabled State */
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

export const AquaGelButton: React.FC<AquaGelButtonProps> = ({
  children,
  onClick,
  variant = 'primary',
  size = 'md',
  disabled = false
}) => {
  return (
    <StyledButton
      variant={variant}
      size={size}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </StyledButton>
  );
};
```

### Glassmorphism Card Component

```tsx
// renderer/src/components/design-system/GlassmorphismCard.tsx

import React from 'react';
import styled from '@emotion/styled';

interface GlassCardProps {
  children: React.ReactNode;
  className?: string;
  elevation?: 'low' | 'medium' | 'high';
}

const StyledCard = styled.div<{ elevation: string }>`
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: 16px;
  padding: 24px;
  box-shadow: ${props => {
    switch (props.elevation) {
      case 'high':
        return '0 12px 48px 0 rgba(31, 38, 135, 0.25)';
      case 'low':
        return '0 4px 16px 0 rgba(31, 38, 135, 0.1)';
      default:
        return 'var(--glass-shadow)';
    }
  }};
  transition: var(--transition-smooth);
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: ${props => {
      switch (props.elevation) {
        case 'high':
          return '0 16px 64px 0 rgba(31, 38, 135, 0.3)';
        case 'low':
          return '0 6px 24px 0 rgba(31, 38, 135, 0.15)';
        default:
          return '0 12px 40px 0 rgba(31, 38, 135, 0.2)';
      }
    }};
  }
`;

export const GlassmorphismCard: React.FC<GlassCardProps> = ({
  children,
  className,
  elevation = 'medium'
}) => {
  return (
    <StyledCard elevation={elevation} className={className}>
      {children}
    </StyledCard>
  );
};
```

### Progress Bar with Animation

```tsx
// renderer/src/components/design-system/TropicalProgressBar.tsx

import React from 'react';
import styled from '@emotion/styled';
import { keyframes } from '@emotion/react';

interface ProgressBarProps {
  progress: number;  // 0-100
  color?: 'cyan' | 'emerald' | 'coral';
  animated?: boolean;
}

const shimmer = keyframes`
  0% {
    background-position: -1000px 0;
  }
  100% {
    background-position: 1000px 0;
  }
`;

const ProgressContainer = styled.div`
  width: 100%;
  height: 24px;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  overflow: hidden;
  position: relative;
`;

const ProgressFill = styled.div<{ progress: number; color: string; animated: boolean }>`
  height: 100%;
  width: ${props => props.progress}%;
  background: ${props => {
    switch (props.color) {
      case 'emerald':
        return 'linear-gradient(90deg, var(--color-tropical-emerald), var(--color-palm-green))';
      case 'coral':
        return 'linear-gradient(90deg, var(--color-sunset-coral), #EF4444)';
      default:
        return 'linear-gradient(90deg, var(--color-lagoon-cyan), var(--color-sky-blue))';
    }
  }};
  transition: width 0.3s ease;
  position: relative;
  
  /* Glossy highlight */
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 50%;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.3), transparent);
  }
  
  /* Animated shimmer */
  ${props => props.animated && `
    &::after {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(
        90deg,
        transparent,
        rgba(255, 255, 255, 0.4),
        transparent
      );
      background-size: 1000px 100%;
      animation: ${shimmer} 2s infinite;
    }
  `}
`;

const ProgressText = styled.span`
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 12px;
  font-weight: 700;
  color: var(--color-gray-900);
  text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
`;

export const TropicalProgressBar: React.FC<ProgressBarProps> = ({
  progress,
  color = 'cyan',
  animated = true
}) => {
  return (
    <ProgressContainer>
      <ProgressFill progress={progress} color={color} animated={animated} />
      <ProgressText>{progress.toFixed(1)}%</ProgressText>
    </ProgressContainer>
  );
};
```

---

## Deployment and Packaging

### Electron Build Configuration

```javascript
// electron-builder.config.js

module.exports = {
  appId: 'com.tropical.downloader',
  productName: 'Tropical Downloader',
  directories: {
    output: 'dist',
    buildResources: 'build'
  },
  files: [
    'dist/main/**/*',
    'dist/renderer/**/*',
    'dist/backend/**/*',
    'package.json'
  ],
  extraResources: [
    {
      from: 'backend-dist',
      to: 'backend',
      filter: ['**/*']
    },
    {
      from: 'resources',
      to: 'resources',
      filter: ['**/*']
    }
  ],
  win: {
    target: ['nsis', 'portable'],
    icon: 'build/icon.ico',
    artifactName: '${productName}-${version}-${arch}.${ext}'
  },
  nsis: {
    oneClick: false,
    perMachine: false,
    allowToChangeInstallationDirectory: true,
    createDesktopShortcut: true,
    createStartMenuShortcut: true,
    shortcutName: 'Tropical Downloader'
  },
  mac: {
    target: ['dmg', 'zip'],
    icon: 'build/icon.icns',
    category: 'public.app-category.utilities',
    hardenedRuntime: true,
    gatekeeperAssess: false
  },
  linux: {
    target: ['AppImage', 'deb'],
    icon: 'build/icons',
    category: 'Utility',
    maintainer: 'Tropical Downloader Team'
  }
};
```

### Python Backend Packaging

```python
# backend/build.py
# PyInstaller 스크립트

import PyInstaller.__main__
import sys
import os

def build_backend():
    """Python 백엔드를 단일 실행 파일로 빌드"""
    
    # PyInstaller 옵션
    options = [
        'main.py',                          # 진입점
        '--name=tropical-backend',          # 출력 파일 이름
        '--onefile',                        # 단일 실행 파일
        '--clean',                          # 빌드 전 캐시 정리
        '--noconfirm',                      # 덮어쓰기 확인 안함
        
        # 추가 데이터 파일
        '--add-data=.env:.',
        
        # 숨겨진 임포트 (PyInstaller가 자동 감지 못하는 모듈)
        '--hidden-import=uvicorn.logging',
        '--hidden-import=uvicorn.loops',
        '--hidden-import=uvicorn.loops.auto',
        '--hidden-import=uvicorn.protocols',
        '--hidden-import=uvicorn.protocols.http',
        '--hidden-import=uvicorn.protocols.http.auto',
        '--hidden-import=uvicorn.protocols.websockets',
        '--hidden-import=uvicorn.protocols.websockets.auto',
        '--hidden-import=uvicorn.lifespan',
        '--hidden-import=uvicorn.lifespan.on',
        '--hidden-import=yt_dlp',
        
        # 콘솔 숨기기 (Windows)
        '--noconsole' if sys.platform == 'win32' else '',
        
        # 출력 디렉토리
        '--distpath=../backend-dist',
        '--workpath=../build/backend',
        '--specpath=../build'
    ]
    
    # 빈 문자열 제거
    options = [opt for opt in options if opt]
    
    PyInstaller.__main__.run(options)

if __name__ == '__main__':
    build_backend()
```

### Build Scripts

```json
// package.json

{
  "name": "tropical-downloader",
  "version": "2.0.0",
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "cd backend && uvicorn main:app --reload --port 8765",
    "dev:frontend": "vite",
    
    "build": "npm run build:backend && npm run build:frontend && npm run build:electron",
    "build:backend": "cd backend && python build.py",
    "build:frontend": "vite build",
    "build:electron": "electron-builder",
    
    "build:win": "npm run build && electron-builder --win",
    "build:mac": "npm run build && electron-builder --mac",
    "build:linux": "npm run build && electron-builder --linux",
    
    "test": "npm run test:frontend && npm run test:backend",
    "test:frontend": "jest",
    "test:backend": "cd backend && pytest",
    
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix"
  }
}
```

---

## Security Considerations

### 1. Backend API 보안

- **CORS 제한**: `localhost` 및 `file://` 프로토콜만 허용
- **입력 검증**: Pydantic 모델로 모든 요청 데이터 검증
- **Rate Limiting**: 과도한 API 호출 방지
- **로그 민감 정보 마스킹**: 쿠키, 비밀번호 등 로그에 기록 금지

```python
# backend/middleware/security.py

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
```

### 2. Electron 보안

- **Context Isolation 활성화**: Renderer와 Main 프로세스 분리
- **nodeIntegration 비활성화**: XSS 공격 방지
- **IPC 화이트리스트**: 허용된 IPC 채널만 사용

```typescript
// main/window.ts

const window = new BrowserWindow({
  webPreferences: {
    contextIsolation: true,          // 필수
    nodeIntegration: false,           // 필수
    sandbox: true,                    // 권장
    preload: path.join(__dirname, 'preload.js')
  }
});
```

### 3. 데이터 보안

- **쿠키 보안 저장**: 브라우저 쿠키 추출 시 읽기 전용 모드
- **민감 정보 암호화**: 사용자 인증 정보는 OS 키체인 활용
- **임시 파일 정리**: 다운로드 중 생성된 임시 파일 자동 삭제

---

## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system-essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property Reflection

After analyzing all acceptance criteria, the following properties were identified and consolidated to eliminate redundancy:

**Consolidations Made:**
- Properties related to metadata extraction (4.1, 4.2, 4.3) were combined into a single comprehensive metadata property
- Download task state management properties (5.1, 5.4, 5.5, 6.1, 6.2, 6.3, 6.5) were consolidated into state transition properties
- Playlist batch download properties (7.1, 7.2, 7.5) were combined into comprehensive playlist handling properties
- History management properties (9.1, 9.2, 9.3) were consolidated into history data integrity properties

**Properties Excluded:**
- Infrastructure as Code properties (backend startup, port binding, process management) are smoke tests, not properties
- UI rendering and interaction behaviors are example-based tests, not universal properties
- Build and deployment requirements are smoke tests verifying artifacts exist
- Documentation requirements are not testable code behavior

### Property 1: JSON Serialization Round-Trip

*For any* API response object (metadata, task status, history entry, config), serializing to JSON and deserializing back should preserve all data fields and their values.

**Validates: Requirements 3.4**

### Property 2: Error Response Structure

*For any* error condition in the Python backend, the HTTP response SHALL include an appropriate status code (4xx or 5xx) and a JSON body containing an error message field.

**Validates: Requirements 3.5, 23.1**

### Property 3: Media Metadata Completeness

*For any* valid media URL that successfully extracts metadata, the response SHALL contain all required fields: title, uploader, duration, thumbnail, description, url, and either formats (for single videos) or playlist_entries (for playlists).

**Validates: Requirements 4.1, 4.2, 4.3, 4.4**

### Property 4: Format Information Completeness

*For any* media URL with available formats, each format object SHALL contain format_id, ext, resolution, vcodec, acodec, filesize, and is_video/is_audio flags.

**Validates: Requirements 4.3**

### Property 5: Playlist Structure Integrity

*For any* playlist URL, if is_playlist flag is true, then playlist_entries list SHALL be non-empty and each entry SHALL contain index, id, title, duration, and url fields.

**Validates: Requirements 4.4**

### Property 6: Download Task Creation

*For any* valid download request (URL, format options), the backend SHALL generate a unique task_id and the task SHALL appear in the active tasks list with status 'queued' or 'downloading'.

**Validates: Requirements 5.1**

### Property 7: Task Status Completion

*For any* download task that completes successfully, the final task status SHALL be 'completed', SHALL include a valid file_path, and SHALL have progress equal to 100%.

**Validates: Requirements 5.4**

### Property 8: Task Status Failure

*For any* download task that encounters an error, the final task status SHALL be 'failed' and SHALL include a non-empty error message field.

**Validates: Requirements 5.5**

### Property 9: Task State Transitions

*For any* download task, state transitions SHALL follow valid sequences: 
- queued → downloading → completed
- queued → downloading → failed
- downloading → paused → downloading
- downloading → cancelled
- failed → queued (retry)

Invalid transitions (e.g., completed → downloading, cancelled → paused) SHALL NOT occur.

**Validates: Requirements 6.1, 6.2, 6.3, 6.4, 6.5**

### Property 10: Task Cancellation Cleanup

*For any* download task that is cancelled, the task status SHALL become 'cancelled', temporary download files SHALL be removed, and the task SHALL no longer appear in active tasks list.

**Validates: Requirements 6.1**

### Property 11: Pause and Resume Consistency

*For any* download task that is paused and then resumed, the download progress SHALL continue from where it stopped (downloaded_bytes SHALL not reset to zero).

**Validates: Requirements 6.2, 6.3**

### Property 12: Retry Task Preservation

*For any* failed download task that is retried, the new task SHALL use the same URL, format options, and download settings as the original failed task.

**Validates: Requirements 6.4**

### Property 13: Playlist Batch Task Creation

*For any* playlist download request with range specification (e.g., "1-10"), the number of tasks created SHALL equal the number of items in the specified range, and each task SHALL have a unique task_id.

**Validates: Requirements 7.1, 7.2**

### Property 14: Task ID Uniqueness

*For any* set of download tasks created (single or batch), all task_ids SHALL be unique - no duplicates SHALL exist in the active tasks list or history.

**Validates: Requirements 7.2**

### Property 15: Playlist Resilience

*For any* playlist batch download where some tasks fail, the remaining tasks SHALL continue to completion independently - failure of one task SHALL NOT cause other tasks to be cancelled or fail.

**Validates: Requirements 7.5**

### Property 16: Filename Template Application

*For any* download with a specified filename template, the output filename SHALL match the template pattern with all template variables (%(title)s, %(id)s, %(playlist_index)s, etc.) correctly substituted.

**Validates: Requirements 7.4**

### Property 17: Download Options Propagation

*For any* download request with advanced options (cookie_browser, proxy, rate_limit, embed_subs, etc.), those options SHALL be present in the yt-dlp configuration used for the download.

**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7**

### Property 18: History Entry Creation

*For any* successfully completed download, a history entry SHALL be created containing title, url, file_path, file_size, format, and timestamp fields.

**Validates: Requirements 9.1**

### Property 19: History Entry Completeness

*For any* history query response, each history entry SHALL contain all required fields: id, title, url, path, size, format, and timestamp.

**Validates: Requirements 9.2**

### Property 20: History Search Filtering

*For any* history search query with a search term, all returned entries SHALL contain the search term as a substring in either the title field or the url field (case-insensitive match).

**Validates: Requirements 9.3**

### Property 21: Data Migration Preservation

*For any* valid PySide6 configuration file or history file, after migration to the new Electron app format, all configuration settings and history entries SHALL be preserved with no data loss.

**Validates: Requirements 22.1, 22.2, 22.3, 22.4, 22.5**

### Property 22: Configuration Round-Trip

*For any* configuration object, saving to disk and loading back SHALL produce an equivalent configuration with all settings preserved (download_path, filename_template, embed options, etc.).

**Validates: Requirements 22.1, 22.2**

---


## Implementation Notes

### Critical Path Items

1. **Python Backend API First**: 백엔드 API를 먼저 구현하고 테스트한 후 프론트엔드 개발 시작
2. **WebSocket Implementation**: 실시간 진행상황 스트리밍은 초기에 구현하여 전체 아키텍처 검증
3. **yt-dlp Integration**: 기존 yt_worker.py 로직을 FastAPI 서비스 레이어로 이전
4. **Design System Components**: Frutiger Aero 디자인 컴포넌트를 재사용 가능한 라이브러리로 구축
5. **Data Migration Script**: 기존 PySide6 데이터를 새 형식으로 변환하는 마이그레이션 스크립트 우선 개발

### Technology Decisions

**Frontend Framework: React vs Vue**
- **권장: React 18+**
  - 더 큰 생태계와 Electron 통합 예제
  - TypeScript 지원 우수
  - React Testing Library로 테스트 용이
  - 단점: 학습 곡선 약간 높음

- **대안: Vue 3+**
  - 더 쉬운 학습 곡선
  - 템플릿 문법이 직관적
  - Composition API는 React Hooks와 유사
  - 단점: Electron 통합 예제 상대적으로 적음

**Backend Framework: FastAPI**
- 선택 이유:
  - 비동기 처리 네이티브 지원 (asyncio)
  - Pydantic 자동 검증
  - 자동 OpenAPI 문서 생성
  - WebSocket 지원 내장
  - 현대적이고 빠른 성능

**Python Bundler: PyInstaller vs Nuitka**
- **권장: PyInstaller**
  - 성숙한 도구, 안정적
  - yt-dlp와 호환성 검증됨
  - 크로스 플랫폼 빌드 지원
  - 단점: 실행 파일 크기 큼

- **대안: Nuitka**
  - 더 작은 실행 파일
  - 더 빠른 실행 속도
  - 단점: 빌드 시간 길고 복잡함

### Performance Optimizations

1. **Frontend Code Splitting**: React.lazy()와 Suspense로 초기 로딩 시간 단축
2. **Backend Connection Pooling**: 데이터베이스 또는 파일 시스템 작업 시 연결 풀 사용
3. **Virtual Scrolling**: 플레이리스트 목록, 히스토리 목록에 가상 스크롤링 적용
4. **WebSocket Message Batching**: 진행상황 업데이트를 100ms 간격으로 배치 전송
5. **Image Lazy Loading**: 썸네일 이미지 지연 로딩

### Migration Strategy

**Phase 1: Backend Development (Week 1-2)**
1. FastAPI 프로젝트 구조 생성
2. Core 모듈 포팅 (yt_worker, info_fetcher, etc.)
3. REST API 엔드포인트 구현
4. WebSocket 서버 구현
5. 유닛 테스트 작성

**Phase 2: Frontend Development (Week 3-4)**
1. Electron 프로젝트 초기화
2. React 프로젝트 설정
3. 디자인 시스템 컴포넌트 구현
4. 주요 탭 컴포넌트 구현 (Quick Download, Format Inspector, Queue)
5. API 클라이언트 및 WebSocket 통합

**Phase 3: Integration (Week 5)**
1. Electron Main Process와 Backend 통합
2. IPC 통신 구현
3. 네이티브 기능 통합 (파일 다이얼로그, 알림)
4. E2E 테스트 작성
5. 버그 수정 및 안정화

**Phase 4: Advanced Features (Week 6)**
1. 인앱 미디어 플레이어
2. 고급 옵션 UI
3. 데이터 마이그레이션 스크립트
4. 히스토리 검색 및 필터링
5. 성능 최적화

**Phase 5: Polish & Release (Week 7-8)**
1. Frutiger Aero 디자인 디테일 완성
2. 빌드 및 패키징 설정
3. 크로스 플랫폼 테스트 (Windows, macOS, Linux)
4. 문서 작성 (README, API 문서, 사용자 가이드)
5. 릴리스 준비

### Risk Mitigation

**Risk 1: yt-dlp 버전 호환성 문제**
- **완화 전략**: yt-dlp 버전을 requirements.txt에 고정, 자동 업데이트 메커니즘 구현

**Risk 2: Electron 빌드 크기 증가**
- **완화 전략**: Tree shaking, 불필요한 의존성 제거, asar 압축 사용

**Risk 3: WebSocket 연결 불안정**
- **완화 전략**: 자동 재연결 로직, 하트비트 메커니즘, 연결 상태 UI 표시

**Risk 4: 크로스 플랫폼 호환성 문제**
- **완화 전략**: 초기부터 3개 플랫폼 테스트 환경 구축, CI/CD 파이프라인 설정

**Risk 5: 기존 사용자 데이터 마이그레이션 실패**
- **완화 전략**: 마이그레이션 전 자동 백업, 롤백 메커니즘, 상세한 에러 로깅

### Future Enhancements

1. **자동 업데이트**: electron-updater를 사용한 자동 업데이트 기능
2. **다중 언어 지원**: i18n 라이브러리를 통한 한국어, 영어, 중국어 등 지원
3. **클라우드 동기화**: 설정 및 히스토리 클라우드 동기화
4. **브라우저 확장 프로그램**: 브라우저에서 직접 다운로드 요청 전송
5. **스케줄 다운로드**: 특정 시간에 자동 다운로드 시작
6. **비디오 편집 기능**: 간단한 트리밍, 병합 기능 추가
7. **자막 편집기**: 다운로드한 자막 편집 기능

---

## Appendix

### API Endpoint Reference

**Base URL**: `http://localhost:8765`

#### Health Check
- **GET** `/`
- Response: `{ "message": "Tropical Downloader API v2.0", "status": "running" }`

#### Media Analysis
- **POST** `/api/analyze`
- Request: `{ "url": "https://..." }`
- Response: `MediaMetadataResponse`

#### Download Management
- **POST** `/api/download` - 다운로드 시작
- **POST** `/api/download/{task_id}/pause` - 일시정지
- **POST** `/api/download/{task_id}/resume` - 재개
- **POST** `/api/download/{task_id}/cancel` - 취소
- **POST** `/api/download/{task_id}/retry` - 재시도
- **GET** `/api/download/{task_id}` - 상태 조회
- **GET** `/api/tasks` - 모든 활성 작업 목록

#### Playlist
- **POST** `/api/playlist/download` - 플레이리스트 일괄 다운로드

#### History
- **GET** `/api/history?limit=100&search=query` - 히스토리 조회
- **DELETE** `/api/history` - 히스토리 삭제

#### Configuration
- **GET** `/api/config` - 설정 조회
- **PUT** `/api/config` - 설정 업데이트

#### File System
- **GET** `/api/files?path=/some/path` - 파일 목록
- **DELETE** `/api/files?path=/some/file` - 파일 삭제
- **GET** `/api/disk-space?path=/some/path` - 디스크 공간 조회

#### Cookies
- **GET** `/api/browsers` - 설치된 브라우저 감지

#### WebSocket
- **WS** `/ws` - 실시간 진행상황 스트리밍

### WebSocket Message Format

**Progress Update**
```json
{
  "type": "progress",
  "data": {
    "task_id": "uuid",
    "progress": 45.5,
    "speed": "2.5 MB/s",
    "eta": "02:30",
    "downloaded_bytes": 50000000,
    "total_bytes": 110000000,
    "status": "downloading"
  }
}
```

**Log Message**
```json
{
  "type": "log",
  "data": {
    "task_id": "uuid",
    "level": "info",
    "message": "[info] Downloading...",
    "timestamp": "2024-01-15T10:30:45Z"
  }
}
```

**Task Complete**
```json
{
  "type": "complete",
  "data": {
    "task_id": "uuid",
    "file_path": "/path/to/file.mp4",
    "title": "Video Title"
  }
}
```

**Task Error**
```json
{
  "type": "error",
  "data": {
    "task_id": "uuid",
    "error": "Download failed: ..."
  }
}
```

### Environment Variables

```bash
# Backend (.env)
API_HOST=127.0.0.1
API_PORT=8765
CORS_ORIGINS=http://localhost:*,file://*
LOG_LEVEL=info
DOWNLOAD_PATH=/path/to/downloads
DATABASE_PATH=/path/to/db.json
MAX_CONCURRENT_DOWNLOADS=5

# Electron
NODE_ENV=production
BACKEND_PORT=8765
BACKEND_EXECUTABLE=./resources/backend/tropical-backend
```

### Project Structure

```
tropical-downloader/
├── backend/                    # Python FastAPI 백엔드
│   ├── main.py                # FastAPI 앱 진입점
│   ├── services/              # 비즈니스 로직 서비스
│   │   ├── download_service.py
│   │   ├── info_fetcher_service.py
│   │   ├── cookie_service.py
│   │   ├── history_service.py
│   │   ├── file_service.py
│   │   ├── config_service.py
│   │   └── websocket_service.py
│   ├── models/                # Pydantic 모델
│   │   └── schemas.py
│   ├── core/                  # 기존 코어 모듈 (포팅)
│   │   ├── yt_worker.py
│   │   ├── info_fetcher.py
│   │   ├── cookie_manager.py
│   │   ├── history_manager.py
│   │   └── disk_manager.py
│   ├── tests/                 # 백엔드 테스트
│   ├── requirements.txt
│   └── build.py               # PyInstaller 빌드 스크립트
│
├── electron/                  # Electron 앱
│   ├── main/                  # Main Process
│   │   ├── index.ts          # 진입점
│   │   ├── window.ts         # 윈도우 관리
│   │   ├── backend.ts        # 백엔드 프로세스 관리
│   │   └── ipc.ts            # IPC 핸들러
│   ├── preload/              # Preload 스크립트
│   │   └── index.ts
│   └── renderer/             # Renderer Process (React)
│       ├── src/
│       │   ├── components/   # React 컴포넌트
│       │   │   ├── tabs/     # 탭 컴포넌트
│       │   │   └── design-system/  # 디자인 시스템
│       │   ├── services/     # API 클라이언트, WebSocket
│       │   ├── hooks/        # Custom React hooks
│       │   ├── store/        # 상태 관리 (Redux/Zustand)
│       │   ├── styles/       # CSS, Tropical theme
│       │   ├── types/        # TypeScript 타입
│       │   └── App.tsx       # 루트 컴포넌트
│       ├── index.html
│       └── vite.config.ts
│
├── e2e/                      # E2E 테스트
│   └── tests/
│
├── build/                    # 빌드 리소스
│   ├── icon.ico
│   ├── icon.icns
│   └── icons/
│
├── resources/                # 런타임 리소스
│
├── package.json
├── electron-builder.config.js
├── tsconfig.json
└── README.md
```

---

## Conclusion

이 설계는 Tropical Downloader를 현대적이고 유지보수 가능한 Electron + Python 아키텍처로 완전히 재구축하는 포괄적인 청사진을 제공합니다. 

**핵심 성과:**
- ✅ 명확한 프론트엔드/백엔드 분리
- ✅ 웹 기술 기반의 유연한 UI (React/Vue)
- ✅ RESTful API + WebSocket 실시간 통신
- ✅ Property-based testing으로 검증 가능한 설계
- ✅ Frutiger Aero 디자인 시스템 재구현
- ✅ 크로스 플랫폼 빌드 및 배포 전략
- ✅ 독재 국가 시민을 위한 완전한 백업 및 아카이브 기능

이 설계를 따라 구현하면, 안정적이고 확장 가능하며 아름다운 유튜브 다운로더 애플리케이션을 완성할 수 있습니다.
