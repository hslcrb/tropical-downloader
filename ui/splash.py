"""
Tropical Downloader - Animated Frutiger Aero Loading Splash Screen
"""
from PySide6.QtWidgets import QSplashScreen, QVBoxLayout, QLabel, QProgressBar, QFrame, QGraphicsDropShadowEffect
from PySide6.QtGui import QPixmap, QColor, QFont
from PySide6.QtCore import Qt, QTimer
from assets.icons import get_app_pixmap

class TropicalSplashScreen(QSplashScreen):
    def __init__(self):
        pixmap = QPixmap(520, 320)
        pixmap.fill(Qt.GlobalColor.transparent)
        super().__init__(pixmap)
        
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Translucent Aqua Container
        self.container = QFrame(self)
        self.container.setFixedSize(480, 280)
        self.container.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 229, 255, 0.95), stop:0.5 rgba(0, 180, 216, 0.95), stop:1 rgba(3, 4, 94, 0.95));
                border: 2px solid #FFFFFF;
                border-radius: 24px;
            }
        """)

        # Drop shadow for Aero depth
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 180, 216, 180))
        shadow.setOffset(0, 10)
        self.container.setGraphicsEffect(shadow)

        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo Image
        logo_lbl = QLabel()
        logo_lbl.setPixmap(get_app_pixmap(88, 88))
        logo_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_lbl)

        # Title Text
        title_lbl = QLabel("Tropical Downloader")
        title_lbl.setStyleSheet("""
            font-size: 24px;
            font-weight: 900;
            color: #FFFFFF;
            letter-spacing: 1px;
            background: transparent;
        """)
        title_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_lbl)

        sub_lbl = QLabel("트로피컬 다운로더 • Frutiger Aero Y2K Edition")
        sub_lbl.setStyleSheet("font-size: 12px; color: #E0F7FA; font-weight: 600; background: transparent;")
        sub_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sub_lbl)

        layout.addSpacing(16)

        # Neon Progress Bar
        self.pbar = QProgressBar()
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)
        self.pbar.setFixedHeight(12)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet("""
            QProgressBar {
                background-color: rgba(255, 255, 255, 0.3);
                border: 1px solid #FFFFFF;
                border-radius: 6px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FFE600, stop:0.5 #06D6A0, stop:1 #FFFFFF);
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.pbar)

        # Status Message
        self.status_msg = QLabel("엔진 초기화 중...")
        self.status_msg.setStyleSheet("font-size: 11px; color: #FFFFFF; font-style: italic; background: transparent;")
        self.status_msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_msg)

    def set_progress(self, val: int, msg: str):
        self.pbar.setValue(val)
        self.status_msg.setText(msg)
        self.repaint()
