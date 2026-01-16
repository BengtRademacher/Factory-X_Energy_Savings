import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from app.components import render_traffic_light
from app.test_env import get_global_history
from app.config import COLOR_PALETTE

@st.fragment(run_every="1s")
def render_mist_extractor_dynamic():
    history = get_global_history()
    if not history:
        st.info("Initializing live data...")
        return
    
    history_df = pd.DataFrame(history)
    latest = history_df.iloc[-1]
    pm10 = latest.get("PM10", 0.0)
    is_active = latest.get("mist_extractor_active", False)

    # Status-Messages
    if is_active:
        st.warning("Extraction active")
    else:
        st.success("Extraction inactive")

    # Layout: Plot left, traffic light right
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Effective power vs. Particulate Matter")
        
        # Plotly Chart with synchronized axes
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Line 1: Power (Mist extractor)
        fig.add_trace(
            go.Scatter(
                x=history_df["timestamp"], 
                y=history_df["Mist extractor"], 
                name="Effective power [W]", 
                line=dict(color=COLOR_PALETTE["FX Blue"], width=2, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(75, 91, 169, 0.1)'
            ),
            secondary_y=False,
        )

        # Line 2: PM10
        fig.add_trace(
            go.Scatter(
                x=history_df["timestamp"], 
                y=history_df["PM10"], 
                name="PM₁₀ [mg/m³]", 
                line=dict(color=COLOR_PALETTE["Light Green"], width=2, shape='spline'),
                fill='tozeroy',
                fillcolor='rgba(177, 203, 33, 0.1)'
            ),
            secondary_y=True,
        )

        # Axis-Synchronization
        y1_max = max(history_df["Mist extractor"].max() * 1.2, 500)
        y2_max = max(history_df["PM10"].max() * 1.2, 5)

        fig.update_yaxes(
            title_text="Effective power [W]", 
            secondary_y=False,
            range=[0, y1_max],
            nticks=6,
            gridcolor='rgba(200, 200, 200, 0.3)',
            showgrid=True
        )
        fig.update_yaxes(
            title_text="PM₁₀ [mg/m³]", 
            secondary_y=True,
            range=[0, y2_max],
            nticks=6,
            showgrid=False
        )
        
        fig.update_xaxes(
            title_text="Timestamp",
            nticks=20,
            gridcolor='rgba(200, 200, 200, 0.3)',
            showgrid=True
        )
        
        fig.update_layout(
            height=400,
            paper_bgcolor='white',
            plot_bgcolor='rgba(250, 250, 250, 0.5)',
            margin=dict(l=10, r=10, t=30, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True, key="mist_extractor_chart")
        
    with col2:
        st.subheader("Status")
        if pm10 <= 2.0:
            color = "green"
        elif pm10 <= 3.0:
            color = "yellow"
        else:
            color = "red"
        
        render_traffic_light(color)
        st.metric("PM₁₀", f"{pm10:.3f} mg/m³")

def render_mist_extractor():
    st.header("Mist extractor")
    render_mist_extractor_dynamic()
