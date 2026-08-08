"""
Tropical Downloader - Detailed Format Inspector Tab
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QPushButton, QComboBox, QCheckBox, QGroupBox, QHeaderView
)
from PySide6.QtCore import Signal, Qt
from assets.icons import get_icon
from core.config import config_manager

class InspectorTab(QWidget):
    start_custom_download = Signal(dict)

    def __init__(self):
        super().__init__()
        self.current_info = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(14)

        # Header Info Label
        self.info_header_lbl = QLabel("상세 미디어 포맷 분석기 - 사용 가능한 비디오/오디오 스트림을 직접 선택하세요.")
        self.info_header_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #0077B6;")
        layout.addWidget(self.info_header_lbl)

        # Formats Table
        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "ID", "확장자", "해상도 / 비트레이트", "FPS", "비디오 코덱", "오디오 코덱", "예상 용량", "비고"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.itemSelectionChanged.connect(self.on_table_selection_changed)
        layout.addWidget(self.table)

        # Options & Container Builder
        builder_group = QGroupBox("맞춤 포맷 조합 설정")
        builder_layout = QHBoxLayout(builder_group)
        builder_layout.setSpacing(16)

        # Stream Selection Combos
        combo_vbox = QVBoxLayout()
        
        v_layout = QHBoxLayout()
        v_layout.addWidget(QLabel("비디오 스트림 ID:"))
        self.combo_video = QComboBox()
        self.combo_video.setMinimumWidth(180)
        v_layout.addWidget(self.combo_video)
        combo_vbox.addLayout(v_layout)

        a_layout = QHBoxLayout()
        a_layout.addWidget(QLabel("오디오 스트림 ID:"))
        self.combo_audio = QComboBox()
        self.combo_audio.setMinimumWidth(180)
        a_layout.addWidget(self.combo_audio)
        combo_vbox.addLayout(a_layout)

        builder_layout.addLayout(combo_vbox)

        # Checkboxes for Post-Processing
        opts_vbox = QVBoxLayout()
        self.chk_embed_subs = QCheckBox("자막 자동 다운로드 및 임베딩")
        self.chk_embed_subs.setChecked(config_manager.get("embed_subs"))
        self.chk_embed_thumb = QCheckBox("썸네일 이미지 임베딩")
        self.chk_embed_thumb.setChecked(config_manager.get("embed_thumbnail"))
        self.chk_embed_meta = QCheckBox("메타데이터 태그 임베딩")
        self.chk_embed_meta.setChecked(config_manager.get("embed_metadata"))

        opts_vbox.addWidget(self.chk_embed_subs)
        opts_vbox.addWidget(self.chk_embed_thumb)
        opts_vbox.addWidget(self.chk_embed_meta)
        builder_layout.addLayout(opts_vbox)

        # Action Button
        action_vbox = QVBoxLayout()
        self.btn_download_custom = QPushButton(" 선택한 포맷 다운로드")
        self.btn_download_custom.setObjectName("btn_accent")
        self.btn_download_custom.setIcon(get_icon("download", 20))
        self.btn_download_custom.setFixedHeight(42)
        self.btn_download_custom.clicked.connect(self.on_download_selected)
        action_vbox.addWidget(self.btn_download_custom)
        builder_layout.addLayout(action_vbox)

        layout.addWidget(builder_group)

    def populate_info(self, info: dict):
        self.current_info = info
        self.table.setRowCount(0)
        self.combo_video.clear()
        self.combo_audio.clear()

        self.combo_video.addItem("자동 최적 비디오 (bestvideo)", "bestvideo")
        self.combo_video.addItem("비디오 없음 (오디오 전용)", "none")

        self.combo_audio.addItem("자동 최적 오디오 (bestaudio)", "bestaudio")
        self.combo_audio.addItem("오디오 없음 (비디오 전용)", "none")

        formats = info.get("formats", [])
        self.info_header_lbl.setText(f"분석 결과: [{info.get('title')}] - 총 {len(formats)}개 스트림 포맷 감지됨")

        for idx, fmt in enumerate(formats):
            self.table.insertRow(idx)
            
            fmt_id = str(fmt.get("format_id", ""))
            ext = str(fmt.get("ext", ""))
            res = str(fmt.get("resolution", ""))
            fps = str(fmt.get("fps", 0)) if fmt.get("fps") else "-"
            vcodec = str(fmt.get("vcodec", ""))
            acodec = str(fmt.get("acodec", ""))
            
            size = fmt.get("filesize", 0)
            size_str = f"{size / (1024*1024):.1f} MB" if size else "--"
            note = str(fmt.get("format_note", ""))

            self.table.setItem(idx, 0, QTableWidgetItem(fmt_id))
            self.table.setItem(idx, 1, QTableWidgetItem(ext))
            self.table.setItem(idx, 2, QTableWidgetItem(res))
            self.table.setItem(idx, 3, QTableWidgetItem(fps))
            self.table.setItem(idx, 4, QTableWidgetItem(vcodec))
            self.table.setItem(idx, 5, QTableWidgetItem(acodec))
            self.table.setItem(idx, 6, QTableWidgetItem(size_str))
            self.table.setItem(idx, 7, QTableWidgetItem(note))

            # Add to comboboxes
            display_str = f"[{fmt_id}] {ext} | {res} | {vcodec}/{acodec}"
            if fmt.get("is_video"):
                self.combo_video.addItem(display_str, fmt_id)
            if fmt.get("is_audio"):
                self.combo_audio.addItem(display_str, fmt_id)

    def on_table_selection_changed(self):
        selected_rows = self.table.selectedItems()
        if not selected_rows:
            return
        row = self.table.currentRow()
        fmt_id = self.table.item(row, 0).text()
        vcodec = self.table.item(row, 4).text()
        acodec = self.table.item(row, 5).text()

        # Auto-match combos
        if vcodec != "none":
            idx = self.combo_video.findData(fmt_id)
            if idx >= 0:
                self.combo_video.setCurrentIndex(idx)
        if acodec != "none":
            idx = self.combo_audio.findData(fmt_id)
            if idx >= 0:
                self.combo_audio.setCurrentIndex(idx)

    def on_download_selected(self):
        if not self.current_info:
            return
        
        v_id = self.combo_video.currentData()
        a_id = self.combo_audio.currentData()

        if v_id == "none" and a_id == "none":
            return

        if v_id == "none":
            fmt_str = a_id
        elif a_id == "none":
            fmt_str = v_id
        else:
            fmt_str = f"{v_id}+{a_id}"

        params = {
            "url": self.current_info.get("url"),
            "format": fmt_str,
            "embed_subs": self.chk_embed_subs.isChecked(),
            "embed_thumbnail": self.chk_embed_thumb.isChecked(),
            "embed_metadata": self.chk_embed_meta.isChecked(),
        }
        self.start_custom_download.emit(params)
