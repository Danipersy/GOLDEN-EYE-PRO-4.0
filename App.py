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

# CSS
st.markdown("""
<style>
    /* Reset */
    .main { background: #0A0A0F; padding: 0 !important; }
    .stApp { background: #0A0A0F; }
    section[data-testid="stSidebar"] { display: none !important; }
    
    /* Header */
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #1A1A24;
        border-bottom: 2px solid #f0b90b;
        padding: 8px 32px;
        z-index: 9999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        height: 70px;
    }
    
    /* Menu */
    .top-menu {
        display: flex;
        gap: 5px;
        background: #2C2C3A;
        padding: 5px;
        border-radius: 40px;
    }
    
    .menu-btn {
        padding: 10px 24px;
        border-radius: 30px;
        color: #9E9EB0;
        font-size: 14px;
        font-weight: 700;
        cursor: pointer;
        border: none;
        background: transparent;
        transition: all 0.3s ease;
    }
    
    .menu-btn:hover {
        background: #3C3C4A;
        color: white;
    }
    
    .menu-btn.active {
        background: #f0b90b;
        color: #0A0A0F;
    }
    
    /* Logo */
    .logo {
        background: linear-gradient(135deg, #f0b90b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 22px;
        font-weight: 800;
    }
    
    /* Contenuto */
    .main-content {
        margin-top: 90px;
        padding: 20px 32px;
        margin-bottom: 70px;
    }
    
    /* Footer */
    .app-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #1A1A24;
        border-top: 1px solid #f0b90b;
        padding: 12px 32px;
        color: #9E9EB0;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        z-index: 9999;
        height: 50px;
    }
    
    /* Card risultati */
    .result-card {
        background: linear-gradient(135deg, #1e1e2e, #1a1a2a);
        border-left: 8px solid;
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# MENU CON PULSANTI STREAMLIT (NON HTML)
# ============================================
cols = st.columns(6)
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]

for i, item in enumerate(menu_items):
    with cols[i]:
        if st.button(item, use_container_width=True, 
                    type="primary" if st.session_state.current_page == item else "secondary"):
            st.session_state.current_page = item
            st.rerun()

st.markdown("---")

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
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
