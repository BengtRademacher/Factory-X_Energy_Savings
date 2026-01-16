import streamlit as st
import pandas as pd
from app.components import create_plotly_chart
from app.config import COLOR_PALETTE
from app.services.data_service import data_service

def init_background_tasks():
    if "threads_started" not in st.session_state:
        data_service.start_background_tasks()
        st.session_state.threads_started = True

@st.fragment(run_every="1s")
def render_dynamic_charts():
    history_df = pd.DataFrame(list(data_service.history))
    if history_df.empty:
        st.info("Waiting for data...")
        return
    col1, col2, col3 = st.columns(3)
    with col1:
        fig1 = create_plotly_chart(history_df, "Main supply", None, COLOR_PALETTE["FX Blue"])
        st.plotly_chart(fig1, use_container_width=True, key="test_main_supply")
    with col2:
        fig2 = create_plotly_chart(history_df, "Mist extractor", None, COLOR_PALETTE["Light Blue"])
        st.plotly_chart(fig2, use_container_width=True, key="test_mist_extractor")
    with col3:
        fig3 = create_plotly_chart(history_df, "Chip conveyor", None, COLOR_PALETTE["Blue"])
        st.plotly_chart(fig3, use_container_width=True, key="test_chip_conveyor")

@st.fragment(run_every="1s")
def render_json_monitor():
    history_df = pd.DataFrame(list(data_service.history))
    col_j1, col_j2 = st.columns(2)
    with col_j1:
        st.write("**Data Server**")
        st.json(data_service.server_data, expanded=True)
    with col_j2:
        st.write("**API Response**")
        if not history_df.empty:
            st.json(history_df.iloc[-1].to_dict(), expanded=True)
        else:
            st.warning("Waiting for data...")

def render_test_env():
    st.subheader("Two-point controller")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        data_service.pm10_rise_rate = st.slider(
            "Pollution rate (PM₁₀ rise)", 
            0.01, 0.50, data_service.pm10_rise_rate, 0.01,
            help="How fast PM₁₀ rises per second when extraction is inactive?",
            key="slider_rise_rate"
        )
    with col_s2:
        data_service.pm10_fall_rate = st.slider(
            "Extraction efficiency (PM₁₀ fall)", 
            0.05, 1.00, data_service.pm10_fall_rate, 0.01,
            help="How fast PM₁₀ falls per second when extraction is active?",
            key="slider_fall_rate"
        )

    st.divider()
    
    st.subheader("JSON Monitor")
    render_json_monitor()

    st.divider()

    st.subheader("Overview")
    render_dynamic_charts()

    st.divider()
    if st.button("System Reset (Reset model to 0 mg/m³)", type="primary", key="reset_btn"):
        data_service.reset_all_data()

def get_global_history():
    return list(data_service.history)
