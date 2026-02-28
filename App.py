import streamlit as st
from datetime import datetime
import sys
from pathlib import Path

# Configurazione path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Configurazione pagina
st.set_page_config(
    page_title="GOLDEN EYE PRO",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS base
st.markdown("""
<style>
    .main { background: #0A0A0F; }
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

# Tentativo di import
try:
    from ui_streamlit import render_main_view
    st.success("✅ App caricata correttamente!")
    render_main_view()
except ImportError as e:
    st.error(f"❌ Errore import: {e}")
    
    # Mostra info debug
    with st.expander("🔧 Debug Info"):
        st.write("Current Directory:", current_dir)
        st.write("Files in current dir:", [f.name for f in current_dir.glob("*")])
        
        ui_path = current_dir / "ui_streamlit"
        if ui_path.exists():
            st.write("Files in ui_streamlit:", [f.name for f in ui_path.glob("*")])
        else:
            st.write("❌ ui_streamlit non trovato!")
    
    # Fallback
    st.subheader("🔍 SCAN Mercati (Fallback)")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("BTC-USD", "$52,345", "+2.3%")
    with col2:
        st.metric("ETH-USD", "$3,124", "+1.2%")
    with col3:
        st.metric("BNB-USD", "$412", "-0.5%")

# Footer
st.markdown(f"""
<div class='app-footer'>
    <span>📅 {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}</span>
    <span>📊 Golden Eye Pro</span>
    <span>⚠️ Solo scopo educativo</span>
</div>
""", unsafe_allow_html=True)
