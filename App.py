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

# CSS GLOBALE PER TUTTA L'APP
st.markdown("""
<style>
    /* Reset e base */
    .main {
        background: linear-gradient(135deg, #0a0e17 0%, #0f141f 100%);
        padding: 0 !important;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Nascondi sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Header fisso con glassmorphism */
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: rgba(26, 31, 46, 0.95);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(240, 185, 11, 0.2);
        padding: 8px 32px;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
    }
    
    /* Menu principale */
    .top-menu {
        display: flex;
        gap: 8px;
        background: rgba(44, 44, 58, 0.5);
        padding: 4px;
        border-radius: 40px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        backdrop-filter: blur(5px);
    }
    
    .menu-item {
        padding: 10px 24px;
        border-radius: 30px;
        color: #9E9EB0;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        border: none;
        background: transparent;
    }
    
    .menu-item:hover {
        background: rgba(60, 60, 74, 0.8);
        color: white;
        transform: translateY(-2px);
    }
    
    .menu-item.active {
        background: linear-gradient(135deg, #f0b90b, #fbbf24);
        color: #0A0A0F;
        box-shadow: 0 4px 15px rgba(240, 185, 11, 0.3);
    }
    
    /* Contenuto principale */
    .main-content {
        margin-top: 80px;
        padding: 20px 32px;
        margin-bottom: 60px;
    }
    
    /* Footer */
    .app-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(26, 31, 46, 0.95);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(240, 185, 11, 0.2);
        padding: 12px 32px;
        color: #9E9EB0;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        z-index: 999;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #1e1e2e, #1a1a2a);
        border-radius: 16px;
        padding: 16px;
        border: 1px solid #3c3c4a;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: #f0b90b;
        box-shadow: 0 8px 24px rgba(240, 185, 11, 0.15);
    }
    
    /* Badge */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        background: rgba(240, 185, 11, 0.1);
        border: 1px solid rgba(240, 185, 11, 0.3);
        color: #f0b90b;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-header {
            padding: 8px 16px;
            flex-direction: column;
            gap: 10px;
        }
        
        .top-menu {
            flex-wrap: wrap;
            justify-content: center;
        }
        
        .menu-item {
            padding: 8px 16px;
            font-size: 12px;
        }
        
        .main-content {
            margin-top: 120px;
            padding: 16px;
        }
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
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
if 'app_start_time' not in st.session_state:
    st.session_state.app_start_time = datetime.now()

# Header con menu
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
menu_icons = ["🔍", "📊", "📋", "⚙️", "🤖", "📡"]

menu_html = '<div class="main-header">'
menu_html += '<div style="display: flex; align-items: center; gap: 16px;">'
menu_html += '<span style="background: linear-gradient(135deg, #f0b90b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px; font-weight: 800;">👁️ GOLDEN EYE</span>'
menu_html += f'<span class="badge">v4.0.0</span>'
menu_html += '</div>'

menu_html += '<div class="top-menu">'
for i, (item, icon) in enumerate(zip(menu_items, menu_icons)):
    active_class = "active" if st.session_state.current_page == item else ""
    menu_html += f'<button class="menu-item {active_class}" onclick="changePage(\'{item}\')">{icon} {item}</button>'
menu_html += '</div>'

menu_html += '<div style="color: #9E9EB0; font-size: 14px;">'
menu_html += f'📊 {len(st.session_state.watchlist)} assets'
menu_html += '</div>'
menu_html += '</div>'

# JavaScript per navigazione
st.markdown("""
<script>
function changePage(page) {
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('page', page);
    window.location.search = queryParams.toString();
}
</script>
""" + menu_html, unsafe_allow_html=True)

# Gestione parametri URL
query_params = st.query_params
if "page" in query_params:
    st.session_state.current_page = query_params["page"]

# Contenuto principale
st.markdown('<div class="main-content">', unsafe_allow_html=True)

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
        st.markdown("## 🛠️ Strumenti Avanzati")
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
        st.markdown("## 🤖 Trading")
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
    if st.session_state.debug_mode:
        st.exception(e)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ Golden Eye Pro 4.0 - Trading Intelligence Platform</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
