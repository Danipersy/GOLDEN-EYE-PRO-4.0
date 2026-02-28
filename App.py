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
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
if 'app_start_time' not in st.session_state:
    st.session_state.app_start_time = datetime.now()

# CSS
st.markdown("""
<style>
    .main { background: #0A0A0F; }
    .stApp { background: #0A0A0F; }
    .app-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #1A1A24;
        border-top: 1px solid #3C3C4A;
        padding: 12px 32px;
        color: #9E9EB0;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# Menu principale
cols = st.columns(5)
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING"]
for i, item in enumerate(menu_items):
    with cols[i]:
        if st.button(item, use_container_width=True, 
                    type="primary" if st.session_state.current_page == item else "secondary"):
            st.session_state.current_page = item
            st.rerun()

st.divider()

# Routing pagine
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
        st.subheader("⚙️ Strumenti")
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
        st.subheader("🤖 Trading")
        tabs = st.tabs(["📝 Paper Trading", "🧠 AutoTrader"])
        
        with tabs[0]:
            from ui_streamlit.pages.paper_trading import render
            render()
        
        with tabs[1]:
            from ui_streamlit.pages.auto_trader import render
            render()
            
except Exception as e:
    st.error(f"Errore: {e}")
    if st.session_state.debug_mode:
        st.exception(e)

# Footer
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>📊 Watchlist: {len(st.session_state.watchlist)} assets</span>
    <span>⚡ {st.session_state.current_page}</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
