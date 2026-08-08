# Implementation Plan - Tropical Downloader ("트로피컬")

"트로피컬" (Tropical-downloader)는 Python과 PySide6 기반의 가볍고 강력한 비디오/오디오 다운로더 애플리케이션입니다.
초보자도 직관적으로 사용할 수 있는 원클릭 다운로드부터, 전문가를 위한 `yt-dlp`의 모든 고급 옵션(포맷 선택, 플레이리스트, 자막/썸네일 임베딩, 쿠키 연동, SponsorBlock, 사용자 정의 CLI 인자)을 제공합니다.
시각적으로는 **트로피컬 아일랜드(Tropical Island)** 분위기와 2000년대 후반 **프루티거 에어로 (Frutiger Aero) / Y2K** 감성이 결합된 입체감 있는 유리 질감(Glassmorphic), 에쿠아(Aqua) 젤 버튼, 청량한 그라데이션, 생동감 있는 마이크로 애니메이션 UI를 구현합니다.

---

## User Review Required

> [!IMPORTANT]
> **라이선스 및 종속성 준수 안내**
> - **PySide6**: LGPL v3 / GPL v3 규정에 맞춰 동적 바인딩 및 소스 코드 공개 / 라이선스 표기 모듈을 포함합니다.
> - **yt-dlp**: Unlicense (Public Domain) 소프트웨어로 자유롭게 번들 및 호출 가능하며 "About" 창에 저작권 및 라이선스를 명시합니다.
> - **FFmpeg**: LGPL/GPL 빌드를 시스템 연동하며, 사용자의 시스템 FFmpeg 설치 여부를 자동으로 탐지하고 설정할 수 있게 지원합니다.

> [!NOTE]
> **디자인 콘셉트 (Frutiger Aero x Tropical Y2K)**
> - **청량한 아일랜드 컬러**: 에메랄드 라군 Blue (`#00E5FF`), 딥 오션 (`#0077B6`), 트로피컬 팜 Green (`#06D6A0`), 선샤인 옐로우 (`#FFD166`), 트로피컬 코랄 Pink (`#FF6B6B`).
> - **Frutiger Aero 스키오모피즘 UI**: 상단 광택이 있는 에쿠아 젤(Aqua Gel) 버튼, 하이라이트 경계선, 부드러운 하단 그림자, 에메랄드 빛 투명 유리 카드가 적용된 QSS 디자인 시스템.

---

## Open Questions

1. 기본 다운로드 폴더 위치를 사용자 시스템의 `Downloads/Tropical` 폴더로 지정해도 괜찮으신가요? (설정에서 변경 가능)
2. 다운로드 완료 시 트로피컬 알림음/효과음 오디오 재생 옵션을 포함할까요?

---

## Proposed Changes

### 1. Project Architecture & Setup
#### [NEW] [requirements.txt](file:///d:/tropical-downloader/requirements.txt)
- `PySide6>=6.6.0`, `yt-dlp>=2026.0.0` 제해더 명시.

#### [NEW] [LICENSE](file:///d:/tropical-downloader/LICENSE) & [NOTICE.md](file:///d:/tropical-downloader/NOTICE.md)
- 오픈소스 라이선스 준수를 위한 MIT/LGPL 및 yt-dlp 라이선스 고지 문서.

---

### 2. Core Engine & yt-dlp Integration
#### [NEW] [core/yt_worker.py](file:///d:/tropical-downloader/core/yt_worker.py)
- PySide6 `QThread` 기반 `yt-dlp` 백그라운드 다운로드 작업자.
- real-time `progress_hook`을 통한 속도(MB/s), 남은시간(ETA), 용량, 진행률(%) 시그널 전송.
- raw stderr/stdout 파싱을 통한 실시간 콘솔 로그 시그널 전송.
- 일시정지/취소 요청 안전 처리.

#### [NEW] [core/info_fetcher.py](file:///d:/tropical-downloader/core/info_fetcher.py)
- UI 멈춤 없는 비동기 미디어 비디오/플레이리스트 메타데이터 파서.
- 썸네일, 제목, 업로더, 재생시간, 사용 가능한 비디오/오디오 스트림 포맷 목록(해상도, 코덱, 비트레이트, 용량) 추출.

#### [NEW] [core/cookie_manager.py](file:///d:/tropical-downloader/core/cookie_manager.py)
- 브라우저(Chrome, Edge, Firefox, Brave, Safari) 쿠키 자동 추출 연동 (`--cookies-from-browser`).

#### [NEW] [core/config.py](file:///d:/tropical-downloader/core/config.py)
- 사용자 설정 저장소 (다운로드 경로, 기본 포맷, FFmpeg 경로, 쿠키 설정, 테마, CLI 사용자 지정 인자).

