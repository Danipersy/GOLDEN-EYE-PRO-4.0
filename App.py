import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Configurazione path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Configurazione pagina
st.set_page_config(
    page_title="GOLDEN EYE PRO 4.0",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS GLOBALE PROFESSIONALE
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* RESET E BASE */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .main {
        background: radial-gradient(circle at 0% 0%, #1a1f35, #0a0e1a);
        padding: 0 !important;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* NASCONDI SIDEBAR */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* HEADER PREMIUM */
    .premium-header {
        background: linear-gradient(90deg, rgba(18, 23, 40, 0.95), rgba(26, 31, 58, 0.95));
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(240, 185, 11, 0.3);
        padding: 0 32px;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 9999;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* TOP BAR MERCATI */
    .market-bar {
        background: linear-gradient(135deg, #1E2338, #161B2F);
        border-radius: 20px;
        padding: 20px 30px;
        margin: 100px 32px 30px 32px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        border-left: 6px solid #f0b90b;
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        backdrop-filter: blur(10px);
    }
    
    /* CARD METRICHE */
    .metric-card-pro {
        background: linear-gradient(135deg, #1E2338, #161B2F);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card-pro::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.5s;
    }
    
    .metric-card-pro:hover::before {
        left: 100%;
    }
    
    .metric-card-pro:hover {
        transform: translateY(-5px);
        border-color: #f0b90b;
        box-shadow: 0 20px 40px rgba(240, 185, 11, 0.2);
    }
    
    /* BADGE LIVE */
    .live-badge {
        background: linear-gradient(135deg, #00ff8820, #00ff8805);
        border: 1px solid #00ff88;
        border-radius: 30px;
        padding: 4px 16px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 0.7; }
        50% { opacity: 1; }
        100% { opacity: 0.7; }
    }
    
    /* FOOTER */
    .premium-footer {
        background: linear-gradient(90deg, #121728, #1A1F3A);
        border-top: 1px solid rgba(240, 185, 11, 0.3);
        padding: 16px 32px;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        color: #94a3b8;
        font-size: 13px;
        display: flex;
        justify-content: space-between;
        z-index: 9999;
        backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# Inizializzazione session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = 'BTC-USD'
if 'radar_select' not in st.session_state:
    st.session_state.radar_select = 'BTC-USD'
if 'current_page' not in st.session_state:
    st.session_state.current_page = "SCAN"
if 'last_scan_time' not in st.session_state:
    st.session_state.last_scan_time = None
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None

# ============================================
# HEADER CON MENU
# ============================================
st.markdown("""
<div class='premium-header'>
    <div style='display: flex; justify-content: space-between; align-items: center; height: 70px;'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <span style='font-size: 28px; font-weight: 800; background: linear-gradient(135deg, #f0b90b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>👁️ GOLDEN EYE</span>
            <span style='background: #2C2C3A; padding: 4px 12px; border-radius: 30px; font-size: 12px; color: #f0b90b; border: 1px solid #f0b90b;'>PRO 4.0</span>
        </div>
        <div style='color: #94a3b8;'>📊 {len(st.session_state.watchlist)} assets</div>
    </div>
</div>
""".format(len(st.session_state.watchlist)), unsafe_allow_html=True)

# Menu con pulsanti Streamlit (distanziati dall'header)
st.markdown("<div style='margin-top: 90px;'></div>", unsafe_allow_html=True)

cols = st.columns(6)
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]

for i, item in enumerate(menu_items):
    with cols[i]:
        if st.button(item, use_container_width=True, 
                    type="primary" if st.session_state.current_page == item else "secondary"):
            st.session_state.current_page = item
            st.rerun()

# ============================================
# MARKET INFO BAR (sotto il menu)
# ============================================
from ui_streamlit.components.market_bar import render_market_bar
render_market_bar()

# ============================================
# ROUTING PAGINE
# ============================================
try:
    if st.session_state.current_page == "SCAN":
        from ui_streamlit.pages.scan import show_page
        show_page()
    
    elif st.session_state.current_page == "DETTAGLIO":
        from ui_streamlit.pages.dettaglio import show_page
        show_page(st.session_state.selected_asset)
    
    elif st.session_state.current_page == "WATCHLIST":
        from ui_streamlit.pages.watchlist import show_page
        show_page()
    
    elif st.session_state.current_page == "STRUMENTI":
        st.markdown("## 🛠️ Strumenti Avanzati")
        tabs = st.tabs(["📊 Validazione", "🎯 Ottimizzazione", "💰 Money Management"])
        
        with tabs[0]:
            from ui_streamlit.pages.validazione import render
            render()
        
        with tabs[1]:
            from ui_streamlit.pages.ottimizzazione import render
            render()
        
        with tabs[2]:
            from ui_streamlit.pages.money_management import render
            render()
    
    elif st.session_state.current_page == "TRADING":
        st.markdown("## 🤖 Trading")
        tabs = st.tabs(["📝 Paper Trading", "🧠 AutoTrader"])
        
        with tabs[0]:
            from ui_streamlit.pages.paper_trading import render
            render()
        
        with tabs[1]:
            from ui_streamlit.pages.auto_trader import render
            render()
    
    elif st.session_state.current_page == "API":
        from ui_streamlit.pages.api_dashboard import render
        render()
        
except Exception as e:
    st.error(f"Errore: {e}")

# Footer
st.markdown(f"""
<div class='premium-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
