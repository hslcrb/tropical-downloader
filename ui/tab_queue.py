"""
Tropical Downloader - Download Queue & Active Tasks Tracker Tab
"""
import os
import subprocess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QProgressBar, QPushButton, QHeaderView, QFrame
)
from PySide6.QtCore import Signal, Qt
from assets.icons import get_icon
from core.history_manager import history_manager

class QueueTab(QWidget):
    cancel_task_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.tasks = {}  # task_id -> row_index
        self.task_data = {} # task_id -> dict(title, file_path, status)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Header bar
        header_layout = QHBoxLayout()
        title_lbl = QLabel("다운로드 진행 현황 & 작업 큐 (Download Queue)")
        title_lbl.setStyleSheet("font-size: 14px; font-weight: bold; color: #0077B6;")
        header_layout.addWidget(title_lbl)

        header_layout.addStretch()

        self.btn_clear_done = QPushButton(" 완료된 작업 지우기")
        self.btn_clear_done.setIcon(get_icon("trash", 16))
        self.btn_clear_done.clicked.connect(self.clear_finished_tasks)
        header_layout.addWidget(self.btn_clear_done)

        layout.addLayout(header_layout)

        # Queue Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "제목", "진행률", "다운로드 속도", "남은 시간", "상태", "작업"
        ])
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(2, 180)
        layout.addWidget(self.table)

    def add_task(self, task_id: str, title: str, url: str):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.tasks[task_id] = row
        self.task_data[task_id] = {"title": title, "path": "", "status": "WAITING"}

        self.table.setItem(row, 0, QTableWidgetItem(task_id))
        self.table.setItem(row, 1, QTableWidgetItem(title))

        # Progress bar
        pbar = QProgressBar()
        pbar.setRange(0, 100)
        pbar.setValue(0)
        self.table.setCellWidget(row, 2, pbar)

        self.table.setItem(row, 3, QTableWidgetItem("0 MB/s"))
        self.table.setItem(row, 4, QTableWidgetItem("--:--"))
        self.table.setItem(row, 5, QTableWidgetItem("대기 중..."))

        # Action Buttons container widget
        action_widget = QWidget()
        act_layout = QHBoxLayout(action_widget)
        act_layout.setContentsMargins(0, 0, 0, 0)
        act_layout.setSpacing(4)

        btn_cancel = QPushButton()
        btn_cancel.setIcon(get_icon("stop", 16))
        btn_cancel.setFixedSize(28, 28)
        btn_cancel.setToolTip("다운로드 취소")
        btn_cancel.clicked.connect(lambda: self.cancel_task_signal.emit(task_id))
        act_layout.addWidget(btn_cancel)

        self.table.setCellWidget(row, 6, action_widget)

    def update_progress(self, task_id: str, percent: float, speed: str, eta: str, downloaded: int, total: int, status: str):
        if task_id not in self.tasks:
            return
        row = self.tasks[task_id]

        pbar = self.table.cellWidget(row, 2)
        if pbar:
            pbar.setValue(int(percent))

        self.table.setItem(row, 3, QTableWidgetItem(speed))
        self.table.setItem(row, 4, QTableWidgetItem(eta))
        
        status_item = QTableWidgetItem(status)
        if status == "FINISHED":
            status_item.setForeground(Qt.GlobalColor.darkGreen)
        elif status == "ERROR":
            status_item.setForeground(Qt.GlobalColor.red)
        
        self.table.setItem(row, 5, status_item)

    def on_task_finished(self, task_id: str, file_path: str, title: str):
        if task_id not in self.tasks:
            return
        row = self.tasks[task_id]
        self.task_data[task_id]["path"] = file_path
        self.task_data[task_id]["status"] = "FINISHED"

        # Replace action buttons with Open Folder / In-App Player / External Play
        action_widget = QWidget()
        act_layout = QHBoxLayout(action_widget)
        act_layout.setContentsMargins(0, 0, 0, 0)
        act_layout.setSpacing(4)

        btn_inapp = QPushButton()
        btn_inapp.setIcon(get_icon("quick", 16))
        btn_inapp.setFixedSize(28, 28)
        btn_inapp.setToolTip("인앱 플레이어로 열기/편집")
        btn_inapp.clicked.connect(lambda: self.open_in_player(file_path))
        act_layout.addWidget(btn_inapp)

        btn_folder = QPushButton()
        btn_folder.setIcon(get_icon("folder", 16))
        btn_folder.setFixedSize(28, 28)
        btn_folder.setToolTip("저장 폴더 열기")
        btn_folder.clicked.connect(lambda: self.open_file_folder(file_path))
        act_layout.addWidget(btn_folder)

        btn_play = QPushButton()
        btn_play.setIcon(get_icon("play", 16))
        btn_play.setFixedSize(28, 28)
        btn_play.setToolTip("외부 미디어 플레이어로 실행")
        btn_play.clicked.connect(lambda: self.open_file(file_path))
        act_layout.addWidget(btn_play)

        self.table.setCellWidget(row, 6, action_widget)

    def open_in_player(self, path: str):
        if not path:
            return
        parent = self.window()
        if hasattr(parent, "open_in_player"):
            parent.open_in_player(path)

    def on_task_error(self, task_id: str, err_msg: str):
        if task_id not in self.tasks:
            return
        row = self.tasks[task_id]
        self.table.setItem(row, 5, QTableWidgetItem("오류 발생"))
        self.table.setItem(row, 3, QTableWidgetItem("-"))
        self.table.setItem(row, 4, QTableWidgetItem("-"))

    def open_file_folder(self, path: str):
        if not path:
            return
        folder = os.path.dirname(path) if os.path.isfile(path) else path
        if os.path.exists(folder):
            os.startfile(folder)

    def open_file(self, path: str):
        if path and os.path.exists(path):
            os.startfile(path)

    def clear_finished_tasks(self):
        to_remove = []
        for task_id, row in list(self.tasks.items()):
            status_item = self.table.item(row, 5)
            if status_item and status_item.text() in ["FINISHED", "FINISHED", "오류 발생"]:
                to_remove.append(task_id)

        # Re-build table
        for task_id in to_remove:
            row = self.tasks[task_id]
            self.table.removeRow(row)
            del self.tasks[task_id]
            del self.task_data[task_id]

        # Update remaining row indices
        self.tasks = {}
        for r in range(self.table.rowCount()):
            t_id = self.table.item(r, 0).text()
            self.tasks[t_id] = r