#### [NEW] [core/history_manager.py](file:///d:/tropical-downloader/core/history_manager.py)
- 다운로드 기록 저장 및 JSON 영속성 관리.

---

### 3. Styling & Frutiger Aero Design System
#### [NEW] [styles/tropical_theme.py](file:///d:/tropical-downloader/styles/tropical_theme.py)
- Frutiger Aero Y2K 트로피컬 QSS 스타일시트 및 색상 토큰.
- 글로시 젤 버튼(Aqua Gloss Button), 유리 패널(Glass Container), 입체 탭 바, 네온 프로그래스 바, 트로피컬 태그 바지.

#### [NEW] [assets/icons.py](file:///d:/tropical-downloader/assets/icons.py)
- 트로피컬 및 Aero 스타일 동적 SVG 아이콘 파서 (야자수, 코코넛, 파도, 선샤인, 기어, 플레이, 다운로드, 폴더, 삭제 등).

---

### 4. User Interface Components
#### [NEW] [ui/header.py](file:///d:/tropical-downloader/ui/header.py)
- 트로피컬 아일랜드 헤더 (로고, 빠른 URL 입력창, 자동 클립보드 감지/붙여넣기 버튼, 빠른 다운로드 버튼, FFmpeg 상태 감지 뱃지).

#### [NEW] [ui/tab_quick.py](file:///d:/tropical-downloader/ui/tab_quick.py)
- **빠른 다운로드 탭**: URL 입력 시 미디어 카드가 나타나며 원클릭 최고화질(4K/1080p), MP3 320k, FLAC 추출 선택 기능.

#### [NEW] [ui/tab_inspector.py](file:///d:/tropical-downloader/ui/tab_inspector.py)
- **상세 분석 탭**: 비디오/오디오 스트림 개별 선택, 컨테이너(MP4, MKV, WEBM, MP3), 코덱, 해상도 테이블 및 썸네일/자막 임베딩 체크박스.

#### [NEW] [ui/tab_playlist.py](file:///d:/tropical-downloader/ui/tab_playlist.py)
- **플레이리스트 탭**: 전체 항목 탐색, 개별 체크박스 선택, 범주 선택(예: 1-10), 파일명 템플릿 설정.

#### [NEW] [ui/tab_advanced.py](file:///d:/tropical-downloader/ui/tab_advanced.py)
- **고급 yt-dlp 탭**: SponsorBlock 장 배제, 속도 제한, 프록시, 사용자 에이전트, 자막 언어 선택, 브라우저 쿠키 선택, **yt-dlp 사용자 정의 CLI 옵션 direct pass-through** (모든 yt-dlp 기능 지원!).

#### [NEW] [ui/tab_queue.py](file:///d:/tropical-downloader/ui/tab_queue.py)
- **다운로드 큐 & 진행상황 탭**: 동시 다운로드 관리, 파도(Wave) 스타일 실시간 프로그래스 바, 일시정지/취소/다시시도, 폴더 열기 / 파일 재생.

#### [NEW] [ui/tab_history.py](file:///d:/tropical-downloader/ui/tab_history.py)
- **기록 및 로그 탭**: 이력 검색, yt-dlp 실시간 CLI stdout/stderr 디버그 콘솔 output log.

#### [NEW] [ui/dialogs/about_dialog.py](file:///d:/tropical-downloader/ui/dialogs/about_dialog.py)
- 트로피컬 다운로더 정보 및 라이선스(PySide6 LGPL/GPL, yt-dlp Unlicense, FFmpeg) 명시 다이얼로그.

#### [NEW] [main.py](file:///d:/tropical-downloader/main.py)
- 앱 메인 실행 파일, QApplication 생성, 테마 적용, 시그널 바인딩.

---

## Verification Plan

### Automated Tests & Code Quality
1. `python -m py_compile main.py core/*.py ui/*.py styles/*.py` 코드가 구문 오류 없이 정상 작동하는지 확인.
2. `yt-dlp` 동적 호출 테스트: 다양한 URL (테스트용 비디오, 오디오 추출) 다운로드 백그라운드 스레드 정상 동작 확인.
3. FFmpeg 연동 확인 테스트.

### Manual Verification
1. PySide6 GUI 실행 후 Frutiger Aero x Tropical Y2K 디자인 레이아웃 visual 확인.
2. URL 붙여넣기 후 영상 메타데이터 파싱 및 썸네일 표시 확인.
3. 빠른 다운로드, 상세 포맷 선택 다운로드, 오디오 전용 추출(MP3) 진행바 및 속도/ETA 정상 갱신 확인.
4. 고급 yt-dlp CLI 커스텀 옵션 전달 기능 확인.
5. 라이선스 고지 창 확인.
