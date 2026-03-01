import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="GOLDEN EYE PRO 4.0", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# CSS personalizzato per un look professionale
st.markdown("""
<style>
    /* Sfondo con gradiente */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #1a1f35, #0a0e1a);
    }
    /* Nascondi elementi di default di Streamlit */
    section[data-testid="stSidebar"], header[data-testid="stHeader"] {
        display: none;
    }
    /* Stile per l'header */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(18,23,40,0.8);
        backdrop-filter: blur(10px);
        padding: 0.8rem 2rem;
        border-radius: 60px;
        border: 1px solid rgba(240,185,11,0.3);
        margin: 1rem 2rem 2rem 2rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.5);
    }
    .logo {
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f0b90b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .market-info {
        display: flex;
        gap: 1.5rem;
        color: #94a3b8;
        font-size: 0.9rem;
    }
    .market-info-item {
        display: flex;
        align-items: center;
        gap: 0.4rem;
    }
    .market-info-item span:last-child {
        font-weight: 600;
    }
    /* Stile per i pulsanti del menu */
    div[data-testid="column"] button {
        border-radius: 40px !important;
        font-weight: 600 !important;
        padding: 0.6rem 0 !important;
        transition: all 0.2s ease !important;
        border: none !important;
    }
    div[data-testid="column"] button[kind="primary"] {
        background: linear-gradient(135deg, #f0b90b, #fbbf24) !important;
        color: #0a0a0f !important;
        box-shadow: 0 4px 12px rgba(240,185,11,0.3) !important;
    }
    div[data-testid="column"] button[kind="secondary"] {
        background: rgba(44,44,58,0.6) !important;
        color: #9ca3af !important;
        backdrop-filter: blur(5px);
        border: 1px solid rgba(240,185,11,0.2) !important;
    }
    div[data-testid="column"] button[kind="secondary"]:hover {
        background: rgba(60,60,74,0.8) !important;
        color: white !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0,0,0,0.3);
    }
    div[data-testid="column"] button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(240,185,11,0.5) !important;
    }
    /* Stile per le card dei risultati (già in card.py, ma assicuriamo coerenza) */
    .custom-card {
        background: linear-gradient(135deg, #1e2338, #161b2f);
        border-radius: 24px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 6px solid;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: 0.2s;
    }
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
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

# ==================== HEADER CON LOGO E INFO MERCATO ====================
now = datetime.now()
weekday = now.weekday()
hour = now.hour

# Stati mercato
crypto_color = "#00ff88"
if weekday < 5 and 9 <= hour <= 16:
    stock_status = "Aperto"
    stock_color = "#00ff88"
    stock_icon = "📈"
else:
    stock_status = "Chiuso" + (" (Weekend)" if weekday >= 5 else "")
    stock_color = "#ff3344"
    stock_icon = "🔒"
forex_status = "Aperto" if weekday < 5 else "Chiuso"
forex_color = "#00ff88" if weekday < 5 else "#ff3344"
forex_icon = "💱" if weekday < 5 else "🔒"

header_html = f"""
<div class="header-container">
    <div class="logo">👁️ GOLDEN EYE</div>
    <div class="market-info">
        <div class="market-info-item">
            <span>🕒</span>
            <span style="color:#f0b90b;">{now.strftime("%H:%M")}</span>
            <span style="font-size:0.8rem;">{now.strftime("%d/%m")}</span>
        </div>
        <div class="market-info-item">
            <span>🪙</span>
            <span style="color:{crypto_color};">24/7</span>
        </div>
        <div class="market-info-item">
            <span>{stock_icon}</span>
            <span style="color:{stock_color};">{stock_status}</span>
        </div>
        <div class="market-info-item">
            <span>{forex_icon}</span>
            <span style="color:{forex_color};">{forex_status}</span>
        </div>
        <div class="market-info-item">
            <span>⚡</span>
            <span style="color:#f0b90b;">4.0.0</span>
        </div>
        <div class="market-info-item" style="border-left:1px solid #3c3c4a; padding-left:1rem;">
            <span>📊</span>
            <span style="color:#f0b90b;">{len(st.session_state.watchlist)}</span>
        </div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

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
