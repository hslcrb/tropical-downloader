"""
Tropical Downloader - Icon Provider
Icon palette based on official logo: Sky Blue (#38BDF8 → #0284C7), Amber Sun (#F59E0B)
All inline SVG — no emoji, no external resources.
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
    """Returns application QIcon preferring ICO, then PNG"""
    if os.path.exists(ICO_PATH):
        return QIcon(ICO_PATH)
    if os.path.exists(PNG_PATH):
        return QIcon(PNG_PATH)
    return get_icon("logo")

def get_app_pixmap(width: int = 64, height: int = 64) -> QPixmap:
    """Returns high-res QPixmap of the app logo"""
    if os.path.exists(PNG_PATH):
        pm = QPixmap(PNG_PATH)
        return pm.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
    return get_pixmap("logo", width, height)


# ─── Inline SVG icon library ────────────────────────────────────────────────
# Palette:
#   Primary blue  : #0284C7 / #38BDF8
#   Accent amber  : #F59E0B
#   Neutral slate : #475569 / #94A3B8
#   White         : #FFFFFF
# ────────────────────────────────────────────────────────────────────────────

SVG_ICONS: dict[str, str] = {

    # ── Fallback logo (matches the real icon style) ──────────────────────────
    "logo": """
    <svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bg" x1="0" y1="0" x2="0" y2="64" gradientUnits="userSpaceOnUse">
          <stop offset="0%" stop-color="#38BDF8"/>
          <stop offset="100%" stop-color="#0284C7"/>
        </linearGradient>
      </defs>
      <rect width="64" height="64" rx="16" fill="url(#bg)"/>
      <!-- sun -->
      <circle cx="47" cy="17" r="8" fill="#F59E0B"/>
      <!-- download arrow -->
      <path d="M32 16 V36 M24 28 L32 37 L40 28" stroke="#FFFFFF" stroke-width="5"
            stroke-linecap="round" stroke-linejoin="round" fill="none"/>
      <!-- bottom bar -->
      <line x1="20" y1="46" x2="44" y2="46" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>
    </svg>
    """,

    # ── Tab: Quick download ──────────────────────────────────────────────────
    "quick": """
    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <path d="M12 3 V15 M6 9 L12 16 L18 9" stroke="#0284C7" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="5" y1="20" x2="19" y2="20" stroke="#0284C7" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    """,

    # ── Tab: Format inspector ────────────────────────────────────────────────
    "inspector": """
    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <circle cx="10.5" cy="10.5" r="6.5" stroke="#0284C7" stroke-width="2"/>
      <line x1="15.5" y1="15.5" x2="21" y2="21" stroke="#0284C7" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="8" y1="10.5" x2="13" y2="10.5" stroke="#F59E0B" stroke-width="1.5" stroke-linecap="round"/>
      <line x1="10.5" y1="8" x2="10.5" y2="13" stroke="#F59E0B" stroke-width="1.5" stroke-linecap="round"/>
    </svg>
    """,

    # ── Tab: Playlist ────────────────────────────────────────────────────────
    "playlist": """
    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <line x1="3" y1="6"  x2="21" y2="6"  stroke="#0284C7" stroke-width="2" stroke-linecap="round"/>
      <line x1="3" y1="12" x2="16" y2="12" stroke="#0284C7" stroke-width="2" stroke-linecap="round"/>
      <line x1="3" y1="18" x2="12" y2="18" stroke="#0284C7" stroke-width="2" stroke-linecap="round"/>
      <polygon points="18,10 23,13 18,16" fill="#F59E0B"/>
    </svg>
    """,

    # ── Tab: Advanced / settings ─────────────────────────────────────────────
    "advanced": """
    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <circle cx="12" cy="12" r="3" stroke="#0284C7" stroke-width="2"/>
      <path d="M19.07 4.93a10 10 0 0 1 0 14.14M4.93 4.93a10 10 0 0 0 0 14.14"
            stroke="#0284C7" stroke-width="2" stroke-linecap="round" opacity="0.4"/>
      <path d="M15.54 8.46a5 5 0 0 1 0 7.07M8.46 8.46a5 5 0 0 0 0 7.07"
            stroke="#0284C7" stroke-width="2" stroke-linecap="round"/>
    </svg>
    """,

    # ── Tab: Download queue ──────────────────────────────────────────────────
    "queue": """
    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <rect x="3" y="3"  width="8" height="8" rx="2" stroke="#0284C7" stroke-width="1.8"/>
      <rect x="13" y="3" width="8" height="8" rx="2" stroke="#0284C7" stroke-width="1.8"/>
      <rect x="3" y="13" width="8" height="8" rx="2" stroke="#0284C7" stroke-width="1.8"/>
      <rect x="13" y="13" width="8" height="8" rx="2" fill="#F59E0B" stroke="#F59E0B" stroke-width="1.8" opacity="0.8"/>
    </svg>
    """,

    # ── Tab: History ─────────────────────────────────────────────────────────
    "history": """
    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <path d="M3 12A9 9 0 1 0 12 3" stroke="#0284C7" stroke-width="2" stroke-linecap="round"/>
      <path d="M3 3 V12 H12" stroke="#0284C7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="12" y1="7" x2="12" y2="12" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
      <line x1="12" y1="12" x2="15" y2="15" stroke="#F59E0B" stroke-width="2" stroke-linecap="round"/>
    </svg>
    """,

    # ── Action icons ─────────────────────────────────────────────────────────
    "download": """
    <svg width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <path d="M12 3 V15 M6 9 L12 16 L18 9" stroke="#FFFFFF" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="4" y1="20" x2="20" y2="20" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    """,

    "download_blue": """
    <svg width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <path d="M12 3 V15 M6 9 L12 16 L18 9" stroke="#0284C7" stroke-width="2.5"
            stroke-linecap="round" stroke-linejoin="round"/>
      <line x1="4" y1="20" x2="20" y2="20" stroke="#0284C7" stroke-width="2.5" stroke-linecap="round"/>
    </svg>
    """,

    "paste": """
    <svg width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <rect x="9" y="2" width="6" height="4" rx="1" fill="#F59E0B"/>
      <path d="M8 2H6A2 2 0 0 0 4 4V20A2 2 0 0 0 6 22H18A2 2 0 0 0 20 20V4A2 2 0 0 0 18 2H16"
            stroke="#475569" stroke-width="2" stroke-linecap="round"/>
    </svg>
    """,

    "folder": """
    <svg width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <path d="M3 7A2 2 0 0 1 5 5H9.586A1 1 0 0 1 10.293 5.293L11.707 6.707A1 1 0 0 0 12.414 7H19A2 2 0 0 1 21 9V18A2 2 0 0 1 19 20H5A2 2 0 0 1 3 18V7Z"
            fill="#FDE68A" stroke="#F59E0B" stroke-width="1.5"/>
    </svg>
    """,

    "play": """
    <svg width="16" height="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <polygon points="6,3 21,12 6,21" fill="#0284C7"/>
    </svg>
    """,

    "stop": """
    <svg width="16" height="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <rect x="4" y="4" width="16" height="16" rx="2" fill="#EF4444"/>
    </svg>
    """,

    "trash": """
    <svg width="16" height="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <polyline points="3,6 5,6 21,6" stroke="#94A3B8" stroke-width="2" stroke-linecap="round"/>
      <path d="M19 6L18 20A2 2 0 0 1 16 22H8A2 2 0 0 1 6 20L5 6"
            stroke="#94A3B8" stroke-width="2" stroke-linecap="round"/>
      <path d="M10 11V17M14 11V17M9 6V4A1 1 0 0 1 10 3H14A1 1 0 0 1 15 4V6"
            stroke="#94A3B8" stroke-width="2" stroke-linecap="round"/>
    </svg>
    """,

    "info": """
    <svg width="20" height="20" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <circle cx="12" cy="12" r="9" stroke="#0284C7" stroke-width="2"/>
      <line x1="12" y1="11" x2="12" y2="17" stroke="#0284C7" stroke-width="2.5" stroke-linecap="round"/>
      <circle cx="12" cy="7.5" r="1.2" fill="#0284C7"/>
    </svg>
    """,

    "check": """
    <svg width="18" height="18" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <polyline points="20,6 9,17 4,12" stroke="#FFFFFF" stroke-width="2.5"
                stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
    """,

    "pause": """
    <svg width="16" height="16" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
      <rect x="6" y="4" width="4" height="16" rx="1" fill="#F59E0B"/>
      <rect x="14" y="4" width="4" height="16" rx="1" fill="#F59E0B"/>
    </svg>
    """,
}


def _svg_to_pixmap(svg_data: str, width: int, height: int) -> QPixmap:
    renderer = QSvgRenderer(QByteArray(svg_data.encode("utf-8")))
    pixmap = QPixmap(QSize(width, height))
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return pixmap


def get_icon(name: str, size: int = 20) -> QIcon:
    """Returns a QIcon from inline SVG template."""
    svg = SVG_ICONS.get(name, SVG_ICONS["logo"])
    return QIcon(_svg_to_pixmap(svg, size, size))


def get_pixmap(name: str, width: int = 48, height: int = 48) -> QPixmap:
    """Returns a QPixmap from inline SVG template."""
    svg = SVG_ICONS.get(name, SVG_ICONS["logo"])
    return _svg_to_pixmap(svg, width, height)
