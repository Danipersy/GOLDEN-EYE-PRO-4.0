# ui_streamlit/pages/scan.py
import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

def show_page():
    st.title("🔍 SCAN Mercati")
    
    # Watchlist dalla session state
    watchlist = st.session_state.get('watchlist', ['BTC-USD', 'ETH-USD', 'BNB-USD'])
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.button("🔄 Aggiorna Dati", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Mostra dati in tempo reale
    cols = st.columns(3)
    
    for idx, symbol in enumerate(watchlist[:6]):  # Max 6 simboli
        with cols[idx % 3]:
            with st.spinner(f"Caricamento {symbol}..."):
                try:
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="1d", interval="1m")
                    
                    if not data.empty:
                        current_price = data['Close'].iloc[-1]
                        prev_price = data['Close'].iloc[0] if len(data) > 1 else current_price
                        change = ((current_price - prev_price) / prev_price) * 100
                        
                        st.metric(
                            label=symbol,
                            value=f"${current_price:.2f}",
                            delta=f"{change:.2f}%"
                        )
                    else:
                        st.metric(label=symbol, value="N/D", delta="0%")
                        
                except Exception as e:
                    st.metric(label=symbol, value="Errore", delta="0%")
    
    # Tabella dettagliata
    st.markdown("---")
    st.subheader("📊 Dettaglio Watchlist")
    
    data_list = []
    for symbol in watchlist:
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            data_list.append({
                'Simbolo': symbol,
                'Prezzo': info.get('regularMarketPrice', 0),
                'Volume': info.get('volume', 0),
                'Market Cap': info.get('marketCap', 0),
                'Cambio 24h': info.get('regularMarketChangePercent', 0)
            })
        except:
            data_list.append({
                'Simbolo': symbol,
                'Prezzo': 0,
                'Volume': 0,
                'Market Cap': 0,
                'Cambio 24h': 0
            })
    
    df = pd.DataFrame(data_list)
    st.dataframe(df, use_container_width=True)
