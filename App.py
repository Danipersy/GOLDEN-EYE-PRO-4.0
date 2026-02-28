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

# CSS GLOBALE - RAFFORZATO
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
    
    /* HEADER FISSO - FORZATO */
    .main-header {
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: rgba(26, 31, 46, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-bottom: 1px solid rgba(240, 185, 11, 0.2) !important;
        padding: 8px 32px !important;
        z-index: 9999 !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5) !important;
        height: 64px !important;
    }
    
    /* Menu - FORZATO */
    .top-menu {
        display: flex !important;
        gap: 8px !important;
        background: rgba(44, 44, 58, 0.5) !important;
        padding: 4px !important;
        border-radius: 40px !important;
        border: 1px solid rgba(240, 185, 11, 0.2) !important;
        backdrop-filter: blur(5px) !important;
    }
    
    .menu-item {
        padding: 8px 20px !important;
        border-radius: 30px !important;
        color: #9E9EB0 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        border: none !important;
        background: transparent !important;
        line-height: normal !important;
    }
    
    .menu-item:hover {
        background: rgba(60, 60, 74, 0.8) !important;
        color: white !important;
        transform: translateY(-2px) !important;
    }
    
    .menu-item.active {
        background: linear-gradient(135deg, #f0b90b, #fbbf24) !important;
        color: #0A0A0F !important;
        box-shadow: 0 4px 15px rgba(240, 185, 11, 0.3) !important;
    }
    
    /* Contenuto principale - con margine per evitare header */
    .main-content {
        margin-top: 80px !important;
        padding: 20px 32px !important;
        margin-bottom: 60px !important;
    }
    
    /* Footer */
    .app-footer {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: rgba(26, 31, 46, 0.95) !important;
        backdrop-filter: blur(10px) !important;
        border-top: 1px solid rgba(240, 185, 11, 0.2) !important;
        padding: 12px 32px !important;
        color: #9E9EB0 !important;
        font-size: 12px !important;
        display: flex !important;
        justify-content: space-between !important;
        z-index: 9999 !important;
        height: 50px !important;
    }
    
    /* Assicura che il contenuto non venga nascosto */
    .stApp > header {
        display: none !important;
    }
    
    /* Per debug - rimuovi dopo */
    .main-header {
        border: 2px solid red !important;
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
if 'detail_data' not in st.session_state:
    st.session_state.detail_data = None

# Menu items
menu_items = ["SCAN", "DETTAGLIO", "WATCHLIST", "STRUMENTI", "TRADING", "API"]
menu_icons = ["🔍", "📊", "📋", "⚙️", "🤖", "📡"]

# Costruisci HTML menu con stile inline per sicurezza
menu_html = '<div class="main-header" style="position: fixed; top: 0; left: 0; right: 0; background: rgba(26, 31, 46, 0.95); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(240, 185, 11, 0.2); padding: 8px 32px; z-index: 9999; display: flex; justify-content: space-between; align-items: center; height: 64px;">'

# Logo
menu_html += '<div style="display: flex; align-items: center; gap: 16px;">'
menu_html += '<span style="background: linear-gradient(135deg, #f0b90b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px; font-weight: 800;">👁️ GOLDEN EYE</span>'
menu_html += '</div>'

# Menu items
menu_html += '<div style="display: flex; gap: 8px; background: rgba(44, 44, 58, 0.5); padding: 4px; border-radius: 40px; border: 1px solid rgba(240, 185, 11, 0.2);">'

for i, (item, icon) in enumerate(zip(menu_items, menu_icons)):
    active_class = "active"
    bg_color = "linear-gradient(135deg, #f0b90b, #fbbf24)" if st.session_state.current_page == item else "transparent"
    text_color = "#0A0A0F" if st.session_state.current_page == item else "#9E9EB0"
    
    menu_html += f'<button onclick="changePage(\'{item}\')" style="padding: 8px 20px; border-radius: 30px; color: {text_color}; font-size: 14px; font-weight: 600; cursor: pointer; border: none; background: {bg_color}; transition: all 0.3s ease;">{icon} {item}</button>'

menu_html += '</div>'

# Watchlist count
menu_html += f'<div style="color: #9E9EB0; font-size: 14px;">📊 {len(st.session_state.watchlist)} assets</div>'
menu_html += '</div>'

# JavaScript per navigazione
st.markdown("""
<script>
function changePage(page) {
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('page', page);
    window.location.search = queryParams.toString();
}

// Forza il refresh del menu
document.addEventListener('DOMContentLoaded', function() {
    console.log('Menu loaded');
});
</script>
""" + menu_html, unsafe_allow_html=True)

# Gestione parametri URL
query_params = st.query_params
if "page" in query_params:
    st.session_state.current_page = query_params["page"]
if "asset" in query_params:
    st.session_state.selected_asset = query_params["asset"]
    st.session_state.radar_select = query_params["asset"]

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

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div class='app-footer' style="position: fixed; bottom: 0; left: 0; right: 0; background: rgba(26, 31, 46, 0.95); backdrop-filter: blur(10px); border-top: 1px solid rgba(240, 185, 11, 0.2); padding: 12px 32px; color: #9E9EB0; font-size: 12px; display: flex; justify-content: space-between; z-index: 9999; height: 50px;">
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>⚡ GOLDEN EYE PRO 4.0</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
