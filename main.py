"""
Tropical Downloader ("트로피컬") - Main Application Entry Point
Frutiger Aero / Y2K Tropical Island Edition
"""
import sys
import os
import uuid
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QStatusBar, QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer

from styles.tropical_theme import apply_theme
from assets.icons import get_icon, get_app_icon
from ui.header import TropicalHeader
from ui.tab_quick import QuickTab
from ui.tab_inspector import InspectorTab
from ui.tab_playlist import PlaylistTab
from ui.tab_advanced import AdvancedTab
from ui.tab_queue import QueueTab
from ui.tab_history import HistoryTab
from ui.dialogs.about_dialog import AboutDialog
from ui.splash import TropicalSplashScreen
from core.yt_worker import DownloadWorker

class TropicalMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tropical Downloader - 트로피컬 아일랜드 Y2K 다운로더")
        self.setWindowIcon(get_app_icon())
        self.resize(1020, 720)
        self.setMinimumSize(880, 600)

        self.active_workers = {}  # task_id -> DownloadWorker

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # 1. Header Bar
        self.header = TropicalHeader()
        self.header.url_submitted.connect(self.on_url_submitted)
        self.header.open_about.connect(self.on_open_about)
        main_layout.addWidget(self.header)

        # 2. Main Tabs System
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Tab 0: Quick Download
        self.tab_quick = QuickTab()
        self.tab_quick.start_download.connect(self.start_download_job)
        self.tabs.addTab(self.tab_quick, get_icon("quick", 20), "빠른 다운로드")

        # Tab 1: Format Inspector
        self.tab_inspector = InspectorTab()
        self.tab_inspector.start_custom_download.connect(self.start_download_job)
        self.tabs.addTab(self.tab_inspector, get_icon("inspector", 20), "상세 포맷 분석")

        # Tab 2: Playlist Batch
        self.tab_playlist = PlaylistTab()
        self.tab_playlist.start_playlist_download.connect(self.start_download_job)
        self.tabs.addTab(self.tab_playlist, get_icon("playlist", 20), "플레이리스트")

        # Tab 3: Advanced Options
        self.tab_advanced = AdvancedTab()
        self.tabs.addTab(self.tab_advanced, get_icon("advanced", 20), "고급 yt-dlp 옵션")

        # Tab 4: Queue & Progress
        self.tab_queue = QueueTab()
        self.tab_queue.cancel_task_signal.connect(self.cancel_download_job)
        self.tabs.addTab(self.tab_queue, get_icon("queue", 20), "진행상황 큐")

        # Tab 5: History & Debug Logs
        self.tab_history = HistoryTab()
        self.tabs.addTab(self.tab_history, get_icon("history", 20), "기록 & 디버그 로그")

        main_layout.addWidget(self.tabs, stretch=1)
        self.setCentralWidget(central_widget)

        # 3. Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("🌴 트로피컬 다운로더 준비 완료. URL을 입력하세요.")
        self.setStatusBar(self.status_bar)

    def on_url_submitted(self, url: str):
        self.status_bar.showMessage(f"미디어 분석 시작: {url}")
        
        # Trigger quick tab analyze
        self.tab_quick.analyze_url(url)
        
        # Connect info fetcher finished signal to populate inspector and playlist tabs
        if hasattr(self.tab_quick, "info_worker") and self.tab_quick.info_worker:
            self.tab_quick.info_worker.finished_info.connect(self.on_info_fetched)

    def on_info_fetched(self, info: dict):
        if info.get("is_playlist"):
            self.tab_playlist.populate_playlist(info)
            self.tabs.setCurrentWidget(self.tab_playlist)
            self.status_bar.showMessage("플레이리스트 분석 완료. 원하는 항목을 선택하세요.")
        else:
            self.tab_inspector.populate_info(info)
            self.status_bar.showMessage(f"미디어 분석 완료: [{info.get('title')}]")

    def start_download_job(self, params: dict):
        url = params.get("url")
        if not url:
            QMessageBox.warning(self, "경고", "다운로드할 URL이 없습니다.")
            return

        task_id = f"task_{uuid.uuid4().hex[:6]}"
        title = self.tab_quick.current_info.get("title", url) if self.tab_quick.current_info else url

        # Retrieve custom CLI args from Advanced Tab if present
        custom_args = self.tab_advanced.get_custom_args()

        # Create worker thread
        worker = DownloadWorker(task_id=task_id, url=url, options_override=params, custom_args=custom_args)
        self.active_workers[task_id] = worker

        # Register in Queue tab
        self.tab_queue.add_task(task_id, title, url)

        # Connect Signals
        worker.progress_signal.connect(self.tab_queue.update_progress)
        worker.log_signal.connect(self.tab_history.append_log)
        worker.finished_signal.connect(self.on_worker_finished)
        worker.error_signal.connect(self.on_worker_error)

        # Start Download Thread
        worker.start()

        # Switch to Queue Tab
        self.tabs.setCurrentWidget(self.tab_queue)
        self.status_bar.showMessage(f"다운로드 시작: [{title}]")

    def on_worker_finished(self, task_id: str, file_path: str, title: str):
        self.tab_queue.on_task_finished(task_id, file_path, title)
        self.tab_history.reload_history()
        self.status_bar.showMessage(f"🎉 다운로드 완료: {title}")
        if task_id in self.active_workers:
            del self.active_workers[task_id]

    def on_worker_error(self, task_id: str, err_msg: str):
        self.tab_queue.on_task_error(task_id, err_msg)
        self.status_bar.showMessage(f"❌ 다운로드 오류: {err_msg}")
        if task_id in self.active_workers:
            del self.active_workers[task_id]

    def cancel_download_job(self, task_id: str):
        if task_id in self.active_workers:
            self.active_workers[task_id].cancel()
            self.status_bar.showMessage(f"다운로드 취소 요청됨: [{task_id}]")

    def on_open_about(self):
        dlg = AboutDialog(self)
        dlg.exec()

def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    app.setWindowIcon(get_app_icon())
    apply_theme(app)

    # Show Splash Screen
    splash = TropicalSplashScreen()
    splash.show()
    splash.set_progress(25, "Frutiger Aero 테마 로딩 중...")
    app.processEvents()

    window = TropicalMainWindow()

    def step2():
        splash.set_progress(60, "yt-dlp 백엔드 및 모듈 연결 중...")
        app.processEvents()
        QTimer.singleShot(300, step3)

    def step3():
        splash.set_progress(100, "준비 완료! 메인 UI 실행 중...")
        app.processEvents()
        QTimer.singleShot(300, finish_splash)

    def finish_splash():
        window.show()
        splash.finish(window)

    QTimer.singleShot(300, step2)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
