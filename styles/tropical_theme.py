"""
Tropical Downloader - Design System & Theme Engine
Supports Light Mode, Dark Mode (Tropical Night), and Auto System Theme Detection.
"""
import sys
import os
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt

def is_system_dark_mode() -> bool:
    """Detects if system theme is set to dark mode (Windows winreg & Qt styleHints fallback)"""
    # 1. Try Windows Registry for precise Windows 10/11 system dark mode check
    if sys.platform == "win32":
        try:
            import winreg
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
            )
            val, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
            winreg.CloseKey(key)
            return val == 0
        except Exception:
            pass

    # 2. Qt 6 Cross-Platform Fallback
    try:
        app = QGuiApplication.instance()
        if app and hasattr(app, "styleHints"):
            return app.styleHints().colorScheme() == Qt.ColorScheme.Dark
    except Exception:
        pass

    return False


# ── TROPICAL LIGHT THEME ───────────────────────────────────────────────────
LIGHT_QSS = """
* {
    font-family: 'Segoe UI', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    color: #0F172A;
}

QMainWindow, QDialog {
    background-color: #F0F9FF;
}

QFrame#glass_card, QFrame#hero_card {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 12px;
}

QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    margin-top: 22px;
    padding: 12px 14px 10px 14px;
    font-weight: 700;
    font-size: 12px;
    color: #0369A1;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 2px 8px;
    background-color: #E0F2FE;
    border-radius: 6px;
    color: #0369A1;
    font-weight: 700;
    font-size: 12px;
}

QLineEdit, QPlainTextEdit, QSpinBox {
    background-color: #FFFFFF;
    border: 1.5px solid #BAE6FD;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0F172A;
    font-size: 13px;
    selection-background-color: #38BDF8;
    selection-color: #FFFFFF;
}
QLineEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {
    border-color: #0EA5E9;
}

QComboBox {
    background-color: #FFFFFF;
    border: 1.5px solid #BAE6FD;
    border-radius: 8px;
    padding: 7px 32px 7px 12px;
    color: #0F172A;
    font-size: 13px;
}
QComboBox:focus { border-color: #0EA5E9; }
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 8px;
    selection-background-color: #E0F2FE;
    selection-color: #0284C7;
    padding: 4px;
    outline: none;
}

QRadioButton, QCheckBox {
    spacing: 10px;
    font-size: 13px;
    font-weight: 500;
    color: #1E293B;
    background: transparent;
    padding: 3px 0;
}
QRadioButton::indicator, QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 2px solid #94A3B8;
    background-color: #FFFFFF;
}
QRadioButton::indicator { border-radius: 8px; }
QRadioButton::indicator:checked, QCheckBox::indicator:checked {
    border-color: #0EA5E9;
    background-color: #0EA5E9;
}

QPushButton {
    background-color: #FFFFFF;
    color: #0F172A;
    font-weight: 600;
    font-size: 13px;
    border: 1.5px solid #BAE6FD;
    border-radius: 8px;
    padding: 7px 16px;
}
QPushButton:hover {
    background-color: #E0F2FE;
    border-color: #38BDF8;
}
QPushButton:pressed { background-color: #BAE6FD; }

QPushButton#btn_primary {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0EA5E9, stop:1 #0284C7);
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 9px;
    padding: 9px 22px;
}
QPushButton#btn_primary:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #38BDF8, stop:1 #0EA5E9);
}

QPushButton#btn_accent {
    background-color: #F59E0B;
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
}
QPushButton#btn_accent:hover { background-color: #D97706; }

QPushButton#btn_ghost {
    background: transparent;
    border: none;
    padding: 4px;
    border-radius: 6px;
}
QPushButton#btn_ghost:hover { background-color: #E0F2FE; }

QTabWidget::pane {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    top: -1px;
    padding: 12px;
}
QTabBar::tab {
    background: transparent;
    color: #64748B;
    font-weight: 600;
    font-size: 13px;
    border: none;
    border-bottom: 2.5px solid transparent;
    padding: 9px 16px 8px 16px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    color: #0284C7;
    border-bottom-color: #0284C7;
    font-weight: 700;
}
QTabBar::tab:hover:!selected {
    color: #0EA5E9;
    background-color: #F0F9FF;
    border-radius: 8px 8px 0 0;
}

QProgressBar {
    border: 1px solid #BAE6FD;
    border-radius: 6px;
    background-color: #F0F9FF;
    text-align: center;
    color: #0F172A;
    font-weight: 600;
    font-size: 11px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #38BDF8, stop:0.6 #0EA5E9, stop:1 #F59E0B);
    border-radius: 5px;
}

QTableWidget, QTreeWidget {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 8px;
    gridline-color: #F0F9FF;
    selection-background-color: #E0F2FE;
    selection-color: #0284C7;
    outline: none;
}
QHeaderView::section {
    background-color: #F0F9FF;
    color: #0369A1;
    font-weight: 700;
    font-size: 12px;
    padding: 8px;
    border: none;
    border-bottom: 1.5px solid #BAE6FD;
}

QScrollBar:vertical { background: transparent; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #BAE6FD; border-radius: 4px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #38BDF8; }

QStatusBar {
    background-color: #FFFFFF;
    color: #475569;
    border-top: 1px solid #BAE6FD;
    font-size: 12px;
    font-weight: 500;
    padding: 2px 8px;
}
"""


