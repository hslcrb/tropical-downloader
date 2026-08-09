"""
Tropical Downloader ("트로피컬") - Main Application Entry Point
Frutiger Aero / Y2K Tropical Island Edition
"""
import sys
import os
import uuid
import traceback
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, QStatusBar, QMessageBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer

from styles.tropical_theme import apply_theme
from assets.icons import get_icon, get_app_icon
from core.config import config_manager
from ui.header import TropicalHeader
from ui.tab_quick import QuickTab
from ui.tab_inspector import InspectorTab
from ui.tab_playlist import PlaylistTab
from ui.tab_advanced import AdvancedTab
from ui.tab_settings import SettingsTab
from ui.tab_queue import QueueTab
from ui.tab_history import HistoryTab
from ui.tab_player import PlayerTab
from ui.dialogs.about_dialog import AboutDialog
from ui.dialogs.disk_space_dialog import DiskSpaceDialog
from ui.splash import TropicalSplashScreen
from core.yt_worker import DownloadWorker

# -----------------------------------------------------------------------------
# Global Crash-Proof Exception Handler
# Guaranteed to prevent application crashes on uncaught exceptions
# -----------------------------------------------------------------------------
def global_exception_hook(exctype, value, tb):
    err_msg = "".join(traceback.format_exception(exctype, value, tb))
    print(f"[CRASH-PROOF ENGINE] Uncaught Exception Intercepted:\n{err_msg}")
    try:
        if QApplication.instance():
            for widget in QApplication.topLevelWidgets():
                if isinstance(widget, TropicalMainWindow):
                    widget.status_bar.showMessage(f"시스템 알림: {value}")
                    break
    except Exception:
        pass

sys.excepthook = global_exception_hook


class TropicalMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tropical Downloader")
        self.setWindowIcon(get_app_icon())
        self.resize(1080, 760)
        self.setMinimumSize(920, 640)

        self.active_workers = {}  # task_id -> DownloadWorker
        self.disk_dialogs = {}    # task_id -> DiskSpaceDialog

        self.init_ui_sandbox()

    def init_ui_sandbox(self):
        """Sandboxed UI Initialization: Guarantees Window is always displayed regardless of tab errors."""
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        # 1. Header Bar
        try:
            self.header = TropicalHeader()
            self.header.url_submitted.connect(self.on_url_submitted)
            self.header.open_about.connect(self.on_open_about)
            main_layout.addWidget(self.header)
        except Exception as e:
            print(f"[Main] Header init warning: {e}")

        # 2. Main Tabs System
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Safe Tab Adder Helper
        def safe_add_tab(widget_cls, icon_key, title, attr_name):
            try:
                instance = widget_cls()
                setattr(self, attr_name, instance)
                self.tabs.addTab(instance, get_icon(icon_key, 20), title)
                return instance
            except Exception as err:
                print(f"[Main] Error initializing {title} ({attr_name}): {err}")
                placeholder = QWidget()
                self.tabs.addTab(placeholder, get_icon("quick", 20), f"{title} (복구모드)")
                return placeholder

        # Tab 0: Quick Download
        self.tab_quick = safe_add_tab(QuickTab, "quick", "빠른 다운로드", "tab_quick")
        if hasattr(self.tab_quick, "start_download"):
            self.tab_quick.start_download.connect(self.start_download_job)

        # Tab 1: Format Inspector
        self.tab_inspector = safe_add_tab(InspectorTab, "inspector", "상세 포맷 분석", "tab_inspector")
        if hasattr(self.tab_inspector, "start_custom_download"):
            self.tab_inspector.start_custom_download.connect(self.start_download_job)

        # Tab 2: Playlist Batch
        self.tab_playlist = safe_add_tab(PlaylistTab, "playlist", "플레이리스트", "tab_playlist")
        if hasattr(self.tab_playlist, "start_playlist_download"):
            self.tab_playlist.start_playlist_download.connect(self.start_download_job)

        # Tab 3: In-App Player & Subtitle/JSON Editor (NEW!)
        self.tab_player = safe_add_tab(PlayerTab, "quick", "🎬 플레이어 & 에디터", "tab_player")

        # Tab 4: Advanced Options
        self.tab_advanced = safe_add_tab(AdvancedTab, "advanced", "고급 yt-dlp 옵션", "tab_advanced")

        # Tab 5: Program Preferences & Settings
        self.tab_settings = safe_add_tab(SettingsTab, "advanced", "⚙️ 설정", "tab_settings")

        # Tab 6: Queue & Progress
        self.tab_queue = safe_add_tab(QueueTab, "queue", "진행상황 큐", "tab_queue")
        if hasattr(self.tab_queue, "cancel_task_signal"):
            self.tab_queue.cancel_task_signal.connect(self.cancel_download_job)

        # Tab 7: History & Debug Logs
        self.tab_history = safe_add_tab(HistoryTab, "history", "기록 & 디버그 로그", "tab_history")

        main_layout.addWidget(self.tabs, stretch=1)
        self.setCentralWidget(central_widget)

        # 3. Status Bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("🌴 트로피컬 다운로더 준비 완료. URL을 입력하세요.")
        self.setStatusBar(self.status_bar)

    def open_in_player(self, file_path: str):
        """Focus on Player Tab and load the file."""
        if hasattr(self, 'tab_player') and isinstance(self.tab_player, PlayerTab):
            self.tabs.setCurrentWidget(self.tab_player)
            self.tab_player.load_file(file_path)

    def on_url_submitted(self, url: str):
        self.status_bar.showMessage(f"미디어 분석 시작: {url}")
        
        # Trigger quick tab analyze
        if hasattr(self.tab_quick, "analyze_url"):
            self.tab_quick.analyze_url(url)
            
            # Connect info fetcher finished signal to populate inspector and playlist tabs
            if hasattr(self.tab_quick, "info_worker") and self.tab_quick.info_worker:
                self.tab_quick.info_worker.finished_info.connect(self.on_info_fetched)

    def on_info_fetched(self, info: dict):
        if info.get("is_playlist"):
            if hasattr(self.tab_playlist, "populate_playlist"):
                self.tab_playlist.populate_playlist(info)
                self.tabs.setCurrentWidget(self.tab_playlist)
                self.status_bar.showMessage("플레이리스트 분석 완료. 원하는 항목을 선택하세요.")
        else:
            if hasattr(self.tab_inspector, "populate_info"):
                self.tab_inspector.populate_info(info)
                self.status_bar.showMessage(f"미디어 분석 완료: [{info.get('title')}]")

    def start_download_job(self, params: dict):
        url = params.get("url")
        if not url:
            QMessageBox.warning(self, "경고", "다운로드할 URL이 없습니다.")
            return

        task_id = f"task_{uuid.uuid4().hex[:6]}"
        title = (getattr(self.tab_quick, "current_info", {}) or {}).get("title", url)

        adv_opts = {}
        try:
            if hasattr(self.tab_advanced, "get_ydl_opts"):
                adv_opts = self.tab_advanced.get_ydl_opts()
        except Exception:
            pass
        params["_adv_opts"] = adv_opts

        custom_args = ""
        try:
            if hasattr(self.tab_advanced, "get_custom_args"):
                custom_args = self.tab_advanced.get_custom_args()
        except Exception:
            pass

        worker = DownloadWorker(task_id=task_id, url=url,
                                options_override=params, custom_args=custom_args)
        self.active_workers[task_id] = worker

        if hasattr(self.tab_queue, "add_task"):
            self.tab_queue.add_task(task_id, title, url)

        if hasattr(self.tab_queue, "update_progress"):
            worker.progress_signal.connect(self.tab_queue.update_progress)
        if hasattr(self.tab_history, "append_log"):
            worker.log_signal.connect(self.tab_history.append_log)
        
        worker.finished_signal.connect(self.on_worker_finished)
        worker.error_signal.connect(self.on_worker_error)
        worker.disk_space_required_signal.connect(self.on_disk_space_required)

        worker.start()
        self.tabs.setCurrentWidget(self.tab_queue)
        self.status_bar.showMessage(f"다운로드 시작: {title}")

    def on_disk_space_required(self, task_id: str, dl_dir: str, req_bytes: int):
        dlg = DiskSpaceDialog(dl_dir, req_bytes, self)
        self.disk_dialogs[task_id] = dlg
        dlg.accepted.connect(lambda: self._on_disk_dialog_resolved(task_id))
        dlg.show()

    def _on_disk_dialog_resolved(self, task_id: str):
        if task_id in self.active_workers:
            self.active_workers[task_id].notify_space_freed()

    def on_worker_finished(self, task_id: str, file_path: str, title: str):
        if hasattr(self.tab_queue, "on_task_finished"):
            self.tab_queue.on_task_finished(task_id, file_path, title)
        if hasattr(self.tab_history, "reload_history"):
            self.tab_history.reload_history()
        
        # Refresh File Explorer in Player Tab
        if hasattr(self.tab_player, "refresh_file_list"):
            self.tab_player.refresh_file_list()

        self.status_bar.showMessage(f"다운로드 완료: {title}")
        if task_id in self.active_workers:
            del self.active_workers[task_id]
        if task_id in self.disk_dialogs:
            del self.disk_dialogs[task_id]

    def on_worker_error(self, task_id: str, err_msg: str):
        if hasattr(self.tab_queue, "on_task_error"):
            self.tab_queue.on_task_error(task_id, err_msg)
        self.status_bar.showMessage(f"다운로드 오류: {err_msg}")
        if task_id in self.active_workers:
            del self.active_workers[task_id]
        if task_id in self.disk_dialogs:
            del self.disk_dialogs[task_id]

    def cancel_download_job(self, task_id: str):
        if task_id in self.active_workers:
            self.active_workers[task_id].cancel()
            self.status_bar.showMessage(f"다운로드 취소 요청됨: [{task_id}]")

    def on_open_about(self):
        self._about_dlg = AboutDialog(self)
        self._about_dlg.show()


def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    
    app = QApplication(sys.argv)
    app.setWindowIcon(get_app_icon())

    # Apply saved theme (Default is "system" mode)
    try:
        theme_mode = config_manager.get("theme_mode", "system")
        apply_theme(app, theme_mode)
    except Exception as e:
        print(f"[Main] Theme application warning: {e}")

    try:
        splash = TropicalSplashScreen()
        splash.show()
        splash.set_progress(25, "Frutiger Aero 테마 및 샌드박스 엔진 초기화 중...")
        app.processEvents()
    except Exception as e:
        print(f"[Main] Splash init warning: {e}")
        splash = None

    # Guaranteed Window Instantiation
    window = TropicalMainWindow()

    def step2():
        if splash:
            splash.set_progress(60, "yt-dlp 백엔드 및 인앱 플레이어 연결 중...")
            app.processEvents()
        QTimer.singleShot(200, step3)

    def step3():
        if splash:
            splash.set_progress(100, "준비 완료! 메인 UI 실행 중...")
            app.processEvents()
        QTimer.singleShot(200, finish_splash)

    def finish_splash():
        window.show()
        if splash:
            splash.finish(window)

    QTimer.singleShot(200, step2)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

