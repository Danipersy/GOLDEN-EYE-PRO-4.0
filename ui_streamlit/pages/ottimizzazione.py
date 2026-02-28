import streamlit as st
from strategy.optimizer import render_optimizer_panel

def render():
    """TAB 3: Ottimizzazione Parametri"""
    if st.session_state.radar_select:
        render_optimizer_panel(st.session_state.radar_select)
    else:
        st.warning("Seleziona un asset dal radar")
