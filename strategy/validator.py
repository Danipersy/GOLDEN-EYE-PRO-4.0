# strategy/validator.py
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime
import plotly.graph_objects as go
from strategy.annual_backtest import run_annual_backtest

def validate_strategy(selected_assets, years=[2023, 2024, 2025]):
    """
    Valida la strategia su più asset e anni
    """
    results = []
    progress_bar = st.progress(0)
    total_tests = len(selected_assets) * len(years)
    current_test = 0
    skipped = 0
    
    for symbol in selected_assets:
        for year in years:
            try:
                res = run_annual_backtest(symbol, year, use_mtf=True)
                
                if res and res['stats']['total_trades'] > 0:
                    results.append({
                        'asset': symbol,
                        'anno': year,
                        'trades': res['stats']['total_trades'],
                        'win_rate': res['stats']['win_rate'],
                        'pnl_totale': res['stats']['total_pnl'],
                        'sharpe': res['stats']['sharpe_ratio'],
                        'max_dd': res['stats']['max_drawdown'],
                        'profit_factor': res['stats']['profit_factor'],
                        'avg_win': res['stats']['avg_win'],
                        'avg_loss': res['stats']['avg_loss']
                    })
                else:
                    skipped += 1
            except Exception as e:
                skipped += 1
            
            current_test += 1
            progress_bar.progress(current_test / total_tests)
    
    progress_bar.empty()
    return pd.DataFrame(results)

def analyze_strategy_quality(df_results):
    """
    Analizza qualità della strategia
    """
    if df_results.empty:
        return {
            'score': 0,
            'voto': 'F',
            'feedback': ['Nessun dato disponibile'],
            'avg_win_rate': 0,
            'avg_sharpe': 0,
            'avg_pf': 0,
            'avg_dd': 0
        }
    
    feedback = []
    score = 0
    
    # 1. Win rate medio
    avg_win_rate = df_results['win_rate'].mean()
    if avg_win_rate >= 60:
        score += 30
        feedback.append(f"✅ Win rate eccellente: {avg_win_rate:.1f}%")
    elif avg_win_rate >= 55:
        score += 20
        feedback.append(f"👍 Win rate buono: {avg_win_rate:.1f}%")
    elif avg_win_rate >= 50:
        score += 10
        feedback.append(f"⚠️ Win rate accettabile: {avg_win_rate:.1f}%")
    else:
        feedback.append(f"❌ Win rate basso: {avg_win_rate:.1f}%")
    
    # 2. Sharpe ratio medio
    avg_sharpe = df_results['sharpe'].mean()
    if avg_sharpe >= 2:
        score += 30
        feedback.append(f"✅ Sharpe eccellente: {avg_sharpe:.2f}")
    elif avg_sharpe >= 1.5:
        score += 20
        feedback.append(f"👍 Sharpe buono: {avg_sharpe:.2f}")
    elif avg_sharpe >= 1:
        score += 10
        feedback.append(f"⚠️ Sharpe accettabile: {avg_sharpe:.2f}")
    else:
        feedback.append(f"❌ Sharpe basso: {avg_sharpe:.2f}")
    
    # 3. Profit factor medio
    avg_pf = df_results['profit_factor'].mean()
    if avg_pf >= 2.5:
        score += 20
        feedback.append(f"✅ Profit factor eccellente: {avg_pf:.2f}")
    elif avg_pf >= 2:
        score += 15
        feedback.append(f"👍 Profit factor buono: {avg_pf:.2f}")
    elif avg_pf >= 1.5:
        score += 10
        feedback.append(f"⚠️ Profit factor accettabile: {avg_pf:.2f}")
    else:
        feedback.append(f"❌ Profit factor basso: {avg_pf:.2f}")
    
    # 4. Max drawdown
    avg_dd = abs(df_results['max_dd'].mean())
    if avg_dd <= 15:
        score += 20
        feedback.append(f"✅ Drawdown controllato: {avg_dd:.1f}%")
    elif avg_dd <= 25:
        score += 10
        feedback.append(f"⚠️ Drawdown moderato: {avg_dd:.1f}%")
    else:
        feedback.append(f"❌ Drawdown alto: {avg_dd:.1f}%")
    
    # Voto finale
    if score >= 90:
        voto = "A+"
    elif score >= 80:
        voto = "A"
    elif score >= 70:
        voto = "B"
    elif score >= 60:
        voto = "C"
    elif score >= 50:
        voto = "D"
    else:
        voto = "F"
    
    return {
        'score': score,
        'voto': voto,
        'feedback': feedback,
        'avg_win_rate': avg_win_rate,
        'avg_sharpe': avg_sharpe,
        'avg_pf': avg_pf,
        'avg_dd': avg_dd
    }

