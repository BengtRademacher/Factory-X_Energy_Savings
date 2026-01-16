import streamlit as st
import pandas as pd
from app.components import render_traffic_light
from app.test_env import get_global_history

@st.fragment(run_every="1s")
def render_mist_extractor():
    st.header("Mist extractor")
    
    # Daten aus der globalen Historie holen
    history = get_global_history()
    if not history:
        st.info("Initialisiere Live-Daten...")
        return

    history_df = pd.DataFrame(history)

    # Layout: Plot links, Ampel rechts
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Leistungsverlauf")
        if "Mist extractor" in history_df.columns:
            chart_data = history_df.set_index("timestamp")[["Mist extractor"]]
            st.line_chart(chart_data)
        
    with col2:
        st.subheader("Status")
        render_traffic_light("animation")

    st.divider()
    st.write("Detaillierte Analyse des Nebelabscheiders folgt hier.")
