# ui_streamlit/pages.py
import streamlit as st
from datetime import datetime

# Import delle funzioni dai componenti
try:
    from ui_streamlit.components.header import render_header
    from ui_streamlit.components.scan_panel import render_scan_panel
    from ui_streamlit.components.detail_panel import render_detail_panel
    from ui_streamlit.components.backtest_panel import render_backtest_panel
    from strategy.validator import render_validation_panel
    from strategy.optimizer import render_optimizer_panel
    from strategy.money_manager import render_money_manager_panel
    from strategy.auto_trader import render_auto_trader_panel
    from strategy.auto_trader_stats import render_stats_panel
    from ui_streamlit.components.paper_trading import render_paper_trading_panel
except ImportError as e:
    print(f"⚠️ Import warning: {e}")

def render_main_view():
    """Vista principale con menu a 2 livelli"""
    
    # Inizializza current_view se non esiste
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'scan'
    
    if 'radar_select' not in st.session_state:
        st.session_state.radar_select = 'BTC-USD'
    
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
    
    # Header
    try:
        render_header()
    except:
        st.markdown("### 🦅 GOLDEN EYE PRO")
    
    # Menu principale
    col1, col2, col3 = st.columns([1, 1, 5])
    with col1:
        if st.button("🔍 SCAN", use_container_width=True, 
                    type="primary" if st.session_state.current_view == "scan" else "secondary"):
            st.session_state.current_view = "scan"
            st.rerun()
    with col2:
        if st.button("📊 DETTAGLIO", use_container_width=True,
                    type="primary" if st.session_state.current_view == "detail" else "secondary"):
            if st.session_state.radar_select:
                st.session_state.current_view = "detail"
                st.rerun()
            else:
                st.warning("Seleziona un asset prima")
    
    st.divider()
    
    # Contenuto principale
    if st.session_state.current_view == "scan":
        try:
            render_scan_panel()
        except Exception as e:
            st.error(f"Errore scan panel: {e}")
            # Fallback
            st.subheader("🔍 SCAN Mercati")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("BTC-USD", "$52,345", "+2.3%")
            with col2:
                st.metric("ETH-USD", "$3,124", "+1.2%")
            with col3:
                st.metric("BNB-USD", "$412", "-0.5%")
    else:
        st.info(f"Dettaglio {st.session_state.radar_select} - In sviluppo")
    
    # Tools section
    st.markdown("---")
    st.markdown("### 🛠️ STRUMENTI")
    
    tab1, tab2, tab3 = st.tabs(["📊 Validazione", "⚙️ Ottimizzazione", "💰 Money Management"])
    
    with tab1:
        st.info("Validazione strategia - In sviluppo")
    with tab2:
        st.info("Ottimizzazione parametri - In sviluppo")
    with tab3:
        st.info("Money management - In sviluppo")

# Esporta la funzione
__all__ = ['render_main_view']

print("✅ pages.py caricato correttamente")
