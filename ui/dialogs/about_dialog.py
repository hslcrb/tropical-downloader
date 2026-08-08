"""
Tropical Downloader - About & License Compliance Dialog
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit
)
from PySide6.QtCore import Qt
from assets.icons import get_app_pixmap, get_app_icon

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Non-modal: user can interact with main window while this is open
        self.setWindowModality(Qt.WindowModality.NonModal)
        self.setWindowTitle("About Tropical Downloader")
        self.setFixedSize(520, 460)
        self.init_ui()
        self.setWindowIcon(get_app_icon())

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Top Header
        top_layout = QHBoxLayout()
        top_layout.setSpacing(14)

        logo_lbl = QLabel()
        logo_lbl.setPixmap(get_app_pixmap(60, 60))
        top_layout.addWidget(logo_lbl)

        info_vbox = QVBoxLayout()
        info_vbox.setSpacing(4)

        title_lbl = QLabel("Tropical Downloader")
        title_lbl.setStyleSheet("font-size: 18px; font-weight: 800; color: #0F172A;")

        ver_lbl = QLabel("v2.0.0  •  Python 3 & PySide6")
        ver_lbl.setStyleSheet("font-size: 12px; color: #475569; font-weight: 600;")

        author_lbl = QLabel("오픈소스 미디어 다운로더")
        author_lbl.setStyleSheet("font-size: 11px; color: #94A3B8;")

        info_vbox.addWidget(title_lbl)
        info_vbox.addWidget(ver_lbl)
        info_vbox.addWidget(author_lbl)
        top_layout.addLayout(info_vbox)

        layout.addLayout(top_layout)

        # License Compliance Text Box
        license_box = QTextEdit()
        license_box.setReadOnly(True)
        license_box.setHtml("""
        <h3>Tropical Downloader — 오픈소스 라이선스 고지</h3>
        <p>본 프로그램은 오픈소스 라이선스 규정을 철저히 준수합니다.</p>
        <hr/>
        <h4>1. PySide6 (Qt for Python)</h4>
        <p><b>라이선스:</b> GNU Lesser General Public License (LGPL) v3</p>
        <p>PySide6 라이브러리는 동적 바인딩 방식으로 연동되어 적용되었습니다.</p>

        <h4>2. yt-dlp</h4>
        <p><b>라이선스:</b> Unlicense (Public Domain)</p>
        <p>yt-dlp 프로젝트는 퍼블릭 도메인으로 자율적 이용이 허용됩니다.</p>

        <h4>3. FFmpeg</h4>
        <p><b>라이선스:</b> GNU LGPL v2.1+ / GPL v2+</p>
        <p>미디어 변환 및 포맷 멀티플렉싱을 위해 시스템 FFmpeg 바이너리를 동적 호출합니다.</p>
        <hr/>
        <p>Copyright &copy; 2026 Tropical Downloader Contributors. MIT License.</p>
        """)
        layout.addWidget(license_box)

        # Close button
        btn_close = QPushButton("확인")
        btn_close.setObjectName("btn_primary")
        btn_close.setFixedHeight(36)
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)
