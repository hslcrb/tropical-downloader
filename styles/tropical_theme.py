"""
Tropical Downloader - Modern Refined Design System
Inspired by official logo palette (#FF512F Sunset, #DD2476 Coral, #3B82F6 Electric Blue)
Clean, elegant, no distorted fonts, no garish over-styling.
"""

TROPICAL_QSS = """
/* ===================================================================
   TROPICAL DOWNLOADER - MODERN SLEEK STYLESHEET
   =================================================================== */

* {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', sans-serif;
    font-size: 13px;
    outline: none;
}

QMainWindow, QDialog {
    background-color: #F8FAFC;
    color: #0F172A;
}

QWidget {
    color: #0F172A;
}

/* -------------------------------------------------------------------
   CONTAINERS & CARDS
   ------------------------------------------------------------------- */
QFrame#glass_card, QWidget#glass_card {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
}

QFrame#hero_card {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #FFFFFF, stop:1 #F1F5F9);
    border: 1px solid #CBD5E1;
    border-radius: 14px;
}

QGroupBox {
    font-weight: 700;
    font-size: 13px;
    color: #1E293B;
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    margin-top: 14px;
    padding: 20px 14px 14px 14px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 14px;
    padding: 0 8px;
    background-color: #FFFFFF;
    color: #2563EB;
}

/* -------------------------------------------------------------------
   LINE EDIT & INPUTS
   ------------------------------------------------------------------- */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 12px;
    color: #0F172A;
    font-size: 13px;
    selection-background-color: #3B82F6;
    selection-color: #FFFFFF;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 1.5px solid #2563EB;
    background-color: #FFFFFF;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border: none;
    background: transparent;
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    selection-background-color: #EFF6FF;
    selection-color: #2563EB;
    padding: 4px;
}

/* -------------------------------------------------------------------
   RADIO BUTTONS & CHECKBOXES (NO TEXT DISTORTION)
   ------------------------------------------------------------------- */
QRadioButton, QCheckBox {
    spacing: 8px;
    font-size: 13px;
    font-weight: 500;
    color: #1E293B;
    background: transparent;
    padding: 4px 0px;
}

QRadioButton::indicator, QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 4px;
}

QRadioButton::indicator {
    border-radius: 9px;
    border: 2px solid #94A3B8;
    background-color: #FFFFFF;
}

QRadioButton::indicator:checked {
    border: 2px solid #2563EB;
    background-color: #2563EB;
}

QCheckBox::indicator {
    border: 1.5px solid #94A3B8;
    background-color: #FFFFFF;
    border-radius: 4px;
}

QCheckBox::indicator:checked {
    border: 1.5px solid #2563EB;
    background-color: #2563EB;
}

/* -------------------------------------------------------------------
   BUTTONS (CLEAN MODERN GRADIENTS & SOLIDS)
   ------------------------------------------------------------------- */
QPushButton {
    background-color: #FFFFFF;
    color: #334155;
    font-weight: 600;
    font-size: 13px;
    border: 1px solid #CBD5E1;
    border-radius: 8px;
    padding: 8px 16px;
    min-height: 20px;
}

QPushButton:hover {
    background-color: #F8FAFC;
    border-color: #94A3B8;
    color: #0F172A;
}

QPushButton:pressed {
    background-color: #F1F5F9;
}

QPushButton:disabled {
    background-color: #F1F5F9;
    color: #94A3B8;
    border-color: #E2E8F0;
}

/* Primary Sunset Button */
QPushButton#btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #FF512F, stop:0.5 #DD2476, stop:1 #3B82F6);
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
}

QPushButton#btn_primary:hover {
    opacity: 0.92;
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #FF6142, stop:0.5 #E03583, stop:1 #4B8BF8);
}

QPushButton#btn_primary:pressed {
    opacity: 0.98;
}

/* Accent Blue Button */
QPushButton#btn_accent {
    background-color: #2563EB;
    color: #FFFFFF;
    font-weight: 600;
    border: none;
    border-radius: 8px;
}

QPushButton#btn_accent:hover {
    background-color: #1D4ED8;
}

/* Danger Button */
QPushButton#btn_danger {
    background-color: #EF4444;
    color: #FFFFFF;
    border: none;
}

QPushButton#btn_danger:hover {
    background-color: #DC2626;
}

/* -------------------------------------------------------------------
   TABS SYSTEM
   ------------------------------------------------------------------- */
QTabWidget::pane {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 12px;
    padding: 12px;
    top: -1px;
}

QTabBar::tab {
    background-color: transparent;
    color: #64748B;
    font-weight: 600;
    border: none;
    border-bottom: 2px solid transparent;
    padding: 10px 18px;
    margin-right: 8px;
}

QTabBar::tab:selected {
    color: #2563EB;
    border-bottom: 2.5px solid #2563EB;
    font-weight: 700;
}

QTabBar::tab:hover:!selected {
    color: #334155;
}

/* -------------------------------------------------------------------
   PROGRESS BAR
   ------------------------------------------------------------------- */
QProgressBar {
    border: 1px solid #E2E8F0;
    border-radius: 6px;
    background-color: #F1F5F9;
    text-align: center;
    color: #0F172A;
    font-weight: 600;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #FF512F, stop:0.5 #DD2476, stop:1 #3B82F6);
    border-radius: 5px;
}

/* -------------------------------------------------------------------
   TABLE & LOG CONSOLE
   ------------------------------------------------------------------- */
QTableWidget {
    background-color: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 8px;
    gridline-color: #F1F5F9;
    selection-background-color: #EFF6FF;
    selection-color: #1E40AF;
}

QHeaderView::section {
    background-color: #F8FAFC;
    color: #475569;
    font-weight: 700;
    padding: 8px;
    border: none;
    border-bottom: 1px solid #E2E8F0;
    border-right: 1px solid #F1F5F9;
}

QStatusBar {
    background-color: #FFFFFF;
    color: #475569;
    border-top: 1px solid #E2E8F0;
    font-weight: 500;
}
"""

def apply_theme(app):
    """Applies the refined modern theme to QApplication"""
    app.setStyleSheet(TROPICAL_QSS)
