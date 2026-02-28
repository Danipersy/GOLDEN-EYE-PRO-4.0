# ui_streamlit/pages/money_management.py
import streamlit as st
from strategy.money_manager import render_money_manager_panel

def render():
    """TAB 4: Money Management"""
    if 'detail_data' in st.session_state:
        data = st.session_state.detail_data
        render_money_manager_panel(
            data.get('p', 0),
            data.get('atr', 0),
            65
        )
    else:
        st.info("ℹ️ Carica prima un dettaglio asset")
