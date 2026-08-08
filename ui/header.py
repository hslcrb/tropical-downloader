"""
Tropical Downloader - Header Bar Component
"""
import shutil
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
)
from PySide6.QtCore import Signal, Qt
from assets.icons import get_icon, get_pixmap

class TropicalHeader(QFrame):
    url_submitted = Signal(str)
    download_requested = Signal(str)
    open_settings = Signal()
    open_about = Signal()

    def __init__(self):
        super().__init__()
        self.setObjectName("glass_card")
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 12, 16, 12)
        main_layout.setSpacing(16)

        # Brand Logo & Title Section
        logo_layout = QHBoxLayout()
        logo_layout.setSpacing(10)
        
        logo_lbl = QLabel()
        logo_lbl.setPixmap(get_pixmap("logo", 44, 44))
        logo_layout.addWidget(logo_lbl)

        title_vbox = QVBoxLayout()
        title_vbox.setSpacing(0)
        
        title_lbl = QLabel("Tropical Downloader")
        title_lbl.setStyleSheet("""
            font-size: 19px;
            font-weight: 900;
            color: #0077B6;
            letter-spacing: 0.5px;
        """)
        
        sub_lbl = QLabel("트로피컬 다운로더 v2.0 • Frutiger Aero Edition")
        sub_lbl.setStyleSheet("font-size: 11px; color: #0096C7; font-weight: 600;")
        
        title_vbox.addWidget(title_lbl)
        title_vbox.addWidget(sub_lbl)
        logo_layout.addLayout(title_vbox)

        main_layout.addLayout(logo_layout)
        main_layout.addSpacing(10)

        # Center: URL Input Box with Aero Gloss styling
        input_layout = QHBoxLayout()
        input_layout.setSpacing(8)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("비디오 또는 플레이리스트 URL을 입력하거나 붙여넣으세요...")
        self.url_input.setFixedHeight(38)
        self.url_input.returnPressed.connect(self.on_submit_url)
        input_layout.addWidget(self.url_input, stretch=1)

        # Paste Button
        self.paste_btn = QPushButton(" 붙여넣기")
        self.paste_btn.setIcon(get_icon("paste", 18))
        self.paste_btn.setFixedHeight(38)
        self.paste_btn.setToolTip("클립보드 URL 자동 감지 및 붙여넣기")
        self.paste_btn.clicked.connect(self.on_paste_url)
        input_layout.addWidget(self.paste_btn)

        # Quick Download Button
        self.dl_btn = QPushButton(" 다운로드")
        self.dl_btn.setObjectName("btn_primary")
        self.dl_btn.setIcon(get_icon("download", 18))
        self.dl_btn.setFixedHeight(38)
        self.dl_btn.clicked.connect(self.on_submit_url)
        input_layout.addWidget(self.dl_btn)

        main_layout.addLayout(input_layout, stretch=1)

        # Right Action Buttons & FFmpeg Status Badge
        right_layout = QHBoxLayout()
        right_layout.setSpacing(8)

        # FFmpeg Badge
        ffmpeg_exists = shutil.which("ffmpeg") is not None
        self.ffmpeg_badge = QLabel("FFmpeg OK" if ffmpeg_exists else "FFmpeg 없음")
        badge_bg = "#06D6A0" if ffmpeg_exists else "#FF6B4A"
        self.ffmpeg_badge.setStyleSheet(f"""
            background-color: {badge_bg};
            color: #FFFFFF;
            font-size: 10px;
            font-weight: bold;
            padding: 4px 8px;
            border-radius: 10px;
        """)
        self.ffmpeg_badge.setToolTip("FFmpeg가 설치되어 있으면 고화질 병합 및 오디오 변환을 지원합니다.")
        right_layout.addWidget(self.ffmpeg_badge)

        # Info/About Button
        self.info_btn = QPushButton()
        self.info_btn.setIcon(get_icon("info", 20))
        self.info_btn.setFixedSize(38, 38)
        self.info_btn.setToolTip("트로피컬 다운로더 정보 및 라이선스 고지")
        self.info_btn.clicked.connect(self.open_about.emit)
        right_layout.addWidget(self.info_btn)

        main_layout.addLayout(right_layout)

    def on_paste_url(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        if text.startswith("http://") or text.startswith("https://"):
            self.url_input.setText(text)
            self.url_submitted.emit(text)

    def on_submit_url(self):
        url = self.url_input.text().strip()
        if url:
            self.url_submitted.emit(url)

    def get_url(self) -> str:
        return self.url_input.text().strip()

    def set_url(self, url: str):
        self.url_input.setText(url)
