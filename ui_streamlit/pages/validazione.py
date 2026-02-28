import streamlit as st
from strategy.validator import render_validation_panel

def render():
    """TAB 2: Validazione Strategia"""
    render_validation_panel(st.session_state.watchlist)
