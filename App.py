import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Aggiungi il percorso corrente per importare i moduli
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="GOLDEN EYE PRO 4.0", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# ==================== CSS TEMA TRADER ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }

    .stApp {
        background: #0B0E14;
    }

    /* Nascondi elementi di default di Streamlit */
    section[data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Header elegante */
    .trader-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #14181F;
        border-radius: 40px;
        padding: 0.6rem 2rem;
        margin: 1rem 2rem 1.5rem 2rem;
        border: 1px solid #2A2F38;
        box-shadow: 0 10px 20px -10px rgba(0,0,0,0.5);
    }

    .logo {
        font-size: 1.8rem;
        font-weight: 700;
        color: #E5E7EB;
        letter-spacing: 0.5px;
    }
    .logo span {
        color: #F0B90B;
        font-weight: 800;
    }

    .market-info {
        display: flex;
        gap: 2rem;
        color: #9CA3AF;
        font-size: 0.9rem;
        font-weight: 500;
    }

    .info-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .info-item .value {
        font-weight: 700;
        color: #F0B90B;
    }
    .info-item .value.green { color: #10B981; }
    .info-item .value.red { color: #EF4444; }

    /* Menu con bottoni nativi personalizzati */
    div[data-testid="column"] button {
        background: #1E242C !important;
        border: 1px solid #2F3540 !important;
        border-radius: 40px !important;
        color: #D1D5DB !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 0 !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
    }

    div[data-testid="column"] button:hover {
        background: #2F3540 !important;
        border-color: #F0B90B !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 8px 16px -8px #F0B90B80 !important;
    }

    div[data-testid="column"] button[kind="primary"] {
        background: #F0B90B !important;
        border-color: #F0B90B !important;
        color: #0B0E14 !important;
        font-weight: 700 !important;
    }

    div[data-testid="column"] button[kind="primary"]:hover {
        background: #FBBF24 !important;
        border-color: #FBBF24 !important;
        box-shadow: 0 8px 20px -8px #F0B90B !important;
    }

    /* Divider personalizzato */
    hr {
        border-color: #2A2F38 !important;
        margin: 1.5rem 2rem !important;
    }

    /* Footer */
    .trader-footer {
        background: #14181F;
        border-radius: 40px;
        padding: 0.6rem 2rem;
        margin: 2rem 2rem 1rem 2rem;
        border: 1px solid #2A2F38;
        color: #9CA3AF;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
    }

    /* Stile per le metriche (già gestito da Streamlit, ma aggiungiamo un tocco) */
    div[data-testid="stMetric"] {
        background: #14181F;
        border-radius: 24px;
        padding: 1rem;
        border: 1px solid #2A2F38;
    }

    div[data-testid="stMetric"] label {
        color: #9CA3AF !important;
    }

    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #F0B90B !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INIZIALIZZAZIONE SESSION STATE ====================
# Import delle funzioni per la watchlist
from storage.watchlist_store import load_watchlist, save_watchlist
from config import DEFAULT_WATCHLIST

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = load_watchlist()
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = st.session_state.watchlist[0] if st.session_state.watchlist else "BTC/USD"
if 'radar_select' not in st.session_state:
    st.session_state.radar_select = st.session_state.selected_asset
if 'current_page' not in st.session_state:
    st.session_state.current_page = "SCAN"
if 'last_scan_time' not in st.session_state:
    st.session_state.last_scan_time = None
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None

# ==================== HEADER ====================
now = datetime.now()
# Determinazione orario e stato mercato (semplificato)
hour = now.hour
weekday = now.weekday()
if weekday < 5 and 9 <= hour <= 16:
    stock_status = ("Aperto", "green")
else:
    stock_status = ("Chiuso" + (" (Weekend)" if weekday >= 5 else ""), "red")

forex_status = ("Aperto" if weekday < 5 else "Chiuso", "green" if weekday < 5 else "red")

header_html = f"""
<div class="trader-header">
    <div class="logo">GOLDEN <span>EYE</span></div>
    <div class="market-info">
        <div class="info-item"><span>🕒</span><span class="value">{now.strftime("%H:%M")}</span><span>{now.strftime("%d/%m")}</span></div>
        <div class="info-item"><span>🪙</span><span class="value green">24/7</span></div>
        <div class="info-item"><span>📈</span><span class="value {stock_status[1]}">{stock_status[0]}</span></div>
        <div class="info-item"><span>💱</span><span class="value {forex_status[1]}">{forex_status[0]}</span></div>
        <div class="info-item"><span>⚡</span><span class="value">4.0.0</span></div>
        <div class="info-item" style="border-left:1px solid #2F3540; padding-left:1rem;"><span>📊</span><span class="value">{len(st.session_state.watchlist)}</span></div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ==================== MENU (BOTTONI STREAMLIT) ====================
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
cols = st.columns(len(menu_items))
for i, item in enumerate(menu_items):
    with cols[i]:
        if st.button(
            item,
            use_container_width=True,
            type="primary" if st.session_state.current_page == item else "secondary",
            key=f"menu_{item}"
        ):
            st.session_state.current_page = item
            st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

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
        st.error(f"Errore nel caricamento della pagina: {e}")

# ==================== FOOTER ====================
footer_html = f"""
<div class="trader-footer">
    <span>📅 {now.strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
