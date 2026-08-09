"""
Tropical Downloader - Quick Download Tab
Clean UX: thumbnail preview + preset cards, no text clipping.
"""
import os
import urllib.request
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QButtonGroup, QAbstractButton, QFrame, QSizePolicy
)
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Signal, QThread, Qt
from assets.icons import get_icon, get_app_pixmap
from core.config import config_manager
from core.info_fetcher import MediaInfoWorker


class ThumbnailLoader(QThread):
    loaded = Signal(bytes)

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def run(self):
        try:
            req = urllib.request.Request(self.url, headers={"User-Agent": "Mozilla/5.0"})
            data = urllib.request.urlopen(req, timeout=8).read()
            self.loaded.emit(data)
        except Exception:
            pass


class PresetCard(QFrame):
    """Clickable preset card frame — eliminates PySide6 button layout rendering overlap."""
    clicked = Signal(int)

    def __init__(self, pid: int, title: str, subtitle: str, parent=None):
        super().__init__(parent)
        self.pid = pid
        self._checked = False
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(2)

        self._title = QLabel(title)
        self._title.setFont(QFont("Segoe UI", 13, QFont.Weight.DemiBold))
        self._title.setWordWrap(True)
        self._title.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        self._sub = QLabel(subtitle)
        self._sub.setFont(QFont("Segoe UI", 11))
        self._sub.setWordWrap(True)
        self._sub.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

        layout.addWidget(self._title)
        layout.addWidget(self._sub)

        self._update_style(False)

    def setChecked(self, checked: bool):
        self._checked = checked
        self._update_style(checked)

    def isChecked(self) -> bool:
        return self._checked

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.pid)
        super().mousePressEvent(event)

    def _update_style(self, checked: bool):
        if checked:
            self.setStyleSheet("""
                PresetCard {
                    background-color: #E0F2FE;
                    border: 2px solid #0EA5E9;
                    border-radius: 10px;
                }
            """)
            self._title.setStyleSheet("color: #0284C7; background: transparent;")
            self._sub.setStyleSheet("color: #0369A1; background: transparent;")
        else:
            self.setStyleSheet("""
                PresetCard {
                    background-color: #FFFFFF;
                    border: 1.5px solid #BAE6FD;
                    border-radius: 10px;
                }
                PresetCard:hover {
                    background-color: #F0F9FF;
                    border-color: #38BDF8;
                }
            """)
            self._title.setStyleSheet("color: #1E293B; background: transparent;")
            self._sub.setStyleSheet("color: #64748B; background: transparent;")




