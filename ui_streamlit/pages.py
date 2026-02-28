# ui_streamlit/pages.py
import streamlit as st
from datetime import datetime

from ui_streamlit.components.header import render_header
from ui_streamlit.components.radar_panel import render_radar_panel
from ui_streamlit.components.detail_panel import render_detail_panel
from ui_streamlit.components.backtest_panel import render_backtest_panel
from ui_streamlit.components.settings_ui import render_settings_page
from ui_streamlit.components.info_ui import render_info_page
from ui_streamlit.components.paper_trading import render_paper_trading_panel
from strategy.validator import render_validation_panel
from strategy.optimizer import render_optimizer_panel
from strategy.money_manager import render_money_manager_panel

def render_main_view():
    """Vista principale con tutti i tab"""
    
    # Inizializzazione
    if 'radar_select' not in st.session_state:
        if st.session_state.watchlist:
            st.session_state.radar_select = st.session_state.watchlist[0]
    
    if 'selected_tab' not in st.session_state:
        st.session_state.selected_tab = 0
    
    # Header
    render_header()
    
    # Radar (sempre visibile)
    render_radar_panel()
    
    st.markdown("---")
    
    # TABS PRINCIPALI
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Dettaglio Asset",
        "🎯 Validazione",
        "⚙️ Ottimizzazione",
        "💰 Money Management",
        "📝 Paper Trading",
    ])
    
    # ============================================================
    # TAB 1: DETTAGLIO ASSET
    # ============================================================
    with tab1:
        if st.session_state.radar_select:
            st.markdown(f"### 📊 Dettaglio {st.session_state.radar_select}")
            data = render_detail_panel(st.session_state.radar_select)
            if data:
                st.markdown("---")
                render_backtest_panel(st.session_state.radar_select)
        else:
            st.warning("Seleziona un asset dal radar")
    
    # ============================================================
    # TAB 2: VALIDAZIONE STRATEGIA
    # ============================================================
    with tab2:
        st.markdown("## 🎯 Validazione Strategia")
        st.caption("Test su multipli asset e anni per valutare la robustezza")
        render_validation_panel(st.session_state.watchlist)
    
    # ============================================================
    # TAB 3: OTTIMIZZAZIONE PARAMETRI
    # ============================================================
    with tab3:
        st.markdown("## ⚙️ Ottimizzazione Parametri")
        st.caption("Cerca la combinazione migliore di SL, TP, ADX e RSI")
        if st.session_state.radar_select:
            render_optimizer_panel(st.session_state.radar_select)
        else:
            st.warning("Seleziona un asset dal radar")
    
    # ============================================================
    # TAB 4: MONEY MANAGEMENT
    # ============================================================
    with tab4:
        st.markdown("## 💰 Money Management")
        st.caption("Gestione del capitale e calcolo dimensioni posizioni")
        if 'detail_data' in st.session_state:
            data = st.session_state.detail_data
            render_money_manager_panel(
                data.get('p', 0),
                data.get('atr', 0),
                65  # signal_score di default
            )
        else:
            st.info("ℹ️ Carica prima un dettaglio asset nel TAB 1")
    
    # ============================================================
    # TAB 5: PAPER TRADING
    # ============================================================
    with tab5:
        st.markdown("## 📝 Paper Trading")
        st.caption("Simula trading con capitale virtuale")
        if 'detail_data' in st.session_state and st.session_state.radar_select:
            data = st.session_state.detail_data
            signal_label = data.get('sig', 'SEGNALE')
            signal_score = 85 if "FORTE" in signal_label else 65
            render_paper_trading_panel(
                st.session_state.radar_select,
                data.get('p', 0),
                data.get('atr', 0),
                signal_score,
                signal_label
            )
        else:
            st.info("ℹ️ Carica prima un dettaglio asset nel TAB 1")
    
    
# ============================================================
# FUNZIONI WRAPPER
# ============================================================
def render_scan(watchlist, refresh_tick):
    render_main_view()

def render_position(refresh_tick):
    st.info("Usa il pannello posizione nel TAB 1")

def render_backtest():
    st.info("Usa il backtest nel TAB 1")

def render_settings():
    render_settings_page()

def render_info():
    render_info_page()