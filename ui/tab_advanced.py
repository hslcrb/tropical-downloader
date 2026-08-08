"""
Tropical Downloader - Advanced yt-dlp & Custom CLI Options Tab
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QCheckBox, QGroupBox, QPushButton, QFileDialog, QTextEdit
)
from PySide6.QtCore import Signal
from assets.icons import get_icon
from core.config import config_manager
from core.cookie_manager import SUPPORTED_BROWSERS

class AdvancedTab(QWidget):
    settings_saved = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # 1. Browser Cookies & Authentication Group
        cookie_group = QGroupBox("쿠키 인증 & 브라우저 연동 (--cookies-from-browser)")
        cookie_layout = QVBoxLayout(cookie_group)

        b_layout = QHBoxLayout()
        b_layout.addWidget(QLabel("웹 브라우저 쿠키 연동:"))
        self.combo_browser = QComboBox()
        for name, code in SUPPORTED_BROWSERS:
            self.combo_browser.addItem(name, code)

        current_b = config_manager.get("cookie_browser")
        idx = self.combo_browser.findData(current_b)
        if idx >= 0:
            self.combo_browser.setCurrentIndex(idx)

        b_layout.addWidget(self.combo_browser, stretch=1)
        cookie_layout.addLayout(b_layout)

        f_layout = QHBoxLayout()
        f_layout.addWidget(QLabel("또는 쿠키 파일 (cookies.txt):"))
        self.txt_cookie_file = QLineEdit(config_manager.get("cookies_file"))
        f_layout.addWidget(self.txt_cookie_file, stretch=1)

        self.btn_browse_cookie = QPushButton("파일 선택")
        self.btn_browse_cookie.clicked.connect(self.on_browse_cookie)
        f_layout.addWidget(self.btn_browse_cookie)
        cookie_layout.addLayout(f_layout)

        layout.addWidget(cookie_group)

        # 2. Network & Speed Options Group
        net_group = QGroupBox("네트워크 & 다운로드 속도 제한")
        net_layout = QHBoxLayout(net_group)

        net_layout.addWidget(QLabel("프록시 (Proxy):"))
        self.txt_proxy = QLineEdit(config_manager.get("proxy"))
        self.txt_proxy.setPlaceholderText("http://127.0.0.1:8080 또는 socks5://...")
        net_layout.addWidget(self.txt_proxy, stretch=1)

        net_layout.addWidget(QLabel("속도 제한 (Rate Limit):"))
        self.txt_rate_limit = QLineEdit(config_manager.get("rate_limit"))
        self.txt_rate_limit.setPlaceholderText("예: 5M, 500k")
        self.txt_rate_limit.setFixedWidth(100)
        net_layout.addWidget(self.txt_rate_limit)

        layout.addWidget(net_group)

        # 3. SponsorBlock & Features
        feat_group = QGroupBox("SponsorBlock & 추가 기능")
        feat_layout = QVBoxLayout(feat_group)

        self.chk_sponsorblock = QCheckBox("SponsorBlock 적용 (협찬/오프닝/쿠키 영상 자동 건너뛰기)")
        self.chk_sponsorblock.setChecked(config_manager.get("sponsorblock"))
        feat_layout.addWidget(self.chk_sponsorblock)

        sub_layout = QHBoxLayout()
        sub_layout.addWidget(QLabel("자막 언어 코드 (Sub Languages):"))
        self.txt_sub_langs = QLineEdit(config_manager.get("sub_langs", "ko,en.*"))
        sub_layout.addWidget(self.txt_sub_langs, stretch=1)
        feat_layout.addLayout(sub_layout)

        layout.addWidget(feat_group)

        # 4. Custom CLI Arguments Direct Pass-through Box (100% yt-dlp Features Support!)
        cli_group = QGroupBox("yt-dlp 사용자 정의 CLI 인자 (Direct CLI Pass-through)")
        cli_layout = QVBoxLayout(cli_group)

        cli_hint = QLabel("yt-dlp의 모든 매개변수 명령어를 그대로 입력할 수 있습니다. (예: --write-comments --geo-bypass --concurrent-fragments 5)")
        cli_hint.setStyleSheet("font-size: 11px; color: #0077B6; font-style: italic;")
        cli_layout.addWidget(cli_hint)

        self.txt_custom_cli = QLineEdit(config_manager.get("custom_cli_args"))
        self.txt_custom_cli.setPlaceholderText("--write-comments --write-info-json --geo-bypass")
        cli_layout.addWidget(self.txt_custom_cli)

        layout.addWidget(cli_group)

        # Save Button
        self.btn_save = QPushButton(" 설정 저장 및 기본값 반영")
        self.btn_save.setObjectName("btn_primary")
        self.btn_save.setIcon(get_icon("check", 18))
        self.btn_save.setFixedHeight(40)
        self.btn_save.clicked.connect(self.save_settings)
        layout.addWidget(self.btn_save)

        layout.addStretch()

    def on_browse_cookie(self):
        fpath, _ = QFileDialog.getOpenFileName(self, "쿠키 파일 선택", "", "Text Files (*.txt);;All Files (*)")
        if fpath:
            self.txt_cookie_file.setText(fpath)

    def save_settings(self):
        config_manager.set("cookie_browser", self.combo_browser.currentData())
        config_manager.set("cookies_file", self.txt_cookie_file.text().strip())
        config_manager.set("proxy", self.txt_proxy.text().strip())
        config_manager.set("rate_limit", self.txt_rate_limit.text().strip())
        config_manager.set("sponsorblock", self.chk_sponsorblock.isChecked())
        config_manager.set("sub_langs", self.txt_sub_langs.text().strip())
        config_manager.set("custom_cli_args", self.txt_custom_cli.text().strip())
        self.settings_saved.emit()

    def get_custom_args(self) -> str:
        return self.txt_custom_cli.text().strip()
