# strategy/optimizer.py
import pandas as pd
import numpy as np
import streamlit as st
from itertools import product
from datetime import datetime
import plotly.graph_objects as go
from strategy.backtest import backtest_engine
from providers.yahoo_provider import fetch_yf_ohlcv
from config import SL_ATR, TP_ATR, ADX_MIN, RSI_LONG_MAX, RSI_SHORT_MIN

def optimize_parameters_auto(symbol, year=2025):
    """
    Ottimizzazione automatica dei parametri per un asset specifico
    """
    # Carica dati specifici per l'asset
    with st.spinner(f"📥 Caricamento dati {symbol} per {year}..."):
        df = fetch_yf_ohlcv(symbol, interval="1h", period="2y", tail=5000)
        
        if df is None or len(df) < 1000:
            st.warning(f"⚠️ Dati insufficienti per {symbol}")
            return None
        
        # Filtra per anno
        df['year'] = pd.to_datetime(df['datetime']).dt.year
        df_year = df[df['year'] == year].copy()
        
        if len(df_year) < 500:
            st.warning(f"⚠️ Pochi dati per {symbol} nel {year}: {len(df_year)} candele")
            return None
    
    # Griglia parametri specifica per tipo di asset
    asset_upper = symbol.upper()
    
    # Parametri personalizzati in base al tipo di asset
    if "BTC" in asset_upper or "ETH" in asset_upper:
        # Criptovalute - più volatili
        sl_values = [1.8, 2.0, 2.2, 2.5, 3.0]
        tp_values = [3.5, 4.0, 4.5, 5.0, 6.0]
        adx_values = [18, 20, 22, 25]
        rsi_long_values = [60, 65, 70, 75]
        rsi_short_values = [25, 30, 35, 40]
    elif "XAU" in asset_upper or "GC" in asset_upper:
        # Oro - meno volatile
        sl_values = [1.2, 1.5, 1.8, 2.0, 2.2]
        tp_values = [2.5, 3.0, 3.5, 4.0, 4.5]
        adx_values = [20, 22, 25, 28]
        rsi_long_values = [60, 65, 70]
        rsi_short_values = [30, 35, 40]
    else:
        # Azioni - default
        sl_values = [1.5, 1.8, 2.0, 2.2, 2.5]
        tp_values = [3.0, 3.5, 4.0, 4.5, 5.0]
        adx_values = [18, 20, 22, 25]
        rsi_long_values = [60, 65, 70]
        rsi_short_values = [30, 35, 40]
    
    results = []
    total_combinations = len(sl_values) * len(tp_values) * len(adx_values) * len(rsi_long_values) * len(rsi_short_values)
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    count = 0
    
    # Salva parametri originali
    original_params = {
        'SL_ATR': SL_ATR,
        'TP_ATR': TP_ATR,
        'ADX_MIN': ADX_MIN,
        'RSI_LONG_MAX': RSI_LONG_MAX,
        'RSI_SHORT_MIN': RSI_SHORT_MIN
    }
    
    for sl, tp, adx, rsi_long, rsi_short in product(
        sl_values, tp_values, adx_values, rsi_long_values, rsi_short_values
    ):
        # Aggiorna progress
        count += 1
        progress = count / total_combinations
        progress_bar.progress(progress)
        status_text.text(f"🔄 Test combinazione {count}/{total_combinations} | SL:{sl} TP:{tp} ADX:{adx}")
        
        # Importa config e modifica parametri temporaneamente
        import config
        config.SL_ATR = sl
        config.TP_ATR = tp
        config.ADX_MIN = adx
        config.RSI_LONG_MAX = rsi_long
        config.RSI_SHORT_MIN = rsi_short
        
        # Esegui backtest
        try:
            bt_result = backtest_engine(df_year, use_mtf=True)
            
            if bt_result and not bt_result['trades'].empty:
                stats = bt_result['stats']
                
                # Calcola score composito (0-100)
                win_rate_score = min(stats['winrate'] * 1.5, 50)  # Max 50 punti
                pnl_score = max(0, min(stats['total_pnl_pct'] * 2, 30))  # Max 30 punti
                sharpe_score = max(0, min(stats.get('sharpe_ratio', 0) * 10, 20))  # Max 20 punti
                
                total_score = win_rate_score + pnl_score + sharpe_score
                
                results.append({
                    'SL': sl,
                    'TP': tp,
                    'ADX': adx,
                    'RSI_LONG': rsi_long,
                    'RSI_SHORT': rsi_short,
                    'trades': stats['n'],
                    'win_rate': stats['winrate'],
                    'pnl_total': stats['total_pnl_pct'],
                    'sharpe': stats.get('sharpe_ratio', 0),
                    'score': total_score
                })
        except Exception as e:
            # Ignora errori e continua
            pass
    
    # Ripristina parametri originali
    import config
    config.SL_ATR = original_params['SL_ATR']
    config.TP_ATR = original_params['TP_ATR']
    config.ADX_MIN = original_params['ADX_MIN']
    config.RSI_LONG_MAX = original_params['RSI_LONG_MAX']
    config.RSI_SHORT_MIN = original_params['RSI_SHORT_MIN']
    
    progress_bar.empty()
    status_text.empty()
    
    if not results:
        return None
    
    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values('score', ascending=False)
    
    best = df_results.iloc[0].to_dict()
    
    return {
        'best_params': best,
        'all_results': df_results,
        'asset': symbol,
        'year': year,
        'original_params': original_params
    }

