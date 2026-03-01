import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

st.set_page_config(page_title="GOLDEN EYE PRO 4.0", page_icon="👁️", layout="wide", initial_sidebar_state="collapsed")

# ==================== SELEZIONE TEMA ====================
temi = {
    "Futuristico (blu/viola)": {
        "bg_start": "#0f172a",
        "bg_end": "#1e293b",
        "accent1": "#38bdf8",
        "accent2": "#a78bfa",
        "text": "#e2e8f0",
        "header_bg": "rgba(15,23,42,0.7)",
        "btn_bg": "rgba(56,189,248,0.1)",
        "btn_border": "#38bdf8",
        "btn_active": "linear-gradient(135deg, #38bdf8, #a78bfa)"
    },
    "Elegante (oro/grafite)": {
        "bg_start": "#1e293b",
        "bg_end": "#0f172a",
        "accent1": "#fbbf24",
        "accent2": "#d97706",
        "text": "#f1f5f9",
        "header_bg": "rgba(30,41,59,0.7)",
        "btn_bg": "rgba(251,191,36,0.1)",
        "btn_border": "#fbbf24",
        "btn_active": "linear-gradient(135deg, #fbbf24, #d97706)"
    },
    "Natura (verde/blu)": {
        "bg_start": "#0e2a47",
        "bg_end": "#1a3a5f",
        "accent1": "#10b981",
        "accent2": "#34d399",
        "text": "#e2e8f0",
        "header_bg": "rgba(14,42,71,0.7)",
        "btn_bg": "rgba(16,185,129,0.1)",
        "btn_border": "#10b981",
        "btn_active": "linear-gradient(135deg, #10b981, #0e2a47)"
    },
    "Minimal (monocromatico)": {
        "bg_start": "#1e1e1e",
        "bg_end": "#2d2d2d",
        "accent1": "#ffffff",
        "accent2": "#cccccc",
        "text": "#f0f0f0",
        "header_bg": "rgba(30,30,30,0.7)",
        "btn_bg": "transparent",
        "btn_border": "#ffffff",
        "btn_active": "#ffffff"
    },
    "Cyberpunk (neon)": {
        "bg_start": "#111827",
        "bg_end": "#1f2937",
        "accent1": "#00ffff",
        "accent2": "#ff00ff",
        "text": "#f0f0f0",
        "header_bg": "rgba(17,24,39,0.7)",
        "btn_bg": "rgba(0,255,255,0.1)",
        "btn_border": "#00ffff",
        "btn_active": "linear-gradient(135deg, #00ffff, #ff00ff)"
    }
}

if "tema_corrente" not in st.session_state:
    st.session_state.tema_corrente = "Futuristico (blu/viola)"

tema = temi[st.session_state.tema_corrente]

# CSS dinamico basato sul tema selezionato
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * {{ font-family: 'Inter', sans-serif; }}
    .stApp {{
        background: linear-gradient(145deg, {tema['bg_start']} 0%, {tema['bg_end']} 100%);
    }}
    section[data-testid="stSidebar"], header[data-testid="stHeader"] {{
        display: none;
    }}
    .modern-header {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: {tema['header_bg']};
        backdrop-filter: blur(12px);
        border-radius: 40px;
        padding: 0.7rem 2rem;
        margin: 1rem 2rem 2rem 2rem;
        border: 1px solid {tema['accent1']}40;
        box-shadow: 0 20px 30px -10px rgba(0,0,0,0.5);
    }}
    .logo {{
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, {tema['accent1']}, {tema['accent2']});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}
    .market-info {{
        display: flex;
        gap: 2rem;
        color: {tema['text']}aa;
        font-size: 0.95rem;
    }}
    .info-item {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .info-value {{ font-weight: 600; }}
    .green {{ color: #4ade80; }}
    .red {{ color: #f87171; }}
    .blue {{ color: #38bdf8; }}
    .purple {{ color: #c084fc; }}
    .menu-row {{
        display: flex;
        gap: 0.8rem;
        margin: 0 2rem 1.5rem 2rem;
    }}
    .menu-btn {{
        flex: 1;
        background: {tema['btn_bg']};
        backdrop-filter: blur(8px);
        border: 1px solid {tema['btn_border']}40;
        border-radius: 40px;
        padding: 0.9rem 0;
        color: {tema['text']};
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.2s ease;
        box-shadow: 0 8px 12px -6px rgba(0,0,0,0.4);
    }}
    .menu-btn:hover {{
        background: {tema['accent1']}20;
        color: white;
        transform: translateY(-3px);
        border-color: {tema['accent1']};
        box-shadow: 0 12px 20px -8px {tema['accent1']}80;
    }}
    .menu-btn.active {{
        background: {tema['btn_active']};
        color: white;
        border: none;
        box-shadow: 0 12px 24px -8px {tema['accent1']};
    }}
    .modern-footer {{
        background: {tema['header_bg']};
        backdrop-filter: blur(8px);
        border-radius: 30px;
        padding: 0.6rem 2rem;
        margin: 2rem 2rem 1rem 2rem;
        border: 1px solid {tema['accent1']}40;
        color: {tema['text']}aa;
        font-size: 0.85rem;
        display: flex;
        justify-content: space-between;
    }}
    div[data-testid="stMetric"] {{
        background: {tema['btn_bg']};
        border-radius: 20px;
        padding: 0.8rem;
        border: 1px solid {tema['accent1']}40;
        backdrop-filter: blur(4px);
    }}
    div[data-testid="stMetric"] label {{
        color: {tema['text']}aa !important;
    }}
    hr {{
        border-color: {tema['accent1']}40 !important;
    }}
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

# ==================== SELEZIONE TEMA (solo in sviluppo) ====================
with st.sidebar:
    st.selectbox("🎨 Seleziona tema", list(temi.keys()), key="tema_corrente")

# ==================== HEADER ====================
now = datetime.now()
weekday = now.weekday()
hour = now.hour

if weekday < 5 and 9 <= hour <= 16:
    stock_status = "Aperto"
    stock_color = "green"
else:
    stock_status = "Chiuso" + (" (Weekend)" if weekday >= 5 else "")
    stock_color = "red"

forex_status = "Aperto" if weekday < 5 else "Chiuso"
forex_color = "green" if weekday < 5 else "red"

header_html = f"""
<div class="modern-header">
    <div class="logo">👁️ GOLDEN EYE</div>
    <div class="market-info">
        <div class="info-item"><span>🕒</span><span class="info-value blue">{now.strftime("%H:%M")}</span><span style="font-size:0.8rem;">{now.strftime("%d/%m")}</span></div>
        <div class="info-item"><span>🪙</span><span class="info-value green">24/7</span></div>
        <div class="info-item"><span>📈</span><span class="info-value {stock_color}">{stock_status}</span></div>
        <div class="info-item"><span>💱</span><span class="info-value {forex_color}">{forex_status}</span></div>
        <div class="info-item"><span>⚡</span><span class="info-value purple">4.0.0</span></div>
        <div class="info-item" style="border-left:1px solid #334155; padding-left:1rem;"><span>📊</span><span class="info-value blue">{len(st.session_state.watchlist)}</span></div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ==================== MENU PULSANTI ====================
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
cols = st.columns(len(menu_items))
for i, item in enumerate(menu_items):
    with cols[i]:
        active_class = "active" if st.session_state.current_page == item else ""
        btn_html = f'<button class="menu-btn {active_class}" onclick="changePage(\'{item}\')">{item}</button>'
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

# ==================== CONTENUTO PAGINE ====================
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
<div class="modern-footer">
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0 • Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)
