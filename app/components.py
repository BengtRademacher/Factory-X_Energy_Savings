import streamlit as st
import plotly.graph_objects as go
from app.config import COLOR_PALETTE

def render_traffic_light(state="animation"):
    """
    Renders the HTML for the traffic light.
    States: 'red', 'yellow', 'green' or 'animation'
    """
    
    # CSS Styles
    css = """
    <style>
      .trafficLight {
        background-color: black;
        width: 50px;
        height: 150px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        padding: 10px 5px;
        border-radius: 10px;
      }
      .trafficLight span {
        width: 40px;
        height: 40px;
        border-radius: 100%;
        background-color: #333;
      }
      
      /* Static colors */
      .light-red { background-color: red !important; box-shadow: 0 0 10px red; }
      .light-yellow { background-color: yellow !important; box-shadow: 0 0 10px yellow; }
      .light-green { background-color: green !important; box-shadow: 0 0 10px green; }

      /* Animations */
      .anim-red { animation: red-anim 5s linear infinite; }
      .anim-yellow { animation: yellow-anim 5s linear infinite; }
      .anim-green { animation: green-anim 5s linear infinite; }

      @keyframes red-anim {
        0%, 33% { background-color: red; box-shadow: 0 0 10px red; }
        34%, 100% { background-color: #333; box-shadow: none; }
      }
      @keyframes yellow-anim {
        0%, 33% { background-color: #333; box-shadow: none; }
        34%, 66% { background-color: yellow; box-shadow: 0 0 10px yellow; }
        67%, 100% { background-color: #333; box-shadow: none; }
      }
      @keyframes green-anim {
        0%, 66% { background-color: #333; box-shadow: none; }
        67%, 100% { background-color: green; box-shadow: 0 0 10px green; }
      }
    </style>
    """
    
    # Classes based on state
    red_class = "anim-red" if state == "animation" else ("light-red" if state == "red" else "")
    yellow_class = "anim-yellow" if state == "animation" else ("light-yellow" if state == "yellow" else "")
    green_class = "anim-green" if state == "animation" else ("light-green" if state == "green" else "")
    
    html = f"""
    {css}
    <div class="trafficLight">
      <span class="{red_class}"></span>
      <span class="{yellow_class}"></span>
      <span class="{green_class}"></span>
    </div>
    """
    st.components.v1.html(html, height=170)

def create_plotly_chart(df, y_col, title, color=None, y_label="Effective power [W]", height=300):
    """
    Creates a modern Plotly line chart.
    """
    if color is None:
        color = COLOR_PALETTE.get("FX Blue", "#4B5BA9")
        
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df["timestamp"],
        y=df[y_col],
        name=y_col,
        mode='lines',
        line=dict(color=color, width=2, shape='spline'),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(list(int(color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + [0.1])}"
    ))
    
    fig.update_layout(
        title=dict(text=title if title else "", font=dict(size=14, color='#333')),
        height=height,
        margin=dict(l=50, r=20, t=20 if not title else 40, b=40),
        paper_bgcolor='white',
        plot_bgcolor='rgba(250, 250, 250, 0.5)',
        xaxis=dict(
            title="Timestamp",
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)',
            nticks=20,
            tickfont=dict(size=9)
        ),
        yaxis=dict(
            title=y_label,
            showgrid=True,
            gridcolor='rgba(200, 200, 200, 0.3)',
            zeroline=True,
            zerolinecolor='rgba(200, 200, 200, 0.5)'
        ),
        hovermode="x unified",
        showlegend=False
    )
    
    return fig
