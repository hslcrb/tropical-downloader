"""
Tropical Downloader - Playlist Batch Download Manager Tab
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QCheckBox, QLineEdit, QGroupBox, QHeaderView
)
from PySide6.QtCore import Signal, Qt
from assets.icons import get_icon

class PlaylistTab(QWidget):
    start_playlist_download = Signal(dict)

    def __init__(self):
        super().__init__()
        self.current_playlist_info = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Header Info Label
        self.header_lbl = QLabel("플레이리스트 관리자 - 다운로드할 항목을 선택하거나 범위를 지정하세요.")
        self.header_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #0077B6;")
        layout.addWidget(self.header_lbl)

        # Playlist Items Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["선택", "#", "비디오 제목", "재생시간"])
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)

        # Selection Control Row
        sel_layout = QHBoxLayout()
        self.btn_select_all = QPushButton("전체 선택")
        self.btn_select_all.clicked.connect(self.select_all)
        self.btn_unselect_all = QPushButton("선택 해제")
        self.btn_unselect_all.clicked.connect(self.unselect_all)
        
        sel_layout.addWidget(self.btn_select_all)
        sel_layout.addWidget(self.btn_unselect_all)

        sel_layout.addSpacing(20)
        sel_layout.addWidget(QLabel("범위 지정 (예: 1-5, 8):"))
        self.range_input = QLineEdit()
        self.range_input.setPlaceholderText("모두 다운로드 시 비워두세요")
        self.range_input.setFixedWidth(180)
        sel_layout.addWidget(self.range_input)
        sel_layout.addStretch()

        layout.addLayout(sel_layout)

        # Naming & Action Options
        group = QGroupBox("플레이리스트 저장 옵션")
        group_layout = QHBoxLayout(group)

        group_layout.addWidget(QLabel("파일명 템플릿:"))
        self.tmpl_input = QLineEdit("%(playlist_index)02d - %(title)s.%(ext)s")
        group_layout.addWidget(self.tmpl_input, stretch=1)

        self.btn_download_playlist = QPushButton(" 플레이리스트 다운로드 시작")
        self.btn_download_playlist.setObjectName("btn_primary")
        self.btn_download_playlist.setIcon(get_icon("playlist", 20))
        self.btn_download_playlist.setFixedHeight(38)
        self.btn_download_playlist.clicked.connect(self.on_download_playlist)
        group_layout.addWidget(self.btn_download_playlist)

        layout.addWidget(group)

    def populate_playlist(self, info: dict):
        self.current_playlist_info = info
        entries = info.get("playlist_entries", [])
        self.header_lbl.setText(f"플레이리스트: [{info.get('title')}] - 총 {len(entries)}개 비디오 항목")
        
        self.table.setRowCount(0)
        for idx, entry in enumerate(entries):
            self.table.insertRow(idx)

            # Checkbox item
            chk = QCheckBox()
            chk.setChecked(True)
            chk_widget = QWidget()
            chk_layout = QHBoxLayout(chk_widget)
            chk_layout.addWidget(chk)
            chk_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            chk_layout.setContentsMargins(0, 0, 0, 0)
            
            dur = entry.get("duration", 0)
            dur_str = f"{dur // 60}:{dur % 60:02d}" if dur else "--:--"

            self.table.setCellWidget(idx, 0, chk_widget)
            self.table.setItem(idx, 1, QTableWidgetItem(str(entry.get("index", idx + 1))))
            self.table.setItem(idx, 2, QTableWidgetItem(entry.get("title", "")))
            self.table.setItem(idx, 3, QTableWidgetItem(dur_str))

    def select_all(self):
        for r in range(self.table.rowCount()):
            widget = self.table.cellWidget(r, 0)
            if widget:
                chk = widget.findChild(QCheckBox)
                if chk:
                    chk.setChecked(True)

    def unselect_all(self):
        for r in range(self.table.rowCount()):
            widget = self.table.cellWidget(r, 0)
            if widget:
                chk = widget.findChild(QCheckBox)
                if chk:
                    chk.setChecked(False)

    def on_download_playlist(self):
        if not self.current_playlist_info:
            return

        params = {
            "url": self.current_playlist_info.get("url"),
            "filename_template": self.tmpl_input.text().strip(),
            "playlist_range": self.range_input.text().strip()
        }
        self.start_playlist_download.emit(params)