def render_validation_panel(watchlist):
    """Renderizza pannello validazione strategia con selettore manuale"""
    
    st.markdown("## 🎯 Validazione Strategia")
    st.caption("Test su multipli asset e anni per valutare la robustezza")
    
    # Layout a colonne per i selettori
    col1, col2 = st.columns(2)
    
    with col1:
        # Selettore manuale degli asset
        selected_assets = st.multiselect(
            "📈 Scegli gli asset da validare",
            options=watchlist,
            default=watchlist[:3] if len(watchlist) >= 3 else watchlist,
            help="Seleziona gli asset che vuoi testare (max 5 consigliato)"
        )
        
        if selected_assets:
            st.caption(f"✅ {len(selected_assets)} asset selezionati")
    
    with col2:
        # Selettore anni
        anni = st.multiselect(
            "📅 Anni da testare",
            [2020, 2021, 2022, 2023, 2024, 2025],
            default=[2023, 2024, 2025],
            help="Seleziona gli anni per il backtest"
        )
        
        if anni:
            st.caption(f"✅ {len(anni)} anni selezionati")
    
    # Opzioni avanzate in expander
    with st.expander("⚙️ Opzioni avanzate", expanded=False):
        col_adv1, col_adv2 = st.columns(2)
        
        with col_adv1:
            max_trades = st.slider(
                "Max trades per asset", 
                min_value=10, 
                max_value=200, 
                value=100,
                help="Filtra asset con troppi trades (anomalie)"
            )
        
        with col_adv2:
            min_trades = st.slider(
                "Min trades richiesti", 
                min_value=1, 
                max_value=50, 
                value=5,
                help="Numero minimo di trades per considerare valido un test"
            )
    
    # Bottone principale
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        run_button = st.button(
            "🚀 AVVIA VALIDAZIONE", 
            use_container_width=True, 
            type="primary",
            disabled=not (selected_assets and anni)
        )
    
    if run_button:
        if not selected_assets:
            st.warning("⚠️ Seleziona almeno un asset")
            return
        
        if not anni:
            st.warning("⚠️ Seleziona almeno un anno")
            return
        
        # Esegui validazione
        with st.spinner(f"📊 Analisi in corso su {len(selected_assets)} asset per {len(anni)} anni..."):
            results = validate_strategy(selected_assets, anni)
            
            if not results.empty:
                # Filtra per numero minimo di trades
                results = results[results['trades'] >= min_trades]
                results = results[results['trades'] <= max_trades]
                
                if results.empty:
                    st.warning(f"⚠️ Nessun test con almeno {min_trades} trades")
                    return
                
                # Analizza qualità
                analysis = analyze_strategy_quality(results)
                
                # Metriche principali
                st.markdown("### 📊 Riepilogo Performance")
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                with col_m1:
                    st.metric(
                        "Score Qualità", 
                        f"{analysis['score']}/100",
                        help="Punteggio composito basato su win rate, sharpe, profit factor e drawdown"
                    )
                
                with col_m2:
                    st.metric(
                        "Voto", 
                        analysis['voto'],
                        help="A+ = Eccellente, A = Ottimo, B = Buono, C = Discreto, D = Sufficiente, F = Scarso"
                    )
                
                with col_m3:
                    st.metric(
                        "Test Validati", 
                        len(results),
                        help=f"Numero di test con almeno {min_trades} trades"
                    )
                
                with col_m4:
                    st.metric(
                        "Asset Testati", 
                        results['asset'].nunique(),
                        help="Numero di asset unici nei test"
                    )
                
                # Feedback dettagliato
                with st.container(border=True):
                    st.markdown("### 📈 Analisi Qualità")
                    
                    col_f1, col_f2 = st.columns(2)
                    
                    with col_f1:
                        for msg in analysis['feedback'][:2]:
                            st.markdown(msg)
                    
                    with col_f2:
                        for msg in analysis['feedback'][2:]:
                            st.markdown(msg)
                
                # Tabella risultati
                st.markdown("### 📋 Dettaglio Test")
                
                # Formatta dataframe per migliore visualizzazione
                display_df = results.copy()
                display_df['win_rate'] = display_df['win_rate'].round(1)
                display_df['pnl_totale'] = display_df['pnl_totale'].round(1)
                display_df['sharpe'] = display_df['sharpe'].round(2)
                display_df['max_dd'] = display_df['max_dd'].round(1)
                display_df['profit_factor'] = display_df['profit_factor'].round(2)
                
                # Colora in base al PnL
                def color_pnl(val):
                    if val > 0:
                        return 'color: #00ff88'
                    elif val < 0:
                        return 'color: #ff3344'
                    return ''
                
                styled_df = display_df.style.map(color_pnl, subset=['pnl_totale'])
                st.dataframe(styled_df, use_container_width=True, hide_index=True)
                
                # Grafico comparativo
                st.markdown("### 📊 Performance Annuale per Asset")
                
                if not results.empty and 'anno' in results.columns and 'pnl_totale' in results.columns:
                    fig = go.Figure()
                    
                    for asset in results['asset'].unique():
                        asset_data = results[results['asset'] == asset]
                        if not asset_data.empty:
                            fig.add_trace(go.Bar(
                                name=asset,
                                x=asset_data['anno'].astype(str),
                                y=asset_data['pnl_totale'],
                                text=asset_data['pnl_totale'].round(1),
                                textposition='outside',
                                textfont=dict(size=10)
                            ))
                    
                    if len(fig.data) > 0:
                        fig.update_layout(
                            template='plotly_dark',
                            height=400,
                            margin=dict(l=40, r=40, t=40, b=40),
                            xaxis_title="Anno",
                            yaxis_title="PnL %",
                            barmode='group',
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="right",
                                x=1
                            )
                        )
                        
                        fig.update_yaxes(zeroline=True, zerolinecolor='#30363d')
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("ℹ️ Dati insufficienti per il grafico")
                
                # Statistiche aggregate
                st.markdown("### 📈 Statistiche Aggregate")
                
                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                
                with col_s1:
                    st.metric(
                        "Win Rate Medio", 
                        f"{results['win_rate'].mean():.1f}%"
                    )
                
                with col_s2:
                    st.metric(
                        "PnL Medio Annuo", 
                        f"{results['pnl_totale'].mean():+.2f}%"
                    )
                
                with col_s3:
                    st.metric(
                        "Sharpe Medio", 
                        f"{results['sharpe'].mean():.2f}"
                    )
                
                with col_s4:
                    st.metric(
                        "Max Drawdown Medio", 
                        f"{abs(results['max_dd']).mean():.1f}%"
                    )
                
                # Best e worst performer
                col_b1, col_b2 = st.columns(2)
                
                with col_b1:
                    best = results.loc[results['pnl_totale'].idxmax()]
                    st.success(
                        f"🏆 **Best Performer**: {best['asset']} {best['anno']} "
                        f"con {best['pnl_totale']:+.2f}% (WR: {best['win_rate']:.1f}%)"
                    )
                
                with col_b2:
                    worst = results.loc[results['pnl_totale'].idxmin()]
                    st.error(
                        f"📉 **Worst Performer**: {worst['asset']} {worst['anno']} "
                        f"con {worst['pnl_totale']:.2f}% (WR: {worst['win_rate']:.1f}%)"
                    )
                
                # Consiglio finale
                st.markdown("---")
                if analysis['voto'] in ['A+', 'A']:
                    st.success("✅ **STRATEGIA ROBUSTA** - I risultati sono eccellenti su più asset e anni. Puoi procedere con paper trading con alta confidenza!")
                elif analysis['voto'] in ['B', 'C']:
                    st.warning("⚠️ **STRATEGIA ACCETTABILE** - I risultati sono discreti ma non eccellenti. Considera di ottimizzare i parametri prima del paper trading.")
                else:
                    st.error("❌ **STRATEGIA DEBOLE** - I risultati non sono consistenti. Rivedi i parametri o la logica di trading prima di procedere.")
                
                # Download risultati
                csv = results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    "📥 Download Report CSV",
                    csv,
                    f"validazione_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
                    "text/csv",
                    use_container_width=True
                )
                
            else:
                st.warning("⚠️ Nessun risultato valido. Prova con parametri diversi o più asset.")
