import streamlit as st

def get_traffic_light_html(state="red"):
    """
    Erzeugt das HTML für die Ampel.
    States: 'red', 'yellow', 'green' oder 'animation'
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
      
      /* Statische Farben */
      .light-red { background-color: red !important; box-shadow: 0 0 10px red; }
      .light-yellow { background-color: yellow !important; box-shadow: 0 0 10px yellow; }
      .light-green { background-color: green !important; box-shadow: 0 0 10px green; }

      /* Animationen */
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
    
    # Klassen basierend auf State
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
    return html

def render_traffic_light(state="animation"):
    st.components.v1.html(get_traffic_light_html(state), height=170)
