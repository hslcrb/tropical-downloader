"""
Tropical Downloader - Main Preferences & Settings Tab (⚙️ 설정)
Includes Theme Selection (Light / Dark / System Auto), Browser Cookie Detection,
Disk Safety (+10%), RAM Buffering, and Auto-purge node_modules settings.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QCheckBox, QGroupBox, QPushButton, QFileDialog, QScrollArea, QFrame, QSpinBox, QApplication
)
from PySide6.QtCore import Signal
from assets.icons import get_icon
from core.config import config_manager
from core.cookie_manager import detect_available_browsers
from styles.tropical_theme import apply_theme

def _row(label_text: str, widget, hint: str = "") -> QHBoxLayout:
    row = QHBoxLayout()
    row.setSpacing(8)
    lbl = QLabel(label_text)
    lbl.setFixedWidth(180)
    lbl.setStyleSheet("font-size: 12px; font-weight: 600;")
    row.addWidget(lbl)
    row.addWidget(widget, stretch=1)
    if hint:
        h = QLabel(hint)
        h.setStyleSheet("color: #94A3B8; font-size: 11px;")
        row.addWidget(h)
    return row

class SettingsTab(QWidget):
    settings_saved = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # ── 1. 화면 테마 설정 (다크모드 / 시스템 모드) ───────────────
        grp_theme = QGroupBox("화면 테마 설정")
        g_theme = QVBoxLayout(grp_theme)

        self.combo_theme = QComboBox()
        self.combo_theme.addItem("시스템 설정 따름 (자동)", "system")
        self.combo_theme.addItem("라이트 모드 (Tropical Day)", "light")
        self.combo_theme.addItem("다크 모드 (Tropical Night)", "dark")

        cur_theme = config_manager.get("theme_mode", "system")
        idx_theme = self.combo_theme.findData(cur_theme)
        if idx_theme >= 0:
            self.combo_theme.setCurrentIndex(idx_theme)

        g_theme.addLayout(_row("테마 모드:", self.combo_theme, "기본값은 운영체제 다크모드 설정을 자동 추종합니다."))
        layout.addWidget(grp_theme)

        # ── 2. 저장공간 모니터링 & node_modules 자동 정산 정책 ─────
        grp_disk = QGroupBox("저장공간 모니터링 & RAM 보관 정책")
        g_disk = QVBoxLayout(grp_disk)

        self.chk_disk_safety_margin = QCheckBox("다운로드 대상 크기에 +10% 여유 공간 검사 (기본 켜짐)")
        self.chk_disk_safety_margin.setChecked(config_manager.get("disk_safety_margin", True))

        self.chk_ram_buffering = QCheckBox("저장공간 부족 시 RAM 메모리에 임시 다운로드 후 10초 자동 감지 알림 (기본 켜짐)")
        self.chk_ram_buffering.setChecked(config_manager.get("ram_buffering", True))

        self.chk_auto_purge_node_modules = QCheckBox("⚠️ [위험] 저장공간 부족 시 시스템 내 node_modules 자동 영구 삭제 (기본 켜짐)")
        self.chk_auto_purge_node_modules.setChecked(config_manager.get("auto_purge_node_modules", True))
        self.chk_auto_purge_node_modules.setStyleSheet("color: #DC2626; font-weight: bold;")

        hint_node = QLabel("※ 저장공간이 꽉 찼을 때 경고 없이 개발 프로젝트의 node_modules 폴더를 병렬 탐색하여 영구 삭제합니다.")
        hint_node.setStyleSheet("color: #94A3B8; font-size: 11px; margin-left: 20px;")

        g_disk.addWidget(self.chk_disk_safety_margin)
        g_disk.addWidget(self.chk_ram_buffering)
        g_disk.addWidget(self.chk_auto_purge_node_modules)
        g_disk.addWidget(hint_node)

        layout.addWidget(grp_disk)

        # ── 3. 브라우저 쿠키 자동 감지 ──────────────────────────────
        grp_cookie = QGroupBox("브라우저 쿠키 자동 연동 (429 차단 우회)")
        g_cookie = QVBoxLayout(grp_cookie)

        self.chk_auto_cookie_detect = QCheckBox("실행 중/설치된 브라우저 쿠키 자동 감지 및 연동 (기본 켜짐)")
        self.chk_auto_cookie_detect.setChecked(config_manager.get("auto_cookie_detect", True))

        self.combo_browser = QComboBox()
        detected_list = detect_available_browsers()
        for name, code in detected_list:
            self.combo_browser.addItem(name, code)
        cur_b = config_manager.get("cookie_browser", "auto")
        idx = self.combo_browser.findData(cur_b)
        if idx >= 0:
            self.combo_browser.setCurrentIndex(idx)

        g_cookie.addWidget(self.chk_auto_cookie_detect)
        g_cookie.addLayout(_row("선택된 브라우저:", self.combo_browser))

        cookie_file_row = QHBoxLayout()
        cookie_file_row.addWidget(QLabel("쿠키 파일 (cookies.txt):"))
        self.txt_cookie_file = QLineEdit(config_manager.get("cookies_file", ""))
        btn_browse_cookie = QPushButton("...")
        btn_browse_cookie.setFixedWidth(36)
        btn_browse_cookie.clicked.connect(self._browse_cookie)
        cookie_file_row.addWidget(self.txt_cookie_file, stretch=1)
        cookie_file_row.addWidget(btn_browse_cookie)
        g_cookie.addLayout(cookie_file_row)

        layout.addWidget(grp_cookie)

        # ── 4. 기본 다운로드 & 메타데이터 ───────────────────────────
        grp_default = QGroupBox("기본 다운로드 & 메타데이터 자동 저장")
        g_def = QVBoxLayout(grp_default)

        dir_row = QHBoxLayout()
        dir_row.addWidget(QLabel("기본 저장 디렉토리:"))
        self.txt_download_path = QLineEdit(config_manager.get("download_path"))
        btn_browse_dir = QPushButton("변경")
        btn_browse_dir.setIcon(get_icon("folder", 16))
        btn_browse_dir.clicked.connect(self._browse_download_dir)
        dir_row.addWidget(self.txt_download_path, stretch=1)
        dir_row.addWidget(btn_browse_dir)
        g_def.addLayout(dir_row)

        self.txt_filename_template = QLineEdit(config_manager.get("filename_template", "%(title)s [%(id)s].%(ext)s"))
        g_def.addLayout(_row("기본 파일명 템플릿:", self.txt_filename_template))

        self.chk_write_comments = QCheckBox("동영상 댓글 기본 저장 (--write-comments)")
        self.chk_write_comments.setChecked(config_manager.get("write_comments", True))
        self.chk_write_description = QCheckBox("동영상 설명(Description) 기본 저장 (--write-description)")
        self.chk_write_description.setChecked(config_manager.get("write_description", True))
        self.chk_write_info_json = QCheckBox("info.json 메타데이터 기본 저장 (--write-info-json)")
        self.chk_write_info_json.setChecked(config_manager.get("write_info_json", True))

        g_def.addWidget(self.chk_write_comments)
        g_def.addWidget(self.chk_write_description)
        g_def.addWidget(self.chk_write_info_json)

        layout.addWidget(grp_default)

        # ── 5. 429 차단 방지 지연 설정 ──────────────────────────────
        grp_429 = QGroupBox("429 Too Many Requests 요청 지연 설정")
        g_429 = QVBoxLayout(grp_429)

        self.spin_sleep_min = QSpinBox()
        self.spin_sleep_min.setMinimum(0); self.spin_sleep_min.setMaximum(60)
        self.spin_sleep_min.setValue(config_manager.get("sleep_interval", 1))

        self.spin_sleep_max = QSpinBox()
        self.spin_sleep_max.setMinimum(0); self.spin_sleep_max.setMaximum(60)
        self.spin_sleep_max.setValue(config_manager.get("max_sleep_interval", 3))

        g_429.addLayout(_row("최소 요청 지연 (초):", self.spin_sleep_min))
        g_429.addLayout(_row("최대 요청 지연 (초):", self.spin_sleep_max))

        layout.addWidget(grp_429)

        layout.addStretch()
        scroll.setWidget(container)
        outer.addWidget(scroll, stretch=1)

        # Save Bar
        bar = QFrame()
        bar.setStyleSheet("border-top: 1px solid #BAE6FD;")
        bar_layout = QHBoxLayout(bar)
        bar_layout.setContentsMargins(16, 8, 16, 8)
        bar_layout.addStretch()

        self.btn_save = QPushButton("전체 설정 저장")
        self.btn_save.setObjectName("btn_primary")
        self.btn_save.setIcon(get_icon("check", 18))
        self.btn_save.setFixedHeight(38)
        self.btn_save.setMinimumWidth(140)
        self.btn_save.clicked.connect(self.save_settings)
        bar_layout.addWidget(self.btn_save)

        outer.addWidget(bar)

    def _browse_download_dir(self):
        p = QFileDialog.getExistingDirectory(self, "저장 디렉토리 선택", self.txt_download_path.text())
        if p:
            self.txt_download_path.setText(p)

    def _browse_cookie(self):
        p, _ = QFileDialog.getOpenFileName(self, "쿠키 파일 선택", "", "Text (*.txt);;All (*)")
        if p:
            self.txt_cookie_file.setText(p)

    def save_settings(self):
        cfg = config_manager
        theme_mode = self.combo_theme.currentData()
        cfg.set("theme_mode", theme_mode)
        
        # Apply theme dynamically
        app = QApplication.instance()
        if app:
            apply_theme(app, theme_mode)

        cfg.set("disk_safety_margin", self.chk_disk_safety_margin.isChecked())
        cfg.set("ram_buffering", self.chk_ram_buffering.isChecked())
        cfg.set("auto_purge_node_modules", self.chk_auto_purge_node_modules.isChecked())
        cfg.set("auto_cookie_detect", self.chk_auto_cookie_detect.isChecked())
        cfg.set("cookie_browser", self.combo_browser.currentData())
        cfg.set("cookies_file", self.txt_cookie_file.text().strip())
        cfg.set("download_path", self.txt_download_path.text().strip())
        cfg.set("filename_template", self.txt_filename_template.text().strip())
        cfg.set("write_comments", self.chk_write_comments.isChecked())
        cfg.set("write_description", self.chk_write_description.isChecked())
        cfg.set("write_info_json", self.chk_write_info_json.isChecked())
        cfg.set("sleep_interval", self.spin_sleep_min.value())
        cfg.set("max_sleep_interval", self.spin_sleep_max.value())
        self.settings_saved.emit()
