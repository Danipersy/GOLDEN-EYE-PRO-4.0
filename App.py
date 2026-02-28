import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="GOLDEN EYE PRO 4.0", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# CSS leggero per migliorare l'aspetto (senza strafare)
st.markdown("""
<style>
    /* Sfondo generale */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #1a1f35, #0a0e1a);
    }
    /* Nascondi sidebar e header di default */
    section[data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none;
    }
    /* Spazio per il contenuto */
    .main-content {
        margin-top: 2rem;
        padding: 0 2rem 4rem;
    }
    /* Stile per i metriche in alto */
    .market-info {
        display: flex;
        gap: 2rem;
        align-items: center;
        background: rgba(18,23,40,0.7);
        padding: 0.8rem 2rem;
        border-radius: 40px;
        border: 1px solid #f0b90b30;
        margin-bottom: 2rem;
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

# ==================== INTESTAZIONE ====================
col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("## 👁️ **GOLDEN EYE**")
    st.caption("PRO 4.0")
with col2:
    # Info mercato in una riga
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour

    crypto_status = "🟢 24/7"
    crypto_color = "#00ff88"
    if weekday < 5 and 9 <= hour <= 16:
        stock_status = "🟢 Aperto"
        stock_color = "#00ff88"
    else:
        stock_status = "🔴 Chiuso" + (" (Weekend)" if weekday >= 5 else "")
        stock_color = "#ff3344"
    forex_status = "🟢 Aperto" if weekday < 5 else "🔴 Chiuso"
    forex_color = "#00ff88" if weekday < 5 else "#ff3344"

    cols = st.columns(6)
    with cols[0]:
        st.metric("🕒", now.strftime("%H:%M"), now.strftime("%d/%m"))
    with cols[1]:
        st.metric("🪙", "24/7", delta=None, delta_color="off")
    with cols[2]:
        st.metric("📈", "Aperto" if "Aperto" in stock_status else "Chiuso", delta_color="off")
    with cols[3]:
        st.metric("💱", "Aperto" if forex_status=="🟢 Aperto" else "Chiuso", delta_color="off")
    with cols[4]:
        st.metric("⚡", "4.0.0")
    with cols[5]:
        st.metric("📊", len(st.session_state.watchlist))

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

# ==================== CONTENUTO PRINCIPALE ====================
with st.container():
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
    st.caption("⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform")
with cols[2]:
    st.caption("⚠️ Solo scopo educativo")
