"""
Tropical Downloader - Dynamic SVG & Native Icon Provider (Frutiger Aero / Y2K Tropical Aesthetics)
"""
import os
from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, QSize, Qt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ICO_PATH = os.path.join(BASE_DIR, "tropical-downloader.ico")
PNG_PATH = os.path.join(BASE_DIR, "tropical-downloader.png")
SVG_PATH = os.path.join(BASE_DIR, "tropical-downloader.svg")

def get_app_icon() -> QIcon:
    """Returns application QIcon from ICO, PNG, or SVG"""
    if os.path.exists(ICO_PATH):
        return QIcon(ICO_PATH)
    elif os.path.exists(PNG_PATH):
        return QIcon(PNG_PATH)
    elif os.path.exists(SVG_PATH):
        return QIcon(SVG_PATH)
    return get_icon("logo")

def get_app_pixmap(width: int = 64, height: int = 64) -> QPixmap:
    """Returns high-res QPixmap of tropical-downloader logo"""
    if os.path.exists(PNG_PATH):
        pm = QPixmap(PNG_PATH)
        return pm.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    elif os.path.exists(SVG_PATH):
        renderer = QSvgRenderer(SVG_PATH)
        pixmap = QPixmap(QSize(width, height))
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap
    return get_pixmap("logo", width, height)


