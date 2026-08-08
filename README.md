# 🌴 트로피컬 다운로더 (Tropical Downloader)
> **Frutiger Aero / Y2K Tropical Island Edition**  
> Python 3 & PySide6 기반의 가볍고 강력한 미디어 다운로더 (yt-dlp 100% 기능 커버)

![Tropical Downloader Logo](tropical-downloader.png)

---

## 🌟 주요 특징

### 🎨 1. Frutiger Aero x Tropical Y2K 디자인 시스템
- **청량한 라군 블루 & 에메랄드 스키마**: Lagoon Cyan (`#00E5FF`), Tropical Emerald (`#06D6A0`), Sunshine Yellow (`#FFD166`), Sunset Coral (`#FF6B6B`).
- **입체적 스키오모피즘 UI**: 상단 광택이 있는 에쿠아 젤(Aqua Gel) 버튼, 투명 유리 아크릴 패널 카드, 입체 탭 UI, 네온 프로그래스 바.
- **로딩 스플래시 스크린**: 앱 실행 시 생동감 있는 부팅 진행바 및 트로피컬 아일랜드 스플래시 연출.
- **zero UI Freezing**: 모든 네트워크 통신, 메타데이터 분석, 썸네일 디코딩, 파일 다운로드 작업이 **100% 비동기 백그라운드 스레드(`QThread`)**로 동작하여 UI 멈춤 현상이 절대 없습니다.

---

### 🚀 2. 다운로드 및 yt-dlp 포괄 기능

1. **⚡ 빠른 다운로드 (Quick Download)**
   - URL 입력 및 자동 클립보드 붙여넣기 기능.
   - 메타데이터 및 썸네일 실시간 비동기 파싱.
   - 최고화질(4K/1080p/720p), MP3 (320k), FLAC 무손실, M4A 즉시 선택.
2. **🔍 상세 포맷 분석기 (Inspector)**
   - 비디오/오디오 스트림 ID별 해상도, 비트레이트, 코덱, 용량 상세 표 제공.
   - 원하는 비디오/오디오 스트림 조합 지정 다운로드.
3. **📚 플레이리스트 & 채널 일괄 다운로드 (Playlist)**
   - 유튜브 채널 및 재생목록 전체 동영상 탐색.
   - 특정 범위 지정 (예: `1-50`) 또는 채널 전체 자동 연속 다운로드.
   - 번호순 파일명 템플릿 지정 (`%(playlist_index)02d - %(title)s.%(ext)s`).
4. **🛡️ 유튜브 차단 및 봇 감지 우회 (Advanced & Geo-Bypass)**
   - **Geo-Bypass**: IP 지오로케이션 조작으로 국가 제한 비디오 자동 회피.
   - **Anti-Bot Client Spoofing**: 모바일 클라이언트(Android/iOS) 위장으로 403 Forbidden 및 로봇 확인 창 차단 회피.
   - **웹 브라우저 쿠키 연동 (`--cookies-from-browser`)**: Chrome, Edge, Firefox, Brave 등 원클릭 쿠키 연동으로 성인/연령 제한 및 멤버십 영상 다운로드.
   - **SponsorBlock 연동**: P2P 데이터베이스 기반 협찬/오프닝 구간 자동 제거.
   - **Direct CLI Pass-through**: `--write-comments`, `--geo-bypass`, `--concurrent-fragments` 등 yt-dlp의 모든 매개변수 direct 전달 가능.
5. **🌊 진행상황 큐 & 실시간 콘솔 로그**
   - 실시간 MB/s 속도, 남은 시간(ETA), 프로그래스 바 추적.
   - 다운로드 완료 즉시 폴더 열기 / 미디어 재생 버튼 제공.
   - raw stderr/stdout 파싱 실시간 yt-dlp 디버그 콘솔 출력.

---

## 💻 설치 및 실행 방법

### 요구 사항
- Python 3.9 이상
- System FFmpeg (고화질 음병합 및 오디오 변환용)

### 1. 패키지 설치
```powershell
pip install -r requirements.txt
```

### 2. 프로그램 실행
```powershell
python main.py
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
