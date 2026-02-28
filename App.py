import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from streamlit_option_menu import option_menu

# Configurazione pagina
st.set_page_config(
    page_title="GOLDEN EYE PRO",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# NUOVA GRAFICA - CSS AVANZATO
# ============================================
st.markdown("""
<style>
    /* Import font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main {
        background: #0A0A0F;
    }
    
    /* Metric Cards - Nuovo design */
    .metric-card {
        background: linear-gradient(135deg, #1E1E2A, #2C2C3A);
        border-radius: 20px;
        padding: 24px;
        border: 1px solid #3C3C4A;
        box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #FFD600, #FF3D00);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        border-color: #FFD600;
        box-shadow: 0 12px 32px rgba(255, 214, 0, 0.2);
    }
    
    .metric-label {
        color: #9E9EB0;
        font-size: 13px;
        font-weight: 500;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    
    .metric-value {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 700;
        font-family: 'Inter', monospace;
    }
    
    /* Signal Badges - Nuovo design */
    .signal-badge {
        padding: 8px 16px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        margin: 4px;
        animation: badgePulse 2s infinite;
        border: 1px solid transparent;
    }
    
    @keyframes badgePulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .strong-buy {
        background: rgba(0, 200, 83, 0.15);
        color: #00C853;
        border: 1px solid rgba(0, 200, 83, 0.3);
        box-shadow: 0 0 10px rgba(0, 200, 83, 0.2);
    }
    
    .buy {
        background: rgba(105, 240, 174, 0.1);
        color: #69F0AE;
        border: 1px solid rgba(105, 240, 174, 0.3);
    }
    
    .neutral {
        background: rgba(158, 158, 176, 0.1);
        color: #9E9EB0;
        border: 1px solid rgba(158, 158, 176, 0.3);
    }
    
    .sell {
        background: rgba(255, 61, 0, 0.15);
        color: #FF3D00;
        border: 1px solid rgba(255, 61, 0, 0.3);
        box-shadow: 0 0 10px rgba(255, 61, 0, 0.2);
    }
    
    /* Tables - Nuovo design */
    .stDataFrame {
        background: #1E1E2A;
        border-radius: 20px;
        border: 1px solid #3C3C4A;
        overflow: hidden;
    }
    
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    
    .dataframe th {
        background: #2C2C3A;
        color: #FFD600;
        font-weight: 600;
        font-size: 13px;
        padding: 16px;
        border-bottom: 2px solid #3C3C4A;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .dataframe td {
        padding: 14px 16px;
        border-bottom: 1px solid #3C3C4A;
        color: #FFFFFF;
        font-size: 14px;
    }
    
    .dataframe tr {
        transition: all 0.2s;
        cursor: pointer;
    }
    
    .dataframe tr:hover {
        background: #2C2C3A;
        transform: translateX(4px);
    }
    
    /* Tabs - Nuovo design */
    .stTabs {
        margin-bottom: 24px;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #1A1A24;
        padding: 8px;
        border-radius: 16px;
        border: 1px solid #3C3C4A;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: #2C2C3A;
        border-radius: 12px;
        padding: 12px 24px;
        color: #9E9EB0;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s;
        border: 1px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        border-color: #FFD600;
        color: #FFFFFF;
    }
    
    .stTabs [aria-selected="true"] {
        background: #FFD600 !important;
        color: #0A0A0F !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 214, 0, 0.3);
    }
    
    /* Buttons - Nuovo design */
    .stButton button {
        background: #2C2C3A;
        color: white;
        border: 1px solid #3C3C4A;
        border-radius: 14px;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .stButton button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton button:active::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton button:hover {
        background: #FFD600;
        color: #0A0A0F;
        border-color: #FFD600;
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(255, 214, 0, 0.3);
    }
    
    .stButton.primary button {
        background: #FFD600;
        color: #0A0A0F;
    }
    
    /* Panels - Nuovo design */
    .panel {
        background: #1E1E2A;
        border-radius: 24px;
        padding: 24px;
        border: 1px solid #3C3C4A;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        transition: all 0.3s;
        animation: slideUp 0.5s ease;
    }
    
    .panel:hover {
        border-color: #FFD600;
        box-shadow: 0 12px 32px rgba(255, 214, 0, 0.1);
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .panel-title {
        color: #FFFFFF;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Asset Tabs */
    .asset-tabs {
        display: flex;
        gap: 12px;
        margin-bottom: 24px;
        flex-wrap: wrap;
    }
    
    .asset-tab {
        padding: 12px 24px;
        background: #2C2C3A;
        border-radius: 30px;
        color: #9E9EB0;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
        border: 1px solid #3C3C4A;
    }
    
    .asset-tab:hover {
        border-color: #FFD600;
        transform: translateY(-2px);
        color: #FFFFFF;
    }
    
    .asset-tab.active {
        background: #FFD600;
        color: #0A0A0F;
        border-color: #FFD600;
        box-shadow: 0 4px 12px rgba(255, 214, 0, 0.3);
    }
    
    /* Form elements */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background: #2C2C3A !important;
        border: 2px solid #3C3C4A !important;
        border-radius: 14px !important;
        color: white !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        transition: all 0.3s !important;
    }
    
    .stTextInput input:focus, .stTextArea textarea:focus, .stSelectbox select:focus {
        border-color: #FFD600 !important;
        box-shadow: 0 0 0 3px rgba(255, 214, 0, 0.1) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Progress bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #FFD600, #FF3D00) !important;
        border-radius: 10px !important;
        height: 8px !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #2C2C3A !important;
        color: #FFD600 !important;
        border-radius: 14px !important;
        border: 1px solid #3C3C4A !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: #1A1A24 !important;
        border-right: 1px solid #3C3C4A !important;
    }
    
    /* Live badge */
    .live-badge {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #00C853;
        font-size: 12px;
        margin-top: 20px;
        padding: 12px;
        background: #1E1E2A;
        border-radius: 30px;
        border: 1px solid #3C3C4A;
        animation: pulse 2s infinite;
    }
    
    .live-dot {
        width: 10px;
        height: 10px;
        background: #00C853;
        border-radius: 50%;
        animation: pulseDot 1.5s infinite;
    }
    
    @keyframes pulseDot {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.5; transform: scale(1.2); }
        100% { opacity: 1; transform: scale(1); }
    }
    
    /* Footer */
    .app-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #1A1A24;
        padding: 16px 32px;
        color: #9E9EB0;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        border-top: 1px solid #3C3C4A;
        z-index: 999;
        backdrop-filter: blur(10px);
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .element-container {
        animation: slideIn 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE (invariato)
# ============================================
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
    
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = 'BTC-USD'
    
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {
        'cash': 10000,
        'positions': {}
    }

# ============================================
# SIDEBAR - Nuovo design
# ============================================
with st.sidebar:
    # Logo con effetto glow
    st.markdown("""
    <div style='text-align: center; margin-bottom: 40px;'>
        <h1 style='background: linear-gradient(135deg, #FFD600, #FF3D00); 
                   -webkit-background-clip: text; 
                   -webkit-text-fill-color: transparent; 
                   font-size: 28px; 
                   font-weight: 800;
                   letter-spacing: -0.5px;
                   animation: glow 2s infinite;'>👁️ GOLDEN EYE PRO</h1>
        <p style='color: #9E9EB0; 
                  background: #2C2C3A; 
                  padding: 4px 12px; 
                  border-radius: 30px; 
                  display: inline-block;
                  font-size: 11px;
                  font-weight: 600;'>v2.0.0</p>
    </div>
    <style>
    @keyframes glow {
        0% { text-shadow: 0 0 10px rgba(255,214,0,0.3); }
        50% { text-shadow: 0 0 20px rgba(255,214,0,0.6); }
        100% { text-shadow: 0 0 10px rgba(255,214,0,0.3); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Menu principale con nuovo stile
    selected = option_menu(
        menu_title=None,
        options=["🔍 SCAN", "📊 DETTAGLIO", "📋 WATCHLIST", "⚙️ STRUMENTI", "🤖 TRADING"],
        icons=["search", "graph-up", "list", "tools", "robot"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#1A1A24",
                "border-radius": "16px",
                "border": "1px solid #3C3C4A"
            },
            "icon": {"color": "#FFD600", "font-size": "18px"},
            "nav-link": {
                "color": "#9E9EB0",
                "font-size": "14px",
                "text-align": "left",
                "margin": "4px 0",
                "padding": "14px 18px",
                "border-radius": "12px",
                "transition": "all 0.3s",
            },
            "nav-link:hover": {
                "color": "#FFFFFF",
                "background-color": "#2C2C3A",
            },
            "nav-link-selected": {
                "background": "linear-gradient(90deg, rgba(255,214,0,0.15), transparent)",
                "color": "#FFD600",
                "font-weight": "600",
                "border-left": "3px solid #FFD600",
            },
        }
    )
    
    # Gestione sottomenu
    if selected == "⚙️ STRUMENTI":
        sub_selected = option_menu(
            menu_title=None,
            options=["📊 Validazione", "🎯 Ottimizzazione", "💰 Money Management"],
            icons=["check-circle", "sliders", "coins"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#2C2C3A",
                    "margin-left": "20px",
                    "border-radius": "12px"
                },
                "icon": {"color": "#FFD600", "font-size": "14px"},
                "nav-link": {
                    "color": "#9E9EB0",
                    "font-size": "13px",
                    "padding": "10px 16px",
                    "border-radius": "8px"
                },
                "nav-link-selected": {"background-color": "#FFD600", "color": "#0A0A0F"},
            }
        )
        st.session_state.sub_page = sub_selected
        
    if selected == "🤖 TRADING":
        sub_selected = option_menu(
            menu_title=None,
            options=["📝 Paper Trading", "🧠 AutoTrader"],
            icons=["file-text", "brain"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {
                    "padding": "0!important",
                    "background-color": "#2C2C3A",
                    "margin-left": "20px",
                    "border-radius": "12px"
                },
                "icon": {"color": "#FFD600", "font-size": "14px"},
                "nav-link": {
                    "color": "#9E9EB0",
                    "font-size": "13px",
                    "padding": "10px 16px",
                    "border-radius": "8px"
                },
                "nav-link-selected": {"background-color": "#FFD600", "color": "#0A0A0F"},
            }
        )
        st.session_state.sub_page = sub_selected
    
    # Quick actions con nuovo design
    st.markdown("<hr style='border-color: #3C3C4A; margin: 24px 0;'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔍 AVVIA SCAN", use_container_width=True):
            st.session_state.current_page = "SCAN"
            st.rerun()
    with col2:
        if st.button("📋 GESTISCI", use_container_width=True):
            st.session_state.current_page = "WATCHLIST"
            st.rerun()
    
    # Watchlist mini con nuovo design
    st.markdown("""
    <div style='background: #1E1E2A; 
                padding: 20px; 
                border-radius: 20px; 
                margin: 20px 0;
                border: 1px solid #3C3C4A;'>
        <h4 style='color: #9E9EB0; 
                   font-size: 12px; 
                   margin-bottom: 16px;
                   letter-spacing: 0.5px;'>
            📌 WATCHLIST RAPIDA
        </h4>
    """, unsafe_allow_html=True)
    
    for asset in st.session_state.watchlist[:5]:
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(asset, key=f"mini_{asset}", use_container_width=True):
                st.session_state.selected_asset = asset
                st.switch_page("pages/dettaglio.py")
        with col2:
            change = np.random.normal(0, 2)
            color = "#00C853" if change > 0 else "#FF3D00"
            st.markdown(f"<span style='color: {color}; font-weight: 600;'>{'+' if change > 0 else ''}{change:.1f}%</span>", unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Live badge nuovo design
    st.markdown(f"""
    <div class='live-badge'>
        <span class='live-dot'></span>
        <span style='font-weight: 600;'>LIVE</span>
        <span style='color: #9E9EB0; margin-left: auto;'>{datetime.now().strftime("%H:%M:%S")}</span>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# HEADER PRINCIPALE - Nuovo design
# ============================================
st.markdown(f"""
<div style='display: flex; 
            justify-content: space-between; 
            align-items: center; 
            margin-bottom: 32px;
            padding: 0 8px;'>
    <h1 style='color: white; 
               font-size: 36px; 
               font-weight: 800;
               letter-spacing: -0.5px;'>
        {selected.replace("🔍 ", "").replace("📊 ", "").replace("📋 ", "").replace("⚙️ ", "").replace("🤖 ", "")}
    </h1>
    <div style='display: flex; 
                gap: 24px; 
                color: #9E9EB0;
                background: #1A1A24;
                padding: 12px 24px;
                border-radius: 40px;
                border: 1px solid #3C3C4A;
                font-size: 13px;
                font-weight: 500;'>
        <span>📊 Watchlist: {len(st.session_state.watchlist)} assets</span>
        <span>⏱️ Ultimo scan: {datetime.now().strftime("%H:%M:%S")}</span>
        <span style='cursor: pointer;' onclick='window.location.reload()'>↻</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# ROUTING
# ============================================
if selected == "🔍 SCAN":
    st.switch_page("pages/scan.py")
elif selected == "📊 DETTAGLIO":
    st.switch_page("pages/dettaglio.py")
elif selected == "📋 WATCHLIST":
    st.switch_page("pages/watchlist.py")
elif selected == "⚙️ STRUMENTI":
    if "Validazione" in st.session_state.sub_page:
        st.switch_page("pages/validazione.py")
    elif "Ottimizzazione" in st.session_state.sub_page:
        st.switch_page("pages/ottimizzazione.py")
    elif "Money" in st.session_state.sub_page:
        st.switch_page("pages/money_management.py")
elif selected == "🤖 TRADING":
    if "Paper" in st.session_state.sub_page:
        st.switch_page("pages/paper_trading.py")
    elif "Auto" in st.session_state.sub_page:
        st.switch_page("pages/autotrader.py")

# ============================================
# FOOTER - Nuovo design
# ============================================
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>📊 Watchlist: {len(st.session_state.watchlist)} assets</span>
    <span>⚠️ Educational purpose only</span>
</div>
""", unsafe_allow_html=True)
