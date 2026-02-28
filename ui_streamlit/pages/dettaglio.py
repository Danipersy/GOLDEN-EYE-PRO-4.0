import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h
from providers.marketaux_provider import fetch_marketaux_sentiment
from indicators.robust_ta import compute_indicators_15m, decide_signal
from ai.asset_analyzer import render_ai_suggestions

def show_page(symbol=None):
    if symbol is None:
        symbol = st.session_state.get('selected_asset', 'BTC-USD')

    st.markdown(f"## 📊 Dettaglio {symbol}", unsafe_allow_html=True)

    # Selezione fonte dati
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col2:
            use_td = st.checkbox("📡 TwelveData", value=True, help="Usa dati precisi TwelveData")

    with st.spinner("Caricamento dati in corso..."):
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

            signal = decide_signal(df_ind, mtf_long, mtf_short)
            current_price = float(df_15m['close'].iloc[-1])

            # Metriche in card orizzontali
            cols = st.columns(4)
            with cols[0]:
                st.metric("💵 Prezzo", f"${current_price:,.2f}")
            with cols[1]:
                st.metric("📊 RSI", f"{signal['rsi']:.1f}")
            with cols[2]:
                st.metric("📈 ADX", f"{signal['adx']:.1f}")
            with cols[3]:
                st.metric("📉 ATR", f"${signal['atr']:.2f}")

            # Segnale
            st.markdown(f"""
            <div style="
                background: {signal['color']}20;
                border-left: 8px solid {signal['color']};
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1.5rem 0;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            ">
                <h3 style="color: {signal['color']}; margin: 0;">{signal['display']}</h3>
                <p style="color: #94a3b8; margin-top: 0.5rem;">
                    Forza: {signal['strength']} | MTF Long: {'✅' if mtf_long else '❌'} | MTF Short: {'✅' if mtf_short else '❌'}
                </p>
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
                line=dict(color='orange', width=2),
                name='EMA 200'
            ))
            fig.update_layout(
                template='plotly_dark',
                height=500,
                xaxis_rangeslider_visible=False,
                title=f"Andamento {symbol}",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)

            # News e AI
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                st.subheader("📰 News Sentiment")
                news = fetch_marketaux_sentiment([symbol])
                if news and news.get('count', 0) > 0:
                    st.info(f"📊 {news.get('count')} news - Sentiment: {news.get('label', 'N/A')}")
                else:
                    st.caption("Nessuna news recente")
            with col_n2:
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

            # SL/TP
            st.subheader("💰 Risk Management")
            col_sl, col_tp, col_rr = st.columns(3)
            with col_sl:
                sl = current_price - (signal['atr'] * 2) if signal['is_long'] else current_price + (signal['atr'] * 2)
                st.metric("🛑 Stop Loss", f"${sl:.2f}", delta=f"{((sl-current_price)/current_price*100):.2f}%", border=True)
            with col_tp:
                tp = current_price + (signal['atr'] * 4) if signal['is_long'] else current_price - (signal['atr'] * 4)
                st.metric("🎯 Take Profit", f"${tp:.2f}", delta=f"{((tp-current_price)/current_price*100):.2f}%", border=True)
            with col_rr:
                risk = abs(current_price - sl)
                reward = abs(tp - current_price)
                rr = reward / risk if risk > 0 else 0
                st.metric("📊 Risk/Reward", f"1:{rr:.2f}", border=True)
        else:
            st.error(f"❌ Impossibile caricare dati per {symbol}")
