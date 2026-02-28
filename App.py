import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="GOLDEN EYE PRO 4.0", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# Applica stili globali
from ui_streamlit.styles import apply_styles
apply_styles()

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

# ==================== HEADER FISSO CON MENU ====================
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
menu_icons = ["🔍", "📊", "📋", "⚙️", "🤖", "📡"]

# Costruisce l'header HTML
header_html = f'''
<div class="custom-header">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <span class="logo">👁️ GOLDEN EYE</span>
        <span style="background: #2c2c3a; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.7rem; color: #f0b90b; border: 1px solid #f0b90b;">PRO 4.0</span>
    </div>
    <div class="menu-container">
'''
for item, icon in zip(menu_items, menu_icons):
    active = "active" if st.session_state.current_page == item else ""
    header_html += f'<button class="menu-btn {active}" onclick="changePage(\'{item}\')">{icon} {item}</button>'

header_html += f'''
    </div>
    <div class="watchlist-badge">📊 {len(st.session_state.watchlist)} assets</div>
</div>

<script>
function changePage(page) {{
    const url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}}
</script>
'''

st.markdown(header_html, unsafe_allow_html=True)

# ==================== MARKET BAR ====================
now = datetime.now()
weekday = now.weekday()
hour = now.hour

# Determinazione stati
crypto_status = "🟢 APERTO 24/7"
crypto_color = "#00ff88"
if weekday < 5 and 9 <= hour <= 16:
    stock_status = "🟢 APERTO"
    stock_color = "#00ff88"
    stock_icon = "📈"
else:
    stock_status = "🔴 CHIUSO" + (" (Weekend)" if weekday >= 5 else "")
    stock_color = "#ff3344"
    stock_icon = "🔒"
forex_status = "🟢 APERTO" if weekday < 5 else "🔴 CHIUSO"
forex_color = "#00ff88" if weekday < 5 else "#ff3344"
forex_icon = "💱" if weekday < 5 else "🔒"

market_html = f'''
<div class="market-bar">
    <div class="market-item">
        <span class="market-label">🕒 Ora</span>
        <div class="market-value">
            <span style="color: #f0b90b;">{now.strftime("%H:%M")}</span>
            <span style="font-size: 0.9rem; color: #94a3b8;">{now.strftime("%d/%m/%Y")}</span>
        </div>
    </div>
    <div class="market-item">
        <span class="market-label">🪙 Crypto</span>
        <div class="market-value">
            <span>🪙</span>
            <span style="color: {crypto_color};">{crypto_status}</span>
        </div>
    </div>
    <div class="market-item">
        <span class="market-label">📈 Azioni</span>
        <div class="market-value">
            <span>{stock_icon}</span>
            <span style="color: {stock_color};">{stock_status}</span>
        </div>
    </div>
    <div class="market-item">
        <span class="market-label">💱 Forex</span>
        <div class="market-value">
            <span>{forex_icon}</span>
            <span style="color: {forex_color};">{forex_status}</span>
        </div>
    </div>
    <div class="market-item">
        <span class="market-label">⚡ Versione</span>
        <div class="market-value">
            <span style="color: #f0b90b;">4.0.0</span>
        </div>
    </div>
</div>
'''
st.markdown(market_html, unsafe_allow_html=True)

# Contenitore principale
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Routing pagine (come prima)
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

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f'''
<div class="custom-footer">
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
''', unsafe_allow_html=True)