# SVG Icon Templates with vibrant gradients, glossy highlights, and crisp paths
SVG_ICONS = {
    "logo": """
    <svg width="64" height="64" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bgGrad" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#00E5FF"/>
          <stop offset="50%" stop-color="#00B4D8"/>
          <stop offset="100%" stop-color="#03045E"/>
        </linearGradient>
        <linearGradient id="sunGrad" x1="0" y1="0" x2="0" y2="24" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#FFE600"/>
          <stop offset="100%" stop-color="#FF6B4A"/>
        </linearGradient>
        <linearGradient id="palmGrad" x1="0" y1="0" x2="32" y2="32" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#00FFB2"/>
          <stop offset="100%" stop-color="#06D6A0"/>
        </linearGradient>
        <linearGradient id="arrowGrad" x1="0" y1="0" x2="0" y2="20" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#FFFFFF"/>
          <stop offset="100%" stop-color="#E0F7FA"/>
        </linearGradient>
        <filter id="gloss" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="1" result="blur"/>
        </filter>
      </defs>
      <!-- Aqua Gloss Shield Background -->
      <rect x="2" y="2" width="60" height="60" rx="18" fill="url(#bgGrad)" stroke="#E0F7FA" stroke-width="1.5"/>
      <!-- Sun Shine -->
      <circle cx="46" cy="18" r="10" fill="url(#sunGrad)"/>
      <circle cx="46" cy="18" r="12" fill="#FFE600" opacity="0.25"/>
      <!-- Palm Leaf Contour -->
      <path d="M12 46C18 34 30 26 44 24C32 30 26 40 24 50C22 42 16 48 12 46Z" fill="url(#palmGrad)"/>
      <path d="M22 52C28 42 40 34 52 36C40 40 34 50 32 58C30 52 24 54 22 52Z" fill="#00C49F" opacity="0.8"/>
      <!-- Download Arrow -->
      <path d="M32 14V36M32 36L22 26M32 36L42 26" stroke="url(#arrowGrad)" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="20" y1="44" x2="44" y2="44" stroke="#FFFFFF" stroke-width="4" stroke-linecap="round"/>
      <!-- Aero Top Gloss Highlight -->
      <path d="M4 18C4 10 10 4 18 4H46C54 4 60 10 60 18C34 26 14 26 4 18Z" fill="#FFFFFF" opacity="0.35"/>
    </svg>
    """,
    
    "quick": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill="#FFE600" stroke="#FF9100" stroke-width="1.5" stroke-linejoin="round"/>
    </svg>
    """,
    
    "inspector": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="10.5" cy="10.5" r="7.5" fill="#00E5FF" opacity="0.2" stroke="#00B4D8" stroke-width="2"/>
      <path d="M16 16L21 21" stroke="#0077B6" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M8 10.5H13M10.5 8V13" stroke="#00B4D8" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    """,
    
    "playlist": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="3" y="4" width="18" height="3" rx="1.5" fill="#06D6A0"/>
      <rect x="3" y="10" width="14" height="3" rx="1.5" fill="#00B4D8"/>
      <rect x="3" y="16" width="10" height="3" rx="1.5" fill="#FF6B4A"/>
      <polygon points="17,14 22,17.5 17,21" fill="#FFE600"/>
    </svg>
    """,
    
    "advanced": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z" stroke="#7209B7" stroke-width="2"/>
      <path d="M19.4 15A1.65 1.65 0 0 0 19.73 16.82L19.79 16.88A2 2 0 0 1 16.96 19.71L16.9 19.65A1.65 1.65 0 0 0 15.08 19.32V19.4A2 2 0 0 1 11.08 19.4V19.32A1.65 1.65 0 0 0 9.26 19.65L9.2 19.71A2 2 0 0 1 6.37 16.88L6.43 16.82A1.65 1.65 0 0 0 6.76 15H6.68A2 2 0 0 1 6.68 11H6.76A1.65 1.65 0 0 0 6.43 9.18L6.37 9.12A2 2 0 0 1 9.2 6.29L9.26 6.35A1.65 1.65 0 0 0 11.08 6.68V6.6A2 2 0 0 1 15.08 6.6V6.68A1.65 1.65 0 0 0 16.9 6.35L16.96 6.29A2 2 0 0 1 19.79 9.12L19.73 9.18A1.65 1.65 0 0 0 19.4 11H19.48A2 2 0 0 1 19.48 15H19.4Z" stroke="#4361EE" stroke-width="2"/>
    </svg>
    """,
    
    "queue": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M2 12C5 8 8 16 12 12C16 8 19 16 22 12" stroke="#00E5FF" stroke-width="2.5" stroke-linecap="round"/>
      <path d="M2 17C5 13 8 21 12 17C16 13 19 21 22 17" stroke="#06D6A0" stroke-width="1.5" stroke-linecap="round" opacity="0.7"/>
    </svg>
    """,
    
    "history": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="9" stroke="#FF6B4A" stroke-width="2"/>
      <path d="M12 7V12L15.5 15.5" stroke="#FFD166" stroke-width="2" stroke-linecap="round"/>
    </svg>
    """,

    "download": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 3V15M12 15L7 10M12 15L17 10" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M4 19H20" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    """,

    "paste": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M16 4H18A2 2 0 0 1 20 6V20A2 2 0 0 1 18 22H6A2 2 0 0 1 4 20V6A2 2 0 0 1 6 4H8" stroke="#00B4D8" stroke-width="2"/>
      <rect x="8" y="2" width="8" height="4" rx="1" fill="#FFE600" stroke="#00B4D8" stroke-width="1.5"/>
    </svg>
    """,

    "folder": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 6A2 2 0 0 1 5 4H9L11 7H19A2 2 0 0 1 21 9V18A2 2 0 0 1 19 20H5A2 2 0 0 1 3 18V6Z" fill="#FFD166" stroke="#F4A261" stroke-width="1.5"/>
    </svg>
    """,

    "play": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <polygon points="6,4 20,12 6,20" fill="#06D6A0" stroke="#04A777" stroke-width="1.5"/>
    </svg>
    """,

    "pause": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="6" y="4" width="4" height="16" rx="1" fill="#FFD166"/>
      <rect x="14" y="4" width="4" height="16" rx="1" fill="#FFD166"/>
    </svg>
    """,

    "stop": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect x="5" y="5" width="14" height="14" rx="2" fill="#FF6B4A"/>
    </svg>
    """,

    "trash": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3 6H21M19 6V20A2 2 0 0 1 17 22H7A2 2 0 0 1 5 20V6M8 6V4A2 2 0 0 1 10 2H14A2 2 0 0 1 16 4V6" stroke="#EF476F" stroke-width="2" stroke-linecap="round"/>
    </svg>
    """,

    "info": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <circle cx="12" cy="12" r="9" fill="#00E5FF" opacity="0.2" stroke="#00B4D8" stroke-width="2"/>
      <line x1="12" y1="11" x2="12" y2="17" stroke="#0077B6" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="12" cy="7.5" r="1.25" fill="#0077B6"/>
    </svg>
    """,

    "check": """
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M20 6L9 17L4 12" stroke="#06D6A0" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """
}

def get_icon(name: str, size: int = 24) -> QIcon:
    """Returns a QIcon generated from SVG template"""
    svg_data = SVG_ICONS.get(name, SVG_ICONS["logo"])
    renderer = QSvgRenderer(QByteArray(svg_data.encode('utf-8')))
    pixmap = QPixmap(QSize(size, size))
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)

def get_pixmap(name: str, width: int = 48, height: int = 48) -> QPixmap:
    """Returns a QPixmap from SVG template"""
    svg_data = SVG_ICONS.get(name, SVG_ICONS["logo"])
    renderer = QSvgRenderer(QByteArray(svg_data.encode('utf-8')))
    pixmap = QPixmap(QSize(width, height))
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return pixmap
