# ui_streamlit/components/detail_panel.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h
from providers.marketaux_provider import fetch_marketaux_sentiment
from providers.multi_provider import fetch_yf_ohlcv
from indicators.robust_ta import compute_indicators_15m, decide_signal
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
    """Fetch dati TwelveData con debug"""
    df15, src15 = fetch_td_15m(symbol)
    df1h, src1h = fetch_td_1h(symbol)
    df4h, src4h = fetch_td_4h(symbol)
    return df15, df1h, df4h

def run_detail(symbol: str, use_td: bool = True):
    """Esegue analisi dettaglio"""
    if use_td:
        df15, df1h, df4h = fetch_td_cached(symbol)
        source = "TwelveData"
    else:
        df15 = fetch_yf_ohlcv(symbol, "15m", "5d")
        df1h = fetch_yf_ohlcv(symbol, "1h", "1mo")
        df4h = fetch_yf_ohlcv(symbol, "4h", "3mo")
        source = "Yahoo"
    
    if df15 is None:
        return f"DATA_INSUFFICIENT - Nessun dato 15m da {source}"
    
    if "BTC" in symbol or "ETH" in symbol:
        min_candles = 100
    else:
        min_candles = 210
    
    if len(df15) < min_candles:
        return f"DATA_INSUFFICIENT - Solo {len(df15)} candles da {source} (min {min_candles})"
    
    st.session_state.data_source = source
    st.session_state.last_data_timestamp = df15["datetime"].iloc[-1]
    st.session_state.last_update = datetime.now()
    
    if use_td and df1h is not None and df4h is not None:
        st.session_state.validation_log = validate_data_quality(df15, df1h, df4h)
    
    # Analisi MTF
    up1h = True
    up4h = True
    if df1h is not None and len(df1h) > 50:
        up1h = df1h["close"].iloc[-1] > df1h["close"].ewm(50).mean().iloc[-1]
    if df4h is not None and len(df4h) > 20:
        up4h = df4h["close"].iloc[-1] > df4h["close"].ewm(20).mean().iloc[-1]
    
    mtf_long = up1h and up4h
    mtf_short = (not up1h) and (not up4h)
    
    # Indicatori
    ind = compute_indicators_15m(df15)
    signal = decide_signal(ind, mtf_long, mtf_short)
    
    p = float(df15["close"].iloc[-1])
    e200 = float(ind["ema200"].iloc[-1])
    
    # SL/TP
    dist = signal['atr'] * SL_ATR
    if signal['is_long']:
        sl = p - dist
        tp = p + dist * (TP_ATR/SL_ATR)
    elif signal['is_long'] is False:
        sl = p + dist
        tp = p - dist * (TP_ATR/SL_ATR)
    else:
        sl = 0
        tp = 0
    
    timeout = calculate_timeout(symbol, signal['atr'], p)
    
    st.session_state.detail_data = {'p': p, 'atr': signal['atr'], 'asset': symbol}
    
    return {
        "p": p, 
        "e200": e200, 
        "rsi": signal['rsi'], 
        "atr": signal['atr'], 
        "adx": signal['adx'],
        "sqz": signal['sqz_on'], 
        "sig": signal['display'], 
        "col": signal['color'], 
        "bias": signal['is_long'], 
        "sl": sl, 
        "tp": tp,
        "timeout": timeout, 
        "hist": df15.set_index("datetime")["close"].tail(90),
        "mtf_long": mtf_long, 
        "mtf_short": mtf_short,
        "strength": signal['strength']
    }

def render_news_simple(symbol: str):
    """News compatte"""
    data = fetch_marketaux_sentiment([symbol])
    if data and data.get('count', 0) > 0:
        st.markdown(f"📰 **News:** {data.get('count', 0)} | **Sentiment:** {data.get('label', 'N/D')}")
    else:
        st.markdown("📰 Nessuna news recente")

def render_detail_panel(symbol: str):
    """Pannello dettaglio completo - SENZA titolo doppio"""
    
    col1, col2 = st.columns([3, 1])
    with col2:
        use_td = st.checkbox("📊 TwelveData", value=True, help="Usa TwelveData (più preciso) o Yahoo", key="td_checkbox")
    
    with st.spinner(f"Caricamento dati {symbol}..."):
        data = run_detail(symbol, use_td)
    
    if isinstance(data, str):
        st.error(f"❌ {data}")
        st.info("💡 Prova a deselezionare 'TwelveData' per usare Yahoo")
        return None
    
    # Card principale
    strength_badge = {
        'STRONG': '🟢 FORTE',
        'WEAK': '🟡 DEBOLE',
        'NONE': '⚪ NEUTRALE'
    }.get(data['strength'], '')
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1e1e2e, #1a1a2a);
        border-left: 6px solid {data['col']};
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    ">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:1.3rem; font-weight:bold;">{data['sig']}</span>
            <span style="color:{data['col']}; font-weight:bold; font-size:1.5rem;">${data['p']:.2f}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:5px;">
            <span style="color:#94a3b8;">{strength_badge}</span>
            <span style="color:#94a3b8;">Fonte: {st.session_state.get('data_source', 'N/D')}</span>
        </div>
        <div style="display:grid; grid-template-columns: repeat(6,1fr); gap:10px; margin-top:15px;">
            <div><small>RSI</small><br><b>{data['rsi']:.0f}</b></div>
            <div><small>ADX</small><br><b>{data['adx']:.0f}</b></div>
            <div><small>ATR</small><br><b>{data['atr']:.2f}</b></div>
            <div><small>TEMPO</small><br><b style="color:{data['timeout']['colore']};">{data['timeout']['ore']}</b></div>
            <div><small>CHIUSURA</small><br><b>{data['timeout']['chiusura']}</b></div>
            <div><small>EMA200</small><br><b>{data['e200']:.2f}</b></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # GRAFICO
    st.subheader("📈 Andamento")
    
    hist_data = data['hist'].reset_index()
    hist_data.columns = ['Data', 'Prezzo']
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=hist_data['Data'],
        y=hist_data['Prezzo'],
        mode='lines',
        line=dict(color=data['col'], width=2),
        name='Prezzo'
    ))
    
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
        st.metric("Stop Loss", f"${data['sl']:.2f}" if data['sl'] and data['sl'] > 0 else "N/A")
    with col_tp:
        st.metric("Take Profit", f"${data['tp']:.2f}" if data['tp'] and data['tp'] > 0 else "N/A")
    
    # Posizione
    render_position_panel(data['p'], 2, data['atr'], symbol)
    
    return data
