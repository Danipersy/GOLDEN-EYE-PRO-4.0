import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go

def show_page(symbol=None):
    if symbol is None:
        symbol = st.session_state.get('selected_asset', 'BTC-USD')
    
    st.title(f"📊 Dettaglio {symbol}")
    
    # Mock grafico
    dates = pd.date_range(end=datetime.now(), periods=100, freq='D')
    prices = np.random.randn(100).cumsum() + 100
    
    fig = go.Figure(data=go.Scatter(x=dates, y=prices, mode='lines'))
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
