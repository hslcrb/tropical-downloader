"""
Tropical Downloader - Header Bar
Sky blue brand colors, clean layout, no emoji.
"""
import shutil
from PySide6.QtWidgets import (
    QFrame, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QApplication
)
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QFont
from assets.icons import get_icon, get_app_pixmap


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
        main_layout.setContentsMargins(16, 10, 16, 10)
        main_layout.setSpacing(14)

        # ── Brand ───────────────────────────────────────────────────
        brand = QHBoxLayout()
        brand.setSpacing(10)

        logo_lbl = QLabel()
        logo_lbl.setPixmap(get_app_pixmap(40, 40))
        brand.addWidget(logo_lbl)

        vbox = QVBoxLayout()
        vbox.setSpacing(1)

        title = QLabel("Tropical Downloader")
        title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #0284C7; letter-spacing: 0.3px;")

        sub = QLabel("yt-dlp powered  •  v2.0")
        sub.setStyleSheet("font-size: 11px; color: #38BDF8; font-weight: 600;")

        vbox.addWidget(title)
        vbox.addWidget(sub)
        brand.addLayout(vbox)
        main_layout.addLayout(brand)
        main_layout.addSpacing(8)

        # ── URL input row ────────────────────────────────────────────
        input_row = QHBoxLayout()
        input_row.setSpacing(8)

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("비디오 · 재생목록 · 채널 URL 입력 또는 붙여넣기…")
        self.url_input.setFixedHeight(38)
        self.url_input.returnPressed.connect(self.on_submit_url)
        input_row.addWidget(self.url_input, stretch=1)

        self.paste_btn = QPushButton("붙여넣기")
        self.paste_btn.setIcon(get_icon("paste", 16))
        self.paste_btn.setFixedHeight(38)
        self.paste_btn.setFixedWidth(100)
        self.paste_btn.setToolTip("클립보드 URL 붙여넣기 (Ctrl+V)")
        self.paste_btn.clicked.connect(self.on_paste_url)
        input_row.addWidget(self.paste_btn)

        self.dl_btn = QPushButton("분석 / 다운로드")
        self.dl_btn.setObjectName("btn_primary")
        self.dl_btn.setIcon(get_icon("download", 16))
        self.dl_btn.setFixedHeight(38)
        self.dl_btn.setFixedWidth(140)
        self.dl_btn.clicked.connect(self.on_submit_url)
        input_row.addWidget(self.dl_btn)

        main_layout.addLayout(input_row, stretch=1)

        # ── Right badges ─────────────────────────────────────────────
        right = QHBoxLayout()
        right.setSpacing(8)

        ffmpeg_ok = shutil.which("ffmpeg") is not None
        badge = QLabel("FFmpeg ✓" if ffmpeg_ok else "FFmpeg ✗")
        badge.setStyleSheet(
            f"background-color:{'#0EA5E9' if ffmpeg_ok else '#EF4444'};"
            "color:#FFFFFF; font-size:11px; font-weight:700;"
            "padding:4px 10px; border-radius:10px;"
        )
        badge.setToolTip(
            "FFmpeg가 설치되어 있습니다. 고화질 병합 및 오디오 변환을 지원합니다."
            if ffmpeg_ok else
            "FFmpeg가 없습니다. 일부 기능이 제한될 수 있습니다."
        )
        right.addWidget(badge)

        self.info_btn = QPushButton()
        self.info_btn.setObjectName("btn_ghost")
        self.info_btn.setIcon(get_icon("info", 20))
        self.info_btn.setFixedSize(36, 36)
        self.info_btn.setToolTip("정보 / 라이선스")
        self.info_btn.clicked.connect(self.open_about.emit)
        right.addWidget(self.info_btn)

        main_layout.addLayout(right)

    def on_paste_url(self):
        text = QApplication.clipboard().text().strip()
        if text.startswith(("http://", "https://")):
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
