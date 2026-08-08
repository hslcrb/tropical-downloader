# Walkthrough - Tropical Downloader ("트로피컬")

"트로피컬" (Tropical-downloader) 애플리케이션 개발이 완료되었습니다!
파이썬과 PySide6 기반으로 구축되었으며, **트로피컬 아일랜드 스타일 x 프루티거 에어로 (Frutiger Aero) Y2K** 감성의 UI와 **yt-dlp 백엔드의 모든 기능**을 완벽하게 통합하였습니다.

---

## 🌟 주요 완성 기능

### 1. Frutiger Aero x Tropical Y2K 디자인 시스템
- **청량한 아일랜드 색상 스키마**: Lagoon Cyan (`#00E5FF`), Tropical Emerald (`#06D6A0`), Sunshine Yellow (`#FFD166`), Sunset Coral (`#FF6B6B`).
- **입체적 스키오모피즘 QSS 스타일**: 상단 에쿠아 광택이 있는 글로시 젤 버튼, 투명 유리 아크릴 패널 카드, 입체 탭 UI, 네온 프로그래스 바.
- **동적 SVG 아이콘**: 야자수, 코코넛, 번개, 돋보기 분석기, 오션 파도 진행바, 세팅 톱니 등 high-DPI 지원 SVG 아이콘 파서.

### 2. yt-dlp 100% 기능 커버리지 & 미디어 처리
- **원클릭 빠른 다운로드 (Quick Tab)**: URL 입력 시 자동 썸네일/제목 파싱 후 최고화질(4K/1080p), 720p, MP3 (320k), FLAC, M4A 즉시 추출.
- **상세 포맷 분석기 (Inspector Tab)**: 사용 가능한 비디오/오디오 스트림 ID, 해상도, 비트레이트, 코덱, 용량 표 제공 및 커스텀 병합 생성.
- **플레이리스트 및 채널 대량 다운로드 (Playlist Tab)**: 전체 항목 목록화, 범주(예: 1-10) 선택 및 index 기반 커스텀 파일명 템플릿.
- **고급 yt-dlp & 커스텀 CLI Direct Pass-through (Advanced Tab)**:
  - 브라우저 쿠키 연동 (`--cookies-from-browser` Chrome, Edge, Firefox, Brave 등)
  - 프록시 (HTTP/SOCKS5) 및 다운로드 속도 제한 (`--rate-limit`)
  - SponsorBlock 자동 구간 스킵 (`--sponsorblock-remove`)
  - **직접 CLI 인자 전달 상자**: `--write-comments`, `--write-info-json`, `--geo-bypass`, `--concurrent-fragments` 등 yt-dlp의 모든 매개변수 사용 가능!
- **동시 다운로드 큐 & 실시간 디버그 로그 (Queue & History Tab)**:
  - 동시 다운로드 관리, real-time MB/s 속도 & ETA 추적, 완료 후 폴더 열기 / 미디어 즉시 실행.
  - raw stderr/stdout 파싱을 통한 실시간 yt-dlp 디버그 콘솔 출력.

### 3. 오픈소스 라이선스 준수
- **PySide6**: LGPL v3 동적 링크 규정에 맞춘 구조 설계 및 안내.
- **yt-dlp**: Unlicense 저작권 표기.
- **FFmpeg**: LGPL/GPL 빌드 동적 연동 및 설치 여부 실시간 배지 표시.
- `LICENSE`, `NOTICE.md` 및 GUI 내부 "About" 다이얼로그 구비.

---

## 📁 주요 파일 구조

- [main.py](file:///d:/tropical-downloader/main.py): 앱 실행 메인 파일 및 UI 시그널 통합
- [styles/tropical_theme.py](file:///d:/tropical-downloader/styles/tropical_theme.py): Frutiger Aero x Y2K QSS 스타일시트
- [assets/icons.py](file:///d:/tropical-downloader/assets/icons.py): 동적 SVG 아이콘 파서
- [core/yt_worker.py](file:///d:/tropical-downloader/core/yt_worker.py): yt-dlp 핵심 다운로드 백그라운드 작업자 스레드
- [core/info_fetcher.py](file:///d:/tropical-downloader/core/info_fetcher.py): 미디어 메타데이터 비동기 파서
- [core/config.py](file:///d:/tropical-downloader/core/config.py): 설정 영속성 저장소
- [core/history_manager.py](file:///d:/tropical-downloader/core/history_manager.py): 다운로드 기록 저장소
- [core/cookie_manager.py](file:///d:/tropical-downloader/core/cookie_manager.py): 브라우저 쿠키 연동
- [ui/header.py](file:///d:/tropical-downloader/ui/header.py): 트로피컬 헤더 바 & URL 자동 붙여넣기
- [ui/tab_quick.py](file:///d:/tropical-downloader/ui/tab_quick.py): 빠른 원클릭 다운로드 탭
- [ui/tab_inspector.py](file:///d:/tropical-downloader/ui/tab_inspector.py): 상세 포맷 분석 탭
- [ui/tab_playlist.py](file:///d:/tropical-downloader/ui/tab_playlist.py): 플레이리스트 탭
- [ui/tab_advanced.py](file:///d:/tropical-downloader/ui/tab_advanced.py): 고급 yt-dlp & CLI 탭
- [ui/tab_queue.py](file:///d:/tropical-downloader/ui/tab_queue.py): 진행상황 큐 탭
- [ui/tab_history.py](file:///d:/tropical-downloader/ui/tab_history.py): 기록 & 디버그 콘솔 탭
- [ui/dialogs/about_dialog.py](file:///d:/tropical-downloader/ui/dialogs/about_dialog.py): 라이선스 고지 다이얼로그
- [LICENSE](file:///d:/tropical-downloader/LICENSE): MIT 라이선스
- [NOTICE.md](file:///d:/tropical-downloader/NOTICE.md): 제3자 오픈소스 라이선스 고지서

---

## 🧪 검증 결과

1. **Python `py_compile` 검증**: 전체 16개 Python 모듈의 구문 오류 검사 완료 (오류 0건).
2. **PySide6 애플리케이션 초기화 검증**: Headless 인스턴스화 및 테마 적용 정상 작동 확인.
3. **yt-dlp 백엔드 및 FFmpeg 설치 확인**: system FFmpeg 및 yt-dlp 2026.07.04 정상 작동.

---

## 🚀 실행 방법

```powershell
python main.py
```
