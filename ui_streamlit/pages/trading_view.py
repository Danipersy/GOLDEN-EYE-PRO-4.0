# ui_streamlit/pages/trading_view.py
import streamlit as st
from datetime import datetime

from ui_streamlit.components.header import render_header
from ui_streamlit.components.scan_panel import render_scan_panel
from ui_streamlit.components.detail_panel import render_detail_panel
from ui_streamlit.components.backtest_panel import render_backtest_panel
from strategy.validator import render_validation_panel
from strategy.optimizer import render_optimizer_panel
from strategy.money_manager import render_money_manager_panel
from strategy.auto_trader import render_auto_trader_panel
from strategy.auto_trader_stats import render_stats_panel

def render_trading_view():
    """Vista principale con menu a 2 livelli"""
    
    if 'current_view' not in st.session_state:
        st.session_state.current_view = 'scan'
    
    render_header()
    
    col1, col2, col3 = st.columns([1, 1, 5])
    with col1:
        scan_btn_type = "primary" if st.session_state.current_view == "scan" else "secondary"
        if st.button("🔍 SCAN", use_container_width=True, type=scan_btn_type, key="scan_btn"):
            st.session_state.current_view = "scan"
            st.rerun()
    with col2:
        detail_btn_type = "primary" if st.session_state.current_view == "detail" else "secondary"
        if st.button("📊 DETTAGLIO", use_container_width=True, type=detail_btn_type, key="detail_btn"):
            if st.session_state.radar_select:
                st.session_state.current_view = "detail"
                st.rerun()
            else:
                st.warning("Prima seleziona un asset dallo SCAN")
    
    st.divider()
    
    if st.session_state.current_view == "scan":
        render_scan_panel()
    else:
        if st.session_state.radar_select:
            render_detail_panel(st.session_state.radar_select)
            st.markdown("---")
            render_backtest_panel(st.session_state.radar_select)
        else:
            st.warning("Nessun asset selezionato. Torna allo SCAN.")
            if st.button("← Torna allo SCAN", key="back_to_scan"):
                st.session_state.current_view = "scan"
                st.rerun()
    
    st.markdown("---")
    st.markdown("### 🛠️ STRUMENTI AVANZATI")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 Validazione",
        "⚙️ Ottimizzazione",
        "💰 Money Management",
        "📝 Paper Trading",
        "🤖 AutoTrader",
    ])
    
    with tab1:
        render_validation_panel(st.session_state.watchlist)
    
    with tab2:
        if st.session_state.radar_select:
            render_optimizer_panel(st.session_state.radar_select)
        else:
            st.info("ℹ️ Seleziona un asset per ottimizzare i parametri")
    
    with tab3:
        if 'detail_data' in st.session_state:
            data = st.session_state.detail_data
            render_money_manager_panel(
                data.get('p', 0),
                data.get('atr', 0),
                65
            )
        else:
            st.info("ℹ️ Carica prima un dettaglio asset")
    
    with tab4:
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
            st.info("ℹ️ Carica prima un dettaglio asset")
    
    with tab5:
        render_auto_trader_panel()
        st.markdown("---")
        render_stats_panel()