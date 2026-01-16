import streamlit as st
import random
import time
import threading
import json
import requests
from fastapi import FastAPI
import uvicorn
from datetime import datetime
import pandas as pd
from collections import deque

# --- GLOBAL SHARED STATE (Thread-Safe outside Streamlit) ---
# Diese Variablen verursachen keine "ScriptRunContext" Warnungen
_GLOBAL_HISTORY = deque(maxlen=60)
_SERVER_DATA = {
    "Main supply": 0,
    "Mist extractor": 0,
    "Chip conveyor": 0,
    "timestamp": ""
}

# --- FASTAPI SETUP ---
api_app = FastAPI()

@api_app.get("/data")
def get_data():
    return _SERVER_DATA

def run_api():
    uvicorn.run(api_app, host="127.0.0.1", port=8000, log_level="error")

# --- GENERATOR SETUP ---
def data_generator():
    global _SERVER_DATA
    while True:
        _SERVER_DATA = {
            "Main supply": random.randint(4000, 4500),
            "Mist extractor": random.randint(380, 395),
            "Chip conveyor": random.randint(250, 275),
            "timestamp": datetime.now().strftime("%H:%M:%S")
        }
        time.sleep(1)

# --- API POLLER ---
def api_poller():
    """Befüllt die globale Historie ohne Streamlit-Kontext."""
    while True:
        try:
            # Pollt die lokale API
            response = requests.get("http://127.0.0.1:8000/data", timeout=0.5)
            if response.status_code == 200:
                api_json = response.json()
                normalized = {
                    "timestamp": api_json.get("timestamp", datetime.now().strftime("%H:%M:%S")),
                    "Main supply": api_json.get("Main supply", api_json.get("Hauptversorgung", 0)),
                    "Mist extractor": api_json.get("Mist extractor", api_json.get("Nebelabscheider", 0)),
                    "Chip conveyor": api_json.get("Chip conveyor", api_json.get("Späneförderer", api_json.get("Chip conveyer", 0)))
                }
                _GLOBAL_HISTORY.append(normalized)
        except Exception:
            pass
        time.sleep(1)

# --- THREAD MANAGEMENT ---
def init_background_tasks():
    if "threads_started" not in st.session_state:
        threading.Thread(target=run_api, daemon=True).start()
        threading.Thread(target=data_generator, daemon=True).start()
        threading.Thread(target=api_poller, daemon=True).start()
        st.session_state.threads_started = True

# --- UI RENDERER ---
@st.fragment(run_every="1s")
def render_test_env():
    # Daten für die UI aus den globalen Variablen holen
    history_df = pd.DataFrame(list(_GLOBAL_HISTORY))
    
    st.subheader("Simulierte Daten (Server-Side Internal)")
    st.json(_SERVER_DATA, expanded=True)
    
    st.divider()
    
    st.subheader("REST-API Response (Background Poller)")
    if not history_df.empty:
        st.json(history_df.iloc[-1].to_dict(), expanded=True)
    else:
        st.warning("Warte auf Hintergrund-Poller...")

    st.divider()

    if not history_df.empty:
        st.subheader("Live Visualisierung")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Main supply [W]**")
            st.line_chart(history_df.set_index("timestamp")["Main supply"])
        with col2:
            st.write("**Mist extractor [W]**")
            st.line_chart(history_df.set_index("timestamp")["Mist extractor"])
        with col3:
            st.write("**Chip conveyor [W]**")
            st.line_chart(history_df.set_index("timestamp")["Chip conveyor"])

def get_global_history():
    """Hilfsfunktion für andere Module."""
    return list(_GLOBAL_HISTORY)
