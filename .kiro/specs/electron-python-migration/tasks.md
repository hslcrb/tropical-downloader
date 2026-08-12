# Tasks

## Phase 1: Backend Foundation (Week 1-2)

### 1.1 Project Setup and Structure

- [~] 1.1.1 FastAPI 프로젝트 구조 생성 (main.py, services/, models/, core/, tests/)
- [~] 1.1.2 requirements.txt 작성 (FastAPI, Uvicorn, yt-dlp, Pydantic, python-socketio)
- [~] 1.1.3 Python 가상 환경 설정 및 의존성 설치
- [~] 1.1.4 .env 파일 및 환경 변수 설정
- [~] 1.1.5 로깅 시스템 설정 (RotatingFileHandler)

### 1.2 Core FastAPI Application

- [~] 1.2.1 FastAPI 앱 초기화 및 CORS 미들웨어 설정
- [~] 1.2.2 Pydantic 모델 정의 (AnalyzeRequest, DownloadRequest, MediaMetadataResponse, TaskStatusResponse 등)
- [~] 1.2.3 전역 예외 핸들러 구현 (ValidationError, General Exception)
- [~] 1.2.4 헬스 체크 엔드포인트 구현 (GET /)
- [~] 1.2.5 API 문서 자동 생성 확인 (/docs)

### 1.3 Core Modules Porting

- [~] 1.3.1 cookie_manager.py 포팅 (브라우저 감지, 쿠키 옵션 생성)
- [~] 1.3.2 history_manager.py 포팅 (JSON 기반 히스토리 저장/로드)
- [~] 1.3.3 disk_manager.py 포팅 (디스크 공간 체크, node_modules 삭제)
- [~] 1.3.4 config_manager.py 리팩토링 (PySide6 의존성 제거)
- [~] 1.3.5 기존 코어 모듈 유닛 테스트 작성

### 1.4 Info Fetcher Service

- [~] 1.4.1 InfoFetcherService 클래스 구현 (fetch_info 메서드)
- [~] 1.4.2 yt-dlp를 사용한 메타데이터 추출 로직
- [~] 1.4.3 DPAPI 쿠키 오류 자동 재시도 로직
- [~] 1.4.4 플레이리스트 감지 및 파싱
- [~] 1.4.5 `/api/analyze` 엔드포인트 구현
- [~] 1.4.6 InfoFetcherService 유닛 테스트 (단일 비디오, 플레이리스트, 에러 처리)

### 1.5 Download Service - Part 1 (Core)

- [~] 1.5.1 DownloadService 클래스 및 DownloadTask 모델 구현
- [~] 1.5.2 작업 ID 생성 및 작업 큐 관리
- [~] 1.5.3 ThreadPoolExecutor를 사용한 비동기 다운로드 실행
- [~] 1.5.4 yt-dlp 옵션 빌더 (_build_ydl_opts 메서드)
- [~] 1.5.5 진행상황 콜백 (_progress_hook) 구현
- [~] 1.5.6 `/api/download` 엔드포인트 구현 (다운로드 시작)

### 1.6 Download Service - Part 2 (Control)

- [~] 1.6.1 `/api/download/{task_id}` 엔드포인트 구현 (상태 조회)
- [~] 1.6.2 `/api/download/{task_id}/pause` 엔드포인트 구현 (일시정지)
- [~] 1.6.3 `/api/download/{task_id}/resume` 엔드포인트 구현 (재개)
- [~] 1.6.4 `/api/download/{task_id}/cancel` 엔드포인트 구현 (취소 및 임시 파일 삭제)
- [~] 1.6.5 `/api/download/{task_id}/retry` 엔드포인트 구현 (재시도)
- [~] 1.6.6 `/api/tasks` 엔드포인트 구현 (모든 활성 작업 목록)

### 1.7 Download Service - Part 3 (Playlist)

- [~] 1.7.1 플레이리스트 일괄 다운로드 로직 (download_playlist 메서드)
- [~] 1.7.2 범위 파싱 (예: "1-10" → [1, 2, ..., 10])
- [~] 1.7.3 개별 작업 생성 및 고유 task_id 할당
- [~] 1.7.4 파일명 템플릿 적용 (%(playlist_index)s, %(title)s 등)
- [~] 1.7.5 `/api/playlist/download` 엔드포인트 구현
- [~] 1.7.6 플레이리스트 다운로드 유닛 테스트

### 1.8 WebSocket Service

