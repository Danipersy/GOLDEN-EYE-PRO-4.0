# ui_streamlit/components/backtest_panel.py
import streamlit as st
import pandas as pd
from strategy.backtest import backtest_engine, load_history_for_backtest
from strategy.annual_backtest import render_annual_backtest_panel, simulate_multi_asset_backtest
from providers.yahoo_provider import fetch_yf_ohlcv
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h

def render_backtest_panel(focus):
    """Renderizza pannello backtest"""
    
    st.markdown("---")
    st.markdown("## Backtest")
    
    tab1, tab2, tab3 = st.tabs(["📊 Backtest Rapido", "📅 Backtest Annuale", "📈 Multi-Asset"])
    
    with tab1:
        # Backtest rapido
        col1, col2, col3 = st.columns([1.4, 1.0, 1.0])
        
        with col1:
            st.selectbox("Sorgente", ["Yahoo (gratis)", "TwelveData"], key="bt_source")
        
        with col2:
            st.number_input("Giorni", 3, 60, 15, key="bt_days")
        
        with col3:
            run_bt = st.button("▶️ Esegui", use_container_width=True, type="primary")
        
        st.checkbox("Usa MTF", value=True, key="bt_mtf")
        
        if run_bt:
            days = int(st.session_state.bt_days)
            src_choice = st.session_state.bt_source
            use_mtf = bool(st.session_state.bt_mtf)
            
            df_bt, used_src = load_history_for_backtest(
                focus, days, src_choice, fetch_yf_ohlcv, fetch_td_15m
            )
            
            if df_bt is None:
                st.error("Dati non disponibili")
                return
            
            df1h_bt = df4h_bt = None
            if use_mtf and used_src == "TwelveData":
                df1h_bt, _ = fetch_td_1h(focus)
                df4h_bt, _ = fetch_td_4h(focus)
            
            bt = backtest_engine(df_bt, use_mtf=use_mtf, df_1h=df1h_bt, df_4h=df4h_bt)
            
            if bt:
                stats = bt["stats"]
                st.caption(f"Sorgente: {used_src} | Asset: {focus}")
                
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Trades", stats.get("n", 0))
                m2.metric("Win rate", f"{stats.get('winrate', 0):.1f}%")
                m3.metric("Avg PnL", f"{stats.get('avg_pnl_pct', 0):+.2f}%")
                m4.metric("Total PnL", f"{stats.get('total_pnl_pct', 0):+.2f}%")
                
                if not bt["trades"].empty:
                    st.dataframe(bt["trades"], use_container_width=True)
    
    with tab2:
        # Backtest annuale
        render_annual_backtest_panel(focus)
    
    with tab3:
        # Multi-asset backtest
        st.markdown("### 📊 Backtest Multi-Asset")
        st.caption("Analizza performance su più asset e più anni")
        
        if st.button("🚀 Avvia Analisi Multi-Asset", use_container_width=True):
            with st.spinner("Analisi in corso (può richiedere qualche minuto)..."):
                watchlist = st.session_state.watchlist[:5]
                results_df = simulate_multi_asset_backtest(watchlist, [2025, 2024, 2023])
                
                if not results_df.empty:
                    st.dataframe(results_df, use_container_width=True)
                    
                    st.markdown("#### 📈 Statistiche Aggregate")
                    col_a1, col_a2, col_a3 = st.columns(3)
                    col_a1.metric("Trades Medi", f"{results_df['trades'].mean():.0f}")
                    col_a2.metric("Win Rate Medio", f"{results_df['win_rate'].mean():.1f}%")
                    col_a3.metric("PnL Medio Annuo", f"{results_df['pnl_totale'].mean():+.2f}%")
                    
                    best = results_df.loc[results_df['pnl_totale'].idxmax()]
                    st.success(f"🏆 Best Performer: {best['asset']} {best['anno']} con {best['pnl_totale']:+.2f}%")
                else:
                    st.warning("Nessun risultato significativo")