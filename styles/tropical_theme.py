"""
Tropical Downloader - Frutiger Aero x Y2K Tropical Island QSS Theme Engine
"""

TROPICAL_QSS = """
/* ===================================================================
   TROPICAL DOWNLOADER - FRUTIGER AERO Y2K DESIGN SYSTEM
   =================================================================== */

QMainWindow, QDialog {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
        stop:0 #E0F7FA, stop:0.35 #B2EBF2, stop:0.7 #80DEEA, stop:1 #4DD0E1);
    font-family: 'Segoe UI', 'SF Pro Text', 'Arial', sans-serif;
    color: #03045E;
}

QWidget {
    font-family: 'Segoe UI', 'SF Pro Text', 'Arial', sans-serif;
    font-size: 13px;
    color: #003049;
}

/* -------------------------------------------------------------------
   GLASS PANELS & CONTAINERS
   ------------------------------------------------------------------- */
QFrame#glass_card, QWidget#glass_card {
    background-color: rgba(255, 255, 255, 0.78);
    border: 1px solid rgba(255, 255, 255, 0.95);
    border-bottom: 2px solid rgba(0, 180, 216, 0.4);
    border-radius: 16px;
}

QFrame#hero_card {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.9), stop:1 rgba(224, 247, 250, 0.7));
    border: 2px solid #00E5FF;
    border-radius: 20px;
}

QGroupBox {
    font-weight: bold;
    font-size: 14px;
    color: #0077B6;
    background-color: rgba(255, 255, 255, 0.65);
    border: 1.5px solid rgba(0, 180, 216, 0.5);
    border-radius: 14px;
    margin-top: 12px;
    padding-top: 18px;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 16px;
    padding: 2px 10px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #00E5FF, stop:1 #0096C7);
    color: #FFFFFF;
    border-radius: 10px;
}

/* -------------------------------------------------------------------
   LINE EDIT & INPUTS
   ------------------------------------------------------------------- */
QLineEdit, QTextEdit, QPlainTextEdit, QSpinBox, QComboBox {
    background-color: rgba(255, 255, 255, 0.92);
    border: 2px solid #00B4D8;
    border-radius: 12px;
    padding: 8px 14px;
    color: #03045E;
    font-size: 13px;
    selection-background-color: #00E5FF;
    selection-color: #03045E;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QSpinBox:focus, QComboBox:focus {
    border: 2.5px solid #00E5FF;
    background-color: #FFFFFF;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 30px;
    border-left: 1px solid #00B4D8;
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #E0F7FA, stop:1 #80DEEA);
}

QComboBox QAbstractItemView {
    background-color: #FFFFFF;
    border: 2px solid #00B4D8;
    border-radius: 10px;
    selection-background-color: #00E5FF;
    selection-color: #03045E;
    padding: 4px;
}

/* -------------------------------------------------------------------
   AQUA GLOSS GEL BUTTONS (FRUTIGER AERO STYLED)
   ------------------------------------------------------------------- */
QPushButton {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #00E5FF, stop:0.45 #00B4D8, stop:0.5 #0096C7, stop:1 #0077B6);
    color: #FFFFFF;
    font-weight: bold;
    font-size: 13px;
    border: 1px solid #0077B6;
    border-top: 1.5px solid #E0F7FA;
    border-radius: 12px;
    padding: 8px 18px;
    min-height: 24px;
}

QPushButton:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #72EFDD, stop:0.45 #48CAE4, stop:0.5 #00B4D8, stop:1 #0096C7);
    border: 1px solid #00B4D8;
    border-top: 2px solid #FFFFFF;
}

QPushButton:pressed {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #0077B6, stop:0.5 #0096C7, stop:1 #00B4D8);
    border-top: 1px solid #005F73;
    padding-top: 10px;
    padding-bottom: 6px;
}

QPushButton:disabled {
    background: #CAE9FF;
    color: #8ECAE6;
    border: 1px solid #ADE8F4;
}

/* Accent Buttons */
QPushButton#btn_primary {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #06D6A0, stop:0.45 #05B386, stop:0.5 #049670, stop:1 #026C50);
    border: 1px solid #026C50;
    border-top: 1.5px solid #A8F5E2;
    color: #FFFFFF;
    font-size: 14px;
}

QPushButton#btn_primary:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #38EFBF, stop:0.45 #06D6A0, stop:0.5 #05B386, stop:1 #049670);
}

QPushButton#btn_accent {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFD166, stop:0.45 #FFB703, stop:0.5 #FB8500, stop:1 #D97706);
    border: 1px solid #D97706;
    border-top: 1.5px solid #FFF3C4;
    color: #03045E;
    font-weight: bold;
}

QPushButton#btn_accent:hover {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FFE699, stop:0.45 #FFD166, stop:0.5 #FFB703, stop:1 #FB8500);
}

QPushButton#btn_danger {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #FF6B6B, stop:0.45 #EE5253, stop:0.5 #FF4757, stop:1 #C82333);
    border: 1px solid #C82333;
    border-top: 1.5px solid #FFC9C9;
    color: #FFFFFF;
}

/* -------------------------------------------------------------------
   TABS SYSTEM (AERO GLASS PILLS)
   ------------------------------------------------------------------- */
QTabWidget::pane {
    background: rgba(255, 255, 255, 0.75);
    border: 2px solid rgba(255, 255, 255, 0.9);
    border-radius: 16px;
    padding: 12px;
    top: -1px;
}

QTabBar::tab {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 rgba(255, 255, 255, 0.8), stop:1 rgba(178, 235, 242, 0.6));
    color: #0077B6;
    font-weight: bold;
    border: 1px solid rgba(0, 180, 216, 0.4);
    border-top-left-radius: 12px;
    border-top-right-radius: 12px;
    padding: 10px 20px;
    margin-right: 4px;
}

QTabBar::tab:selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #00E5FF, stop:0.3 #00B4D8, stop:1 #0077B6);
    color: #FFFFFF;
    border: 1.5px solid #0077B6;
    border-bottom: none;
    border-top: 2px solid #FFFFFF;
}

QTabBar::tab:hover:!selected {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #E0F7FA, stop:1 #B2EBF2);
    color: #0096C7;
}

/* -------------------------------------------------------------------
   PROGRESS BAR (NEON OCEAN WAVE)
   ------------------------------------------------------------------- */
QProgressBar {
    border: 2px solid #00B4D8;
    border-radius: 10px;
    background-color: rgba(255, 255, 255, 0.9);
    text-align: center;
    color: #03045E;
    font-weight: bold;
}

QProgressBar::chunk {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
        stop:0 #06D6A0, stop:0.5 #00E5FF, stop:1 #FFD166);
    border-radius: 8px;
}

/* -------------------------------------------------------------------
   TABLE & TREE WIDGETS
   ------------------------------------------------------------------- */
QTableWidget, QTreeWidget, QListWidget {
    background-color: rgba(255, 255, 255, 0.9);
    border: 1.5px solid #00B4D8;
    border-radius: 12px;
    gridline-color: #E0F7FA;
    selection-background-color: #00E5FF;
    selection-color: #03045E;
}

QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
        stop:0 #00E5FF, stop:1 #0096C7);
    color: #FFFFFF;
    font-weight: bold;
    padding: 6px;
    border: none;
    border-right: 1px solid #0077B6;
}

/* -------------------------------------------------------------------
   SCROLLBAR (SMOOTH AERO GLASS)
   ------------------------------------------------------------------- */
QScrollBar:vertical {
    border: none;
    background: rgba(224, 247, 250, 0.5);
    width: 10px;
    border-radius: 5px;
}

QScrollBar::handle:vertical {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00E5FF, stop:1 #0096C7);
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #06D6A0;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* -------------------------------------------------------------------
   STATUS BAR & TOOLTIPS
   ------------------------------------------------------------------- */
QStatusBar {
    background: rgba(255, 255, 255, 0.85);
    color: #0077B6;
    border-top: 1px solid #00B4D8;
    font-weight: 500;
}

QToolTip {
    background-color: #03045E;
    color: #FFFFFF;
    border: 1px solid #00E5FF;
    border-radius: 8px;
    padding: 6px 10px;
    opacity: 230;
}
"""

def apply_theme(app):
    """Applies the Tropical Frutiger Aero theme to QApplication"""
    app.setStyleSheet(TROPICAL_QSS)
