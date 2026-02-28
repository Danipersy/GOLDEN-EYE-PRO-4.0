import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import sys
from pathlib import Path
# All'inizio di App.py, dopo gli import
import os
import sys
from pathlib import Path

print("🔍 DEBUG PATH:")
print(f"Current dir: {Path(__file__).parent.absolute()}")
print(f"sys.path: {sys.path}")

# Verifica se ui_streamlit esiste
ui_path = Path(__file__).parent / "ui_streamlit"
print(f"ui_streamlit exists: {ui_path.exists()}")

if ui_path.exists():
    print(f"Files in ui_streamlit: {[f.name for f in ui_path.glob('*.py')]}")
    
    pages_path = ui_path / "pages.py"
    print(f"pages.py exists: {pages_path.exists()}")
    
    if pages_path.exists():
        print("Content of pages.py:")
        with open(pages_path, 'r') as f:
            print(f.read()[:500])  # Prime 500 caratteri
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
    
if 'radar_select' not in st.session_state:
    st.session_state.radar_select = 'BTC-USD'
    
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'scan'

# ============================================
# FUNZIONE DI IMPORT CORRETTA
# ============================================
def import_main_view():
    """Importa la vista principale"""
    try:
        from ui_streamlit.pages import render_main_view
        print("✅ render_main_view importata correttamente")
        return render_main_view
    except ImportError as e:
        print(f"❌ Errore import: {e}")
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
    .main-content {
        padding: 20px 32px;
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
# CONTENUTO PRINCIPALE
# ============================================
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Importa e renderizza la vista principale
main_view = import_main_view()
if main_view:
    main_view()
else:
    st.error("❌ Impossibile caricare l'applicazione")
    
    # Mock data come fallback
    st.subheader("🔍 SCAN Mercati (Modalità Fallback)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("BTC-USD", "$52,345", "+2.3%")
    with col2:
        st.metric("ETH-USD", "$3,124", "+1.2%")
    with col3:
        st.metric("BNB-USD", "$412", "-0.5%")

st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>📊 Watchlist: {len(st.session_state.watchlist)} assets</span>
    <span>⚡ Golden Eye Pro v4.0.0</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
