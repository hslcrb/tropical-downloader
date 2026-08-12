# Tropical Downloader v2.0 — 구현 완료 Walkthrough

## 개요

PySide6 기반의 "트로피컬 다운로더"를 **Electron + Python FastAPI 백엔드** 아키텍처로 완전히 재구축하였습니다.
유튜브 채널 및 계정 데이터의 영구 아카이브 기능을 포함하여, 독재 국가 민주 시민을 위한 **정보의 자유 보전** 사명을 수행합니다.

---

## 변경 사항 요약

### 🐍 Python FastAPI 백엔드 (`backend/`)

| 파일 | 설명 |
|---|---|
| backend/main.py | FastAPI 앱 진입점, CORS, 전역 예외 핸들러 |
| backend/models/schemas.py | Pydantic 요청/응답 모델 |
| backend/routes/api_router.py | 전체 REST API 엔드포인트 + WebSocket /ws |
| backend/services/info_service.py | yt-dlp 메타데이터 추출 (DPAPI 쿠키 자동 재시도) |
| backend/services/download_service.py | 멀티스레드 다운로드 엔진 (일시정지/재개/취소/재시도) |
| backend/services/channel_backup_service.py | 유튜브 채널 완전 아카이브 |
| backend/services/websocket_service.py | 실시간 WebSocket 브로드캐스트 |
| backend/tests/test_backend_api.py | API 통합 테스트 (10/10 통과) |

### ⚡ Electron 앱 (`electron/`)
- electron/main.js — Python 백엔드 자동 실행, BrowserWindow, IPC
- electron/preload.js — contextBridge window.api
- package.json — 프로젝트 설정

### 🎨 Frutiger Aero 프론트엔드 (`src/`)
9개 탭: 빠른 다운로드 / 포맷 분석 / 플레이리스트 / 채널 백업 / 큐 / 기록 / 플레이어 / 고급 옵션 / 설정

---

## 테스트 결과: 10/10 통과 ✅

---

## 실행 방법

```bash
# 백엔드 단독 실행
python backend/main.py
# → http://127.0.0.1:8765/docs (Swagger UI)

# Electron 앱 전체
npm start

# 테스트
python -m pytest backend/tests/ -v
```

## 사명 🌴
탄압받는 독재 국가의 민주 시민세력이 정보의 자유를 보전하고 영구 보존하기 위한 사명있는 프로젝트.
