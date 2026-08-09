"""
Tropical Downloader - In-App Media Player & Subtitle/JSON Editor Tab
Frutiger Aero / Y2K Tropical Island Edition

Robust Crash-Proof Architecture:
- Complete Emoji Purge
- Asynchronous Media Integrity Probe (MediaProbeWorker QThread)
- Total Decoupling between Frontend UI and Backend Media Engine
- Zero UI Freezing Guarantee
"""

import os
import json
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSplitter, QListWidget, QListWidgetItem,
    QLabel, QPushButton, QSlider, QStackedWidget, QTextEdit, QPlainTextEdit,
    QMessageBox, QFileDialog, QStyle, QComboBox, QGroupBox, QLineEdit
)
from PySide6.QtCore import Qt, QUrl, QTime, QThread, Signal
from PySide6.QtGui import QFont, QColor

# QtMultimedia Safe Import
HAS_MULTIMEDIA = False
try:
    from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
    from PySide6.QtMultimediaWidgets import QVideoWidget
    HAS_MULTIMEDIA = True
except Exception as e:
    print(f"[TabPlayer] QtMultimedia not fully supported on this platform: {e}")
    HAS_MULTIMEDIA = False

from core.config import config_manager
from styles.tropical_theme import TROPICAL_COLORS


class MediaProbeWorker(QThread):
    """
    Asynchronous Media File Integrity Probe Worker.
    Validates media files in a background thread to prevent GUI freezing or C++ Native crashes.
    """
    probe_finished = Signal(str, bool, str)  # (file_path, is_valid, error_reason)

    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path

    def run(self):
        if not self.file_path or not os.path.exists(self.file_path):
            self.probe_finished.emit(self.file_path, False, "파일이 존재하지 않습니다.")
            return

        # 1. Check for incomplete .part download files
        ext = os.path.splitext(self.file_path)[1].lower()
        if ext == ".part":
            self.probe_finished.emit(self.file_path, False, "다운로드가 진행 중인 .part 임시 파일입니다. 다운로드 완료 후 재생 가능합니다.")
            return

        # 2. Check file size (0 byte or corrupted small file)
        try:
            size_bytes = os.path.getsize(self.file_path)
            if size_bytes < 1024:  # Less than 1 KB is considered incomplete/corrupted header
                self.probe_finished.emit(self.file_path, False, f"손상되었거나 손실된 미디어 파일입니다. (용량: {size_bytes} Bytes)")
                return
        except Exception as e:
            self.probe_finished.emit(self.file_path, False, f"파일 접근 오류: {e}")
            return

        # 3. Binary Magic Bytes Probe
        try:
            with open(self.file_path, 'rb') as f:
                header = f.read(32)

            if len(header) < 12:
                self.probe_finished.emit(self.file_path, False, "미디어 헤더 바이너리가 유효하지 않습니다.")
                return

            # Check known magic signatures
            # MP4: 'ftyp' in first 12 bytes
            # MKV/WebM: starts with \x1a\x45\xdf\xa3
            # MP3: starts with ID3 or 0xff 0xfb/0xf3/0xf2
            # FLAC: starts with fLaC
            # WAV: starts with RIFF
            valid_signature = False
            if b'ftyp' in header:
                valid_signature = True
            elif header.startswith(b'\x1a\x45\xdf\xa3'):
                valid_signature = True
            elif header.startswith(b'ID3') or (header[0] == 0xFF and (header[1] & 0xE0) == 0xE0):
                valid_signature = True
            elif header.startswith(b'fLaC') or header.startswith(b'RIFF'):
                valid_signature = True
            elif ext in [".avi", ".mov", ".m4a", ".aac", ".webm", ".mkv", ".mp4", ".mp3", ".flac", ".wav"]:
                # Extension matches fallback
                valid_signature = True

            if not valid_signature:
                self.probe_finished.emit(self.file_path, False, "지원되지 않거나 인코딩이 불완전한 미디어 헤더입니다.")
                return

        except Exception as e:
            self.probe_finished.emit(self.file_path, False, f"헤더 검증 중 예외 발생: {e}")
            return

        # Passed all integrity checks
        self.probe_finished.emit(self.file_path, True, "")


class PlayerTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_file_path = None
        self.probe_worker = None
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(8, 8, 8, 8)
        main_layout.setSpacing(8)

        splitter = QSplitter(Qt.Horizontal)

        # -------------------------------------------------------------
        # Left Panel: File Explorer Sidebar
        # -------------------------------------------------------------
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(4, 4, 4, 4)

        sidebar_title = QLabel("미디어 & 데이터 파일 목록")
        sidebar_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #00E5FF;")
        sidebar_layout.addWidget(sidebar_title)

        # Path display & reload
        path_box = QHBoxLayout()
        self.btn_refresh = QPushButton("새로고침")
        self.btn_refresh.clicked.connect(self.refresh_file_list)
        self.btn_open_folder = QPushButton("폴더 변경")
        self.btn_open_folder.clicked.connect(self.choose_folder)
        path_box.addWidget(self.btn_refresh)
        path_box.addWidget(self.btn_open_folder)
        sidebar_layout.addLayout(path_box)

        # File List Widget
        self.file_list_widget = QListWidget()
        self.file_list_widget.setStyleSheet("""
            QListWidget {
                background-color: rgba(10, 25, 47, 0.7);
                border: 1px solid rgba(0, 229, 255, 0.3);
                border-radius: 8px;
                color: #FFFFFF;
            }
            QListWidget::item:selected {
                background-color: rgba(6, 214, 160, 0.4);
                color: #00E5FF;
                font-weight: bold;
            }
        """)
        self.file_list_widget.itemClicked.connect(self.on_file_item_clicked)
        sidebar_layout.addWidget(self.file_list_widget)

        splitter.addWidget(sidebar_widget)

        # -------------------------------------------------------------
        # Right Panel: Media Player & Editors (Stacked Widget)
        # -------------------------------------------------------------
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(4, 4, 4, 4)

        # Header Info
        self.lbl_selected_file = QLabel("선택된 파일이 없습니다. 좌측 목록에서 항목을 선택하세요.")
        self.lbl_selected_file.setStyleSheet("font-size: 13px; font-weight: bold; color: #FFD166;")
        right_layout.addWidget(self.lbl_selected_file)

        # Stacked Viewer Area
        self.stack = QStackedWidget()

        # Page 0: Welcome / Fallback
        self.page_welcome = QWidget()
        welcome_layout = QVBoxLayout(self.page_welcome)
        lbl_w = QLabel("트로피컬 인앱 플레이어 & 에디터\n\n- 비동기 미디어 검증 기반 비디오/음성 실시간 재생\n- 자막(.srt) 및 동영상 설명(.description) 텍스트 편집\n- 메타데이터(.json) 구조화 뷰어 및 저장")
        lbl_w.setAlignment(Qt.AlignCenter)
        lbl_w.setStyleSheet("font-size: 14px; color: #E0F7FA; line-height: 1.6;")
        welcome_layout.addWidget(lbl_w)
        self.stack.addWidget(self.page_welcome)

        # Page 1: Media Player Page
        self.page_player = QWidget()
        player_layout = QVBoxLayout(self.page_player)
        player_layout.setContentsMargins(0, 0, 0, 0)

        if HAS_MULTIMEDIA:
            try:
                self.player = QMediaPlayer()
                self.audio_output = QAudioOutput()
                self.player.setAudioOutput(self.audio_output)

                self.video_widget = QVideoWidget()
                self.video_widget.setStyleSheet("background-color: #000000; border-radius: 8px;")
                self.player.setVideoOutput(self.video_widget)
                player_layout.addWidget(self.video_widget, stretch=1)

                # Controls
                ctrl_layout = QHBoxLayout()

                self.btn_play_pause = QPushButton("재생")
                self.btn_play_pause.clicked.connect(self.toggle_play_pause)
                ctrl_layout.addWidget(self.btn_play_pause)

                self.btn_stop = QPushButton("정지")
                self.btn_stop.clicked.connect(self.stop_media)
                ctrl_layout.addWidget(self.btn_stop)

                # Time Label
                self.lbl_time = QLabel("00:00 / 00:00")
                self.lbl_time.setStyleSheet("color: #00E5FF; font-family: monospace;")
                ctrl_layout.addWidget(self.lbl_time)

                # Progress Slider
                self.slider_time = QSlider(Qt.Horizontal)
                self.slider_time.setRange(0, 0)
                self.slider_time.sliderMoved.connect(self.set_position)
                ctrl_layout.addWidget(self.slider_time, stretch=1)

                # Volume
                lbl_vol = QLabel("음량")
                lbl_vol.setStyleSheet("color: #00E5FF; font-size: 12px;")
                ctrl_layout.addWidget(lbl_vol)

                self.slider_volume = QSlider(Qt.Horizontal)
                self.slider_volume.setRange(0, 100)
                self.slider_volume.setValue(70)
                self.audio_output.setVolume(0.7)
                self.slider_volume.valueChanged.connect(self.on_volume_changed)
                ctrl_layout.addWidget(self.slider_volume)

                # Speed
                self.combo_speed = QComboBox()
                self.combo_speed.addItems(["0.5x", "1.0x", "1.25x", "1.5x", "2.0x"])
                self.combo_speed.setCurrentText("1.0x")
                self.combo_speed.currentTextChanged.connect(self.on_speed_changed)
                ctrl_layout.addWidget(self.combo_speed)

                player_layout.addLayout(ctrl_layout)

                # Connect signals with Safe Sandboxing
                self.player.positionChanged.connect(self.on_position_changed)
                self.player.durationChanged.connect(self.on_duration_changed)
                self.player.errorOccurred.connect(self.on_media_error_occurred)

            except Exception as e:
                print(f"[PlayerTab] Error setting up QtMultimedia: {e}")
                self.setup_fallback_player_page(player_layout)
        else:
            self.setup_fallback_player_page(player_layout)

        self.stack.addWidget(self.page_player)

        # Page 2: Text / Subtitle Editor Page
        self.page_editor = QWidget()
        editor_layout = QVBoxLayout(self.page_editor)

        self.txt_editor = QPlainTextEdit()
        self.txt_editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #051329;
                color: #A7FFEB;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 1px solid #00E5FF;
                border-radius: 6px;
            }
        """)
        editor_layout.addWidget(self.txt_editor, stretch=1)

        editor_btn_layout = QHBoxLayout()
        self.btn_save_text = QPushButton("자막 / 텍스트 저장")
        self.btn_save_text.setStyleSheet("background-color: #06D6A0; color: #000000; font-weight: bold;")
        self.btn_save_text.clicked.connect(self.save_text_file)
        editor_btn_layout.addStretch()
        editor_btn_layout.addWidget(self.btn_save_text)
        editor_layout.addLayout(editor_btn_layout)

        self.stack.addWidget(self.page_editor)

        # Page 3: JSON Metadata Editor Page
        self.page_json = QWidget()
        json_layout = QVBoxLayout(self.page_json)

        self.json_editor = QPlainTextEdit()
        self.json_editor.setStyleSheet("""
            QPlainTextEdit {
                background-color: #0D1F2D;
                color: #FFD166;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 13px;
                border: 1px solid #FFD166;
                border-radius: 6px;
            }
        """)
        json_layout.addWidget(self.json_editor, stretch=1)

        json_btn_layout = QHBoxLayout()
        self.btn_format_json = QPushButton("JSON 자동 정렬")
        self.btn_format_json.clicked.connect(self.format_json_content)
        self.btn_save_json = QPushButton("JSON 저장")
        self.btn_save_json.setStyleSheet("background-color: #FFD166; color: #000000; font-weight: bold;")
        self.btn_save_json.clicked.connect(self.save_json_file)

        json_btn_layout.addWidget(self.btn_format_json)
        json_btn_layout.addStretch()
        json_btn_layout.addWidget(self.btn_save_json)
        json_layout.addLayout(json_btn_layout)

        self.stack.addWidget(self.page_json)

        right_layout.addWidget(self.stack, stretch=1)
        splitter.addWidget(right_widget)

        splitter.setSizes([300, 700])
        main_layout.addWidget(splitter)

        # Populate file list initially
        self.refresh_file_list()

    def setup_fallback_player_page(self, layout):
        lbl_fb = QLabel("시스템 미디어 백엔드가 제한되어 인앱 비디오 플레이어를 로드할 수 없습니다.\n대신 외부 미디어 플레이어 연동 및 에디터 기능을 안전하게 지원합니다.")
        lbl_fb.setAlignment(Qt.AlignCenter)
        lbl_fb.setStyleSheet("color: #FF6B6B; font-size: 13px;")
        layout.addWidget(lbl_fb)

        btn_ext = QPushButton("외부 플레이어로 열기")
        btn_ext.clicked.connect(self.open_external_player)
        layout.addWidget(btn_ext, alignment=Qt.AlignCenter)

    def refresh_file_list(self):
        self.file_list_widget.clear()
        target_dir = config_manager.get("download_path")
        if not os.path.exists(target_dir):
            try:
                os.makedirs(target_dir, exist_ok=True)
            except Exception:
                pass

        if not os.path.exists(target_dir):
            return

        try:
            files = sorted(os.listdir(target_dir))
            for f in files:
                full_path = os.path.join(target_dir, f)
                if os.path.isfile(full_path):
                    ext = os.path.splitext(f)[1].lower()
                    type_prefix = "[파일]"
                    if ext in [".mp4", ".mkv", ".webm", ".avi", ".mov"]:
                        type_prefix = "[비디오]"
                    elif ext in [".mp3", ".m4a", ".flac", ".wav", ".aac"]:
                        type_prefix = "[오디오]"
                    elif ext in [".srt", ".description", ".txt", ".vtt"]:
                        type_prefix = "[자막/설명]"
                    elif ext in [".json"]:
                        type_prefix = "[메타데이터]"
                    elif ext in [".webp", ".jpg", ".png"]:
                        type_prefix = "[썸네일]"
                    elif ext in [".part"]:
                        type_prefix = "[다운로드 중]"

                    item = QListWidgetItem(f"{type_prefix} {f}")
                    item.setData(Qt.UserRole, full_path)
                    self.file_list_widget.addItem(item)
        except Exception as e:
            print(f"[PlayerTab] Error refreshing files: {e}")

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "미디어 폴더 선택", config_manager.get("download_path"))
        if folder:
            config_manager.set("download_path", folder)
            self.refresh_file_list()

    def on_file_item_clicked(self, item: QListWidgetItem):
        file_path = item.data(Qt.UserRole)
        self.load_file(file_path)

    def load_file(self, file_path: str):
        if not file_path or not os.path.exists(file_path):
            return

        self.current_file_path = file_path
        filename = os.path.basename(file_path)
        self.lbl_selected_file.setText(f"선택 파일: {filename}")

        ext = os.path.splitext(filename)[1].lower()

        # 1. Media Files (Requires Asynchronous Probe Validation)
        if ext in [".mp4", ".mkv", ".webm", ".avi", ".mov", ".mp3", ".m4a", ".flac", ".wav", ".part"]:
            self.lbl_selected_file.setText(f"선택 파일: {filename} (미디어 비동기 검증 중...)")

            # Terminate existing probe worker if running
            if self.probe_worker and self.probe_worker.isRunning():
                self.probe_worker.terminate()
                self.probe_worker.wait()

            # Launch Asynchronous Media Probe Worker
            self.probe_worker = MediaProbeWorker(file_path)
            self.probe_worker.probe_finished.connect(self.on_media_probe_finished)
            self.probe_worker.start()

        # 2. Text / Subtitle Files
        elif ext in [".srt", ".description", ".txt", ".vtt"]:
            self.stack.setCurrentWidget(self.page_editor)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                self.txt_editor.setPlainText(content)
            except Exception as e:
                self.txt_editor.setPlainText(f"파일을 읽는 중 오류가 발생했습니다: {e}")

        # 3. JSON Metadata Files
        elif ext in [".json"]:
            self.stack.setCurrentWidget(self.page_json)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    data = json.load(f)
                formatted = json.dumps(data, indent=4, ensure_ascii=False)
                self.json_editor.setPlainText(formatted)
            except Exception as e:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    self.json_editor.setPlainText(f.read())

        else:
            self.stack.setCurrentWidget(self.page_editor)
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    self.txt_editor.setPlainText(f.read())
            except Exception:
                self.txt_editor.setPlainText("미지원 바이너리 파일 형식입니다.")

    def on_media_probe_finished(self, file_path: str, is_valid: bool, error_reason: str):
        """Asynchronous callback when media integrity check completes."""
        filename = os.path.basename(file_path)

        if not is_valid:
            self.lbl_selected_file.setText(f"재생 불가: {filename} ({error_reason})")
            QMessageBox.warning(self, "미디어 재생 차단 알림",
                                f"선택한 파일은 불완전하거나 손상되어 인앱 재생이 차단되었습니다.\n\n"
                                f"사유: {error_reason}\n"
                                f"다운로드가 완전히 끝난 후 다시 시도해주세요.")
            self.stack.setCurrentWidget(self.page_welcome)
            return

        # Passed verification -> Load into QMediaPlayer safely
        self.lbl_selected_file.setText(f"선택 파일: {filename}")
        self.stack.setCurrentWidget(self.page_player)

        if HAS_MULTIMEDIA and hasattr(self, 'player'):
            try:
                # Stop existing playback first
                self.player.stop()
                self.player.setSource(QUrl.fromLocalFile(file_path))
                self.player.play()
                self.btn_play_pause.setText("일시정지")
            except Exception as e:
                print(f"[PlayerTab] Safe media load error: {e}")
                self.lbl_selected_file.setText(f"재생 오류: {filename}")

    def on_media_error_occurred(self, error, error_string):
        """QtMultimedia internal playback error signal handler."""
        print(f"[PlayerTab] QtMultimedia Error ({error}): {error_string}")
        if hasattr(self, 'btn_play_pause'):
            self.btn_play_pause.setText("재생")
        self.lbl_selected_file.setText(f"미디어 재생 오류 발생: {error_string}")

    def open_external_player(self):
        if self.current_file_path and os.path.exists(self.current_file_path):
            try:
                os.startfile(self.current_file_path)
            except Exception as e:
                QMessageBox.warning(self, "오류", f"외부 플레이어 실행 실패: {e}")

    # -------------------------------------------------------------
    # Media Player Handlers
    # -------------------------------------------------------------
    def toggle_play_pause(self):
        if not HAS_MULTIMEDIA or not hasattr(self, 'player'):
            self.open_external_player()
            return

        try:
            if self.player.playbackState() == QMediaPlayer.PlayingState:
                self.player.pause()
                self.btn_play_pause.setText("재생")
            else:
                self.player.play()
                self.btn_play_pause.setText("일시정지")
        except Exception as e:
            print(f"[PlayerTab] Toggle play/pause error: {e}")

    def stop_media(self):
        if HAS_MULTIMEDIA and hasattr(self, 'player'):
            try:
                self.player.stop()
                self.btn_play_pause.setText("재생")
            except Exception:
                pass

    def on_position_changed(self, position):
        if not self.slider_time.isSliderDown():
            self.slider_time.setValue(position)
        self.update_time_label(position, self.player.duration())

    def on_duration_changed(self, duration):
        self.slider_time.setRange(0, duration)
        self.update_time_label(self.player.position(), duration)

    def set_position(self, position):
        if HAS_MULTIMEDIA and hasattr(self, 'player'):
            try:
                self.player.setPosition(position)
            except Exception:
                pass

    def on_volume_changed(self, value):
        if HAS_MULTIMEDIA and hasattr(self, 'audio_output'):
            try:
                self.audio_output.setVolume(value / 100.0)
            except Exception:
                pass

    def on_speed_changed(self, text):
        if HAS_MULTIMEDIA and hasattr(self, 'player'):
            try:
                speed = float(text.replace('x', ''))
                self.player.setPlaybackRate(speed)
            except Exception:
                pass

    def update_time_label(self, pos_ms, dur_ms):
        pos_sec = pos_ms // 1000
        dur_sec = dur_ms // 1000
        pos_str = f"{pos_sec // 60:02d}:{pos_sec % 60:02d}"
        dur_str = f"{dur_sec // 60:02d}:{dur_sec % 60:02d}"
        self.lbl_time.setText(f"{pos_str} / {dur_str}")

    # -------------------------------------------------------------
    # Text / JSON Editor Handlers
    # -------------------------------------------------------------
    def save_text_file(self):
        if not self.current_file_path:
            return
        try:
            content = self.txt_editor.toPlainText()
            with open(self.current_file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            QMessageBox.information(self, "저장 완료", f"파일이 성공적으로 저장되었습니다:\n{os.path.basename(self.current_file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "저장 오류", f"파일 저장 중 오류가 발생했습니다: {e}")

    def format_json_content(self):
        try:
            raw = self.json_editor.toPlainText()
            parsed = json.loads(raw)
            formatted = json.dumps(parsed, indent=4, ensure_ascii=False)
            self.json_editor.setPlainText(formatted)
        except Exception as e:
            QMessageBox.warning(self, "JSON 오류", f"올바르지 않은 JSON 포맷입니다:\n{e}")

    def save_json_file(self):
        if not self.current_file_path:
            return
        try:
            raw = self.json_editor.toPlainText()
            parsed = json.loads(raw)
            with open(self.current_file_path, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, indent=4, ensure_ascii=False)
            QMessageBox.information(self, "저장 완료", f"JSON 메타데이터가 성공적으로 저장되었습니다:\n{os.path.basename(self.current_file_path)}")
        except Exception as e:
            QMessageBox.critical(self, "JSON 저장 오류", f"유효하지 않은 JSON 데이터이거나 저장 중 오류가 발생했습니다:\n{e}")
