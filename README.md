# 🌴 트로피컬 다운로더 (Tropical Downloader)
> **Frutiger Aero / Y2K Tropical Island Edition**  
> Python 3 & PySide6 기반의 가볍고 강력한 미디어 다운로더, 인앱 미디어 플레이어 & 자막/JSON 에디터

![Tropical Downloader Logo](tropical-downloader.png)

---

## 🌟 주요 특징

### 🎨 1. Frutiger Aero x Tropical Y2K 디자인 시스템
- **청량한 라군 블루 & 에메랄드 스키마**: Lagoon Cyan (`#00E5FF`), Tropical Emerald (`#06D6A0`), Sunshine Yellow (`#FFD166`), Sunset Coral (`#FF6B6B`).
- **입체적 스키오모피즘 UI**: 상단 광택 에쿠아 젤(Aqua Gel) 버튼, 투명 유리 아크릴 패널 카드, 입체 탭 UI, 네온 프로그래스 바.
- **로딩 스플래시 스크린**: 앱 실행 시 생동감 있는 부팅 진행바 및 트로피컬 아일랜드 스플래시 연출.
- **Zero UI Freezing**: 모든 네트워크 통신, 메타데이터 분석, 썸네일 디코딩, 파일 다운로드 작업이 **100% 비동기 백그라운드 스레드(`QThread`)**로 동작하여 UI 멈춤 현상이 절대 없습니다.

---

### 🛡️ 2. 방탄 크래시 방지 엔진 (Crash-Proof Safe Boot)
- **전역 예외 포착 시스템 (`sys.excepthook`)**: 시스템 내부나 라이브러리에서 예기치 않은 오류가 발생하더라도 앱이 튕기거나(Crash) 종료되지 않고 안전하게 포착하여 실행 상태를 100% 보장합니다.
- **UI 탭 샌드박싱 (`init_ui_sandbox`)**: 개별 모듈이나 탭 초기화 중 예외가 발생하더라도 메인 윈도우 창은 무조건 정상 렌더링되고 가동됩니다.
- **설정 파일 Auto-Healing**: 설정 및 히스토리 데이터 파일 손상 시 자동으로 기본값으로 복구합니다.

---

### 🎬 3. 인앱 미디어 플레이어 & 자막/JSON 에디터 (Player & Editor Tab)
- **인앱 비디오 & 오디오 플레이어**: 다운로드한 동영상/음악을 앱 내부에서 즉시 재생/일시정지/탐색/볼륨 조절/배속 조절.
- **인앱 자막(.srt) & 동영상 설명(.description) 에디터**: 앱 내에서 자막 구문 및 타임코드를 바로 수정하고 원클릭 저장.
- **인앱 JSON 메타데이터(.json) 뷰어 & 에디터**: 영상 정보 JSON 데이터를 가독성 높게 정렬하고 자유롭게 편집/저장.
- **통합 미디어 탐색기 패널**: 다운로드 폴더 내부의 파일들을 종류별 아이콘으로 시각화하여 바로 열기.

---

### 🚀 4. 다운로드 및 yt-dlp 포괄 기능
1. **⚡ 빠른 다운로드 (Quick Download)**
   - URL 입력 및 자동 클립보드 붙여넣기 기능.
   - 최고화질(4K/1080p/720p), MP3 (320k), FLAC 무손실, M4A 원클릭 프리셋.
2. **🔍 상세 포맷 분석기 (Inspector)**
   - 비디오/오디오 스트림 ID별 해상도, 비트레이트, 코덱, 용량 표 제공 및 사용자 지정 수동 조합 다운로드.
3. **📚 플레이리스트 & 채널 일괄 다운로드 (Playlist)**
   - 유튜브 채널 및 재생목록 전체 동영상 탐색 및 특정 범위 지정 (`1-50`) 일괄 다운로드.
4. **🛡️ 유튜브 차단 및 봇 감지 우회 (Advanced & Geo-Bypass)**
   - **Anti-Bot Client Spoofing**: 모바일/TV 클라이언트(Android/iOS/Web/TV) 위장으로 403 Forbidden 차단 회피.
   - **Geo-Bypass**: IP 지오로케이션 조작으로 국가 제한 비디오 회피.
   - **웹 브라우저 쿠키 연동**: Chrome, Edge, Firefox, Brave 등 원클릭 쿠키 가져오기로 성인/연령 제한 및 멤버십 영상 다운로드.
   - **SponsorBlock 연동**: P2P 데이터베이스 기반 협찬/광고/오프닝 구간 자동 스킵.

---

## 💻 가상환경(venv) 구축 및 실행 가이드 (권장)

본 프로젝트는 **파이썬 전용 가상환경(`.venv`)** 내에서 독립적으로 구동하는 것을 강력하게 권장합니다.

### 1. 파이썬 가상환경 생성
```powershell
python -m venv .venv
```

### 2. 가상환경 패키지 설치
Windows PowerShell:
```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 3. 가상환경 기반 앱 실행
```powershell
.\.venv\Scripts\python.exe main.py
```

---

## ⚖️ 오픈소스 라이선스 준수 (Open Source Notices)

본 프로젝트는 오픈소스 라이선스 규정을 준수합니다:

1. **PySide6 (Qt for Python)**: GNU LGPL v3 라이선스를 준수하며 동적 바인딩 방식으로 연동되었습니다.
2. **yt-dlp**: Unlicense (Public Domain) 라이선스를 따릅니다.
3. **FFmpeg**: GNU LGPL v2.1+ / GPL v2+ 동적 바이너리 연동.

상세 정보는 [NOTICE.md](NOTICE.md) 및 앱 내 "About" 창에서 확인하실 수 있습니다.

---

<p align="center">
  <b>Tropical Downloader Team • MIT License</b>
</p>

