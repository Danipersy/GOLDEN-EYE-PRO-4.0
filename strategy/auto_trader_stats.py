# strategy/auto_trader_stats.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

def calculate_performance(trades):
    """Calcola metriche di performance"""
    if not trades:
        return {}
    
    df = pd.DataFrame(trades)
    closed_trades = df[df['status'] == 'closed']
    
    if closed_trades.empty:
        return {}
    
    # Calcoli
    total_trades = len(closed_trades)
    winning_trades = len(closed_trades[closed_trades['pnl'] > 0])
    win_rate = (winning_trades / total_trades) * 100 if total_trades > 0 else 0
    
    total_pnl = closed_trades['pnl'].sum()
    total_pnl_pct = (total_pnl / 10000) * 100  # Capitale iniziale 10k
    
    # Profit factor
    gross_profit = closed_trades[closed_trades['pnl'] > 0]['pnl'].sum()
    gross_loss = abs(closed_trades[closed_trades['pnl'] < 0]['pnl'].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    # Sharpe ratio (semplificato)
    returns = closed_trades['pnl'] / 10000
    sharpe = (returns.mean() / returns.std() * (252**0.5)) if returns.std() > 0 else 0
    
    return {
        'total_trades': total_trades,
        'winning_trades': winning_trades,
        'win_rate': win_rate,
        'total_pnl': total_pnl,
        'total_pnl_pct': total_pnl_pct,
        'profit_factor': profit_factor,
        'sharpe': sharpe,
        'avg_pnl': closed_trades['pnl'].mean(),
        'max_win': closed_trades['pnl'].max(),
        'max_loss': closed_trades['pnl'].min()
    }

def render_stats_panel():
    """Renderizza pannello statistiche"""
    
    st.markdown("### 📊 Performance AutoTrader")
    
    if 'auto_trades' not in st.session_state:
        st.info("Nessun trade ancora")
        return
    
    trades = st.session_state.auto_trades
    stats = calculate_performance(trades)
    
    if not stats:
        st.info("Nessun trade chiuso ancora")
        return
    
    # Metriche principali
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Trades Totali", stats['total_trades'])
    
    with col2:
        st.metric("Win Rate", f"{stats['win_rate']:.1f}%")
    
    with col3:
        delta_color = "normal" if stats['total_pnl'] > 0 else "inverse"
        st.metric("P&L Totale", f"${stats['total_pnl']:+.2f}", 
                 delta=f"{stats['total_pnl_pct']:+.1f}%", 
                 delta_color=delta_color)
    
    with col4:
        st.metric("Profit Factor", f"{stats['profit_factor']:.2f}")
    
    # Grafico equity
    if trades:
        df = pd.DataFrame([t for t in trades if t.get('status') == 'closed'])
        
        if not df.empty:
            df = df.sort_values('time')
            df['cum_pnl'] = df['pnl'].cumsum() + 10000
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['time'],
                y=df['cum_pnl'],
                mode='lines',
                line=dict(color='#f0b90b', width=3),
                fill='tozeroy',
                name='Equity'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                height=300,
                title="Curva Equity",
                xaxis_title="Data",
                yaxis_title="Capitale ($)",
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    # Tabella ultimi trade
    st.markdown("### 📋 Ultimi Trade")
    
    display_trades = []
    for t in trades[-10:]:
        display_trades.append({
            'Ora': t['time'].strftime('%H:%M'),
            'Simbolo': t['symbol'],
            'Direzione': t['direction'],
            'Entry': f"${t['entry']:.2f}",
            'Livello': f"L{t['level']}",
            'P&L': f"${t.get('pnl', 0):+.2f}" if 'pnl' in t else 'aperto',
            'Stato': t['status']
        })
    
    st.dataframe(display_trades, use_container_width=True, hide_index=True)
