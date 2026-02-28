import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path

# ============================================
# CONFIGURAZIONE PATH
# ============================================
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Configurazione pagina
st.set_page_config(
    page_title="GOLDEN EYE PRO",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# SESSION STATE
# ============================================
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
    
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = 'BTC-USD'
    
if 'current_page' not in st.session_state:
    st.session_state.current_page = "SCAN"
    
if 'radar_select' not in st.session_state:
    st.session_state.radar_select = 'BTC-USD'

# ============================================
# FUNZIONE DI IMPORT CORRETTA
# ============================================
def import_page(module_name):
    """Importa dinamicamente una pagina"""
    try:
        # Mappa dei nomi dei moduli alle funzioni
        module_map = {
            "scan": ("ui_streamlit.pages.scan", "show_page"),
            "dettaglio": ("ui_streamlit.pages.dettaglio", "show_page"),
            "watchlist": ("ui_streamlit.pages.watchlist", "show_page"),
            "validazione": ("ui_streamlit.pages.validazione", "render"),
            "ottimizzazione": ("ui_streamlit.pages.ottimizzazione", "render"),
            "money_management": ("ui_streamlit.pages.money_management", "render"),
            "paper_trading": ("ui_streamlit.pages.paper_trading", "render"),
            "auto_trader": ("ui_streamlit.pages.auto_trader", "render"),
            "info": ("ui_streamlit.pages.info", "render"),
            "settings": ("ui_streamlit.pages.settings", "render"),
        }
        
        if module_name in module_map:
            module_path, func_name = module_map[module_name]
            module = __import__(module_path, fromlist=[func_name])
            return getattr(module, func_name, None)
        
        return None
        
    except ImportError as e:
        print(f"❌ Errore import {module_name}: {e}")
        return None
    except Exception as e:
        print(f"❌ Errore: {e}")
        return None

# ============================================
# CSS BASE
# ============================================
st.markdown("""
<style>
    .main {
        background: #0A0A0F;
        padding: 0 !important;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .main-header {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        background: #1A1A24;
        border-bottom: 1px solid #3C3C4A;
        padding: 8px 32px;
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
        backdrop-filter: blur(10px);
    }
    .top-menu {
        display: flex;
        gap: 8px;
        background: #2C2C3A;
        padding: 4px;
        border-radius: 40px;
        border: 1px solid #3C3C4A;
    }
    .menu-item {
        padding: 10px 24px;
        border-radius: 30px;
        color: #9E9EB0;
        font-size: 14px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    .menu-item:hover {
        background: #3C3C4A;
        color: white;
    }
    .menu-item.active {
        background: #FFD600;
        color: #0A0A0F;
    }
    .main-content {
        margin-top: 70px;
        padding: 20px 32px;
        margin-bottom: 50px;
    }
    .quick-watchlist {
        display: flex;
        gap: 12px;
        background: #2C2C3A;
        padding: 8px 16px;
        border-radius: 40px;
        border: 1px solid #3C3C4A;
    }
    .quick-asset {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }
    .quick-asset:hover {
        background: #3C3C4A;
    }
    .app-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: #1A1A24;
        border-top: 1px solid #3C3C4A;
        padding: 12px 32px;
        color: #9E9EB0;
        font-size: 12px;
        display: flex;
        justify-content: space-between;
        z-index: 999;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================
menu_items = [
    {"name": "SCAN", "icon": "🔍", "page": "SCAN"},
    {"name": "DETTAGLIO", "icon": "📊", "page": "DETTAGLIO"},
    {"name": "WATCHLIST", "icon": "📋", "page": "WATCHLIST"},
    {"name": "STRUMENTI", "icon": "⚙️", "page": "STRUMENTI"},
    {"name": "TRADING", "icon": "🤖", "page": "TRADING"}
]

# JavaScript per gestire i click
st.markdown("""
<script>
function changePage(page) {
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('page', page);
    window.location.search = queryParams.toString();
}

function selectAsset(asset) {
    const queryParams = new URLSearchParams(window.location.search);
    queryParams.set('asset', asset);
    queryParams.set('page', 'DETTAGLIO');
    window.location.search = queryParams.toString();
}
</script>
""", unsafe_allow_html=True)

# Header HTML
menu_html = '<div class="main-header">'
menu_html += '<div style="display: flex; align-items: center; gap: 16px;">'
menu_html += '<span style="background: linear-gradient(135deg, #FFD600, #FF3D00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 20px; font-weight: 800;">👁️ GOLDEN EYE</span>'
menu_html += '<span style="background: #2C2C3A; padding: 4px 8px; border-radius: 20px; font-size: 10px; color: #9E9EB0;">v4.0.0</span>'
menu_html += '</div>'
menu_html += '<div class="top-menu">'
for item in menu_items:
    active_class = "active" if st.session_state.current_page == item["page"] else ""
    menu_html += f'<div class="menu-item {active_class}" onclick="changePage(\'{item["page"]}\')">{item["icon"]} {item["name"]}</div>'
menu_html += '</div>'
menu_html += '<div class="quick-watchlist">'
for asset in st.session_state.watchlist[:3]:
    menu_html += f'<div class="quick-asset" onclick="selectAsset(\'{asset}\')">{asset}</div>'
menu_html += '</div>'
menu_html += '</div>'

st.markdown(menu_html, unsafe_allow_html=True)

# Gestione parametri URL
query_params = st.query_params
if "page" in query_params:
    st.session_state.current_page = query_params["page"]
if "asset" in query_params:
    st.session_state.selected_asset = query_params["asset"]
    st.session_state.radar_select = query_params["asset"]

# ============================================
# CONTENUTO PRINCIPALE
# ============================================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Routing pagine
try:
    if st.session_state.current_page == "SCAN":
        show_func = import_page("scan")
        if show_func:
            show_func()
        else:
            st.warning("Pagina SCAN non disponibile")
            
    elif st.session_state.current_page == "DETTAGLIO":
        show_func = import_page("dettaglio")
        if show_func:
            show_func(st.session_state.selected_asset)
        else:
            st.warning("Pagina DETTAGLIO non disponibile")
            
    elif st.session_state.current_page == "WATCHLIST":
        show_func = import_page("watchlist")
        if show_func:
            show_func()
        else:
            st.warning("Pagina WATCHLIST non disponibile")
            
    elif st.session_state.current_page == "STRUMENTI":
        st.subheader("⚙️ Strumenti")
        tabs = st.tabs(["📊 Validazione", "🎯 Ottimizzazione", "💰 Money Management"])
        
        with tabs[0]:
            show_func = import_page("validazione")
            if show_func:
                show_func()
            else:
                st.info("Validazione non disponibile")
        
        with tabs[1]:
            show_func = import_page("ottimizzazione")
            if show_func:
                show_func()
            else:
                st.info("Ottimizzazione non disponibile")
        
        with tabs[2]:
            show_func = import_page("money_management")
            if show_func:
                show_func()
            else:
                st.info("Money Management non disponibile")
                
    elif st.session_state.current_page == "TRADING":
        st.subheader("🤖 Trading")
        tabs = st.tabs(["📝 Paper Trading", "🧠 AutoTrader"])
        
        with tabs[0]:
            show_func = import_page("paper_trading")
            if show_func:
                show_func()
            else:
                st.info("Paper Trading non disponibile")
        
        with tabs[1]:
            show_func = import_page("auto_trader")
            if show_func:
                show_func()
            else:
                st.info("AutoTrader non disponibile")
                
except Exception as e:
    st.error(f"Errore: {e}")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>📊 Watchlist: {len(st.session_state.watchlist)} assets</span>
    <span>⚡ {st.session_state.current_page}</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
