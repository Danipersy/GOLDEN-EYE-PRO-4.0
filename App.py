import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import sys
import os
from pathlib import Path

# ============================================
# CONFIGURAZIONE PATH - QUESTA È LA PARTE IMPORTANTE!
# ============================================
# Aggiungi la directory corrente al path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Aggiungi anche ui_streamlit al path esplicitamente
ui_streamlit_path = current_dir / "ui_streamlit"
if str(ui_streamlit_path) not in sys.path:
    sys.path.insert(0, str(ui_streamlit_path))

# Debug: stampa i path per vedere cosa sta succedendo
print("🔍 Path caricati:")
for p in sys.path[:3]:
    print(f"  - {p}")

# Configurazione pagina
st.set_page_config(
    page_title="GOLDEN EYE PRO",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# FUNZIONE DI IMPORT MIGLIORATA
# ============================================
def import_page(module_name):
    """Importa dinamicamente una pagina cercando in diverse posizioni"""
    
    # Lista di possibili percorsi da provare
    possible_imports = [
        f"ui_streamlit.pages.{module_name}",  # ui_streamlit.pages.scan
        f"pages.{module_name}",                # pages.scan
        module_name,                            # scan
        f"ui_streamlit.{module_name}"           # ui_streamlit.scan
    ]
    
    # Lista di possibili nomi di funzioni
    possible_functions = ['show_page', 'show', 'render', 'main', f'show_{module_name}']
    
    for import_path in possible_imports:
        try:
            print(f"🔄 Provando a importare: {import_path}")
            module = __import__(import_path, fromlist=[''])
            
            # Cerca la funzione
            for func_name in possible_functions:
                if hasattr(module, func_name):
                    print(f"✅ Trovato {func_name} in {import_path}")
                    return getattr(module, func_name)
            
            # Se non trova funzioni specifiche, ritorna il modulo
            print(f"⚠️ Modulo {import_path} importato ma nessuna funzione riconosciuta")
            return lambda: None  # funzione vuota
            
        except ImportError as e:
            print(f"❌ Fallito {import_path}: {e}")
            continue
        except Exception as e:
            print(f"❌ Errore inaspettato con {import_path}: {e}")
            continue
    
    print(f"❌ Nessun import riuscito per {module_name}")
    return None

# ============================================
# CSS BASE
# ============================================
st.markdown("""
<style>
    /* Reset e base */
    .main {
        background: #0A0A0F;
        padding: 0 !important;
    }
    
    /* Nascondi sidebar */
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Header fisso */
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
    
    /* Menu in alto */
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
        text-decoration: none;
    }
    
    .menu-item:hover {
        background: #3C3C4A;
        color: white;
    }
    
    .menu-item.active {
        background: #FFD600;
        color: #0A0A0F;
    }
    
    /* Contenuto principale */
    .main-content {
        margin-top: 70px;
        padding: 20px 32px;
        margin-bottom: 50px;
    }
    
    /* Watchlist rapida */
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
    
    /* Footer */
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
# SESSION STATE
# ============================================
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
    
if 'selected_asset' not in st.session_state:
    st.session_state.selected_asset = 'BTC-USD'
    
if 'current_page' not in st.session_state:
    st.session_state.current_page = "SCAN"

# ============================================
# HEADER FISSO CON MENU
# ============================================
menu_items = [
    {"name": "SCAN", "icon": "🔍", "page": "SCAN"},
    {"name": "DETTAGLIO", "icon": "📊", "page": "DETTAGLIO"},
    {"name": "WATCHLIST", "icon": "📋", "page": "WATCHLIST"},
    {"name": "STRUMENTI", "icon": "⚙️", "page": "STRUMENTI"},
    {"name": "TRADING", "icon": "🤖", "page": "TRADING"}
]

# Header HTML
menu_html = '<div class="main-header">'
menu_html += '<div style="display: flex; align-items: center; gap: 16px;">'
menu_html += '<span style="background: linear-gradient(135deg, #FFD600, #FF3D00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 20px; font-weight: 800;">👁️ GOLDEN EYE</span>'
menu_html += '<span style="background: #2C2C3A; padding: 4px 8px; border-radius: 20px; font-size: 10px; color: #9E9EB0;">v2.0.0</span>'
menu_html += '</div>'

# Menu items
menu_html += '<div class="top-menu">'
for item in menu_items:
    active_class = "active" if st.session_state.current_page == item["page"] else ""
    menu_html += f'<div class="menu-item {active_class}" onclick="changePage(\'{item["page"]}\')">{item["icon"]} {item["name"]}</div>'
menu_html += '</div>'

# Quick watchlist
menu_html += '<div class="quick-watchlist">'
for asset in st.session_state.watchlist[:3]:
    change = np.random.normal(0, 2)
    color = "#00C853" if change > 0 else "#FF3D00"
    menu_html += f'<div class="quick-asset" onclick="selectAsset(\'{asset}\')">{asset}<span style="color: {color}; margin-left: 4px;">{change:.1f}%</span></div>'
menu_html += '</div>'
menu_html += '</div>'

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
""" + menu_html, unsafe_allow_html=True)

# Gestione parametri URL
query_params = st.query_params
if "page" in query_params:
    st.session_state.current_page = query_params["page"]
if "asset" in query_params:
    st.session_state.selected_asset = query_params["asset"]

# ============================================
# DEBUG INFO (RIMUOVI DOPO AVER RISOLTO)
# ============================================
with st.expander("🔧 Debug Info", expanded=False):
    st.write("**Current Directory:**", current_dir)
    st.write("**UI Streamlit Path:**", ui_streamlit_path)
    st.write("**Sys Path:**", sys.path[:5])
    
    # Lista file in ui_streamlit/pages
    pages_dir = ui_streamlit_path / "pages"
    if pages_dir.exists():
        st.write("**File in ui_streamlit/pages:**")
        files = list(pages_dir.glob("*.py"))
        for f in files:
            st.write(f"  - {f.name}")
    else:
        st.write("**❌ Cartella ui_streamlit/pages non trovata!**")

# ============================================
# CONTENUTO PRINCIPALE
# ============================================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Routing pagine
if st.session_state.current_page == "SCAN":
    show_func = import_page("scan")
    if show_func:
        with st.spinner("Caricamento SCAN..."):
            show_func()
    else:
        st.warning("🔍 Pagina SCAN non trovata, uso mock data")
        # Mock scan
        st.subheader("🔍 SCAN Mercati")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("BTC-USD", "$52,345", "+2.3%")
        with col2:
            st.metric("ETH-USD", "$3,124", "+1.2%")
        with col3:
            st.metric("BNB-USD", "$412", "-0.5%")
            
elif st.session_state.current_page == "DETTAGLIO":
    show_func = import_page("dettaglio")
    if show_func:
        with st.spinner(f"Caricamento {st.session_state.selected_asset}..."):
            show_func(st.session_state.selected_asset)
    else:
        st.subheader(f"📊 Dettaglio {st.session_state.selected_asset}")
        
        # Mock grafico
        dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
        prices = np.random.randn(100).cumsum() + 100
        fig = go.Figure(data=go.Scatter(x=dates, y=prices, mode='lines'))
        fig.update_layout(template='plotly_dark')
        st.plotly_chart(fig, use_container_width=True)
        
elif st.session_state.current_page == "WATCHLIST":
    show_func = import_page("watchlist")
    if show_func:
        with st.spinner("Caricamento Watchlist..."):
            show_func()
    else:
        st.subheader("📋 Watchlist")
        for asset in st.session_state.watchlist:
            col1, col2, col3, col4 = st.columns([2,2,1,1])
            with col1:
                st.write(asset)
            with col2:
                price = np.random.randn()*1000 + 1000
                st.write(f"${price:.2f}")
            with col3:
                change = np.random.normal(0, 2)
                color = "🟢" if change > 0 else "🔴"
                st.write(f"{color} {change:.1f}%")
            with col4:
                if st.button("📊", key=f"view_{asset}"):
                    st.session_state.selected_asset = asset
                    st.session_state.current_page = "DETTAGLIO"
                    st.rerun()
                    
elif st.session_state.current_page == "STRUMENTI":
    st.subheader("⚙️ Strumenti")
    tabs = st.tabs(["📊 Validazione", "🎯 Ottimizzazione", "💰 Money Management"])
    
    with tabs[0]:
        show_func = import_page("validazione")
        if show_func:
            show_func()
        else:
            st.info("📊 Pannello Validazione (mock)")
            
    with tabs[1]:
        show_func = import_page("ottimizzazione")
        if show_func:
            show_func()
        else:
            st.info("🎯 Pannello Ottimizzazione (mock)")
            
    with tabs[2]:
        show_func = import_page("money_management")
        if show_func:
            show_func()
        else:
            st.info("💰 Pannello Money Management (mock)")
            
elif st.session_state.current_page == "TRADING":
    st.subheader("🤖 Trading")
    tabs = st.tabs(["📝 Paper Trading", "🧠 AutoTrader"])
    
    with tabs[0]:
        show_func = import_page("paper_trading")
        if show_func:
            show_func()
        else:
            st.info("📝 Paper Trading (mock)")
            
    with tabs[1]:
        show_func = import_page("auto_trader")
        if show_func:
            show_func()
        else:
            st.info("🧠 AutoTrader (mock)")

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
