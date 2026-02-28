import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Configurazione path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Configurazione pagina
st.set_page_config(
    page_title="GOLDEN EYE PRO",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inizializza session state
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = 'BTC-USD'
if 'current_page' not in st.session_state:
    st.session_state.current_page = "SCAN"

# CSS
st.markdown("""
<style>
    .main { background: #0A0A0F; }
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

# Menu
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING"]
cols = st.columns(len(menu_items))
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
        # Prova a importare scan
        try:
            from ui_streamlit.pages.scan import show_page
            show_page()
        except ImportError:
            st.subheader("🔍 SCAN Mercati")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("BTC-USD", "$52,345", "+2.3%")
            with col2:
                st.metric("ETH-USD", "$3,124", "+1.2%")
            with col3:
                st.metric("BNB-USD", "$412", "-0.5%")
    
    elif st.session_state.current_page == "DETTAGLIO":
        st.subheader(f"📊 Dettaglio {st.session_state.selected_asset}")
        st.info("Pagina in costruzione")
    
    elif st.session_state.current_page == "WATCHLIST":
        st.subheader("📋 Watchlist")
        for asset in st.session_state.watchlist:
            st.write(f"- {asset}")
    
    elif st.session_state.current_page == "STRUMENTI":
        st.subheader("⚙️ Strumenti")
        tab1, tab2, tab3 = st.tabs(["Validazione", "Ottimizzazione", "Money Management"])
        with tab1:
            st.info("Validazione strategia")
        with tab2:
            st.info("Ottimizzazione parametri")
        with tab3:
            st.info("Money management")
    
    elif st.session_state.current_page == "TRADING":
        st.subheader("🤖 Trading")
        tab1, tab2 = st.tabs(["Paper Trading", "AutoTrader"])
        with tab1:
            st.info("Paper trading")
        with tab2:
            st.info("AutoTrader")
            
except Exception as e:
    st.error(f"Errore: {e}")

# Footer
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>📊 Watchlist: {len(st.session_state.watchlist)} assets</span>
    <span>⚡ {st.session_state.current_page}</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
