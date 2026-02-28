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

# CSS minimale per sfondo
st.markdown("""
<style>
    .main {
        background: #0A0A0F;
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
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

# Header con logo e watchlist
col1, col2, col3 = st.columns([1, 4, 1])
with col1:
    st.markdown("### 👁️ **GOLDEN EYE**")
with col3:
    st.markdown(f"### 📊 {len(st.session_state.watchlist)}")

# Menu con pulsanti
st.markdown("---")
cols = st.columns(6)
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]

for i, item in enumerate(menu_items):
    with cols[i]:
        if st.button(item, use_container_width=True, 
                    type="primary" if st.session_state.current_page == item else "secondary"):
            st.session_state.current_page = item
            st.rerun()

st.markdown("---")

# Market Info Bar (solo testo)
now = datetime.now()
weekday = now.weekday()
hour = now.hour

crypto_status = "🟢 APERTO 24/7"
if weekday < 5 and 9 <= hour <= 16:
    stock_status = "🟢 APERTO"
else:
    stock_status = "🔴 CHIUSO" + (" (Weekend)" if weekday >= 5 else "")

if weekday < 5:
    forex_status = "🟢 APERTO"
else:
    forex_status = "🔴 CHIUSO"

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🕒 Ora", now.strftime("%H:%M"), now.strftime("%d/%m/%Y"))
with col2:
    st.metric("🪙 Crypto", crypto_status)
with col3:
    st.metric("📈 Azioni", stock_status)
with col4:
    st.metric("💱 Forex", forex_status)
with col5:
    st.metric("⚡ Versione", "4.0.0")

st.markdown("---")

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
        st.subheader("🛠️ Strumenti Avanzati")
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
    
    elif st.session_state.current_page == "API":
        from ui_streamlit.pages.api_dashboard import render
        render()
        
except Exception as e:
    st.error(f"Errore: {e}")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
with col2:
    st.caption("⚡ GOLDEN EYE PRO 4.0")
with col3:
    st.caption("⚠️ Solo scopo educativo")
