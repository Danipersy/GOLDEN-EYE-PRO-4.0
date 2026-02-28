# ui_streamlit/components/backtest_stats.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import (
    COLOR_STRONG_LONG, COLOR_WEAK_LONG,
    COLOR_STRONG_SHORT, COLOR_WEAK_SHORT,
    COLOR_NEUTRAL
)

def show_signal_breakdown(trades_df):
    """Mostra breakdown performance per tipo segnale"""
    if trades_df.empty:
        st.info("Nessun trade disponibile per l'analisi")
        return
        
    st.subheader("📊 Performance per Tipo Segnale")
    
    # Verifica colonne necessarie
    if 'signal_strength' not in trades_df.columns:
        st.warning("Dati segnale non disponibili")
        return
    
    # Separa per forza segnale
    strong_trades = trades_df[trades_df['signal_strength'] == 'STRONG']
    weak_trades = trades_df[trades_df['signal_strength'] == 'WEAK']
    
    # Metriche principali
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "📊 Trades Totali", 
            len(trades_df),
            delta=None
        )
        winrate_total = (trades_df['pnl_pct'] > 0).mean() * 100
        st.metric(
            "🎯 Winrate Totale", 
            f"{winrate_total:.1f}%",
            delta=f"{winrate_total - 50:.1f}% vs 50%"
        )
    
    with col2:
        if len(strong_trades) > 0:
            strong_winrate = (strong_trades['pnl_pct'] > 0).mean() * 100
            st.metric(
                "💪 Trades STRONG", 
                len(strong_trades),
                delta=f"Winrate {strong_winrate:.1f}%"
            )
            st.metric(
                "📈 Avg P&L STRONG",
                f"{strong_trades['pnl_pct'].mean():.2f}%",
                delta=f"Best: {strong_trades['pnl_pct'].max():.2f}%"
            )
        else:
            st.info("Nessun trade STRONG")
    
    with col3:
        if len(weak_trades) > 0:
            weak_winrate = (weak_trades['pnl_pct'] > 0).mean() * 100
            st.metric(
                "📉 Trades WEAK", 
                len(weak_trades),
                delta=f"Winrate {weak_winrate:.1f}%"
            )
            st.metric(
                "📉 Avg P&L WEAK",
                f"{weak_trades['pnl_pct'].mean():.2f}%",
                delta=f"Best: {weak_trades['pnl_pct'].max():.2f}%"
            )
        else:
            st.info("Nessun trade WEAK")
    
    # Grafico comparativo se ci sono entrambi i tipi
    if len(strong_trades) > 0 and len(weak_trades) > 0:
        st.subheader("📈 Distribuzione P&L: STRONG vs WEAK")
        
        fig = go.Figure()
        
        fig.add_trace(go.Box(
            y=strong_trades['pnl_pct'],
            name='STRONG',
            marker_color=COLOR_STRONG_LONG,
            boxmean='sd'
        ))
        
        fig.add_trace(go.Box(
            y=weak_trades['pnl_pct'],
            name='WEAK',
            marker_color=COLOR_WEAK_LONG,
            boxmean='sd'
        ))
        
        fig.update_layout(
            title="Confronto Distribuzione P&L",
            yaxis_title="P&L %",
            showlegend=True,
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistiche aggiuntive
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**📊 Statistiche STRONG**")
            strong_stats = {
                "Mediana": f"{strong_trades['pnl_pct'].median():.2f}%",
                "Std Dev": f"{strong_trades['pnl_pct'].std():.2f}%",
                "Max Drawdown": f"{strong_trades['pnl_pct'].min():.2f}%",
                "Profit Factor": f"{(strong_trades[strong_trades['pnl_pct']>0]['pnl_pct'].sum() / abs(strong_trades[strong_trades['pnl_pct']<0]['pnl_pct'].sum())):.2f}" if len(strong_trades[strong_trades['pnl_pct']<0]) > 0 else "N/A"
            }
            for k, v in strong_stats.items():
                st.text(f"{k}: {v}")
        
        with col2:
            st.markdown("**📊 Statistiche WEAK**")
            weak_stats = {
                "Mediana": f"{weak_trades['pnl_pct'].median():.2f}%",
                "Std Dev": f"{weak_trades['pnl_pct'].std():.2f}%",
                "Max Drawdown": f"{weak_trades['pnl_pct'].min():.2f}%",
                "Profit Factor": f"{(weak_trades[weak_trades['pnl_pct']>0]['pnl_pct'].sum() / abs(weak_trades[weak_trades['pnl_pct']<0]['pnl_pct'].sum())):.2f}" if len(weak_trades[weak_trades['pnl_pct']<0]) > 0 else "N/A"
            }
            for k, v in weak_stats.items():
                st.text(f"{k}: {v}")

def show_timeline_chart(trades_df, df_indicators=None):
    """Mostra timeline dei trade con colori per forza segnale"""
    if trades_df.empty:
        return
    
    st.subheader("⏱️ Timeline Trade")
    
    fig = go.Figure()
    
    # Prepara dati per scatter plot
    colors = []
    for _, trade in trades_df.iterrows():
        if trade['signal_strength'] == 'STRONG':
            colors.append(COLOR_STRONG_LONG if trade['side'] == 'LONG' else COLOR_STRONG_SHORT)
        elif trade['signal_strength'] == 'WEAK':
            colors.append(COLOR_WEAK_LONG if trade['side'] == 'LONG' else COLOR_WEAK_SHORT)
        else:
            colors.append(COLOR_NEUTRAL)
    
    # Aggiungi trade come punti
    fig.add_trace(go.Scatter(
        x=trades_df['time_exit'],
        y=trades_df['pnl_pct'],
        mode='markers+text',
        marker=dict(
            size=10,
            color=colors,
            symbol='circle'
        ),
        text=trades_df['side'],
        textposition="top center",
        name='Trade',
        hovertemplate='<b>%{text}</b><br>P&L: %{y:.2f}%<br>Forza: %{customdata}<extra></extra>',
        customdata=trades_df['signal_strength']
    ))
    
    # Linea dello zero
    fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
    
    fig.update_layout(
        title="Performance Trade nel Tempo",
        xaxis_title="Data",
        yaxis_title="P&L %",
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