def render_optimizer_panel(symbol):
    """Renderizza pannello ottimizzazione automatica"""
    
    st.markdown("## ⚙️ Ottimizzazione Parametri")
    st.caption(f"Ricerca parametri ottimali per **{symbol}**")
    
    # Mostra parametri attuali
    with st.container(border=True):
        st.markdown("### 📊 Parametri Attuali")
        col_a1, col_a2, col_a3, col_a4, col_a5 = st.columns(5)
        col_a1.metric("SL (ATR)", f"{SL_ATR}x")
        col_a2.metric("TP (ATR)", f"{TP_ATR}x")
        col_a3.metric("ADX Min", ADX_MIN)
        col_a4.metric("RSI Long Max", RSI_LONG_MAX)
        col_a5.metric("RSI Short Min", RSI_SHORT_MIN)
    
    # Selezione anno
    col1, col2 = st.columns([1, 3])
    with col1:
        year = st.selectbox(
            "Anno di ottimizzazione",
            [2025, 2024, 2023, 2022],
            index=0,
            key="opt_year_auto"
        )
    
    # Bottone ottimizzazione
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        run_opt = st.button(
            "🚀 AVVIA OTTIMIZZAZIONE", 
            use_container_width=True, 
            type="primary"
        )
    
    if run_opt:
        results = optimize_parameters_auto(symbol, year)
        
        if results:
            best = results['best_params']
            
            st.success(f"✅ Ottimizzazione completata per {symbol}!")
            
            # Parametri ottimali
            st.markdown("### 🏆 Parametri Ottimali Trovati")
            
            col_p1, col_p2, col_p3, col_p4, col_p5 = st.columns(5)
            with col_p1:
                st.metric(
                    "SL (ATR)", 
                    f"{best['SL']}x",
                    delta=f"{best['SL'] - SL_ATR:+.1f}x",
                    delta_color="off"
                )
            with col_p2:
                st.metric(
                    "TP (ATR)", 
                    f"{best['TP']}x",
                    delta=f"{best['TP'] - TP_ATR:+.1f}x",
                    delta_color="off"
                )
            with col_p3:
                st.metric(
                    "ADX Min", 
                    best['ADX'],
                    delta=f"{best['ADX'] - ADX_MIN:+d}",
                    delta_color="off"
                )
            with col_p4:
                st.metric(
                    "RSI Long Max", 
                    best['RSI_LONG'],
                    delta=f"{best['RSI_LONG'] - RSI_LONG_MAX:+d}",
                    delta_color="off"
                )
            with col_p5:
                st.metric(
                    "RSI Short Min", 
                    best['RSI_SHORT'],
                    delta=f"{best['RSI_SHORT'] - RSI_SHORT_MIN:+d}",
                    delta_color="off"
                )
            
            # Performance attesa
            st.markdown("### 📈 Performance Attesa")
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            col_r1.metric("Trades/anno", f"{best['trades']:.0f}")
            col_r2.metric("Win Rate", f"{best['win_rate']:.1f}%")
            col_r3.metric("PnL Atteso", f"{best['pnl_total']:+.2f}%")
            col_r4.metric("Sharpe", f"{best['sharpe']:.2f}")
            
            # Top 10 risultati
            with st.expander("📋 Top 10 Combinazioni"):
                top10 = results['all_results'].head(10)
                display_top = top10[['SL', 'TP', 'ADX', 'RSI_LONG', 'RSI_SHORT', 
                                    'win_rate', 'pnl_total', 'sharpe', 'score']].copy()
                display_top['win_rate'] = display_top['win_rate'].round(1)
                display_top['pnl_total'] = display_top['pnl_total'].round(1)
                display_top['sharpe'] = display_top['sharpe'].round(2)
                display_top['score'] = display_top['score'].round(0)
                st.dataframe(display_top, use_container_width=True, hide_index=True)
            
            # Grafico distribuzione
            st.markdown("### 📊 Distribuzione Performance")
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=results['all_results']['SL'],
                y=results['all_results']['score'],
                mode='markers',
                marker=dict(
                    size=results['all_results']['win_rate'],
                    color=results['all_results']['pnl_total'],
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="PnL %")
                ),
                text=results['all_results'].apply(
                    lambda x: f"SL:{x['SL']} TP:{x['TP']}<br>Win:{x['win_rate']:.1f}% PnL:{x['pnl_total']:+.1f}%",
                    axis=1
                ),
                hoverinfo='text'
            ))
            
            fig.update_layout(
                template='plotly_dark',
                height=400,
                title="Score per combinazione SL/TP",
                xaxis_title="SL (ATR)",
                yaxis_title="Score"
            )
            
            st.plotly_chart(fig, use_container_width=True)
