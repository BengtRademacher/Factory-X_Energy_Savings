import streamlit as st
import pandas as pd
import requests
from app.components import create_plotly_chart
from app.config import COLOR_PALETTE
from app.services.data_service import data_service

API_BASE_URL = "http://127.0.0.1:8000"


def init_background_tasks():
    if "threads_started" not in st.session_state:
        data_service.start_background_tasks()
        st.session_state.threads_started = True


def _check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=0.25)
        if response.status_code == 200:
            return "available", response.json()
        return f"unavailable ({response.status_code})", None
    except requests.RequestException:
        return "unavailable", None


def _apply_pm10_rate_sliders():
    data_service.set_pm10_rates(
        st.session_state.slider_rise_rate,
        st.session_state.slider_fall_rate,
        source="Streamlit UI",
        command_name="set_pm10_rates",
    )


def _sync_slider_state_from_service():
    metadata = data_service.get_control_metadata_snapshot()
    service_rise_rate = data_service.pm10_rise_rate
    service_fall_rate = data_service.pm10_fall_rate

    if "slider_rise_rate" not in st.session_state:
        st.session_state.slider_rise_rate = service_rise_rate
    if "slider_fall_rate" not in st.session_state:
        st.session_state.slider_fall_rate = service_fall_rate

    if metadata.get("last_command_source") == "REST API":
        st.session_state.slider_rise_rate = service_rise_rate
        st.session_state.slider_fall_rate = service_fall_rate


def _render_external_control():
    status, health = _check_api_health()
    metadata = data_service.get_control_metadata_snapshot()

    st.subheader("External control")
    col_status, col_command, col_source = st.columns(3)
    col_status.metric("API status", status)
    col_command.metric("Last command", metadata.get("last_command") or "None")
    col_source.metric("Command source", metadata.get("last_command_source") or "None")

    st.caption(
        "Optional external demonstrator interface. Streamlit and REST commands "
        "control the same local simulation state."
    )

    endpoints = pd.DataFrame([
        {"Method": "GET", "Endpoint": f"{API_BASE_URL}/health", "Purpose": "API availability"},
        {"Method": "GET", "Endpoint": f"{API_BASE_URL}/state", "Purpose": "Current state and control metadata"},
        {"Method": "GET", "Endpoint": f"{API_BASE_URL}/history", "Purpose": "Recent simulation samples"},
        {"Method": "POST", "Endpoint": f"{API_BASE_URL}/control/pm10-rates", "Purpose": "Set PM10 rise/fall rates"},
        {"Method": "POST", "Endpoint": f"{API_BASE_URL}/control/reset", "Purpose": "Reset simulation state"},
    ])
    st.dataframe(endpoints, use_container_width=True, hide_index=True)

    if health:
        st.json(health, expanded=False)


@st.fragment(run_every="1s")
def render_dynamic_charts():
    history_df = pd.DataFrame(data_service.get_history_snapshot())
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
def render_live_state():
    history_df = pd.DataFrame(data_service.get_history_snapshot())
    metadata = data_service.get_control_metadata_snapshot()
    col_j1, col_j2, col_j3 = st.columns(3)
    with col_j1:
        st.write("**Current service state**")
        st.json(data_service.get_server_data_snapshot(), expanded=True)
    with col_j2:
        st.write("**Latest history sample**")
        if not history_df.empty:
            st.json(history_df.iloc[-1].to_dict(), expanded=True)
        else:
            st.warning("Waiting for data...")
    with col_j3:
        st.write("**External-control metadata**")
        st.json(metadata, expanded=True)


def render_test_env():
    st.header("Settings")
    _render_external_control()

    st.divider()

    st.subheader("Two-point controller")
    _sync_slider_state_from_service()
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        pm10_rise_rate = st.slider(
            "Pollution rate (PM10 rise)",
            0.01,
            0.50,
            data_service.pm10_rise_rate,
            0.01,
            help="How fast PM10 rises per second when extraction is inactive?",
            key="slider_rise_rate",
            on_change=_apply_pm10_rate_sliders,
        )
    with col_s2:
        pm10_fall_rate = st.slider(
            "Extraction efficiency (PM10 fall)",
            0.05,
            1.00,
            data_service.pm10_fall_rate,
            0.01,
            help="How fast PM10 falls per second when extraction is active?",
            key="slider_fall_rate",
            on_change=_apply_pm10_rate_sliders,
        )
    st.caption(
        f"Applied rise rate: {pm10_rise_rate:.2f} mg/m3/s - "
        f"Applied fall rate: {pm10_fall_rate:.2f} mg/m3/s"
    )

    st.divider()

    st.subheader("Live state")
    render_live_state()

    st.divider()

    st.subheader("Overview")
    render_dynamic_charts()

    st.divider()
    if st.button("System Reset (Reset model to 0 mg/m3)", type="primary", key="reset_btn"):
        data_service.reset_all_data(source="Streamlit UI", command_name="reset")


def get_global_history():
    return data_service.get_history_snapshot()
