# ui_streamlit/components/backtest_ui.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

from strategy.backtest import backtest_engine, load_history_for_backtest
from ui_streamlit.components.backtest_stats import show_signal_breakdown, show_timeline_chart
from config import DEFAULT_SYMBOLS, MIN_DAYS_HISTORY

def render_backtest_ui(fetch_yf, fetch_td_15m, fetch_td_1h, fetch_td_4h):
    """Renderizza l'interfaccia di backtest"""
    
    st.markdown("## 📊 Backtest Strategia")
    st.markdown("Testa la strategia su dati storici con classificazione STRONG/WEAK")
    
    # Sidebar per parametri backtest
    with st.sidebar:
        st.markdown("### ⚙️ Parametri Backtest")
        
        # Selezione simbolo
        symbol = st.selectbox(
            "Simbolo",
            options=DEFAULT_SYMBOLS + ["Personalizzato"],
            index=0
        )
        
        if symbol == "Personalizzato":
            symbol = st.text_input("Inserisci simbolo", value="BTCUSDT").upper()
        
        # Fonte dati
        source = st.radio(
            "Fonte Dati",
            options=["TwelveData", "Yahoo (gratis)"],
            index=0,
            help="TwelveData: più preciso, Yahoo: gratuito ma meno affidabile"
        )
        
        # Giorni di backtest
        days = st.slider(
            "Giorni di backtest",
            min_value=MIN_DAYS_HISTORY,
            max_value=180,
            value=60,
            step=5,
            help="Numero di giorni di storico da analizzare"
        )
        
        # Opzioni MTF
        st.markdown("### 📈 Multi-Timeframe")
        use_mtf = st.checkbox(
            "Abilita MTF",
            value=True,
            help="Usa timeframe 1h e 4h per conferma trend"
        )
        
        # Parametri avanzati
        with st.expander("🔧 Parametri Avanzati"):
            st.markdown("**Soglie STRONG**")
            col1, col2 = st.columns(2)
            with col1:
                rsi_long_max = st.number_input("RSI Long Max", value=55, min_value=30, max_value=80)
            with col2:
                rsi_short_min = st.number_input("RSI Short Min", value=45, min_value=20, max_value=70)
            
            adx_min = st.number_input("ADX Min", value=25, min_value=10, max_value=50)
            
            st.markdown("**Coefficienti SL/TP**")
            col1, col2 = st.columns(2)
            with col1:
                strong_sl = st.number_input("STRONG SL (ATR)", value=1.2, min_value=0.5, max_value=5.0, step=0.1)
                strong_tp = st.number_input("STRONG TP (ATR)", value=2.5, min_value=1.0, max_value=10.0, step=0.1)
            with col2:
                weak_sl = st.number_input("WEAK SL (ATR)", value=2.0, min_value=0.5, max_value=5.0, step=0.1)
                weak_tp = st.number_input("WEAK TP (ATR)", value=4.0, min_value=1.0, max_value=10.0, step=0.1)
        
        # Pulsante esegui
        run_bt = st.button("🚀 Esegui Backtest", type="primary", use_container_width=True)
        
        st.markdown("---")
        st.caption("Il backtest simula l'esecuzione della strategia su dati storici")
    
    # Area principale
    if run_bt:
        with st.spinner("⏳ Caricamento dati ed esecuzione backtest..."):
            try:
                # Carica dati
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("📥 Caricamento dati 15m...")
                df_15m, src_used = load_history_for_backtest(symbol, days, source, fetch_yf, fetch_td_15m)
                progress_bar.progress(30)
                
                if df_15m is None or df_15m.empty:
                    st.error(f"❌ Impossibile caricare dati per {symbol}")
                    return
                
                df_1h = df_4h = None
                if use_mtf:
                    status_text.text("📥 Caricamento dati 1h...")
                    if source == "Yahoo (gratis)":
                        df_1h, _ = fetch_yf(symbol, "1h", f"{days}d", tail=days*24)
                    else:
                        df_1h, _ = fetch_td_1h(symbol)
                    progress_bar.progress(50)
                    
                    status_text.text("📥 Caricamento dati 4h...")
                    if source == "Yahoo (gratis)":
                        df_4h, _ = fetch_yf(symbol, "4h", f"{days}d", tail=days*6)
                    else:
                        df_4h, _ = fetch_td_4h(symbol)
                    progress_bar.progress(70)
                
                status_text.text("⚙️ Esecuzione backtest...")
                
                # Esegui backtest
                start_time = time.time()
                results = backtest_engine(df_15m, use_mtf, df_1h, df_4h)
                elapsed = time.time() - start_time
                
                progress_bar.progress(100)
                status_text.text("✅ Backtest completato!")
                time.sleep(0.5)
                progress_bar.empty()
                status_text.empty()
                
                if results is None:
                    st.warning("⚠️ Dati insufficienti per il backtest")
                    return
                
                # Mostra risultati
                st.markdown(f"## 📈 Risultati Backtest - {symbol}")
                
                # Metriche principali
                stats = results['stats']
                trades = results['trades']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "📊 Trades Totali",
                        stats['n'],
                        delta=f"{stats['strong_trades']} STRONG / {stats['weak_trades']} WEAK" if stats['n'] > 0 else None
                    )
                
                with col2:
                    st.metric(
                        "🎯 Winrate",
                        f"{stats['winrate']:.1f}%",
                        delta=f"{stats['winrate'] - 50:.1f}% vs 50%" if stats['n'] > 0 else None
                    )
                
                with col3:
                    st.metric(
                        "📈 Avg P&L",
                        f"{stats['avg_pnl_pct']:.2f}%",
                        delta=None
                    )
                
                with col4:
                    st.metric(
                        "⏱️ Tempo",
                        f"{elapsed:.1f}s",
                        delta=None
                    )
                
                st.markdown("---")
                
                # Performance per tipo segnale
                if not trades.empty:
                    show_signal_breakdown(trades)
                    
                    st.markdown("---")
                    
                    # Timeline trade
                    show_timeline_chart(trades, results.get('df_indicators'))
                    
                    st.markdown("---")
                    
                    # Tabella trades
                    with st.expander("📋 Dettaglio Trades", expanded=False):
                        # Formatta dataframe per visualizzazione
                        display_trades = trades.copy()
                        
                        # Seleziona e riordina colonne
                        cols_to_show = ['time_exit', 'side', 'entry', 'exit', 'reason', 
                                      'pnl_pct', 'signal_strength', 'signal_type',
                                      'rsi_entry', 'adx_entry', 'slope_entry']
                        
                        available_cols = [c for c in cols_to_show if c in display_trades.columns]
                        display_trades = display_trades[available_cols]
                        
                        # Formatta numeri
                        for col in ['entry', 'exit']:
                            if col in display_trades.columns:
                                display_trades[col] = display_trades[col].map(lambda x: f"{x:.2f}")
                        
                        if 'pnl_pct' in display_trades.columns:
                            display_trades['pnl_pct'] = display_trades['pnl_pct'].map(lambda x: f"{x:.2f}%")
                        
                        if 'rsi_entry' in display_trades.columns:
                            display_trades['rsi_entry'] = display_trades['rsi_entry'].map(lambda x: f"{x:.1f}")
                        
                        if 'adx_entry' in display_trades.columns:
                            display_trades['adx_entry'] = display_trades['adx_entry'].map(lambda x: f"{x:.1f}")
                        
                        if 'slope_entry' in display_trades.columns:
                            display_trades['slope_entry'] = display_trades['slope_entry'].map(lambda x: f"{x:.3f}")
                        
                        # Rinomina colonne
                        rename_map = {
                            'time_exit': 'Data/Uscita',
                            'side': 'Direzione',
                            'entry': 'Entrata',
                            'exit': 'Uscita',
                            'reason': 'Motivo',
                            'pnl_pct': 'P&L %',
                            'signal_strength': 'Forza',
                            'signal_type': 'Tipo',
                            'rsi_entry': 'RSI Entry',
                            'adx_entry': 'ADX Entry',
                            'slope_entry': 'Pendenza'
                        }
                        
                        display_trades = display_trades.rename(columns={k: v for k, v in rename_map.items() if k in display_trades.columns})
                        
                        st.dataframe(
                            display_trades,
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        # Statistiche riassuntive
                        st.markdown("**📊 Statistiche Riassuntive**")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**Per Direzione**")
                            for side in trades['side'].unique():
                                side_trades = trades[trades['side'] == side]
                                winrate_side = (side_trades['pnl_pct'] > 0).mean() * 100
                                st.text(f"{side}: {len(side_trades)} trades, {winrate_side:.1f}% winrate")
                        
                        with col2:
                            st.markdown("**Per Motivo Uscita**")
                            for reason in trades['reason'].unique():
                                reason_trades = trades[trades['reason'] == reason]
                                st.text(f"{reason}: {len(reason_trades)} trades")
                        
                        with col3:
                            st.markdown("**Per Forza Segnale**")
                            if 'signal_strength' in trades.columns:
                                for strength in trades['signal_strength'].unique():
                                    if strength != 'unknown':
                                        strength_trades = trades[trades['signal_strength'] == strength]
                                        winrate_strength = (strength_trades['pnl_pct'] > 0).mean() * 100
                                        st.text(f"{strength}: {len(strength_trades)} trades, {winrate_strength:.1f}%")
                    
                    # Download CSV
                    csv = trades.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Trades CSV",
                        data=csv,
                        file_name=f"backtest_{symbol}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
            except Exception as e:
                st.error(f"❌ Errore durante il backtest: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
    
    else:
        # Mostra messaggio iniziale
        st.info("👈 Imposta i parametri nella sidebar e clicca 'Esegui Backtest'")
        
        # Esempio di utilizzo
        with st.expander("ℹ️ Come usare il backtest"):
            st.markdown("""
            ### Come interpretare i risultati
            
            Il backtest classifica i segnali in **STRONG** e **WEAK**:
            
            - **💪 Segnali STRONG**: Condizioni più restrittive (RSI ≤ 55, ADX ≥ 25, pendenza > 1.0)
              - SL/TP più stretti (risk management conservativo)
              - Ci aspettiamo maggiore affidabilità
            
            - **📉 Segnali WEAK**: Condizioni più lasche (RSI ≤ 65, ADX ≥ 20, pendenza ≥ 0.2)
              - SL/TP più larghi (più spazio per respirare)
              - Trade meno probabili ma con potenziale maggiore
            
            ### Metriche principali
            
            - **Winrate**: Percentuale di trade vincenti
            - **Avg P&L**: Profitto/perdita medio per trade
            - **STRONG vs WEAK**: Confronto performance tra i due tipi
            
            ### Suggerimenti
            
            - Testa diversi simboli per vedere quale si adatta meglio
            - Confronta winrate STRONG vs WEAK per ottimizzare i filtri
            - Usa almeno 60 giorni di dati per risultati significativi
            """)
        
        # Statistiche veloci (placeholder)
        st.markdown("### 📊 Statistiche Globali (da backtest precedenti)")
        
        # Qui potresti caricare statistiche aggregate da file o DB
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Trades Analizzati", "1,234", delta="+12%")
        
        with col2:
            st.metric("Winrate Medio", "58.3%", delta="+2.1%")
        
        with col3:
            st.metric("Avg P&L", "+1.24%", delta="-0.3%")

# Funzione helper per inizializzare il modulo
def init_backtest_ui():
    """Inizializza lo stato della sessione per backtest UI"""
    if 'backtest_results' not in st.session_state:
        st.session_state.backtest_results = None
    
    if 'backtest_symbol' not in st.session_state:
        st.session_state.backtest_symbol = None
    
    if 'backtest_params' not in st.session_state:
        st.session_state.backtest_params = {}

# Funzione per esportare risultati (utile per confronti)
def export_backtest_results(results, format='json'):
    """Esporta risultati in vari formati"""
    if results is None:
        return None
    
    export_data = {
        'timestamp': datetime.now().isoformat(),
        'stats': results.get('stats', {}),
        'trades_count': len(results.get('trades', [])),
        'summary': {
            'total_trades': results.get('stats', {}).get('n', 0),
            'winrate': results.get('stats', {}).get('winrate', 0),
            'avg_pnl': results.get('stats', {}).get('avg_pnl_pct', 0),
            'strong_trades': results.get('stats', {}).get('strong_trades', 0),
            'weak_trades': results.get('stats', {}).get('weak_trades', 0)
        }
    }
    
    if format == 'json':
        return export_data
    elif format == 'df':
        return results.get('trades', pd.DataFrame())
    else:
        return None