- [~] 1.8.1 WebSocketService 클래스 구현 (연결 관리)
- [~] 1.8.2 `/ws` WebSocket 엔드포인트 구현
- [~] 1.8.3 진행상황 브로드캐스트 (broadcast_progress)
- [~] 1.8.4 로그 메시지 브로드캐스트 (broadcast_log)
- [~] 1.8.5 작업 완료/에러 알림 메시지
- [~] 1.8.6 WebSocket 연결 유지 및 재연결 처리
- [~] 1.8.7 WebSocket 통신 통합 테스트

### 1.9 History Service

- [~] 1.9.1 HistoryService 클래스 구현
- [~] 1.9.2 `/api/history` GET 엔드포인트 구현 (조회, 검색)
- [~] 1.9.3 히스토리 검색 필터링 로직 (제목, URL 기반)
- [~] 1.9.4 `/api/history` DELETE 엔드포인트 구현 (전체 삭제)
- [~] 1.9.5 다운로드 완료 시 히스토리 자동 저장 통합
- [~] 1.9.6 History Service 유닛 테스트

### 1.10 File System Service

- [~] 1.10.1 FileService 클래스 구현
- [~] 1.10.2 `/api/files` GET 엔드포인트 (다운로드 폴더 파일 목록)
- [~] 1.10.3 `/api/files` DELETE 엔드포인트 (파일 삭제)
- [~] 1.10.4 `/api/disk-space` GET 엔드포인트 (디스크 공간 조회)
- [~] 1.10.5 디스크 공간 부족 시 경고 로직
- [~] 1.10.6 File Service 유닛 테스트

### 1.11 Config Service

- [~] 1.11.1 ConfigService 클래스 구현
- [~] 1.11.2 `/api/config` GET 엔드포인트 (설정 조회)
- [~] 1.11.3 `/api/config` PUT 엔드포인트 (설정 업데이트)
- [~] 1.11.4 설정 파일 JSON 저장/로드
- [~] 1.11.5 기본 설정값 정의
- [~] 1.11.6 Config Service 유닛 테스트

### 1.12 Cookie Service

- [~] 1.12.1 CookieService 클래스 구현
- [~] 1.12.2 `/api/browsers` GET 엔드포인트 (설치된 브라우저 감지)
- [~] 1.12.3 브라우저별 프로필 경로 검색
- [~] 1.12.4 자동 감지 로직 (최적 브라우저 선택)
- [~] 1.12.5 Cookie Service 유닛 테스트

### 1.13 Backend Integration Tests

- [~] 1.13.1 API 엔드포인트 통합 테스트 작성 (TestClient 사용)
- [~] 1.13.2 분석 → 다운로드 → 완료 전체 플로우 테스트
- [~] 1.13.3 플레이리스트 일괄 다운로드 통합 테스트
- [~] 1.13.4 에러 시나리오 통합 테스트 (잘못된 URL, 네트워크 오류 등)
- [~] 1.13.5 WebSocket 실시간 업데이트 통합 테스트

### 1.14 Backend Performance & Security

- [~] 1.14.1 Rate Limiting 미들웨어 추가 (slowapi)
- [~] 1.14.2 보안 헤더 추가 (X-Content-Type-Options, X-Frame-Options 등)
- [~] 1.14.3 로그 민감 정보 마스킹 (쿠키, 비밀번호)
- [~] 1.14.4 동시 다운로드 제한 설정 (MAX_CONCURRENT_DOWNLOADS)
- [~] 1.14.5 성능 테스트 (동시 요청 처리)

---

## Phase 2: Frontend Foundation (Week 3-4)

### 2.1 Electron Project Setup

- [~] 2.1.1 Electron 프로젝트 초기화 (package.json, electron-builder 설정)
- [~] 2.1.2 TypeScript 설정 (tsconfig.json)
- [~] 2.1.3 Main Process 디렉토리 구조 생성 (main/, preload/)
- [~] 2.1.4 Renderer Process 디렉토리 구조 생성 (renderer/)
- [~] 2.1.5 개발 환경 스크립트 설정 (dev, build, test)

### 2.2 React Project Setup

- [~] 2.2.1 Vite + React + TypeScript 프로젝트 생성
- [~] 2.2.2 React Router 설정 (탭 네비게이션)
- [~] 2.2.3 상태 관리 라이브러리 선택 및 설정 (Redux Toolkit 또는 Zustand)
- [~] 2.2.4 CSS 프레임워크 설정 (TailwindCSS 또는 Emotion)
- [~] 2.2.5 ESLint 및 Prettier 설정

