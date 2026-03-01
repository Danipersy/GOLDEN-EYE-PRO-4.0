import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="GOLDEN EYE PRO 4.0", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# Applica gli stili centralizzati
from ui_streamlit.styles import apply_styles
apply_styles()

# Inizializzazione session state
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

# Header
now = datetime.now()
weekday = now.weekday()
hour = now.hour

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

# Menu
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]

st.markdown('<div class="menu-container">', unsafe_allow_html=True)
cols = st.columns(len(menu_items))
for i, item in enumerate(menu_items):
    with cols[i]:
        if st.button(item, use_container_width=True,
                     type="primary" if st.session_state.current_page == item else "secondary",
                     key=f"menu_{item}"):
            st.session_state.current_page = item
            st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# Contenuto principale (invariato)
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

# Footer
footer_html = f"""
<div class="trader-footer">
    <span>📅 {now.strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
