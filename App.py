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

# CSS GLOBALE - FORZATO
st.markdown("""
<style>
    /* Reset completo */
    .main {
        background: linear-gradient(135deg, #0a0e17 0%, #0f141f 100%);
        padding: 0 !important;
    }
    
    .stApp {
        background: transparent;
    }
    
    /* Nascondi sidebar di Streamlit */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* HEADER FISSO CON MENU - VISIBILE SEMPRE */
    .main-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #1A1A24 !important;
        border-bottom: 2px solid #f0b90b !important;
        padding: 8px 32px !important;
        z-index: 10000 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        height: 70px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
    }
    
    /* Menu container */
    .top-menu {
        display: flex !important;
        gap: 5px !important;
        background: #2C2C3A !important;
        padding: 5px !important;
        border-radius: 40px !important;
        border: 1px solid #f0b90b !important;
    }
    
    /* Pulsanti menu */
    .menu-btn {
        padding: 10px 24px !important;
        border-radius: 30px !important;
        color: #9E9EB0 !important;
        font-size: 14px !important;
        font-weight: 700 !important;
        cursor: pointer !important;
        border: none !important;
        background: transparent !important;
        transition: all 0.3s ease !important;
    }
    
    .menu-btn:hover {
        background: #3C3C4A !important;
        color: white !important;
    }
    
    .menu-btn.active {
        background: #f0b90b !important;
        color: #0A0A0F !important;
    }
    
    /* Logo */
    .logo {
        background: linear-gradient(135deg, #f0b90b, #fbbf24);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 22px;
        font-weight: 800;
    }
    
    /* Watchlist count */
    .watchlist-count {
        background: #2C2C3A;
        padding: 8px 16px;
        border-radius: 30px;
        color: #f0b90b;
        font-weight: 600;
        border: 1px solid #f0b90b;
    }
    
    /* Contenuto principale - distanziato dall'header */
    .main-content {
        margin-top: 90px !important;
        padding: 20px 32px !important;
        margin-bottom: 70px !important;
    }
    
    /* Footer */
    .app-footer {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #1A1A24 !important;
        border-top: 1px solid #f0b90b !important;
        padding: 12px 32px !important;
        color: #9E9EB0 !important;
        font-size: 12px !important;
        display: flex !important;
        justify-content: space-between !important;
        z-index: 10000 !important;
        height: 50px !important;
    }
    
    /* Nascondi header di default di Streamlit */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* Fix per i div che vedi */
    div[style*="border-left: 8px solid"] {
        display: block !important;
        margin: 16px 0 !important;
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

# Menu items
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
menu_icons = ["🔍", "📊", "📋", "⚙️", "🤖", "📡"]

# Costruisci header HTML
header_html = '<div class="main-header">'

# Logo
header_html += '<div style="display: flex; align-items: center; gap: 10px;">'
header_html += '<span class="logo">👁️ GOLDEN EYE</span>'
header_html += '<span style="background: #2C2C3A; padding: 4px 8px; border-radius: 20px; font-size: 10px; color: #f0b90b;">v4.0.0</span>'
header_html += '</div>'

# Menu
header_html += '<div class="top-menu">'
for i, (item, icon) in enumerate(zip(menu_items, menu_icons)):
    active_class = "active" if st.session_state.current_page == item else ""
    header_html += f'<button class="menu-btn {active_class}" onclick="changePage(\'{item}\')">{icon} {item}</button>'
header_html += '</div>'

# Watchlist count
header_html += f'<div class="watchlist-count">📊 {len(st.session_state.watchlist)} assets</div>'
header_html += '</div>'

# JavaScript per navigazione
st.markdown("""
<script>
function changePage(page) {
    const url = new URL(window.location.href);
    url.searchParams.set('page', page);
    window.location.href = url.toString();
}

// Assicura che il menu sia visibile
window.addEventListener('load', function() {
    console.log('Menu loaded');
});
</script>
""" + header_html, unsafe_allow_html=True)

# Gestione parametri URL
query_params = st.query_params
if "page" in query_params:
    st.session_state.current_page = query_params["page"]
if "asset" in query_params:
    st.session_state.selected_asset = query_params["asset"]
    st.session_state.radar_select = query_params["asset"]

# Contenuto principale
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Routing pagine con try/except
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
    st.error(f"Errore nel caricamento della pagina: {e}")
    if st.session_state.get('debug_mode', False):
        st.exception(e)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
