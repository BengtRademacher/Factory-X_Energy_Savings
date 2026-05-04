from pathlib import Path
import base64

import streamlit as st


_APP_ROOT = Path(__file__).resolve().parents[1]
_ASSETS_DIR = _APP_ROOT / "assets"
_EXPERIMENTS_IMAGE = _ASSETS_DIR / "mist_extraction_experiments.png"
_SAVINGS_IMAGE = _ASSETS_DIR / "mist_extraction_savings.png"


def _image_data_uri(path: Path) -> str:
    with path.open("rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


def _render_image_panel(path: Path, alt_text: str) -> None:
    st.markdown(
        f"""
<div class="savings-image-panel">
  <img src="{_image_data_uri(path)}" alt="{alt_text}" />
</div>
""",
        unsafe_allow_html=True,
    )


def render_mist_extractor_savings():
    st.header("Energy savings for demand-oriented mist extraction")
    st.markdown(
        """
<style>
    .savings-image-panel {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.12);
        border-radius: 8px;
        width: 75%;
        padding: 18px;
        margin: 18px auto 28px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }
    .savings-image-panel img {
        display: block;
        width: 100%;
        height: auto;
    }
</style>
""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
- Figure 1: Control strategies based on the two-point controller used in the energy savings concept
- Figure 2: Energy savings achieved using the control strategies
"""
    )

    _render_image_panel(_EXPERIMENTS_IMAGE, "Control strategies based on the two-point controller")
    _render_image_panel(_SAVINGS_IMAGE, "Energy savings achieved using the control strategies")
