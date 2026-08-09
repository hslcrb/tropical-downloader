"""
Tropical Downloader - Refined Loading Splash Screen
"""
from PySide6.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar, QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtCore import Qt
from assets.icons import get_app_pixmap

class TropicalSplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(500, 300)
        pixmap.fill(Qt.GlobalColor.transparent)
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()

    def init_ui(self):
        self.container = QFrame(self)
        self.container.setFixedSize(460, 260)
        self.container.move(20, 20)
        self.container.setStyleSheet("""
            QFrame {
                background-color: #0F172A;
                border: 1px solid #334155;
                border-radius: 20px;
            }
        """)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(15, 23, 42, 200))
        shadow.setOffset(0, 8)
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo Image
        logo_lbl = QLabel()
        logo_lbl.setPixmap(get_app_pixmap(80, 80))
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_lbl)

        # Title Text
        title_lbl = QLabel("Tropical Downloader")
        title_lbl.setStyleSheet("""
            font-size: 22px;
            font-weight: 800;
            color: #F8FAFC;
            letter-spacing: 0.5px;
            background: transparent;
        """)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        sub_lbl = QLabel("트로피컬 다운로더 • Official Edition")
        sub_lbl.setStyleSheet("font-size: 12px; color: #94A3B8; font-weight: 500; background: transparent;")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub_lbl)

        layout.addSpacing(14)

        # Progress Bar
        self.pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)
        self.pbar.setFixedHeight(8)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet("""
            QProgressBar {
                background-color: #1E293B;
                border: none;
                border-radius: 4px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FF512F, stop:0.5 #DD2476, stop:1 #3B82F6);
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.pbar)

        # Status Message
        self.status_msg = QLabel("모듈 초기화 중...")
        self.status_msg.setStyleSheet("font-size: 11px; color: #64748B; background: transparent;")
        self.status_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_msg)

    def set_progress(self, val: int, msg: str):
        self.pbar.setValue(val)
        self.status_msg.setText(msg)
        self.repaint()