# ── TROPICAL DARK THEME (Deep Ocean Night) ─────────────────────────────────
DARK_QSS = """
* {
    font-family: 'Segoe UI', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    color: #F1F5F9;
}

QMainWindow, QDialog {
    background-color: #0B132B;
}

QFrame#glass_card, QFrame#hero_card {
    background-color: #1C2541;
    border: 1px solid #334155;
    border-radius: 12px;
}

QGroupBox {
    background-color: #1C2541;
    border: 1px solid #334155;
    border-radius: 10px;
    margin-top: 22px;
    padding: 12px 14px 10px 14px;
    font-weight: 700;
    font-size: 12px;
    color: #38BDF8;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 2px 8px;
    background-color: #0F172A;
    border-radius: 6px;
    color: #38BDF8;
    font-weight: 700;
    font-size: 12px;
}

QLineEdit, QPlainTextEdit, QSpinBox {
    background-color: #0F172A;
    border: 1.5px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    color: #F8FAFC;
    font-size: 13px;
    selection-background-color: #0EA5E9;
    selection-color: #FFFFFF;
}
QLineEdit:focus, QPlainTextEdit:focus, QSpinBox:focus {
    border-color: #38BDF8;
}

QComboBox {
    background-color: #0F172A;
    border: 1.5px solid #334155;
    border-radius: 8px;
    padding: 7px 32px 7px 12px;
    color: #F8FAFC;
    font-size: 13px;
}
QComboBox:focus { border-color: #38BDF8; }
QComboBox QAbstractItemView {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
    selection-background-color: #1E293B;
    selection-color: #38BDF8;
    padding: 4px;
    outline: none;
}

QRadioButton, QCheckBox {
    spacing: 10px;
    font-size: 13px;
    font-weight: 500;
    color: #E2E8F0;
    background: transparent;
    padding: 3px 0;
}
QRadioButton::indicator, QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 2px solid #64748B;
    background-color: #0F172A;
}
QRadioButton::indicator { border-radius: 8px; }
QRadioButton::indicator:checked, QCheckBox::indicator:checked {
    border-color: #38BDF8;
    background-color: #38BDF8;
}

QPushButton {
    background-color: #1E293B;
    color: #F8FAFC;
    font-weight: 600;
    font-size: 13px;
    border: 1.5px solid #334155;
    border-radius: 8px;
    padding: 7px 16px;
}
QPushButton:hover {
    background-color: #334155;
    border-color: #38BDF8;
}
QPushButton:pressed { background-color: #0F172A; }

QPushButton#btn_primary {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0284C7, stop:1 #0EA5E9);
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 9px;
    padding: 9px 22px;
}
QPushButton#btn_primary:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0EA5E9, stop:1 #38BDF8);
}

QPushButton#btn_accent {
    background-color: #D97706;
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
}
QPushButton#btn_accent:hover { background-color: #F59E0B; }

QPushButton#btn_ghost {
    background: transparent;
    border: none;
    padding: 4px;
    border-radius: 6px;
}
QPushButton#btn_ghost:hover { background-color: #1E293B; }

QTabWidget::pane {
    background-color: #1C2541;
    border: 1px solid #334155;
    border-radius: 10px;
    top: -1px;
    padding: 12px;
}
QTabBar::tab {
    background: transparent;
    color: #94A3B8;
    font-weight: 600;
    font-size: 13px;
    border: none;
    border-bottom: 2.5px solid transparent;
    padding: 9px 16px 8px 16px;
    margin-right: 4px;
}
QTabBar::tab:selected {
    color: #38BDF8;
    border-bottom-color: #38BDF8;
    font-weight: 700;
}
QTabBar::tab:hover:!selected {
    color: #7DD3FC;
    background-color: #0F172A;
    border-radius: 8px 8px 0 0;
}

QProgressBar {
    border: 1px solid #334155;
    border-radius: 6px;
    background-color: #0F172A;
    text-align: center;
    color: #F8FAFC;
    font-weight: 600;
    font-size: 11px;
}
QProgressBar::chunk {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #0284C7, stop:0.6 #38BDF8, stop:1 #F59E0B);
    border-radius: 5px;
}

QTableWidget, QTreeWidget {
    background-color: #0F172A;
    border: 1px solid #334155;
    border-radius: 8px;
    gridline-color: #1E293B;
    selection-background-color: #1E293B;
    selection-color: #38BDF8;
    outline: none;
}
QHeaderView::section {
    background-color: #1E293B;
    color: #38BDF8;
    font-weight: 700;
    font-size: 12px;
    padding: 8px;
    border: none;
    border-bottom: 1.5px solid #334155;
}

QScrollBar:vertical { background: transparent; width: 8px; border-radius: 4px; }
QScrollBar::handle:vertical { background: #334155; border-radius: 4px; min-height: 24px; }
QScrollBar::handle:vertical:hover { background: #38BDF8; }

QStatusBar {
    background-color: #1C2541;
    color: #94A3B8;
    border-top: 1px solid #334155;
    font-size: 12px;
    font-weight: 500;
    padding: 2px 8px;
}
"""

def get_theme_qss(theme_mode: str = "system") -> str:
    """Returns QSS string for 'system', 'light', or 'dark'"""
    if theme_mode == "dark":
        return DARK_QSS
    elif theme_mode == "light":
        return LIGHT_QSS
    else:
        # System theme mode
        return DARK_QSS if is_system_dark_mode() else LIGHT_QSS

def apply_theme(app, theme_mode: str = "system"):
    """Applies stylesheet to QApplication instance"""
    if app:
        qss = get_theme_qss(theme_mode)
        app.setStyleSheet(qss)