### 2.3 Electron Main Process

- [~] 2.3.1 Main Process 진입점 (main/index.ts) 구현
- [~] 2.3.2 BrowserWindow 생성 및 관리 (main/window.ts)
- [~] 2.3.3 Context Isolation 및 Preload 스크립트 설정
- [~] 2.3.4 개발/프로덕션 모드 분기 처리
- [~] 2.3.5 앱 생명주기 이벤트 핸들링 (ready, window-all-closed, activate)

### 2.4 Backend Process Management

- [~] 2.4.1 BackendProcessManager 클래스 구현 (main/backend.ts)
- [~] 2.4.2 Python 백엔드 프로세스 spawn 로직
- [~] 2.4.3 백엔드 포트 동적 할당 또는 고정 포트 사용
- [~] 2.4.4 백엔드 시작 대기 및 헬스 체크 (포트 응답 확인)
- [~] 2.4.5 백엔드 종료 로직 (SIGTERM 전송)
- [~] 2.4.6 백엔드 크래시 감지 및 재시작
- [~] 2.4.7 백엔드 로그 파일 캡처 및 저장

### 2.5 IPC Communication

- [~] 2.5.1 IPC 핸들러 등록 (main/ipc.ts)
- [~] 2.5.2 `selectFolder` IPC 핸들러 (폴더 선택 대화상자)
- [~] 2.5.3 `openPath` IPC 핸들러 (파일/폴더 열기)
- [~] 2.5.4 `showNotification` IPC 핸들러 (시스템 알림)
- [~] 2.5.5 `getBackendStatus` IPC 핸들러 (백엔드 상태 조회)
- [~] 2.5.6 Preload 스크립트에서 IPC API 노출 (contextBridge)

### 2.6 API Client Service

- [~] 2.6.1 APIClient 클래스 구현 (renderer/src/services/apiClient.ts)
- [~] 2.6.2 axios 또는 fetch 기반 HTTP 요청 래퍼
- [~] 2.6.3 Base URL 설정 및 요청/응답 인터셉터
- [~] 2.6.4 에러 핸들링 래퍼 (handleAPICall)
- [~] 2.6.5 모든 API 메서드 구현 (analyzeMedia, startDownload, pauseDownload, etc.)
- [~] 2.6.6 TypeScript 타입 정의 (models.ts)

### 2.7 WebSocket Client Service

- [~] 2.7.1 WebSocketClient 클래스 구현 (renderer/src/services/websocketClient.ts)
- [~] 2.7.2 WebSocket 연결 및 이벤트 리스너 등록
- [~] 2.7.3 자동 재연결 로직 (Exponential Backoff)
- [~] 2.7.4 메시지 타입별 콜백 등록 (onProgress, onLog, onTaskComplete, onTaskError)
- [~] 2.7.5 연결 상태 관리 (connecting, connected, disconnected, error)
- [~] 2.7.6 WebSocket 클라이언트 유닛 테스트

### 2.8 Design System - Theme & Variables

- [~] 2.8.1 Tropical 컬러 팔레트 CSS 변수 정의 (tropical-theme.css)
- [~] 2.8.2 다크 모드 CSS 변수 정의
- [~] 2.8.3 Glassmorphism 스타일 변수 정의
- [~] 2.8.4 애니메이션 및 트랜지션 변수 정의
- [~] 2.8.5 테마 전환 로직 구현 (light, dark, system)

### 2.9 Design System - Components

- [~] 2.9.1 AquaGelButton 컴포넌트 구현 (variants, sizes, disabled state)
- [~] 2.9.2 GlassmorphismCard 컴포넌트 구현 (elevation levels)
- [~] 2.9.3 TropicalProgressBar 컴포넌트 구현 (shimmer animation)
- [~] 2.9.4 TropicalIcon 컴포넌트 구현 (SVG 아이콘 라이브러리)
- [~] 2.9.5 MediaCard 컴포넌트 구현 (썸네일, 제목, 업로더, 재생시간)
- [~] 2.9.6 FormatTable 컴포넌트 구현 (정렬, 필터링)
- [~] 2.9.7 디자인 시스템 Storybook 설정 (선택적)

### 2.10 Quick Download Tab

