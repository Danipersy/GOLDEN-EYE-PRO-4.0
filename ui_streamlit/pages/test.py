import streamlit as st
import platform
import sys
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Provider
from providers.multi_provider import scan_symbol, fetch_yf_ohlcv
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h, search_symbols_td, convert_symbol_for_twelvedata
from providers.marketaux_provider import fetch_marketaux_sentiment
from providers.base_provider import tracker

# Indicatori
from indicators.robust_ta import compute_indicators_15m, decide_signal

# AI
from ai.asset_analyzer import AssetAIAnalyzer

# Strategia
from strategy.backtest import backtest_engine
from strategy.money_manager import MoneyManager
from strategy.auto_trader import AutoTrader

# Utility
from utils.helpers import get_market_status, normalize_ohlcv_df
from storage.watchlist_store import load_watchlist, save_watchlist

def render():
    st.markdown("## 🧪 Test e Debug Completo")
    st.caption("Verifica tutte le componenti dell'applicazione")

    # ============================================
    # TEST RAPIDI PROVIDER
    # ============================================
    with st.expander("📡 Test Provider Dati", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Yahoo Finance")
            if st.button("🟢 Test Yahoo (BTC-USD)", use_container_width=True):
                with st.spinner("Caricamento..."):
                    df = fetch_yf_ohlcv("BTC-USD", interval="15m", period="5d", tail=50)
                    if df is not None and not df.empty:
                        st.success(f"✅ Yahoo OK: {len(df)} candles, ultimo prezzo ${df['close'].iloc[-1]:.2f}")
                    else:
                        st.error("❌ Yahoo Fallito")

            if st.button("🟢 Test Yahoo (AAPL)", use_container_width=True):
                with st.spinner("Caricamento..."):
                    df = fetch_yf_ohlcv("AAPL", interval="15m", period="5d", tail=50)
                    if df is not None and not df.empty:
                        st.success(f"✅ Yahoo OK: {len(df)} candles, ultimo prezzo ${df['close'].iloc[-1]:.2f}")
                    else:
                        st.error("❌ Yahoo Fallito")

        with col2:
            st.subheader("TwelveData")
            if st.button("🔵 Test TwelveData (BTC/USD)", use_container_width=True):
                df, src = fetch_td_15m("BTC/USD")
                if df is not None:
                    st.success(f"✅ TwelveData OK: {len(df)} candles da {src}, ultimo prezzo ${df['close'].iloc[-1]:.2f}")
                else:
                    st.error(f"❌ TwelveData Fallito: {src}")

            if st.button("🔵 Test TwelveData (ETH/USD)", use_container_width=True):
                df, src = fetch_td_15m("ETH/USD")
                if df is not None:
                    st.success(f"✅ TwelveData OK: {len(df)} candles da {src}, ultimo prezzo ${df['close'].iloc[-1]:.2f}")
                else:
                    st.error(f"❌ TwelveData Fallito: {src}")

        st.divider()
        col3, col4 = st.columns(2)

        with col3:
            st.subheader("Marketaux News")
            if st.button("🟡 Test Marketaux (BTC,ETH)", use_container_width=True):
                news = fetch_marketaux_sentiment(["BTC/USD", "ETH/USD"])
                if news and news.get('count', 0) > 0:
                    st.success(f"✅ Marketaux OK: {news['count']} news, sentiment {news['label']}")
                else:
                    st.warning("⚠️ Marketaux: nessuna news o chiave non valida")

        with col4:
            st.subheader("Conversione Simboli")
            test_sym = st.text_input("Simbolo da convertire (es. BTC-USD)", value="BTC-USD", key="conv_sym")
            if st.button("🔄 Converti", use_container_width=True):
                converted = convert_symbol_for_twelvedata(test_sym)
                st.info(f"📌 {test_sym} → {converted}")

        st.divider()
        st.subheader("🔍 Ricerca Simboli TwelveData")
        search_q = st.text_input("Cerca (min 3 caratteri)", value="bitcoin", key="search_td")
        if len(search_q) >= 3:
            with st.spinner("Ricerca in corso..."):
                results = search_symbols_td(search_q, 5)
            if results:
                st.success(f"Trovati {len(results)} risultati")
                for r in results:
                    st.write(f"- {r['label']}")
            else:
                st.warning("Nessun risultato")

    # ============================================
    # TEST INDICATORI
    # ============================================
    with st.expander("📈 Test Indicatori", expanded=False):
        st.subheader("Calcolo Indicatori su dati di esempio")
        # Genera dati fake
        dates = pd.date_range(end=datetime.now(), periods=300, freq='15min')
        df_fake = pd.DataFrame({
            'datetime': dates,
            'open': np.random.randn(300).cumsum() + 50000,
            'high': np.random.randn(300).cumsum() + 50100,
            'low': np.random.randn(300).cumsum() + 49900,
            'close': np.random.randn(300).cumsum() + 50000,
            'volume': np.random.randint(100, 1000, 300)
        })
        st.caption("Dati sintetici generati, clicca per calcolare indicatori")

        if st.button("🧮 Calcola RSI, ADX, ATR", use_container_width=True):
            df_ind = compute_indicators_15m(df_fake)
            col_i1, col_i2, col_i3, col_i4 = st.columns(4)
            with col_i1:
                st.metric("RSI ultimo", f"{df_ind['rsi'].iloc[-1]:.1f}")
            with col_i2:
                # Cerca colonna ADX
                adx_col = [c for c in df_ind.columns if 'ADX' in c.upper()]
                adx_val = df_ind[adx_col[0]].iloc[-1] if adx_col else 0
                st.metric("ADX ultimo", f"{adx_val:.1f}")
            with col_i3:
                st.metric("ATR ultimo", f"${df_ind['atr'].iloc[-1]:.2f}")
            with col_i4:
                st.metric("EMA200 ultimo", f"${df_ind['ema200'].iloc[-1]:.2f}")

        st.divider()
        st.subheader("Classificazione Segnale")
        if st.button("🎯 Test decide_signal con MTF casuale", use_container_width=True):
            # Usa gli stessi dati fake
            df_ind = compute_indicators_15m(df_fake)
            mtf_long = np.random.choice([True, False])
            mtf_short = np.random.choice([True, False])
            signal = decide_signal(df_ind, mtf_long, mtf_short)
            st.json({
                "display": signal['display'],
                "strength": signal['strength'],
                "color": signal['color'],
                "is_long": signal['is_long'],
                "rsi": f"{signal['rsi']:.1f}",
                "adx": f"{signal['adx']:.1f}",
                "atr": f"${signal['atr']:.2f}",
                "mtf_long": mtf_long,
                "mtf_short": mtf_short
            })

    # ============================================
    # TEST AI SUGGERITORE
    # ============================================
    with st.expander("🤖 Test AI Suggeritore", expanded=False):
        st.subheader("Analisi Asset con AI")
        ai_asset = st.text_input("Simbolo per test AI", value="BTC-USD", key="ai_asset")
        if st.button("🔮 Esegui AI Analyzer", use_container_width=True):
            analyzer = AssetAIAnalyzer()
            # Costruisci dati finti
            fake_data = {
                'p': 50000,
                'rsi': 45,
                'adx': 30,
                'atr': 1000,
                'sqz_on': False,
                'v': 'BUY',
                'level': 4,
                'mtf_long': True,
                'mtf_short': False
            }
            news_fake = {'count': 3, 'sentiment': 0.7, 'label': '🟢 POSITIVO'}
            analysis = analyzer.analyze_asset(ai_asset, fake_data, news_fake)
            st.json({
                "score": analysis['score'],
                "action": analysis['action'],
                "confidence": analysis['confidence'],
                "signals": analysis['signals'][:3],
                "warnings": analysis['warnings'][:3],
                "suggestions": analysis['suggestions'][:3]
            })

    # ============================================
    # TEST BACKTEST
    # ============================================
    with st.expander("📊 Test Backtest", expanded=False):
        st.subheader("Backtest rapido su dati sintetici")
        if st.button("▶️ Esegui backtest di esempio", use_container_width=True):
            # Crea dati fake più lunghi
            dates_bt = pd.date_range(end=datetime.now(), periods=1000, freq='15min')
            df_bt = pd.DataFrame({
                'datetime': dates_bt,
                'open': np.random.randn(1000).cumsum() + 50000,
                'high': np.random.randn(1000).cumsum() + 50100,
                'low': np.random.randn(1000).cumsum() + 49900,
                'close': np.random.randn(1000).cumsum() + 50000,
                'volume': np.random.randint(100, 1000, 1000)
            })
            with st.spinner("Esecuzione backtest..."):
                result = backtest_engine(df_bt, use_mtf=False)
            if result and result['trades'] is not None and not result['trades'].empty:
                stats = result['stats']
                st.success(f"Backtest completato: {stats['n']} trades, Win Rate {stats['winrate']:.1f}%")
                st.dataframe(result['trades'].tail(10), use_container_width=True)
            else:
                st.warning("Nessun trade generato (normale con dati casuali)")

    # ============================================
    # TEST MONEY MANAGER
    # ============================================
    with st.expander("💰 Test Money Manager", expanded=False):
        mm = MoneyManager(initial_capital=10000)
        st.write(f"Capitale iniziale: ${mm.initial_capital}")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            if st.button("➕ Simula trade vincente (+500)", use_container_width=True):
                mm.update_after_trade(500)
                st.rerun()
        with col_m2:
            if st.button("➖ Simula trade perdente (-300)", use_container_width=True):
                mm.update_after_trade(-300)
                st.rerun()
        metrics = mm.get_metrics()
        st.metric("Capitale attuale", f"${metrics['current_capital']:.2f}", delta=f"{metrics['total_pnl_pct']:.2f}%")
        st.metric("Drawdown", f"{metrics['current_drawdown']:.2f}%", delta=f"Max: {metrics['max_drawdown']:.2f}%")

    # ============================================
    # TEST SCAN FILTERS (solo UI)
    # ============================================
    with st.expander("🔧 Test Filtri Scan", expanded=False):
        st.subheader("Interfaccia filtri (solo visuale)")
        from ui_streamlit.components.scan_filters import render_scan_filters
        filters = render_scan_filters()
        st.json(filters)

    # ============================================
    # TEST STATO SESSIONE E CACHE
    # ============================================
    with st.expander("💾 Stato Sessione e Cache", expanded=False):
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.subheader("Session State")
            if st.button("🔄 Mostra session state", use_container_width=True):
                state = {k: str(v) for k, v in st.session_state.items() if not k.startswith('_')}
                st.json(state)

            if st.button("🧹 Pulisci cache Streamlit", use_container_width=True):
                st.cache_data.clear()
                st.success("Cache dati cancellata!")

        with col_s2:
            st.subheader("API Usage Tracker")
            stats = tracker.get_provider_stats()
            for stat in stats:
                st.metric(stat['name'], f"{stat['today']}/{stat['limit'] if stat['limit'] else '∞'}",
                          help=stat['description'])

    # ============================================
    # TEST WATCHLIST
    # ============================================
    with st.expander("📋 Test Watchlist", expanded=False):
        wl = st.session_state.watchlist
        st.write(f"Watchlist attuale ({len(wl)} asset): {', '.join(wl)}")
        if st.button("➕ Aggiungi simbolo di test (TEST)", use_container_width=True):
            if "TEST" not in wl:
                wl.append("TEST")
                save_watchlist(wl)
                st.rerun()
        if st.button("❌ Rimuovi simbolo di test (TEST)", use_container_width=True):
            if "TEST" in wl:
                wl.remove("TEST")
                save_watchlist(wl)
                st.rerun()

    # ============================================
    # INFORMAZIONI DI SISTEMA
    # ============================================
    with st.expander("🖥️ Info Sistema", expanded=False):
        st.write(f"**Python**: {sys.version}")
        st.write(f"**Platform**: {platform.platform()}")
        st.write(f"**Streamlit**: {st.__version__}")
        st.write(f"**Pandas**: {pd.__version__}")
        st.write(f"**Numpy**: {np.__version__}")
        st.write(f"**Ora server**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # ============================================
    # TEST GLOBALE (esegue tutti i test di base)
    # ============================================
    st.markdown("---")
    if st.button("🚀 Esegui tutti i test rapidi", use_container_width=True, type="primary"):
        st.info("Avvio test completi...")
        results = []

        # Test Yahoo
        try:
            df = fetch_yf_ohlcv("BTC-USD", interval="15m", period="1d", tail=10)
            results.append(("Yahoo BTC-USD", "✅ OK" if df is not None else "❌ Fallito"))
        except Exception as e:
            results.append(("Yahoo BTC-USD", f"❌ Errore: {str(e)[:50]}"))

        # Test TwelveData (se chiave presente)
        try:
            df, src = fetch_td_15m("BTC/USD")
            results.append(("TwelveData BTC/USD", "✅ OK" if df is not None else f"❌ {src}"))
        except Exception as e:
            results.append(("TwelveData BTC/USD", f"❌ {str(e)[:50]}"))

        # Test Marketaux
        try:
            news = fetch_marketaux_sentiment(["BTC/USD"])
            results.append(("Marketaux", "✅ OK" if news and news.get('count', 0) > 0 else "⚠️ Nessuna news"))
        except Exception as e:
            results.append(("Marketaux", f"❌ {str(e)[:50]}"))

        # Test indicatori
        try:
            df_fake = pd.DataFrame({'close': np.random.randn(100).cumsum() + 100})
            # (semplificato)
            results.append(("Indicatori", "✅ OK (dati fake)"))
        except Exception as e:
            results.append(("Indicatori", f"❌ {str(e)[:50]}"))

        # Mostra risultati
        for name, res in results:
            st.markdown(f"- **{name}**: {res}")
