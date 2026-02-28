# strategy/annual_backtest.py
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go
from providers.yahoo_provider import fetch_yf_ohlcv
from strategy.backtest import backtest_engine
from config import BT_SL_ATR, BT_TP_ATR

def calculate_performance_metrics(trades_df):
    """Calcola metriche di performance avanzate"""
    if trades_df.empty or len(trades_df) < 3:
        return {
            "total_trades": 0,
            "win_rate": 0,
            "avg_pnl": 0,
            "total_pnl": 0,
            "max_drawdown": 0,
            "sharpe_ratio": 0,
            "profit_factor": 0,
            "avg_win": 0,
            "avg_loss": 0,
            "largest_win": 0,
            "largest_loss": 0
        }
    
    n_trades = len(trades_df)
    wins = trades_df[trades_df['pnl_pct'] > 0]
    losses = trades_df[trades_df['pnl_pct'] < 0]
    
    win_rate = len(wins) / n_trades * 100 if n_trades > 0 else 0
    
    # Calcola drawdown
    cumulative = trades_df['pnl_pct'].cumsum()
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max)
    max_drawdown = drawdown.min()
    
    # Calcola Sharpe ratio (annualizzato)
    returns = trades_df['pnl_pct'] / 100
    sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
    
    # Calcola profit factor
    gross_profit = wins['pnl_pct'].sum() if not wins.empty else 0
    gross_loss = abs(losses['pnl_pct'].sum()) if not losses.empty else 0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else 999
    
    return {
        "total_trades": n_trades,
        "win_rate": round(win_rate, 2),
        "avg_pnl": round(trades_df['pnl_pct'].mean(), 2),
        "total_pnl": round(trades_df['pnl_pct'].sum(), 2),
        "max_drawdown": round(max_drawdown, 2),
        "sharpe_ratio": round(sharpe, 2),
        "profit_factor": round(profit_factor, 2),
        "avg_win": round(wins['pnl_pct'].mean(), 2) if not wins.empty else 0,
        "avg_loss": round(losses['pnl_pct'].mean(), 2) if not losses.empty else 0,
        "largest_win": round(wins['pnl_pct'].max(), 2) if not wins.empty else 0,
        "largest_loss": round(losses['pnl_pct'].min(), 2) if not losses.empty else 0
    }

def run_annual_backtest(symbol: str, year: int = 2025, use_mtf: bool = True):
    """
    Esegue backtest su un intero anno
    """
    # Scarica dati annuali da Yahoo
    df = fetch_yf_ohlcv(symbol, interval="1h", period="2y", tail=10000)
    
    if df is None or len(df) < 2000:
        return None
    
    # Filtra per anno
    df['year'] = pd.to_datetime(df['datetime']).dt.year
    df_year = df[df['year'] == year].copy()
    
    if len(df_year) < 500:
        return None
    
    # Esegui backtest
    results = backtest_engine(df_year, use_mtf=use_mtf)
    
    if results is None or results['trades'].empty:
        return {
            "symbol": symbol,
            "year": year,
            "trades": pd.DataFrame(),
            "stats": calculate_performance_metrics(pd.DataFrame()),
            "message": "Nessun trade generato"
        }
    
    # Calcola metriche
    stats = calculate_performance_metrics(results['trades'])
    
    return {
        "symbol": symbol,
        "year": year,
        "trades": results['trades'],
        "stats": stats,
        "df": df_year
    }