- [~] 2.10.1 QuickDownloadTab 컴포넌트 구조 생성
- [~] 2.10.2 URL 입력 필드 및 검증
- [~] 2.10.3 클립보드 자동 감지 및 붙여넣기 버튼
- [~] 2.10.4 분석 버튼 및 로딩 스피너
- [~] 2.10.5 MediaCard 표시 (분석 결과)
- [~] 2.10.6 원클릭 프리셋 버튼 (4K, 1080p, 720p, MP3, FLAC)
- [~] 2.10.7 다운로드 시작 및 큐로 이동
- [~] 2.10.8 QuickDownloadTab 유닛 테스트

### 2.11 Format Inspector Tab

- [~] 2.11.1 FormatInspectorTab 컴포넌트 구조 생성
- [~] 2.11.2 URL 입력 및 분석 (QuickDownloadTab과 공유 가능)
- [~] 2.11.3 FormatTable 통합 (비디오/오디오 포맷 목록)
- [~] 2.11.4 비디오 스트림 선택 (라디오 버튼 또는 드롭다운)
- [~] 2.11.5 오디오 스트림 선택
- [~] 2.11.6 컨테이너 포맷 선택 (MP4, MKV, WEBM)
- [~] 2.11.7 자막 및 썸네일 임베딩 체크박스
- [~] 2.11.8 고급 다운로드 버튼
- [~] 2.11.9 FormatInspectorTab 유닛 테스트

### 2.12 Playlist Tab

- [~] 2.12.1 PlaylistTab 컴포넌트 구조 생성
- [~] 2.12.2 플레이리스트 URL 입력 및 분석
- [~] 2.12.3 플레이리스트 항목 목록 표시 (가상 스크롤링)
- [~] 2.12.4 항목별 체크박스 및 전체 선택/해제
- [~] 2.12.5 범위 선택 입력 (예: "1-10", "1,3,5")
- [~] 2.12.6 파일명 템플릿 설정 입력
- [~] 2.12.7 일괄 다운로드 버튼
- [~] 2.12.8 PlaylistTab 유닛 테스트

### 2.13 Queue Tab

- [~] 2.13.1 QueueTab 컴포넌트 구조 생성
- [~] 2.13.2 활성 작업 목록 표시 (WebSocket 연동)
- [~] 2.13.3 각 작업의 진행률 바 및 상태 표시
- [~] 2.13.4 다운로드 속도, ETA, 파일 크기 표시
- [~] 2.13.5 일시정지/재개/취소 버튼
- [~] 2.13.6 완료된 작업: 파일 열기, 폴더 열기 버튼
- [~] 2.13.7 실패한 작업: 재시도 버튼
- [~] 2.13.8 작업 상태 실시간 업데이트
- [~] 2.13.9 QueueTab 유닛 테스트

### 2.14 History Tab

- [~] 2.14.1 HistoryTab 컴포넌트 구조 생성
- [~] 2.14.2 히스토리 목록 표시 (가상 스크롤링)
- [~] 2.14.3 검색 입력 필드 및 필터링
- [~] 2.14.4 히스토리 항목 클릭 시 상세 정보 모달
- [~] 2.14.5 히스토리 전체 삭제 버튼
- [~] 2.14.6 히스토리 항목별 파일 열기, 폴더 열기
- [~] 2.14.7 HistoryTab 유닛 테스트

### 2.15 Advanced Options Tab

- [~] 2.15.1 AdvancedOptionsTab 컴포넌트 구조 생성
- [~] 2.15.2 브라우저 쿠키 선택 드롭다운 (감지된 브라우저 목록)
- [~] 2.15.3 쿠키 파일 경로 입력 및 파일 선택 버튼
- [~] 2.15.4 SponsorBlock 옵션 체크박스 그룹
- [~] 2.15.5 다운로드 속도 제한 입력
- [~] 2.15.6 프록시 설정 입력
- [~] 2.15.7 자막 언어 선택 (다중 선택)
- [~] 2.15.8 사용자 정의 yt-dlp CLI 인자 텍스트 영역
- [~] 2.15.9 옵션 저장 및 적용
- [~] 2.15.10 AdvancedOptionsTab 유닛 테스트

### 2.16 Settings Tab

- [~] 2.16.1 SettingsTab 컴포넌트 구조 생성
- [~] 2.16.2 다운로드 폴더 경로 입력 및 폴더 선택 대화상자 (IPC 사용)
- [~] 2.16.3 파일명 템플릿 설정 입력
- [~] 2.16.4 FFmpeg 경로 설정 입력
- [~] 2.16.5 테마 선택 (Light, Dark, System)
- [~] 2.16.6 알림 활성화 체크박스
- [~] 2.16.7 설정 저장 및 API 호출
- [~] 2.16.8 SettingsTab 유닛 테스트

