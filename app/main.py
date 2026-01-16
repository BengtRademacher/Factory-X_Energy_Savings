"""Hauptmodul für die Factory-X Energy Savings App.
"""

from __future__ import annotations
from pathlib import Path
import streamlit as st
import base64

from app.config import APP_TITLE, LOGO_FILENAME, TAB_NAMES
from app.test_env import render_test_env, init_background_tasks
from app.mist_extractor import render_mist_extractor
from app.chip_conveyor import render_chip_conveyor

_APP_ROOT = Path(__file__).resolve().parents[1]
_LOGO_PATH = _APP_ROOT / "assets" / LOGO_FILENAME
_STYLE_PATH = _APP_ROOT / "assets" / "FX_style_top_right.svg"


def _get_base64(path: Path) -> str:
    """Lädt eine Datei als Base64-String."""
    if not path.exists():
        return ""
    with path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _inject_styles() -> None:
    """Injiziert globale CSS-Styles."""
    style_base64 = _get_base64(_STYLE_PATH)
    
    # Hintergrundkonfiguration (Hellgrün mit Transparenz)
    bg_color_hex = "#B1CB21"
    bg_opacity = 0.3
    
    # Hex zu RGB Konvertierung für die Nutzung in rgba()
    h = bg_color_hex.lstrip('#')
    r, g, b = tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    rgba_bg = f"rgba({r}, {g}, {b}, {bg_opacity})"
    
    # CSS für das Hintergrund-SVG
    bg_style = ""
    if style_base64:
        bg_style = f"""
        [data-testid="stAppViewContainer"]::before {{
            content: "";
            position: fixed;
            top: -5px;
            right: -5px;
            width: 400px;
            height: 400px;
            background-image: url('data:image/svg+xml;base64,{style_base64}');
            background-size: contain;
            background-repeat: no-repeat;
            background-position: top right;
            opacity: 0.4;
            transform: rotate(180deg);
            pointer-events: none;
            z-index: 0;
        }}
        """

    st.markdown(f"""
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" />
<style>
    {bg_style}
    
    /* --- START BACKGROUND FADE SNIPPET --- */
    /* Haupt-Hintergrund mit Radial Gradient (Fokus oben links, Rest transparent) */
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(
            circle at top left, 
            {rgba_bg} 0%, 
            rgba(255, 255, 255, 0) 70%
        ) !important;
        background-attachment: fixed !important;
    }}
    /* --- END BACKGROUND FADE SNIPPET --- */

    /* Vergrößert das st.logo und passt den Container an */
    [data-testid="stSidebarHeader"] {{
        height: 120px !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }}
    [data-testid="stSidebarHeader"] img {{
        height: 100px !important;
        width: auto !important;
    }}
    /* Content über dem Hintergrund */
    [data-testid="stMainBlockContainer"] {{
        position: relative;
        z-index: 1;
        padding-top: 2rem !important;
    }}
    /* Header transparent machen */
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
    }}
    /* Sidebar Footer Styling */
    .sidebar-footer {{
        position: fixed;
        bottom: 20px;
        left: 20px;
        color: #888888;
        font-size: 0.8rem;
    }}
    .sidebar-hr {{
        border: none;
        border-top: 1px solid #cccccc;
        margin: 10px 0;
    }}
</style>
""", unsafe_allow_html=True)


def run_app() -> None:
    """Startet die Anwendung."""
    st.set_page_config(layout="wide", page_title=APP_TITLE)
    
    # Hintergrund-Tasks sofort beim Starten der App initialisieren
    init_background_tasks()
    
    # Logo in die Sidebar setzen
    if _LOGO_PATH.exists():
        st.logo(str(_LOGO_PATH))
    
    # Sidebar
    st.sidebar.header("Einstellungen")
    
    # Netzwerkeinstellungen Expander
    with st.sidebar.expander("Netzwerkeinstellungen", expanded=False):
        st.session_state.api_url = st.text_input(
            "REST-API URL", 
            value=st.session_state.get("api_url", "http://127.0.0.1:8000/data"),
            help="Konfiguriert den Endpunkt für den Datenabruf."
        )
    
    # Sidebar Footer (Grauer Balken und Versionsnummer)
    st.sidebar.markdown("""
        <hr class="sidebar-hr">
        <div style="color: gray; font-size: 0.8rem;">
            Factory-X Energy Savings v0.1
        </div>
        """, unsafe_allow_html=True)
    
    # Header mit ausgewähltem Icon
    st.markdown(
        f"""
        <div style='display:flex; align-items:center; gap:16px; margin-bottom:1rem;'>
            <span class="material-symbols-rounded" style="font-size:54px; color:black;">energy_savings_leaf</span>
            <span style='font-size:48px; font-weight:700; letter-spacing:0.8px;'>
                {APP_TITLE}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    _inject_styles()
    
    # Tabs
    tabs = st.tabs(TAB_NAMES)
    for i, tab in enumerate(tabs):
        with tab:
            if TAB_NAMES[i] == "Testing":
                render_test_env()
            elif TAB_NAMES[i] == "Mist extractor":
                render_mist_extractor()
            elif TAB_NAMES[i] == "Chip conveyor":
                render_chip_conveyor()
            else:
                st.header(TAB_NAMES[i])
                st.write(f"Inhalt für {TAB_NAMES[i]} hier einfügen.")


if __name__ == "__main__":
    run_app()
