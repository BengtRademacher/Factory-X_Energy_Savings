from pathlib import Path

import streamlit as st


_APP_ROOT = Path(__file__).resolve().parents[1]
_ASSETS_DIR = _APP_ROOT / "assets"
_EXPERIMENTS_IMAGE = _ASSETS_DIR / "mist_extraction_experiments.png"
_SAVINGS_IMAGE = _ASSETS_DIR / "mist_extraction_savings.png"


def render_mist_extractor_savings():
    st.header("Energy savings for demand-oriented mist extraction")
    st.markdown(
        """
- The experiment plot compares operating states, PM10 concentration, and effective power to show how mist extraction demand changes over time.
- The savings plot summarizes the potential energy reduction when extraction runs on demand instead of continuously.
"""
    )

    st.image(str(_EXPERIMENTS_IMAGE), use_container_width=True)
    st.image(str(_SAVINGS_IMAGE), use_container_width=True)
