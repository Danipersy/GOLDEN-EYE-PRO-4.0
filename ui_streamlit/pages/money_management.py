import streamlit as st
from strategy.money_manager import render_money_manager_panel

def render():
    """TAB 4: Money Management"""
    if 'detail_data' in st.session_state:
        data = st.session_state.detail_data
        # Usa score dal segnale se disponibile, altrimenti default 65
        signal_score = data.get('score', 65)
        render_money_manager_panel(
            data.get('p', 0),
            data.get('atr', 0),
            signal_score
        )
    else:
        st.info("ℹ️ Carica prima un dettaglio asset")