class QuickTab(QWidget):
    start_download = Signal(dict)

    # Preset definitions: (id, title, subtitle, params)
    PRESETS = [
        (0, "최고 화질",         "최대 해상도 비디오 + 최고 오디오 (4K/1080p)",
            {"format": "bestvideo+bestaudio/best"}),
        (1, "Full HD 1080p",    "1080p MP4",
            {"format": "bestvideo[height<=1080]+bestaudio/best[height<=1080]"}),
        (2, "HD 720p",          "720p MP4",
            {"format": "bestvideo[height<=720]+bestaudio/best[height<=720]"}),
        (3, "MP3 320 kbps",     "오디오만 추출 — 고음질 MP3",
            {"extract_audio": True, "audio_format": "mp3", "audio_quality": "320"}),
        (4, "FLAC 무손실",       "오디오만 추출 — 무손실 FLAC",
            {"extract_audio": True, "audio_format": "flac", "audio_quality": "0"}),
        (5, "M4A 오디오",        "오디오만 추출 — M4A",
            {"extract_audio": True, "audio_format": "m4a", "audio_quality": "192"}),
    ]

    def __init__(self):
        super().__init__()
        self.current_info = None
        self.thumb_worker = None
        self.info_worker = None
        self._selected_pid = 0
        self._cards: dict[int, PresetCard] = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # ── Media preview card ──────────────────────────────────────
        self.hero_card = QFrame()
        self.hero_card.setObjectName("hero_card")
        hero_layout = QHBoxLayout(self.hero_card)
        hero_layout.setContentsMargins(14, 14, 14, 14)
        hero_layout.setSpacing(14)

        self.thumb_lbl = QLabel()
        self.thumb_lbl.setFixedSize(200, 113)
        self.thumb_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumb_lbl.setStyleSheet(
            "background:#F0F9FF; border:1px solid #BAE6FD; border-radius:8px;"
        )
        self.thumb_lbl.setPixmap(get_app_pixmap(56, 56))
        hero_layout.addWidget(self.thumb_lbl)

        info_col = QVBoxLayout()
        info_col.setSpacing(4)

        self.title_lbl = QLabel("URL을 입력하면 여기에 영상 정보가 표시됩니다")
        self.title_lbl.setWordWrap(True)
        self.title_lbl.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))

        self.meta_lbl = QLabel("채널: —  •  재생시간: —")
        self.meta_lbl.setStyleSheet("color: #475569; font-size: 12px;")

        self.status_lbl = QLabel("대기 중")
        self.status_lbl.setStyleSheet("color: #94A3B8; font-size: 12px;")

        info_col.addWidget(self.title_lbl)
        info_col.addWidget(self.meta_lbl)
        info_col.addWidget(self.status_lbl)
        info_col.addStretch()
        hero_layout.addLayout(info_col, stretch=1)

        layout.addWidget(self.hero_card)

        # ── Preset grid (2 columns) ─────────────────────────────────
        grid_label = QLabel("다운로드 형식 선택")
        grid_label.setStyleSheet("font-weight: 700; color: #0369A1; font-size: 13px;")
        layout.addWidget(grid_label)

        grid_layout = QVBoxLayout()
        grid_layout.setSpacing(6)

        for pid, title, sub, _ in self.PRESETS:
            card = PresetCard(pid, title, sub)
            card.clicked.connect(self._on_card_selected)
            self._cards[pid] = card
            grid_layout.addWidget(card)

        self._on_card_selected(0)
        layout.addLayout(grid_layout)

        # ── Save path row ───────────────────────────────────────────
        path_row = QHBoxLayout()
        path_row.setSpacing(8)

        path_label = QLabel("저장 위치:")
        path_label.setStyleSheet("font-weight: 600; font-size: 13px;")
        path_label.setFixedWidth(68)
        path_row.addWidget(path_label)

        self.path_lbl = QLabel(config_manager.get("download_path"))
        self.path_lbl.setStyleSheet(
            "background:#FFFFFF; border:1.5px solid #BAE6FD; border-radius:8px;"
            "padding:6px 12px; color:#0F172A; font-size:13px;"
        )
        self.path_lbl.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        path_row.addWidget(self.path_lbl, stretch=1)

        browse_btn = QPushButton("변경")
        browse_btn.setIcon(get_icon("folder", 16))
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self.on_browse_folder)
        path_row.addWidget(browse_btn)
        layout.addLayout(path_row)

        # ── Download button ─────────────────────────────────────────
        self.dl_btn = QPushButton("다운로드 시작")
        self.dl_btn.setObjectName("btn_primary")
        self.dl_btn.setIcon(get_icon("download", 18))
        self.dl_btn.setFixedHeight(46)
        self.dl_btn.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        self.dl_btn.clicked.connect(self.on_quick_start)
        layout.addWidget(self.dl_btn)

        layout.addStretch()

    def _on_card_selected(self, pid: int):
        self._selected_pid = pid
        for p, card in self._cards.items():
            card.setChecked(p == pid)

    # ── Async metadata fetch ────────────────────────────────────────
    def analyze_url(self, url: str):
        self.status_lbl.setText("분석 중...")
        self.title_lbl.setText("정보를 가져오는 중입니다...")
        self.info_worker = MediaInfoWorker(url)
        self.info_worker.finished_info.connect(self.on_info_loaded)
        self.info_worker.error_occurred.connect(self.on_info_error)
        self.info_worker.start()

    def on_info_loaded(self, info: dict):
        self.current_info = info
        self.title_lbl.setText(info.get("title", "제목 없음"))
        dur = info.get("duration", 0)
        dur_str = f"{dur // 60}분 {dur % 60}초" if dur else "알 수 없음"
        self.meta_lbl.setText(f"채널: {info.get('uploader', '—')}  •  재생시간: {dur_str}")
        self.status_lbl.setText("분석 완료. 형식을 선택하고 다운로드를 누르세요.")
        thumb_url = info.get("thumbnail")
        if thumb_url:
            self.thumb_worker = ThumbnailLoader(thumb_url)
            self.thumb_worker.loaded.connect(self.on_thumb_loaded)
            self.thumb_worker.start()

    def on_thumb_loaded(self, data: bytes):
        pm = QPixmap()
        pm.loadFromData(data)
        scaled = pm.scaled(200, 113,
                           Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                           Qt.TransformationMode.SmoothTransformation)
        self.thumb_lbl.setPixmap(scaled)

    def on_info_error(self, msg: str):
        self.status_lbl.setText(f"오류: {msg}")
        self.title_lbl.setText("정보를 가져올 수 없습니다.")

    def on_browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "저장 폴더 선택", self.path_lbl.text())
        if path:
            self.path_lbl.setText(path)
            config_manager.set("download_path", path)

    def on_quick_start(self):
        url = (self.current_info or {}).get("url", "")
        if not url:
            mw = self.window()
            if hasattr(mw, "header"):
                url = mw.header.get_url()
        if not url:
            self.status_lbl.setText("먼저 URL을 입력해 주세요.")
            return

        pid = self._selected_pid
        _, _, _, base_params = self.PRESETS[pid] if 0 <= pid < len(self.PRESETS) else self.PRESETS[0]

        params = {"url": url, "download_path": self.path_lbl.text(), "extract_audio": False}
        params.update(base_params)
        self.start_download.emit(params)
