"""
Tropical Downloader - Quick Download Tab (Clean Modern Edition)
"""
import os
import urllib.request
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog,
    QGroupBox, QRadioButton, QButtonGroup, QFrame
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Signal, QThread, Qt
from assets.icons import get_icon, get_pixmap
from core.config import config_manager
from core.info_fetcher import MediaInfoWorker

class ThumbnailLoader(QThread):
    loaded = Signal(bytes)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            req = urllib.request.Request(self.url, headers={'User-Agent': 'Mozilla/5.0'})
            data = urllib.request.urlopen(req).read()
            self.loaded.emit(data)
        except Exception:
            pass

class QuickTab(QWidget):
    start_download = Signal(dict)

    def __init__(self):
        super().__init__()
        self.current_info = None
        self.thumb_worker = None
        self.info_worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)

        # Hero Card: Media Preview Section
        self.hero_card = QFrame()
        self.hero_card.setObjectName("hero_card")
        hero_layout = QHBoxLayout(self.hero_card)
        hero_layout.setContentsMargins(16, 16, 16, 16)
        hero_layout.setSpacing(16)

        # Thumbnail Label
        self.thumb_lbl = QLabel()
        self.thumb_lbl.setFixedSize(220, 124)
        self.thumb_lbl.setStyleSheet("""
            background-color: #F1F5F9;
            border: 1px solid #CBD5E1;
            border-radius: 10px;
        """)
        self.thumb_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumb_lbl.setPixmap(get_pixmap("logo", 56, 56))
        hero_layout.addWidget(self.thumb_lbl)

        # Info Details
        info_vbox = QVBoxLayout()
        info_vbox.setSpacing(6)

        self.title_lbl = QLabel("다운로드할 비디오 URL을 입력해 주세요")
        self.title_lbl.setStyleSheet("font-size: 15px; font-weight: 700; color: #0F172A;")
        self.title_lbl.setWordWrap(True)

        self.meta_lbl = QLabel("채널: --  •  재생시간: --")
        self.meta_lbl.setStyleSheet("font-size: 12px; color: #475569; font-weight: 500;")

        self.status_lbl = QLabel("대기 중... URL을 입력하면 메타데이터 분석이 시작됩니다.")
        self.status_lbl.setStyleSheet("font-size: 12px; color: #64748B;")

        info_vbox.addWidget(self.title_lbl)
        info_vbox.addWidget(self.meta_lbl)
        info_vbox.addWidget(self.status_lbl)
        info_vbox.addStretch()

        hero_layout.addLayout(info_vbox, stretch=1)
        layout.addWidget(self.hero_card)

        # Quality Preset Selection Box
        preset_group = QGroupBox("원클릭 빠른 다운로드 프리셋 선택")
        preset_layout = QVBoxLayout(preset_group)
        preset_layout.setSpacing(10)

        self.preset_group_btn = QButtonGroup(self)

        self.radio_best = QRadioButton("최고 화질 비디오 (Original Best Video + Best Audio)")
        self.radio_1080 = QRadioButton("Full HD 1080p (MP4)")
        self.radio_720 = QRadioButton("HD 720p (MP4)")
        self.radio_mp3 = QRadioButton("MP3 고음질 오디오 추출 (320 kbps)")
        self.radio_flac = QRadioButton("FLAC 무손실 오디오 추출")
        self.radio_m4a = QRadioButton("M4A 오디오 추출")

        self.radio_best.setChecked(True)

        radios = [self.radio_best, self.radio_1080, self.radio_720, self.radio_mp3, self.radio_flac, self.radio_m4a]
        for idx, r in enumerate(radios):
            self.preset_group_btn.addButton(r, idx)
            preset_layout.addWidget(r)

        layout.addWidget(preset_group)

        # Download Target Folder Selector
        folder_layout = QHBoxLayout()
        folder_layout.setSpacing(8)

        folder_lbl = QLabel("저장 위치:")
        folder_lbl.setStyleSheet("font-weight: 600; color: #334155;")
        folder_layout.addWidget(folder_lbl)

        self.path_lbl = QLabel(config_manager.get("download_path"))
        self.path_lbl.setStyleSheet("""
            background-color: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            padding: 6px 12px;
            color: #0F172A;
            font-weight: 500;
        """)
        folder_layout.addWidget(self.path_lbl, stretch=1)

        self.browse_btn = QPushButton(" 폴더 변경")
        self.browse_btn.setIcon(get_icon("folder", 18))
        self.browse_btn.clicked.connect(self.on_browse_folder)
        folder_layout.addWidget(self.browse_btn)

        layout.addLayout(folder_layout)

        # Clean Action Button
        self.action_btn = QPushButton(" 원클릭 다운로드 시작 (Quick Download)")
        self.action_btn.setObjectName("btn_primary")
        self.action_btn.setIcon(get_icon("quick", 20))
        self.action_btn.setFixedHeight(44)
        self.action_btn.setStyleSheet("font-size: 15px; font-weight: 700;")
        self.action_btn.clicked.connect(self.on_quick_start)
        layout.addWidget(self.action_btn)

        layout.addStretch()

    def analyze_url(self, url: str):
        """Starts background metadata parsing"""
        self.status_lbl.setText("미디어 정보를 분석하는 중입니다...")
        self.title_lbl.setText("정보를 불러오는 중입니다...")
        
        self.info_worker = MediaInfoWorker(url)
        self.info_worker.finished_info.connect(self.on_info_loaded)
        self.info_worker.error_occurred.connect(self.on_info_error)
        self.info_worker.start()

    def on_info_loaded(self, info: dict):
        self.current_info = info
        self.title_lbl.setText(info.get("title", "제목 없음"))
        
        duration = info.get("duration", 0)
        dur_str = f"{duration // 60}분 {duration % 60}초" if duration else "알 수 없음"
        self.meta_lbl.setText(f"채널: {info.get('uploader')}  •  재생시간: {dur_str}")
        self.status_lbl.setText("분석 완료. 프리셋을 선택하고 다운로드 버튼을 누르세요.")

        # Load Thumbnail
        thumb_url = info.get("thumbnail")
        if thumb_url:
            self.thumb_worker = ThumbnailLoader(thumb_url)
            self.thumb_worker.loaded.connect(self.on_thumb_loaded)
            self.thumb_worker.start()

    def on_thumb_loaded(self, data_bytes: bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(data_bytes)
        scaled = pixmap.scaled(220, 124, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.thumb_lbl.setPixmap(scaled)

    def on_info_error(self, err_msg: str):
        self.status_lbl.setText(f"분석 실패: {err_msg}")
        self.title_lbl.setText("미디어 정보를 불러오지 못했습니다.")

    def on_browse_folder(self):
        current = self.path_lbl.text()
        chosen = QFileDialog.getExistingDirectory(self, "다운로드 저장 폴더 선택", current)
        if chosen:
            self.path_lbl.setText(chosen)
            config_manager.set("download_path", chosen)

    def on_quick_start(self):
        url = self.current_info.get("url") if self.current_info else ""
        if not url:
            main_window = self.window()
            if hasattr(main_window, "header"):
                url = main_window.header.get_url()

        if not url:
            self.status_lbl.setText("먼저 상단 주소창에 다운로드할 URL을 입력해 주세요.")
            return

        preset_idx = self.preset_group_btn.checkedId()
        params = {
            "url": url,
            "download_path": self.path_lbl.text(),
            "extract_audio": False,
            "format": "bestvideo+bestaudio/best"
        }

        if preset_idx == 0:  # Best
            params["format"] = "bestvideo+bestaudio/best"
        elif preset_idx == 1:  # 1080p
            params["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        elif preset_idx == 2:  # 720p
            params["format"] = "bestvideo[height<=720]+bestaudio/best[height<=720]"
        elif preset_idx == 3:  # MP3 320k
            params["extract_audio"] = True
            params["audio_format"] = "mp3"
            params["audio_quality"] = "320"
        elif preset_idx == 4:  # FLAC
            params["extract_audio"] = True
            params["audio_format"] = "flac"
            params["audio_quality"] = "0"
        elif preset_idx == 5:  # M4A
            params["extract_audio"] = True
            params["audio_format"] = "m4a"
            params["audio_quality"] = "192"

        self.start_download.emit(params)