### 2.17 Media Player Tab

- [~] 2.17.1 PlayerTab 컴포넌트 구조 생성
- [~] 2.17.2 HTML5 video/audio 플레이어 통합
- [~] 2.17.3 재생, 일시정지, 탐색 컨트롤
- [~] 2.17.4 볼륨 조절, 음소거
- [~] 2.17.5 배속 조절 (0.5x, 1x, 1.5x, 2x)
- [~] 2.17.6 전체화면 모드
- [~] 2.17.7 다운로드 폴더 파일 목록 표시 (비디오/오디오 필터링)
- [~] 2.17.8 자막 파일 (.srt) 자동 감지 및 표시
- [~] 2.17.9 PlayerTab 유닛 테스트

### 2.18 Global UI Components

- [~] 2.18.1 App Shell (헤더, 탭 네비게이션, 메인 콘텐츠 영역)
- [~] 2.18.2 헤더 컴포넌트 (로고, 백엔드 상태 표시, 설정 아이콘)
- [~] 2.18.3 ErrorBoundary 컴포넌트 (전역 에러 처리)
- [~] 2.18.4 Toast 알림 시스템 (성공, 경고, 에러 메시지)
- [~] 2.18.5 로딩 스피너 및 스켈레톤 UI
- [~] 2.18.6 확인 대화상자 컴포넌트 (삭제, 취소 확인 등)

### 2.19 State Management

- [~] 2.19.1 Redux/Zustand 스토어 구조 설계
- [~] 2.19.2 Downloads Slice (활성 작업 상태 관리)
- [~] 2.19.3 History Slice (히스토리 데이터)
- [~] 2.19.4 Config Slice (앱 설정)
- [~] 2.19.5 UI Slice (현재 탭, 모달 상태 등)
- [~] 2.19.6 WebSocket 이벤트와 스토어 통합
- [~] 2.19.7 스토어 유닛 테스트

### 2.20 Frontend Integration

- [~] 2.20.1 모든 탭 컴포넌트를 App Router에 통합
- [~] 2.20.2 API Client와 컴포넌트 통합
- [~] 2.20.3 WebSocket Client와 Queue Tab 통합
- [~] 2.20.4 IPC 호출 통합 (파일 선택, 알림 등)
- [~] 2.20.5 에러 핸들링 및 Toast 알림 통합
- [~] 2.20.6 테마 전환 동작 확인

---

## Phase 3: Integration & Testing (Week 5)

### 3.1 Electron-Backend Integration

- [~] 3.1.1 Electron 앱 시작 시 Python 백엔드 자동 실행 통합
- [~] 3.1.2 백엔드 시작 대기 및 헬스 체크 통합
- [~] 3.1.3 백엔드 시작 실패 시 에러 UI 표시
- [~] 3.1.4 Electron 앱 종료 시 백엔드 자동 종료 통합
- [~] 3.1.5 백엔드 크래시 감지 및 사용자 알림

### 3.2 End-to-End Workflow Testing

- [~] 3.2.1 Playwright 또는 Spectron E2E 테스트 환경 설정
- [~] 3.2.2 E2E 테스트: 빠른 다운로드 전체 플로우
- [~] 3.2.3 E2E 테스트: 포맷 분석 및 고급 다운로드
- [~] 3.2.4 E2E 테스트: 플레이리스트 일괄 다운로드
- [~] 3.2.5 E2E 테스트: 다운로드 일시정지/재개/취소
- [~] 3.2.6 E2E 테스트: 히스토리 검색 및 조회
- [~] 3.2.7 E2E 테스트: 설정 변경 및 저장
- [~] 3.2.8 E2E 테스트: 인앱 플레이어 재생

### 3.3 Property-Based Testing Implementation

