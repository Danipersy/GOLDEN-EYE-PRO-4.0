import streamlit as st
from strategy.auto_trader import render_auto_trader_panel
from strategy.auto_trader_stats import render_stats_panel

def render():
    """TAB 6: AutoTrader con Statistiche"""
    render_auto_trader_panel()
    st.markdown("---")
    render_stats_panel()
