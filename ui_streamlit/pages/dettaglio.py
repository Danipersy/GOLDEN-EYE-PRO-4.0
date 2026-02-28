# ui_streamlit/pages/dettaglio.py
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show_page(symbol=None):
    if symbol is None:
        symbol = st.session_state.get('selected_asset', 'BTC-USD')
    
    st.title(f"📊 Dettaglio {symbol}")
    
    # Periodo selettore
    period = st.selectbox(
        "Periodo",
        ["1d", "5d", "1mo", "3mo", "6mo", "1y"],
        index=2
    )
    
    with st.spinner("Caricamento dati..."):
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        
        if not hist.empty:
            # Grafico candlestick
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close']
            )])
            
            fig.update_layout(
                template='plotly_dark',
                height=500,
                title=f"Andamento {symbol}",
                yaxis_title="Prezzo ($)",
                xaxis_title="Data"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Metriche
            col1, col2, col3, col4 = st.columns(4)
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
            change = ((current - prev) / prev) * 100
            
            col1.metric("Prezzo Attuale", f"${current:.2f}", f"{change:.2f}%")
            col2.metric("Massimo", f"${hist['High'].max():.2f}")
            col3.metric("Minimo", f"${hist['Low'].min():.2f}")
            col4.metric("Volume Medio", f"{hist['Volume'].mean():,.0f}")
            
            # Dati tabellari
            with st.expander("📋 Dati Storici"):
                st.dataframe(hist.tail(10), use_container_width=True)
        else:
            st.error(f"Nessun dato disponibile per {symbol}")