- [~] 3.3.1 Python 백엔드 Property 테스트 프레임워크 선택 (Hypothesis)
- [~] 3.3.2 Property 1 구현: JSON 직렬화 라운드트립 (test_json_serialization_roundtrip)
- [~] 3.3.3 Property 2 구현: 에러 응답 구조 (test_error_response_structure)
- [~] 3.3.4 Property 3 구현: 미디어 메타데이터 완전성 (test_metadata_completeness)
- [~] 3.3.5 Property 4 구현: 포맷 정보 완전성 (test_format_info_completeness)
- [~] 3.3.6 Property 5 구현: 플레이리스트 구조 무결성 (test_playlist_structure_integrity)
- [~] 3.3.7 Property 6 구현: 다운로드 작업 생성 (test_download_task_creation)
- [~] 3.3.8 Property 7 구현: 작업 상태 완료 (test_task_status_completion)
- [~] 3.3.9 Property 8 구현: 작업 상태 실패 (test_task_status_failure)
- [~] 3.3.10 Property 9 구현: 작업 상태 전환 (test_task_state_transitions)
- [~] 3.3.11 Property 10 구현: 작업 취소 정리 (test_task_cancellation_cleanup)
- [~] 3.3.12 Property 11 구현: 일시정지/재개 일관성 (test_pause_resume_consistency)
- [~] 3.3.13 Property 12 구현: 재시도 작업 보존 (test_retry_task_preservation)
- [~] 3.3.14 Property 13 구현: 플레이리스트 일괄 작업 생성 (test_playlist_batch_task_creation)
- [~] 3.3.15 Property 14 구현: 작업 ID 고유성 (test_task_id_uniqueness)
- [~] 3.3.16 Property 15 구현: 플레이리스트 복원력 (test_playlist_resilience)
- [~] 3.3.17 Property 16 구현: 파일명 템플릿 적용 (test_filename_template_application)
- [~] 3.3.18 Property 17 구현: 다운로드 옵션 전파 (test_download_options_propagation)
- [~] 3.3.19 Property 18 구현: 히스토리 항목 생성 (test_history_entry_creation)
- [~] 3.3.20 Property 19 구현: 히스토리 항목 완전성 (test_history_entry_completeness)
- [~] 3.3.21 Property 20 구현: 히스토리 검색 필터링 (test_history_search_filtering)
- [~] 3.3.22 Property 21 구현: 데이터 마이그레이션 보존 (test_data_migration_preservation)
- [~] 3.3.23 Property 22 구현: 설정 라운드트립 (test_configuration_roundtrip)

### 3.4 Bug Fixing & Stabilization

- [~] 3.4.1 통합 테스트에서 발견된 버그 수정
- [~] 3.4.2 E2E 테스트에서 발견된 버그 수정
- [~] 3.4.3 Property 테스트 실패 케이스 분석 및 수정
- [~] 3.4.4 메모리 누수 검사 및 수정
- [~] 3.4.5 성능 병목 지점 분석 및 최적화

### 3.5 Error Handling Validation

- [~] 3.5.1 백엔드 에러 처리 시나리오 테스트 (잘못된 URL, 네트워크 오류, 디스크 부족 등)
- [~] 3.5.2 프론트엔드 에러 처리 UI 검증
- [~] 3.5.3 WebSocket 연결 끊김 및 재연결 테스트
- [~] 3.5.4 백엔드 크래시 복구 테스트
- [~] 3.5.5 에러 로그 기록 확인

### 3.6 Security Audit

- [~] 3.6.1 Electron 보안 설정 검증 (contextIsolation, nodeIntegration, sandbox)
- [~] 3.6.2 IPC 화이트리스트 검증 (허용된 채널만 사용)
- [~] 3.6.3 백엔드 API CORS 설정 검증
- [~] 3.6.4 민감 정보 로그 마스킹 확인
- [~] 3.6.5 입력 검증 및 SQL/Command Injection 방어 확인

---

## Phase 4: Advanced Features (Week 6)

### 4.1 Data Migration Script

- [~] 4.1.1 PySide6 설정 파일 포맷 파싱 로직
- [~] 4.1.2 PySide6 히스토리 파일 포맷 파싱 로직
- [~] 4.1.3 새 Electron 앱 설정 포맷으로 변환
- [~] 4.1.4 새 Electron 앱 히스토리 포맷으로 변환
- [~] 4.1.5 마이그레이션 스크립트 CLI 인터페이스
- [~] 4.1.6 마이그레이션 실패 시 롤백 메커니즘
- [~] 4.1.7 마이그레이션 스크립트 테스트 (다양한 데이터 형식)

### 4.2 Advanced yt-dlp Options Integration

