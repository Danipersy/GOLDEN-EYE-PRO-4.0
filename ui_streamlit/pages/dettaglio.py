import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h
from providers.marketaux_provider import fetch_marketaux_sentiment
from indicators.robust_ta import compute_indicators_15m, decide_signal
from ai.asset_analyzer import render_ai_suggestions

def show_page(symbol=None):
    if symbol is None:
        symbol = st.session_state.get('selected_asset', 'BTC-USD')
    
    st.title(f"📊 Analisi {symbol}")
    
    # Selezione fonte dati
    col1, col2 = st.columns([3, 1])
    with col2:
        use_td = st.checkbox("Usa TwelveData (preciso)", value=True)
    
    with st.spinner("Caricamento dati..."):
        if use_td:
            df_15m, src = fetch_td_15m(symbol)
            df_1h, _ = fetch_td_1h(symbol)
            df_4h, _ = fetch_td_4h(symbol)
        else:
            from providers.multi_provider import fetch_yf_ohlcv
            df_15m = fetch_yf_ohlcv(symbol, "15m", "5d")
            df_1h = fetch_yf_ohlcv(symbol, "1h", "1mo")
            df_4h = fetch_yf_ohlcv(symbol, "4h", "3mo")
        
        if df_15m is not None and not df_15m.empty:
            # Calcola indicatori
            df_ind = compute_indicators_15m(df_15m)
            
            # Analisi MTF
            up_1h = True
            up_4h = True
            if df_1h is not None and len(df_1h) > 50:
                up_1h = df_1h['close'].iloc[-1] > df_1h['close'].ewm(50).mean().iloc[-1]
            if df_4h is not None and len(df_4h) > 20:
                up_4h = df_4h['close'].iloc[-1] > df_4h['close'].ewm(20).mean().iloc[-1]
            
            mtf_long = up_1h and up_4h
            mtf_short = (not up_1h) and (not up_4h)
            
            # Segnale
            signal = decide_signal(df_ind, mtf_long, mtf_short)
            
            # Prezzo attuale
            current_price = float(df_15m['close'].iloc[-1])
            
            # Metriche principali
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Prezzo", f"${current_price:.2f}")
            col2.metric("RSI", f"{signal['rsi']:.1f}")
            col3.metric("ADX", f"{signal['adx']:.1f}")
            col4.metric("ATR", f"${signal['atr']:.2f}")
            
            # Segnale
            st.markdown(f"""
            <div style="
                background: {signal['color']}20;
                border-left: 5px solid {signal['color']};
                border-radius: 5px;
                padding: 15px;
                margin: 10px 0;
            ">
                <h3 style="color:{signal['color']};">{signal['display']}</h3>
                <p>Forza: {signal['strength']} | MTF Long: {mtf_long} | MTF Short: {mtf_short}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Grafico
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df_15m['datetime'],
                open=df_15m['open'],
                high=df_15m['high'],
                low=df_15m['low'],
                close=df_15m['close'],
                name='OHLC'
            ))
            
            fig.add_trace(go.Scatter(
                x=df_15m['datetime'],
                y=df_ind['ema200'],
                line=dict(color='orange', width=1),
                name='EMA 200'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                height=500,
                xaxis_rangeslider_visible=False,
                title=f"Andamento {symbol}"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # News sentiment
            st.subheader("📰 News Sentiment")
            news = fetch_marketaux_sentiment([symbol])
            if news and news.get('count', 0) > 0:
                st.info(f"📊 {news.get('count')} news - Sentiment: {news.get('label', 'N/A')}")
            else:
                st.caption("Nessuna news recente")
            
            # AI Suggeritore
            st.subheader("🤖 AI Analisi")
            data_for_ai = {
                'p': current_price,
                'rsi': signal['rsi'],
                'adx': signal['adx'],
                'atr': signal['atr'],
                'sqz_on': signal['sqz_on'],
                'v': signal['signal'],
                'level': 5 if signal['strength'] == 'STRONG' else 4 if signal['strength'] == 'WEAK' else 3,
                'mtf_long': mtf_long,
                'mtf_short': mtf_short
            }
            render_ai_suggestions(symbol, data_for_ai, news)
            
            # Dettaglio indicatori
            with st.expander("📊 Dettaglio Indicatori"):
                col_i1, col_i2, col_i3 = st.columns(3)
                with col_i1:
                    st.metric("RSI", f"{signal['rsi']:.1f}")
                    st.metric("ADX", f"{signal['adx']:.1f}")
                with col_i2:
                    st.metric("ATR", f"${signal['atr']:.2f}")
                    st.metric("Pendenza", f"{signal['slope']:.3f}")
                with col_i3:
                    st.metric("Squeeze", "ON" if signal['sqz_on'] else "OFF")
                    st.metric("EMA200", f"${df_ind['ema200'].iloc[-1]:.2f}")
            
            # SL/TP
            st.subheader("💰 Risk Management")
            col_sl, col_tp = st.columns(2)
            with col_sl:
                sl = current_price - (signal['atr'] * 2) if signal['is_long'] else current_price + (signal['atr'] * 2)
                st.metric("Stop Loss", f"${sl:.2f}")
            with col_tp:
                tp = current_price + (signal['atr'] * 4) if signal['is_long'] else current_price - (signal['atr'] * 4)
                st.metric("Take Profit", f"${tp:.2f}")
            
        else:
            st.error(f"Impossibile caricare dati per {symbol}")
