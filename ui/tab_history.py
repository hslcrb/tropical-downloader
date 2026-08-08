"""
Tropical Downloader - History & Raw Log Console Tab
"""
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QTextEdit, QPushButton, QHeaderView, QSplitter
)
from PySide6.QtCore import Qt
from assets.icons import get_icon
from core.history_manager import history_manager

class HistoryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(10)

        splitter = QSplitter(Qt.Orientation.Vertical)

        # Top Container: History Table
        hist_widget = QWidget()
        hist_layout = QVBoxLayout(hist_widget)
        hist_layout.setContentsMargins(0, 0, 0, 0)

        hist_header = QHBoxLayout()
        lbl_h = QLabel("다운로드 내역 (History)")
        lbl_h.setStyleSheet("font-size: 14px; font-weight: bold; color: #0077B6;")
        hist_header.addWidget(lbl_h)
        hist_header.addStretch()

        btn_refresh = QPushButton("새로고침")
        btn_refresh.clicked.connect(self.reload_history)
        hist_header.addWidget(btn_refresh)

        btn_clear = QPushButton("기록 전체 삭제")
        btn_clear.setIcon(get_icon("trash", 16))
        btn_clear.clicked.connect(self.clear_history)
        hist_header.addWidget(btn_clear)

        hist_layout.addLayout(hist_header)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "시간", "비디오 제목", "포맷", "용량", "저장 경로", "작업"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        hist_layout.addWidget(self.table)

        splitter.addWidget(hist_widget)

        # Bottom Container: Real-Time Debug Log Console
        log_widget = QWidget()
        log_layout = QVBoxLayout(log_widget)
        log_layout.setContentsMargins(0, 0, 0, 0)

        log_header = QHBoxLayout()
        lbl_l = QLabel("실시간 yt-dlp 디버그 콘솔 출력 (Log Terminal)")
        lbl_l.setStyleSheet("font-size: 13px; font-weight: bold; color: #0077B6;")
        log_header.addWidget(lbl_l)
        log_header.addStretch()

        btn_clear_log = QPushButton("로그 지우기")
        btn_clear_log.clicked.connect(self.clear_log)
        log_header.addWidget(btn_clear_log)

        log_layout.addLayout(log_header)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet("""
            background-color: #03045E;
            color: #00E5FF;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 12px;
            border-radius: 10px;
            padding: 8px;
        """)
        log_layout.addWidget(self.log_console)

        splitter.addWidget(log_widget)
        splitter.setSizes([300, 200])

        layout.addWidget(splitter)

        self.reload_history()

    def reload_history(self):
        history_manager.load()
        entries = history_manager.history
        self.table.setRowCount(0)
        
        for idx, item in enumerate(entries):
            self.table.insertRow(idx)
            self.table.setItem(idx, 0, QTableWidgetItem(item.get("timestamp", "")))
            self.table.setItem(idx, 1, QTableWidgetItem(item.get("title", "")))
            self.table.setItem(idx, 2, QTableWidgetItem(item.get("format", "")))
            self.table.setItem(idx, 3, QTableWidgetItem(item.get("size", "")))
            self.table.setItem(idx, 4, QTableWidgetItem(item.get("path", "")))

            # Actions widget
            fpath = item.get("path", "")
            action_widget = QWidget()
            act_layout = QHBoxLayout(action_widget)
            act_layout.setContentsMargins(0, 0, 0, 0)
            act_layout.setSpacing(4)

            btn_folder = QPushButton()
            btn_folder.setIcon(get_icon("folder", 16))
            btn_folder.setFixedSize(28, 28)
            btn_folder.setToolTip("폴더 열기")
            btn_folder.clicked.connect(lambda _, p=fpath: self.open_folder(p))
            act_layout.addWidget(btn_folder)

            self.table.setCellWidget(idx, 5, action_widget)

    def append_log(self, task_id: str, line: str):
        self.log_console.append(f"[{task_id}] {line}")

    def clear_log(self):
        self.log_console.clear()

    def clear_history(self):
        history_manager.clear()
        self.reload_history()

    def open_folder(self, path: str):
        if not path:
            return
        folder = os.path.dirname(path) if os.path.isfile(path) else path
        if os.path.exists(folder):
            os.startfile(folder)