- [~] 4.2.1 SponsorBlock 옵션 백엔드 통합
- [~] 4.2.2 속도 제한 옵션 백엔드 통합
- [~] 4.2.3 프록시 설정 옵션 백엔드 통합
- [~] 4.2.4 자막 다운로드 및 임베딩 옵션 통합
- [~] 4.2.5 썸네일 임베딩 옵션 통합
- [~] 4.2.6 사용자 정의 CLI 인자 파싱 및 적용 (shlex 사용)
- [~] 4.2.7 고급 옵션 통합 테스트

### 4.3 Performance Optimization

- [~] 4.3.1 프론트엔드 코드 스플리팅 (React.lazy, Suspense)
- [~] 4.3.2 가상 스크롤링 적용 (Playlist, History 목록)
- [~] 4.3.3 이미지 지연 로딩 (썸네일)
- [~] 4.3.4 WebSocket 메시지 배칭 (100ms 간격)
- [~] 4.3.5 백엔드 비동기 처리 최적화 (asyncio, ThreadPoolExecutor)
- [~] 4.3.6 번들 크기 분석 및 최적화 (webpack-bundle-analyzer)
- [~] 4.3.7 성능 프로파일링 및 병목 지점 제거

### 4.4 Accessibility Improvements

- [~] 4.4.1 키보드 네비게이션 지원 (Tab, Enter, Esc 등)
- [~] 4.4.2 ARIA 속성 추가 (role, aria-label, aria-describedby)
- [~] 4.4.3 포커스 관리 (모달, 드롭다운)
- [~] 4.4.4 색상 대비 비율 확인 (WCAG AA 준수)
- [~] 4.4.5 스크린 리더 테스트 (NVDA, JAWS)

### 4.5 Logging and Debugging

- [~] 4.5.1 실시간 yt-dlp 로그 캡처 및 표시
- [~] 4.5.2 로그 레벨 필터링 (info, warning, error)
- [~] 4.5.3 로그 자동 스크롤 옵션
- [~] 4.5.4 로그 파일 내보내기 기능
- [~] 4.5.5 디버그 모드 활성화 옵션 (더 상세한 로깅)

### 4.6 User Experience Enhancements

- [~] 4.6.1 클립보드 자동 감지 및 URL 자동 붙여넣기
- [~] 4.6.2 다운로드 완료 시 시스템 알림 (Notification API)
- [~] 4.6.3 드래그 앤 드롭으로 URL 입력
- [~] 4.6.4 최근 다운로드한 URL 히스토리 (빠른 접근)
- [~] 4.6.5 다크 모드 자동 전환 (시스템 테마 감지)
- [~] 4.6.6 다운로드 완료 사운드 효과 (선택적)

---

## Phase 5: Build, Test & Release (Week 7-8)

### 5.1 Python Backend Packaging

- [~] 5.1.1 PyInstaller 빌드 스크립트 작성 (backend/build.py)
- [~] 5.1.2 히든 임포트 및 데이터 파일 설정
- [~] 5.1.3 Windows 빌드 테스트 (tropical-backend.exe)
- [~] 5.1.4 macOS 빌드 테스트 (tropical-backend)
- [~] 5.1.5 Linux 빌드 테스트 (tropical-backend)
- [~] 5.1.6 빌드된 백엔드 실행 파일 단독 테스트

### 5.2 Electron App Packaging

- [~] 5.2.1 electron-builder 설정 파일 작성 (electron-builder.config.js)
- [~] 5.2.2 아이콘 파일 준비 (icon.ico, icon.icns, icons/)
- [~] 5.2.3 백엔드 실행 파일을 extraResources에 포함
- [~] 5.2.4 Windows NSIS 설치 프로그램 설정
- [~] 5.2.5 macOS DMG 설정
- [~] 5.2.6 Linux AppImage/deb 설정
- [~] 5.2.7 빌드 스크립트 통합 (npm run build)

### 5.3 Cross-Platform Build & Test

- [~] 5.3.1 Windows 빌드 (NSIS, Portable)
- [~] 5.3.2 Windows 설치 및 실행 테스트
- [~] 5.3.3 macOS 빌드 (DMG)
- [~] 5.3.4 macOS 설치 및 실행 테스트
- [~] 5.3.5 Linux 빌드 (AppImage, deb)
- [~] 5.3.6 Linux 설치 및 실행 테스트
- [~] 5.3.7 크로스 플랫폼 호환성 이슈 해결

### 5.4 Code Signing & Notarization

- [~] 5.4.1 Windows 코드 서명 인증서 획득 (선택적)
- [~] 5.4.2 Windows 실행 파일 서명
- [~] 5.4.3 macOS 코드 서명 인증서 획득 (선택적)
- [~] 5.4.4 macOS 앱 서명 및 공증 (Notarization)
- [~] 5.4.5 서명된 앱 실행 테스트

