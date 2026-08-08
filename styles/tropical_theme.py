"""
Tropical Downloader - Design System
Brand palette: Sky (#38BDF8 · #0EA5E9 · #0284C7), Amber accent (#F59E0B), Slate neutrals.
"""

TROPICAL_QSS = """
/* ── Global reset ─────────────────────────────────────────────── */
* {
    font-family: 'Segoe UI', 'Malgun Gothic', 'Apple SD Gothic Neo', sans-serif;
    color: #0F172A;
}

QMainWindow, QDialog {
    background-color: #F0F9FF;
}

/* ── Panels ─────────────────────────────────────────────────────── */
QFrame#glass_card {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 12px;
}

QFrame#hero_card {
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

/* ── Inputs ─────────────────────────────────────────────────────── */
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
QComboBox::drop-down {
    border: none;
    width: 28px;
    background: transparent;
}
QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 8px;
    selection-background-color: #E0F2FE;
    selection-color: #0284C7;
    padding: 4px;
    outline: none;
}

/* ── Radio & Check  ─────────────────────────────────────────────
   KEY FIX: no min-height / height constraint on the row itself;
   indicator is sized explicitly but NOT applied to the text line-height.
   ─────────────────────────────────────────────────────────────── */
QRadioButton {
    spacing: 10px;
    font-size: 13px;
    font-weight: 500;
    color: #1E293B;
    background: transparent;
    padding: 3px 0;
    /* NEVER set height here — it clips descenders in Korean */
}
QRadioButton::indicator {
    width: 16px;
    height: 16px;
    border-radius: 8px;
    border: 2px solid #94A3B8;
    background-color: #FFFFFF;
}
QRadioButton::indicator:checked {
    border-color: #0EA5E9;
    background-color: #0EA5E9;
    image: url(none);   /* let Qt draw the dot via border trick */
}
QRadioButton::indicator:checked {
    background-color: #0EA5E9;
    border: 4px solid #0EA5E9;
    /* Inner white dot via outline-offset trick not available;
       use a solid accent fill — clean and readable */
    background-clip: padding-box;
}

QCheckBox {
    spacing: 10px;
    font-size: 13px;
    font-weight: 500;
    color: #1E293B;
    background: transparent;
    padding: 3px 0;
}
QCheckBox::indicator {
    width: 16px;
    height: 16px;
    border-radius: 4px;
    border: 2px solid #94A3B8;
    background-color: #FFFFFF;
}
QCheckBox::indicator:checked {
    border-color: #0EA5E9;
    background-color: #0EA5E9;
}

/* ── Buttons ────────────────────────────────────────────────────── */
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
QPushButton:disabled { color: #94A3B8; border-color: #E2E8F0; background-color: #F8FAFC; }

/* Sky primary */
QPushButton#btn_primary {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #0EA5E9, stop:1 #0284C7);
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 9px;
    padding: 9px 22px;
}
QPushButton#btn_primary:hover {
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #38BDF8, stop:1 #0EA5E9);
}
QPushButton#btn_primary:pressed {
    background: #0284C7;
}

/* Amber accent */
QPushButton#btn_accent {
    background-color: #F59E0B;
    color: #FFFFFF;
    font-weight: 700;
    border: none;
    border-radius: 8px;
    padding: 8px 18px;
}
QPushButton#btn_accent:hover { background-color: #D97706; }

/* Danger */
QPushButton#btn_danger {
    background-color: #EF4444;
    color: #FFFFFF;
    border: none;
    border-radius: 8px;
    padding: 8px 16px;
}
QPushButton#btn_danger:hover { background-color: #DC2626; }

/* Ghost (icon-only, borderless) */
QPushButton#btn_ghost {
    background: transparent;
    border: none;
    padding: 4px;
    border-radius: 6px;
}
QPushButton#btn_ghost:hover { background-color: #E0F2FE; }

/* ── Tabs ───────────────────────────────────────────────────────── */
QTabWidget::pane {
    background-color: #FFFFFF;
    border: 1px solid #BAE6FD;
    border-radius: 10px;
    top: -1px;
    padding: 12px;
}
QTabBar {
    background: transparent;
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

/* ── Progress bar ───────────────────────────────────────────────── */
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
    background: qlineargradient(x1:0,y1:0,x2:1,y2:0,
        stop:0 #38BDF8, stop:0.6 #0EA5E9, stop:1 #F59E0B);
    border-radius: 5px;
}

/* ── Tables ─────────────────────────────────────────────────────── */
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
QTableWidget::item { padding: 4px 8px; }

/* ── Scrollbars ─────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #BAE6FD;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover { background: #38BDF8; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: transparent;
    height: 8px;
    border-radius: 4px;
}
QScrollBar::handle:horizontal {
    background: #BAE6FD;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover { background: #38BDF8; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }

/* ── Status bar ─────────────────────────────────────────────────── */
QStatusBar {
    background-color: #FFFFFF;
    color: #475569;
    border-top: 1px solid #BAE6FD;
    font-size: 12px;
    font-weight: 500;
    padding: 2px 8px;
}

/* ── Tooltip ─────────────────────────────────────────────────────  */
QToolTip {
    background-color: #0F172A;
    color: #F8FAFC;
    border: none;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
}

/* ── Splitter ───────────────────────────────────────────────────── */
QSplitter::handle {
    background-color: #BAE6FD;
    border-radius: 2px;
}
QSplitter::handle:vertical { height: 4px; }
QSplitter::handle:horizontal { width: 4px; }

/* ── Text console (log) ─────────────────────────────────────────── */
QTextEdit#log_console {
    background-color: #0F172A;
    color: #38BDF8;
    border: 1px solid #1E293B;
    border-radius: 8px;
    padding: 8px;
    font-family: 'Consolas', 'Cascadia Code', 'Courier New', monospace;
    font-size: 12px;
}
"""

def apply_theme(app):
    app.setStyleSheet(TROPICAL_QSS)
