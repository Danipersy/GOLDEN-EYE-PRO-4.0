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

# CSS leggero per uniformare sfondo e nascondere sidebar
st.markdown("""
<style>
    .main { background-color: #0E1117; }
    section[data-testid="stSidebar"] { display: none; }
    div[data-testid="stMetricValue"] { font-size: 1.2rem; }
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

# ==================== HEADER ====================
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("## 👁️ **GOLDEN EYE**")
with col3:
    st.markdown(f"## 📊 {len(st.session_state.watchlist)}")
st.divider()

# ==================== MENU ====================
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
cols = st.columns(len(menu_items))
for i, item in enumerate(menu_items):
    with cols[i]:
        if st.button(item, use_container_width=True,
                     type="primary" if st.session_state.current_page == item else "secondary"):
            st.session_state.current_page = item
            st.rerun()
st.divider()

# ==================== MARKET BAR ====================
now = datetime.now()
weekday = now.weekday()
hour = now.hour

crypto_status = "🟢 APERTO 24/7"
if weekday < 5 and 9 <= hour <= 16:
    stock_status = "🟢 APERTO"
else:
    stock_status = "🔴 CHIUSO" + (" (Weekend)" if weekday >= 5 else "")
forex_status = "🟢 APERTO" if weekday < 5 else "🔴 CHIUSO"

cols = st.columns(5)
with cols[0]:
    st.metric("🕒 Ora", now.strftime("%H:%M"), now.strftime("%d/%m/%Y"))
with cols[1]:
    st.metric("🪙 Crypto", crypto_status)
with cols[2]:
    st.metric("📈 Azioni", stock_status)
with cols[3]:
    st.metric("💱 Forex", forex_status)
with cols[4]:
    st.metric("⚡ Versione", "4.0.0")
st.divider()

# ==================== ROUTING PAGINE ====================
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

# ==================== FOOTER ====================
st.divider()
cols = st.columns(3)
with cols[0]:
    st.caption(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
with cols[1]:
    st.caption("⚡ GOLDEN EYE PRO 4.0")
with cols[2]:
    st.caption("⚠️ Solo scopo educativo")