### 5.5 Documentation

- [~] 5.5.1 README.md 업데이트 (새 아키텍처 설명)
- [~] 5.5.2 개발 환경 설정 가이드 작성
- [~] 5.5.3 빌드 및 배포 가이드 작성
- [~] 5.5.4 API 엔드포인트 명세 문서 작성 (OpenAPI 자동 생성 또는 수동)
- [~] 5.5.5 프론트엔드 컴포넌트 구조 문서 작성
- [~] 5.5.6 사용자 가이드 작성 (각 탭 기능 설명)
- [~] 5.5.7 NOTICE.md 업데이트 (Electron, React, FastAPI 라이선스 추가)

### 5.6 License & Legal Compliance

- [~] 5.6.1 About 대화상자 구현 (라이선스 정보 표시)
- [~] 5.6.2 PySide6 라이선스 제거
- [~] 5.6.3 Electron MIT 라이선스 고지
- [~] 5.6.4 React MIT 라이선스 고지
- [~] 5.6.5 FastAPI MIT 라이선스 고지
- [~] 5.6.6 yt-dlp Unlicense 고지 유지
- [~] 5.6.7 FFmpeg LGPL/GPL 고지 유지
- [~] 5.6.8 NOTICE.md 최종 검토

### 5.7 Regression Testing

- [~] 5.7.1 모든 유닛 테스트 실행 및 통과 확인
- [~] 5.7.2 모든 통합 테스트 실행 및 통과 확인
- [~] 5.7.3 모든 E2E 테스트 실행 및 통과 확인
- [~] 5.7.4 모든 Property 테스트 실행 및 통과 확인 (100 iterations)
- [~] 5.7.5 성능 테스트 실행 및 벤치마크 확인
- [~] 5.7.6 보안 테스트 재실행
- [~] 5.7.7 회귀 테스트 결과 문서화

### 5.8 Beta Testing

- [~] 5.8.1 베타 버전 빌드 (v2.0.0-beta.1)
- [~] 5.8.2 내부 테스터에게 배포
- [~] 5.8.3 베타 피드백 수집
- [~] 5.8.4 버그 수정 및 개선 사항 적용
- [~] 5.8.5 베타 버전 2 빌드 및 재배포 (필요시)

### 5.9 Release Preparation

- [~] 5.9.1 버전 번호 최종 확정 (v2.0.0)
- [~] 5.9.2 CHANGELOG.md 작성
- [~] 5.9.3 릴리스 노트 작성
- [~] 5.9.4 프로덕션 빌드 (모든 플랫폼)
- [~] 5.9.5 빌드 아티팩트 체크섬 생성 (SHA256)
- [~] 5.9.6 릴리스 패키지 압축 및 업로드
- [~] 5.9.7 GitHub Release 생성 또는 배포 웹사이트 업데이트

### 5.10 Post-Release

- [~] 5.10.1 릴리스 발표 (GitHub, 커뮤니티 등)
- [~] 5.10.2 사용자 피드백 모니터링
- [~] 5.10.3 긴급 버그 수정 계획 (핫픽스)
- [~] 5.10.4 향후 개선 사항 로드맵 작성
- [~] 5.10.5 자동 업데이트 메커니즘 구현 (선택적, v2.1.0)

---

## Summary

**총 작업 항목**: 250+ tasks
**예상 소요 기간**: 7-8주
**핵심 마일스톤**:
- Week 2: Python Backend API 완성
- Week 4: Electron Frontend UI 완성
- Week 5: 통합 및 테스트 완료
- Week 6: 고급 기능 및 최적화
- Week 8: 릴리스 준비 완료

**우선순위**:
1. **P0 (Critical)**: Backend API, Electron Main Process, 핵심 UI 탭 (Quick Download, Queue)
2. **P1 (High)**: WebSocket 통신, Design System, 나머지 UI 탭
3. **P2 (Medium)**: 고급 옵션, 데이터 마이그레이션, 성능 최적화
4. **P3 (Low)**: 추가 UX 개선, 접근성, 문서화

이 마이그레이션 프로젝트를 완료하면, Tropical Downloader는 현대적이고 안정적이며 확장 가능한 Electron + Python 아키텍처를 갖춘 강력한 유튜브 다운로더로 거듭날 것입니다.