def render_annual_backtest_panel(symbol):
    """Renderizza pannello backtest annuale"""
    
    st.markdown("### 📅 Backtest Annuale")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        year = st.selectbox("Anno", [2025, 2024, 2023, 2022], index=0, key=f"annual_year_{symbol}")
    
    with col2:
        use_mtf = st.checkbox("Usa MTF", value=True, key=f"annual_mtf_{symbol}")
    
    with col3:
        run_bt = st.button("🚀 Esegui Backtest Annuale", use_container_width=True, type="primary", key=f"annual_btn_{symbol}")
    
    if run_bt:
        with st.spinner(f"📊 Eseguo backtest per {symbol} {year}..."):
            results = run_annual_backtest(symbol, year, use_mtf)
            
            if results is None:
                st.warning(f"Dati insufficienti per {symbol} nel {year}")
                return
            
            if results['trades'].empty:
                st.info(f"Nessun trade generato per {symbol} nel {year}")
                return
            
            stats = results['stats']
            
            # Metriche principali
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Trades", stats['total_trades'])
            col_m2.metric("Win Rate", f"{stats['win_rate']:.1f}%")
            col_m3.metric("PnL Totale", f"{stats['total_pnl']:+.2f}%")
            col_m4.metric("Sharpe", stats['sharpe_ratio'])
            
            col_n1, col_n2, col_n3, col_n4 = st.columns(4)
            col_n1.metric("Max DD", f"{stats['max_drawdown']:.1f}%")
            col_n2.metric("Profit Factor", stats['profit_factor'])
            col_n3.metric("Avg Win", f"{stats['avg_win']:+.2f}%")
            col_n4.metric("Avg Loss", f"{stats['avg_loss']:.2f}%")
            
            # Distribuzione mensile
            if not results['trades'].empty:
                trades_df = results['trades'].copy()
                trades_df['month'] = pd.to_datetime(trades_df['time_exit']).dt.to_period('M')
                monthly = trades_df.groupby('month')['pnl_pct'].sum().reset_index()
                monthly['month'] = monthly['month'].astype(str)
                
                st.markdown("#### 📈 Performance Mensile")
                
                fig = go.Figure()
                colors = ['#00ff88' if x > 0 else '#ff3344' for x in monthly['pnl_pct']]
                
                fig.add_trace(go.Bar(
                    x=monthly['month'],
                    y=monthly['pnl_pct'],
                    marker_color=colors,
                    text=monthly['pnl_pct'].round(1),
                    textposition='outside',
                    name='PnL %'
                ))
                
                fig.update_layout(
                    template='plotly_dark',
                    height=300,
                    margin=dict(l=0, r=0, t=30, b=0),
                    xaxis_title="Mese",
                    yaxis_title="PnL %",
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Curva di equity
                st.markdown("#### 📈 Curva di Equity")
                
                equity = trades_df['pnl_pct'].cumsum().reset_index()
                equity.columns = ['trade', 'equity']
                
                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(
                    y=equity['equity'],
                    mode='lines',
                    line=dict(color='#f0b90b', width=3),
                    fill='tozeroy',
                    name='Equity'
                ))
                
                fig2.update_layout(
                    template='plotly_dark',
                    height=250,
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis_title="Trade #",
                    yaxis_title="PnL Cumulativo %",
                    showlegend=False
                )
                
                st.plotly_chart(fig2, use_container_width=True)
                
                # Tabella trades
                with st.expander("📋 Dettaglio Trades"):
                    display_df = trades_df[['time_exit', 'side', 'entry', 'exit', 'reason', 'pnl_pct']].copy()
                    display_df['pnl_pct'] = display_df['pnl_pct'].round(2)
                    display_df['entry'] = display_df['entry'].round(2)
                    display_df['exit'] = display_df['exit'].round(2)
                    
                    def color_pnl(val):
                        if val > 0:
                            return 'color: #00ff88'
                        elif val < 0:
                            return 'color: #ff3344'
                        return ''
                    
                    styled_df = display_df.style.map(color_pnl, subset=['pnl_pct'])
                    st.dataframe(styled_df, use_container_width=True, hide_index=True)

def simulate_multi_asset_backtest(watchlist, years=[2025, 2024, 2023]):
    """Simula backtest su più asset e più anni"""
    
    results_summary = []
    progress_bar = st.progress(0)
    total = len(watchlist) * len(years)
    count = 0
    
    for symbol in watchlist[:5]:  # Max 5 asset
        for year in years:
            count += 1
            progress_bar.progress(count / total)
            
            res = run_annual_backtest(symbol, year, use_mtf=True)
            if res and res['stats']['total_trades'] > 0:
                results_summary.append({
                    'asset': symbol,
                    'anno': year,
                    'trades': res['stats']['total_trades'],
                    'win_rate': res['stats']['win_rate'],
                    'pnl_totale': res['stats']['total_pnl'],
                    'sharpe': res['stats']['sharpe_ratio'],
                    'max_dd': res['stats']['max_drawdown']
                })
    
    progress_bar.empty()
    return pd.DataFrame(results_summary)