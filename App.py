import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="GOLDEN EYE PRO 4.0", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# ==================== TEMA CYBER ORO & ROSSO ====================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp {
        background: radial-gradient(circle at 20% 30%, #3a1a1a, #0f0a0a);
    }
    section[data-testid="stSidebar"], header[data-testid="stHeader"] { display: none !important; }
    
    .cyber-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(20, 10, 10, 0.7);
        backdrop-filter: blur(15px);
        border-radius: 60px;
        padding: 0.7rem 2rem;
        margin: 1rem 2rem 2rem 2rem;
        border: 1px solid rgba(251, 191, 36, 0.3);
        box-shadow: 0 20px 40px -15px rgba(248, 113, 113, 0.3);
    }
    .logo {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(145deg, #fbbf24, #f87171);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .market-info {
        display: flex;
        gap: 2rem;
        color: rgba(255, 235, 235, 0.8);
        font-size: 1rem;
    }
    .info-item {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .gold { color: #fbbf24; text-shadow: 0 0 8px #fbbf24; }
    .red { color: #f87171; text-shadow: 0 0 8px #f87171; }
    
    .menu-container {
        display: flex;
        gap: 1rem;
        margin: 0 2rem 2rem 2rem;
    }
    .menu-btn {
        flex: 1;
        background: rgba(30, 15, 15, 0.6);
        backdrop-filter: blur(10px);
        border: 1.5px solid #fbbf24;
        border-radius: 50px;
        padding: 1rem 0;
        color: #ffebeb;
        font-weight: 700;
        cursor: pointer;
        transition: 0.25s;
        text-transform: uppercase;
    }
    .menu-btn:hover {
        background: rgba(248, 113, 113, 0.2);
        border-color: #f87171;
        transform: translateY(-5px);
        box-shadow: 0 20px 30px -10px #f87171;
    }
    .menu-btn.active {
        background: linear-gradient(145deg, #fbbf24, #f87171);
        border-color: transparent;
        color: #0f0a0a;
        box-shadow: 0 0 25px #f87171;
    }
    .cyber-footer {
        background: rgba(10, 5, 5, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 40px;
        padding: 0.8rem 2rem;
        margin: 3rem 2rem 1rem 2rem;
        border: 1px solid #fbbf24;
        color: #ffd7b3;
        display: flex;
        justify-content: space-between;
        box-shadow: 0 0 20px #f87171;
    }
    div[data-testid="stMetric"] {
        background: rgba(20, 10, 10, 0.5);
        backdrop-filter: blur(5px);
        border-radius: 30px;
        padding: 1rem;
        border: 1px solid #fbbf24;
    }
</style>
""", unsafe_allow_html=True)

# ==================== INIZIALIZZAZIONE SESSION STATE ====================
from config import DEFAULT_WATCHLIST
from storage.watchlist_store import load_watchlist, save_watchlist

if 'watchlist' not in st.session_state:
    st.session_state.watchlist = load_watchlist() or DEFAULT_WATCHLIST
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = st.session_state.watchlist[0]
if 'radar_select' not in st.session_state:
    st.session_state.radar_select = st.session_state.watchlist[0]
if 'current_page' not in st.session_state:
    st.session_state.current_page = "SCAN"
if 'last_scan_time' not in st.session_state:
    st.session_state.last_scan_time = None
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None

# ==================== HEADER CON INFO MERCATO ====================
from utils.helpers import get_market_status
now = datetime.now()
market = get_market_status("BTC-USD", None)  # solo per avere stato generico

header_html = f"""
<div class="cyber-header">
    <div class="logo">👁️ GOLDEN EYE</div>
    <div class="market-info">
        <div class="info-item"><span>🕒</span><span class="gold">{now.strftime("%H:%M")}</span><span>{now.strftime("%d/%m")}</span></div>
        <div class="info-item"><span>🪙</span><span class="gold">24/7</span></div>
        <div class="info-item"><span>📈</span><span class="red">Chiuso</span></div>
        <div class="info-item"><span>💱</span><span class="red">Chiuso</span></div>
        <div class="info-item"><span>⚡</span><span class="gold">4.0.0</span></div>
        <div class="info-item" style="border-left:1px solid #fbbf24; padding-left:1rem;"><span>📊</span><span class="gold">{len(st.session_state.watchlist)}</span></div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ==================== MENU ====================
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
cols = st.columns(len(menu_items))
for i, item in enumerate(menu_items):
    with cols[i]:
        active = "active" if st.session_state.current_page == item else ""
        btn_html = f'<button class="menu-btn {active}" onclick="changePage(\'{item}\')">{item}</button>'
        st.markdown(btn_html, unsafe_allow_html=True)

st.markdown("""
<script>
function changePage(page) {
    const url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}
</script>
""", unsafe_allow_html=True)

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
footer_html = f"""
<div class="cyber-footer">
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
