import streamlit as st
import pandas as pd
from app.components import render_traffic_light, create_plotly_chart
from app.test_env import get_global_history
from app.config import COLOR_PALETTE

@st.fragment(run_every="1s")
def render_chip_conveyor_dynamic():
    history = get_global_history()
    if not history:
        st.info("Initializing live data...")
        return
    
    history_df = pd.DataFrame(history)
    
    # Layout: Plot left, traffic light right
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Effective Power")
        if "Chip conveyor" in history_df.columns:
            fig = create_plotly_chart(
                history_df, 
                "Chip conveyor", 
                None,
                color=COLOR_PALETTE["Blue"]
            )
            st.plotly_chart(fig, use_container_width=True, key="chip_conveyor_chart")
        
    with col2:
        st.subheader("Status")
        render_traffic_light("animation")

def render_chip_conveyor():
    st.header("Chip conveyor")
    render_chip_conveyor_dynamic()
