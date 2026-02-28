# ui_streamlit/pages/paper_trading.py
import streamlit as st
from ui_streamlit.components.paper_trading import render_paper_trading_panel

def render():
    """TAB 5: Paper Trading"""
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
