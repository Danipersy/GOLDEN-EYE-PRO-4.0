# ui_streamlit/components/detail_panel.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h
from providers.marketaux_provider import fetch_marketaux_sentiment
from providers.yahoo_provider import fetch_yf_ohlcv
from indicators.robust_ta import compute_indicators_15m, decide_signal
from utils.helpers import get_market_status
from ui_streamlit.components.validation_panel import validate_data_quality
from ui_streamlit.components.position_panel import render_position_panel
from ai.asset_analyzer import render_ai_suggestions
from config import SL_ATR, TP_ATR

def calculate_timeout(asset: str, atr: float, price: float) -> dict:
    """Stima tempo posizione"""
    if atr <= 0 or price <= 0:
        return {"ore": "N/D", "chiusura": "N/D", "colore": "#999999"}
    
    ore = (atr * 3) / (atr / 24) if atr > 0 else 0
    ore = min(ore, 168)
    expiry = datetime.now() + timedelta(hours=ore)
    
    if ore < 4:
        colore = "#ff3344"
    elif ore < 12:
        colore = "#f0b90b"
    else:
        colore = "#00ff88"
    
    return {
        "ore": f"{ore:.1f}h",
        "chiusura": expiry.strftime("%d/%m %H:%M"),
        "colore": colore
    }

def fetch_td_cached(symbol: str):
    """Fetch dati TwelveData"""
    return fetch_td_15m(symbol)[0], fetch_td_1h(symbol)[0], fetch_td_4h(symbol)[0]

def run_detail(symbol: str, use_td: bool = True):
    """Esegue analisi dettaglio"""
    if use_td:
        df15, df1h, df4h = fetch_td_cached(symbol)
        source = "TwelveData"
    else:
        df15 = fetch_yf_ohlcv(symbol, "15m", "5d", 420)
        df1h = fetch_yf_ohlcv(symbol, "1h", "1mo", 320)
        df4h = fetch_yf_ohlcv(symbol, "4h", "3mo", 220)
        source = "Yahoo"
    
    if df15 is None or len(df15) < (100 if "BTC" in symbol else 210):
        return "DATA_INSUFFICIENT"
    
    st.session_state.data_source = source
    st.session_state.last_data_timestamp = df15["datetime"].iloc[-1]
    st.session_state.last_update = datetime.now()
    
    if use_td and df1h is not None and df4h is not None:
        st.session_state.validation_log = validate_data_quality(df15, df1h, df4h)
    
    # Analisi MTF
    up1h = True
    up4h = True
    if df1h is not None:
        up1h = df1h["close"].iloc[-1] > df1h["close"].ewm(50).mean().iloc[-1]
    if df4h is not None:
        up4h = df4h["close"].iloc[-1] > df4h["close"].ewm(20).mean().iloc[-1]
    
    mtf_long = up1h and up4h
    mtf_short = (not up1h) and (not up4h)
    
    # Indicatori
    ind = compute_indicators_15m(df15)
    sig, col, bias, rsi, atr, slope, adx, sqz = decide_signal(ind, mtf_long, mtf_short)
    
    p = float(df15["close"].iloc[-1])
    e200 = float(ind["ema200"].iloc[-1])
    
    # SL/TP
    dist = atr * SL_ATR
    sl = p - dist if bias is True else p + dist if bias is False else 0
    tp = p + dist * (TP_ATR/SL_ATR) if bias is True else p - dist * (TP_ATR/SL_ATR) if bias is False else 0
    
    timeout = calculate_timeout(symbol, atr, p)
    
    st.session_state.detail_data = {'p': p, 'atr': atr, 'asset': symbol}
    
    return {
        "p": p, "e200": e200, "rsi": rsi, "atr": atr, "adx": adx,
        "sqz": sqz, "sig": sig, "col": col, "bias": bias, "sl": sl, "tp": tp,
        "timeout": timeout, "hist": df15.set_index("datetime")["close"].tail(90),
        "mtf_long": mtf_long, "mtf_short": mtf_short
    }

def render_news_simple(symbol: str):
    """News compatte"""
    data = fetch_marketaux_sentiment([symbol])
    if data:
        st.markdown(f"📰 **News:** {data.get('count', 0)} | **Sentiment:** {data.get('label', 'N/D')}")
    else:
        st.markdown("📰 Nessuna news recente")

def render_detail_panel(symbol: str):
    """Pannello dettaglio completo"""
    st.markdown(f"## 📊 {symbol}")
    
    col1, col2 = st.columns([3, 1])
    with col2:
        use_td = st.checkbox("📊 TwelveData", value=True)
    
    data = run_detail(symbol, use_td)
    
    if isinstance(data, str):
        st.error(f"Errore: {data}")
        return None
    
    # Card principale
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1e1e2e, #1a1a2a);
        border-left: 6px solid {data['col']};
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    ">
        <div style="display:flex; justify-content:space-between;">
            <span style="font-size:1.2rem;">{data['sig']}</span>
            <span style="color:{data['col']}; font-weight:bold;">{data['p']:.2f}</span>
        </div>
        <div style="display:grid; grid-template-columns: repeat(5,1fr); gap:10px; margin-top:15px;">
            <div><small>RSI</small><br><b>{data['rsi']:.0f}</b></div>
            <div><small>ADX</small><br><b>{data['adx']:.0f}</b></div>
            <div><small>ATR</small><br><b>{data['atr']:.2f}</b></div>
            <div><small>TEMPO</small><br><b style="color:{data['timeout']['colore']};">{data['timeout']['ore']}</b></div>
            <div><small>CHIUSURA</small><br><b>{data['timeout']['chiusura']}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # GRAFICO CORRETTO
    st.subheader("📈 Andamento")
    
    # Prepara i dati
    hist_data = data['hist'].reset_index()
    hist_data.columns = ['Data', 'Prezzo']
    
    # Crea figura
    fig = go.Figure()
    
    # Aggiungi linea
    fig.add_trace(go.Scatter(
        x=hist_data['Data'],
        y=hist_data['Prezzo'],
        mode='lines',
        line=dict(color=data['col'], width=2),
        name='Prezzo'
    ))
    
    # Configura layout
    fig.update_layout(
        template='plotly_dark',
        height=250,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='#30363d'),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # News
    st.subheader("📰 News")
    render_news_simple(symbol)
    
    # AI Suggeritore
    render_ai_suggestions(symbol, data, st.session_state.get('marketaux_data'))
    
    # Risk Management
    st.subheader("💰 Risk Management")
    col_sl, col_tp = st.columns(2)
    with col_sl:
        st.metric("Stop Loss", f"${data['sl']:.2f}" if data['sl'] else "N/A")
    with col_tp:
        st.metric("Take Profit", f"${data['tp']:.2f}" if data['tp'] else "N/A")
    
    # Posizione
    render_position_panel(data['p'], 2, data['atr'], symbol)
    
    return data