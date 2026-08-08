"""
Tropical Downloader - Disk Space Warning & Auto-Detect Dialog
Continuously monitors disk space for 10 seconds. Auto-closes when space is freed.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from assets.icons import get_app_icon, get_icon
from core.disk_manager import get_free_space

class DiskSpaceDialog(QDialog):
    def __init__(self, target_path: str, required_bytes: int, parent=None):
        super().__init__(parent)
        self.target_path = target_path
        self.required_bytes = required_bytes
        self.seconds_left = 10
        self.space_freed = False

        self.setWindowTitle("저장공간 부족 — 공간 확보 대기 중")
        self.setFixedSize(500, 260)
        self.setWindowIcon(get_app_icon())
        self.setWindowModality(Qt.WindowModality.NonModal)

        self.init_ui()

        # 10 second auto-monitor timer (1s interval)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._on_timer_tick)
        self.timer.start()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        # Title / Warning Message
        self.msg_lbl = QLabel(
            "⚠️ <b>저장공간이 부족하여 다운로드한 미디어를 램(RAM) 메모리에 보관 중입니다.</b><br><br>"
            "저장 공간을 비워주시고 아래 확인 버튼을 눌러주세요.<br>"
            "(10초 동안 실시간으로 저장공간을 자동 감지합니다.)"
        )
        self.msg_lbl.setWordWrap(True)
        self.msg_lbl.setStyleSheet("font-size: 13px; color: #0F172A;")
        layout.addWidget(self.msg_lbl)

        # Space Status Info
        req_mb = self.required_bytes / 1048576
        free_mb = get_free_space(self.target_path) / 1048576

        self.status_lbl = QLabel(
            f"• 필요 저장공간 (대상의 +10% 여유분 포함): <b>{req_mb:.1f} MB</b><br>"
            f"• 현재 디스크 여유 공간: <b style='color:#EF4444;'>{free_mb:.1f} MB</b>"
        )
        self.status_lbl.setStyleSheet("font-size: 12px; background: #F0F9FF; padding: 10px; border-radius: 8px; border: 1px solid #BAE6FD;")
        layout.addWidget(self.status_lbl)

        # Countdown Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 10)
        self.progress_bar.setValue(10)
        self.progress_bar.setFormat("자동 감지 잔여 시간: %v초")
        layout.addWidget(self.progress_bar)

        # Action Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        self.btn_confirm = QPushButton("저장공간 비움 확인 / 저장 완료")
        self.btn_confirm.setObjectName("btn_primary")
        self.btn_confirm.setIcon(get_icon("check", 18))
        self.btn_confirm.setFixedHeight(38)
        self.btn_confirm.clicked.connect(self._on_user_confirm)
        btn_layout.addWidget(self.btn_confirm)

        layout.addLayout(btn_layout)

    def _on_timer_tick(self):
        self.seconds_left -= 1
        self.progress_bar.setValue(max(0, self.seconds_left))

        current_free = get_free_space(self.target_path)
        free_mb = current_free / 1048576
        req_mb = self.required_bytes / 1048576

        if current_free >= self.required_bytes:
            self.space_freed = True
            self.timer.stop()
            self.status_lbl.setText(
                f"🎉 <b>저장공간이 확보된 것을 확인했습니다!</b><br>"
                f"• 현재 디스크 여유 공간: <b style='color:#0EA5E9;'>{free_mb:.1f} MB</b> (필요: {req_mb:.1f} MB)"
            )
            self.msg_lbl.setText("<b>저장공간 확보 감지 완료! 파일을 디스크에 성공적으로 저장하고 창을 닫습니다.</b>")
            self.btn_confirm.setText("완료 처리 중...")
            self.btn_confirm.setEnabled(False)
            QTimer.singleShot(1500, self.accept)
        else:
            self.status_lbl.setText(
                f"• 필요 저장공간 (대상의 +10% 여유분 포함): <b>{req_mb:.1f} MB</b><br>"
                f"• 현재 디스크 여유 공간: <b style='color:#EF4444;'>{free_mb:.1f} MB</b>"
            )
            if self.seconds_left <= 0:
                self.progress_bar.setFormat("자동 감지 대기 완료 — 비운 후 확인 버튼을 눌러주세요")

    def _on_user_confirm(self):
        current_free = get_free_space(self.target_path)
        if current_free >= self.required_bytes:
            self.accept()
        else:
            free_mb = current_free / 1048576
            req_mb = self.required_bytes / 1048576
            self.status_lbl.setText(
                f"⚠️ 아직 저장공간이 부족합니다. (현재: {free_mb:.1f} MB / 필요: {req_mb:.1f} MB)<br>"
                f"불필요한 파일을 더 비워주신 후 다시 확인 버튼을 눌러주세요."
            )
