# ui_streamlit/components/position_ui.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

from providers.yahoo_provider import fetch_yahoo_ohlcv
from ui_streamlit.components.indicators import atr_wilder_last, rischio

def render_position_page(refresh_tick: int = 0):
    """Pagina monitoraggio posizioni"""
    
    st.markdown("## 📌 Position Manager")
    
    position = st.session_state.get('position', {})
    
    if not position or not position.get('active', False):
        st.info("ℹ️ Nessuna posizione attiva. Apri una posizione dalla pagina SCAN.")
        
        # Storico demo
        with st.expander("📜 Storico Posizioni (demo)"):
            history_data = {
                'Data': ['2026-02-20', '2026-02-19', '2026-02-18'],
                'Asset': ['AAPL', 'MSFT', 'TSLA'],
                'Azione': ['BUY', 'SELL', 'BUY'],
                'Entry': [185.50, 415.20, 198.30],
                'Exit': [191.75, 401.50, 213.45],
                'PnL %': [3.37, -3.30, 7.64]
            }
            df_history = pd.DataFrame(history_data)
            st.dataframe(df_history, use_container_width=True, hide_index=True)
        
        return
    
    # Posizione attiva
    asset = position.get('asset', '')
    action = position.get('action', '')
    flow = position.get('flow', action)
    entry = position.get('entry', 0)
    sl = position.get('sl', 0)
    tp = position.get('tp', 0)
    timestamp = position.get('timestamp', datetime.now().isoformat())
    
    # Header
    col_h1, col_h2, col_h3, col_h4 = st.columns(4)
    
    with col_h1:
        st.markdown(f"## {asset}")
        st.caption(f"Aperta: {timestamp[:10]}")
    
    with col_h2:
        st.metric("Direzione", flow, border=True)
    
    with col_h3:
        st.metric("Entry", f"${entry:.2f}", border=True)
    
    with col_h4:
        st.metric("Stato", "🟢 ATTIVA", border=True)
    
    st.divider()
    
    # Fetch dati live
    with st.spinner("Caricamento dati..."):
        df = fetch_yahoo_ohlcv(asset, period="2d", interval="5m")
    
    if df is None or df.empty:
        st.error("Impossibile caricare dati live")
        return
    
    # Prezzo attuale
    current_price = float(df['close'].iloc[-1])
    price_change = ((current_price - entry) / entry) * 100 if entry != 0 else 0
    
    # Calcola P&L
    if flow == "LONG":
        pnl_pct = price_change
    else:
        pnl_pct = -price_change
    
    # Check stop loss / take profit
    stop_hit = False
    take_profit_hit = False
    
    if flow == "LONG":
        if sl and current_price <= sl:
            stop_hit = True
        elif tp and current_price >= tp:
            take_profit_hit = True
    else:
        if sl and current_price >= sl:
            stop_hit = True
        elif tp and current_price <= tp:
            take_profit_hit = True
    
    if stop_hit:
        st.error(f"🔴 STOP LOSS HIT! Prezzo: ${current_price:.2f}")
        if st.button("Conferma chiusura posizione"):
            st.session_state['position'] = {'active': False}
            st.rerun()
    
    if take_profit_hit:
        st.success(f"🟢 TAKE PROFIT RAGGIUNTO! Prezzo: ${current_price:.2f}")
        if st.button("Conferma chiusura posizione"):
            st.session_state['position'] = {'active': False}
            st.rerun()
    
    # Metriche
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Prezzo Attuale", f"${current_price:.2f}", 
                 delta=f"{price_change:+.2f}%", border=True)
    
    with m2:
        st.metric("P&L", f"{pnl_pct:+.2f}%", 
                 delta_color="normal" if pnl_pct > 0 else "inverse", border=True)
    
    with m3:
        st.metric("Stop Loss", f"${sl:.2f}" if sl else "N/A", border=True)
    
    with m4:
        st.metric("Take Profit", f"${tp:.2f}" if tp else "N/A", border=True)
    
    # Grafico
    st.markdown("### 📈 Chart")
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.03, row_heights=[0.7, 0.3])
    
    # Candlestick
    fig.add_trace(
        go.Candlestick(
            x=df.index, open=df['open'], high=df['high'],
            low=df['low'], close=df['close'], name=asset
        ), row=1, col=1
    )
    
    # Linee
    fig.add_hline(y=entry, line_dash="dash", line_color="yellow", 
                  annotation_text="Entry", row=1, col=1)
    if sl:
        fig.add_hline(y=sl, line_dash="dash", line_color="red", 
                      annotation_text="SL", row=1, col=1)
    if tp:
        fig.add_hline(y=tp, line_dash="dash", line_color="green", 
                      annotation_text="TP", row=1, col=1)
    
    # Volume
    fig.add_trace(
        go.Bar(x=df.index, y=df['volume'], name='Volume', marker_color='#60A5FA'),
        row=2, col=1
    )
    
    fig.update_layout(height=500, template='plotly_dark', 
                     showlegend=False, xaxis_rangeslider_visible=False)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Azioni
    st.markdown("### ⚙️ Azioni")
    col_a1, col_a2, col_a3 = st.columns(3)
    
    with col_a1:
        if st.button("🔄 Aggiorna", use_container_width=True):
            st.rerun()
    
    with col_a2:
        if st.button("✏️ Modifica SL/TP", use_container_width=True):
            st.session_state['editing_position'] = True
    
    with col_a3:
        if st.button("🔴 Chiudi Posizione", use_container_width=True, type="primary"):
            st.session_state['position'] = {'active': False}
            st.success("Posizione chiusa")
            st.rerun()
    
    # Modifica SL/TP
    if st.session_state.get('editing_position', False):
        with st.form("edit_position"):
            st.markdown("**Modifica SL/TP**")
            new_sl = st.number_input("Nuovo Stop Loss", value=sl if sl else 0.0, format="%.2f")
            new_tp = st.number_input("Nuovo Take Profit", value=tp if tp else 0.0, format="%.2f")
            
            col_s1, col_s2 = st.columns(2)
            with col_s1:
                if st.form_submit_button("Salva"):
                    position['sl'] = new_sl
                    position['tp'] = new_tp
                    st.session_state['position'] = position
                    st.session_state['editing_position'] = False
                    st.rerun()
            
            with col_s2:
                if st.form_submit_button("Annulla"):
                    st.session_state['editing_position'] = False
                    st.rerun()
