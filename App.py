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

# ==================== HEADER UNICO (logo, menu, info mercato) ====================
now = datetime.now()
weekday = now.weekday()
hour = now.hour

# Stati mercato
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

menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
menu_icons = ["🔍", "📊", "📋", "⚙️", "🤖", "📡"]

# Costruisce i bottoni del menu
menu_buttons = ""
for item, icon in zip(menu_items, menu_icons):
    active_class = "active" if st.session_state.current_page == item else ""
    menu_buttons += f'<button class="menu-btn {active_class}" onclick="changePage(\'{item}\')">{icon} {item}</button>'

header_html = f'''
<div style="display: flex; align-items: center; justify-content: space-between; padding: 0.5rem 2rem; background: rgba(18, 23, 40, 0.95); backdrop-filter: blur(12px); border-bottom: 2px solid #f0b90b; position: fixed; top: 0; left: 0; right: 0; z-index: 10000; flex-wrap: wrap; gap: 1rem; font-family: 'Inter', sans-serif;">
    <!-- Logo -->
    <div style="display: flex; align-items: center; gap: 0.5rem;">
        <span style="font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #f0b90b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">👁️ GOLDEN EYE</span>
        <span style="background: #2c2c3a; padding: 0.2rem 0.8rem; border-radius: 30px; font-size: 0.7rem; color: #f0b90b; border: 1px solid #f0b90b;">PRO 4.0</span>
    </div>
    
    <!-- Menu -->
    <div style="display: flex; gap: 0.3rem; background: rgba(44, 44, 58, 0.6); padding: 0.3rem; border-radius: 40px; border: 1px solid rgba(240, 185, 11, 0.3); flex-wrap: wrap;">
        {menu_buttons}
    </div>
    
    <!-- Info mercato compatte -->
    <div style="display: flex; align-items: center; gap: 1rem; color: #94a3b8; font-size: 0.8rem;">
        <div style="display: flex; align-items: center; gap: 0.3rem;">
            <span>🕒</span>
            <span style="color: #f0b90b; font-weight: 600;">{now.strftime("%H:%M")}</span>
            <span style="font-size: 0.7rem;">{now.strftime("%d/%m")}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.3rem;">
            <span>🪙</span>
            <span style="color: {crypto_color};">24/7</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.3rem;">
            <span>{stock_icon}</span>
            <span style="color: {stock_color};">{'Aperto' if 'APERTO' in stock_status else 'Chiuso'}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.3rem;">
            <span>{forex_icon}</span>
            <span style="color: {forex_color};">{'Aperto' if 'APERTO' in forex_status else 'Chiuso'}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.3rem; border-left: 1px solid #3c3c4a; padding-left: 1rem;">
            <span>⚡</span>
            <span style="color: #f0b90b;">4.0.0</span>
        </div>
        <div style="background: #2c2c3a; border: 1px solid #f0b90b; border-radius: 30px; padding: 0.2rem 1rem; color: #f0b90b; font-weight: 600;">
            📊 {len(st.session_state.watchlist)}
        </div>
    </div>
</div>

<script>
function changePage(page) {{
    const url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}}
</script>

<style>
.menu-btn {{
    padding: 0.5rem 1.2rem;
    border-radius: 30px;
    border: none;
    font-weight: 600;
    font-size: 0.9rem;
    background: transparent;
    color: #9ca3af;
    cursor: pointer;
    transition: 0.2s;
}}
.menu-btn:hover {{
    background: rgba(60, 60, 74, 0.8);
    color: white;
}}
.menu-btn.active {{
    background: #f0b90b;
    color: #0a0a0f;
}}
</style>
'''

# Usa components.html per iniettare l'header in modo sicuro
st.components.v1.html(header_html, height=100)

# Contenitore principale con margine superiore
st.markdown('<div class="main-content" style="margin-top: 6rem; padding: 0 2rem 4rem;">', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f'''
<div style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(18, 23, 40, 0.95); backdrop-filter: blur(12px); border-top: 1px solid #f0b90b; padding: 0.8rem 2rem; color: #94a3b8; font-size: 0.8rem; display: flex; justify-content: space-between; z-index: 9999;">
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
''', unsafe_allow_html=True)
