import streamlit as st
import platform
import sys
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Provider
from providers.multi_provider import scan_symbol, fetch_yf_ohlcv
from providers.twelvedata_provider import (
    fetch_td_15m, fetch_td_1h, fetch_td_4h, 
    search_symbols_td, convert_symbol_for_twelvedata
)
from providers.marketaux_provider import fetch_marketaux_sentiment
from providers.base_provider import tracker
from providers.telegram_provider import send_telegram_alert
from providers.polygon_provider import polygon_provider

# Indicatori
from indicators.robust_ta import compute_indicators_15m, decide_signal

# AI
from ai.asset_analyzer import AssetAIAnalyzer

# Strategia
from strategy.backtest import backtest_engine
from strategy.money_manager import MoneyManager
from strategy.auto_trader import AutoTrader
from ui_streamlit.components.validation_panel import validate_data_quality

# Utility
from utils.helpers import get_market_status, normalize_ohlcv_df, convert_symbol_to_yfinance
from storage.watchlist_store import load_watchlist, save_watchlist
from ui_streamlit.components.card import render_result_card
from ui_streamlit.components.scan_filters import render_scan_filters

def render():
    st.markdown("## 🧪 Diagnostic Center")
    st.caption("Verifica rapida dello stato dell'applicazione")

    # Metriche di sistema in alto
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Python", f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    with col2:
        st.metric("Streamlit", st.__version__)
    with col3:
        st.metric("Pandas", pd.__version__)
    with col4:
        st.metric("Numpy", np.__version__)

    st.divider()

    # Tabs principali
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📡 Provider", 
        "📊 Indicatori & Filtri", 
        "🤖 AI & Strategia", 
        "⚙️ Sistema",
        "💰 Money Manager",
        "🔧 Altri test"
    ])

    # ==================== TAB 1: PROVIDER ====================
    with tab1:
        col_a, col_b = st.columns(2)

        with col_a:
            st.subheader("Yahoo Finance")
            if st.button("🟢 Test BTC-USD", use_container_width=True):
                with st.spinner("Caricamento..."):
                    df = fetch_yf_ohlcv("BTC-USD", interval="15m", period="1d")
                    if df is not None and not df.empty:
                        st.success(f"✅ {len(df)} candles, ultimo prezzo ${df['close'].iloc[-1]:,.2f}")
                    else:
                        st.error("❌ Fallito")

            if st.button("🟢 Test AAPL", use_container_width=True):
                with st.spinner("Caricamento..."):
                    df = fetch_yf_ohlcv("AAPL", interval="15m", period="1d")
                    if df is not None and not df.empty:
                        st.success(f"✅ {len(df)} candles, ultimo prezzo ${df['close'].iloc[-1]:,.2f}")
                    else:
                        st.error("❌ Fallito")

        with col_b:
            st.subheader("TwelveData")
            if st.button("🔵 Test BTC/USD (15m)", use_container_width=True):
                df, src = fetch_td_15m("BTC/USD")
                if df is not None:
                    st.success(f"✅ {len(df)} candles da {src}, prezzo ${df['close'].iloc[-1]:,.2f}")
                else:
                    st.error(f"❌ Fallito: {src}")

            if st.button("🔵 Test BTC/USD (1h)", use_container_width=True):
                df, src = fetch_td_1h("BTC/USD")
                if df is not None:
                    st.success(f"✅ {len(df)} candles da {src}, prezzo ${df['close'].iloc[-1]:,.2f}")
                else:
                    st.error(f"❌ Fallito: {src}")

            if st.button("🔵 Test BTC/USD (4h)", use_container_width=True):
                df, src = fetch_td_4h("BTC/USD")
                if df is not None:
                    st.success(f"✅ {len(df)} candles da {src}, prezzo ${df['close'].iloc[-1]:,.2f}")
                else:
                    st.error(f"❌ Fallito: {src}")

        st.divider()

        col_c, col_d = st.columns(2)
        with col_c:
            st.subheader("Marketaux News")
            if st.button("🟡 Test sentiment BTC", use_container_width=True):
                news = fetch_marketaux_sentiment(["BTC/USD"])
                if news and news.get('count', 0) > 0:
                    st.success(f"✅ {news['count']} news - {news['label']}")
                else:
                    st.warning("⚠️ Nessuna news o chiave non valida")

        with col_d:
            st.subheader("Ricerca simboli TwelveData")
            search_q = st.text_input("Cerca (min 3 caratteri)", value="bitcoin", key="search_td_simple")
            if len(search_q) >= 3:
                with st.spinner("Ricerca..."):
                    results = search_symbols_td(search_q, 5)
                if results:
                    st.success(f"Trovati {len(results)} risultati")
                    for r in results:
                        st.caption(f"• {r['label']}")
                else:
                    st.warning("Nessun risultato")

        st.divider()
        st.subheader("Conversione simboli")
        test_sym = st.text_input("Simbolo da convertire", value="BTC-USD", key="conv_sym_advanced")
        if st.button("🔄 Converti", use_container_width=True):
            converted = convert_symbol_for_twelvedata(test_sym)
            st.info(f"📌 {test_sym} → {converted}")

        st.divider()
                st.subheader("Polygon.io")
        polygon_key = st.secrets.get("POLYGON_KEY", "") or st.session_state.get('polygon_key', '')
        if not polygon_key:
            st.warning("⚠️ Chiave Polygon non trovata. Aggiungila in Configurazione o nei secrets.")

        from utils.helpers import convert_symbol_for_polygon

        col_p1, col_p2 = st.columns(2)
        with col_p1:
            if st.button("🟠 Test Polygon (BTC-USD)", use_container_width=True):
                with st.spinner("Caricamento..."):
                    if not polygon_key:
                        st.error("❌ Chiave mancante")
                    else:
                        poly_symbol = convert_symbol_for_polygon("BTC-USD")
                        df, src = polygon_provider.fetch_aggregates(poly_symbol, timespan='minute', multiplier=15, limit=100)
                        if df is not None:
                            st.success(f"✅ {len(df)} candles da {src}, prezzo ${df['close'].iloc[-1]:,.2f}")
                        else:
                            st.error(f"❌ Fallito: {src} (simbolo convertito: {poly_symbol})")

            if st.button("🟠 Test Polygon (AAPL)", use_container_width=True):
                with st.spinner("Caricamento..."):
                    if not polygon_key:
                        st.error("❌ Chiave mancante")
                    else:
                        poly_symbol = convert_symbol_for_polygon("AAPL")
                        df, src = polygon_provider.fetch_aggregates(poly_symbol, timespan='minute', multiplier=15, limit=100)
                        if df is not None:
                            st.success(f"✅ {len(df)} candles da {src}, prezzo ${df['close'].iloc[-1]:,.2f}")
                        else:
                            st.error(f"❌ Fallito: {src} (simbolo convertito: {poly_symbol})")

        with col_p2:
            if st.button("🟠 Test ricerca Polygon (bitcoin)", use_container_width=True):
                with st.spinner("Ricerca..."):
                    if not polygon_key:
                        st.error("❌ Chiave mancante")
                    else:
                        results = polygon_provider.search_symbols("bitcoin", limit=5)
                        if results:
                            st.success(f"Trovati {len(results)} risultati")
                            for r in results:
                                st.write(f"- {r['symbol']}: {r['name']}")
                        else:
                            st.warning("Nessun risultato o chiave non valida")

    # ==================== TAB 2: INDICATORI & FILTRI ====================
    with tab2:
        st.subheader("Calcolo indicatori su dati reali (esempio BTC)")
        if st.button("📥 Scarica dati BTC e calcola", use_container_width=True):
            with st.spinner("Caricamento dati..."):
                df, src = fetch_td_15m("BTC/USD")
                if df is not None:
                    df_ind = compute_indicators_15m(df)
                    cols = st.columns(4)
                    with cols[0]:
                        st.metric("RSI", f"{df_ind['rsi'].iloc[-1]:.1f}")
                    with cols[1]:
                        adx_col = [c for c in df_ind.columns if 'ADX' in c.upper()]
                        adx_val = df_ind[adx_col[0]].iloc[-1] if adx_col else 0
                        st.metric("ADX", f"{adx_val:.1f}")
                    with cols[2]:
                        st.metric("ATR", f"${df_ind['atr'].iloc[-1]:.2f}")
                    with cols[3]:
                        st.metric("EMA200", f"${df_ind['ema200'].iloc[-1]:.2f}")
                else:
                    st.error("Impossibile caricare dati")

        st.divider()
        st.subheader("Test filtri scan (livelli L1-L5)")
        test_changes = [-3.5, -1.5, -0.8, -0.2, 0.1, 0.6, 1.2, 2.5]
        results = []
        for change in test_changes:
            if abs(change) > 2:
                level = 5
            elif abs(change) > 1:
                level = 4
            elif abs(change) > 0.5:
                level = 3
            elif abs(change) > 0.1:
                level = 2
            else:
                level = 1
            results.append({"Variazione %": change, "Livello": f"L{level}"})
        df_levels = pd.DataFrame(results)
        st.dataframe(df_levels, use_container_width=True)

        st.divider()
        st.subheader("Test filtri UI")
        if st.checkbox("Mostra filtri avanzati"):
            filters = render_scan_filters()
            st.json(filters)

    # ==================== TAB 3: AI & STRATEGIA ====================
    with tab3:
        st.subheader("AI Suggeritore")
        if st.button("🔮 Test AI con dati finti", use_container_width=True):
            analyzer = AssetAIAnalyzer()
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
            analysis = analyzer.analyze_asset("BTC-USD", fake_data, news_fake)
            st.metric("Score AI", f"{analysis['score']}/100")
            st.success(f"Azione: {analysis['action']}")
            with st.expander("Dettaglio segnali"):
                for s in analysis['signals']:
                    st.write(f"- {s}")

        st.divider()
        st.subheader("Backtest con dati reali (BTC)")
        if st.button("📊 Esegui backtest su BTC (ultimi 30 giorni)", use_container_width=True):
            with st.spinner("Scaricamento dati e backtest..."):
                df_bt = fetch_yf_ohlcv("BTC-USD", interval="15m", period="30d")
                if df_bt is not None and len(df_bt) > 200:
                    result = backtest_engine(df_bt, use_mtf=False)
                    if result and result['trades'] is not None and not result['trades'].empty:
                        stats = result['stats']
                        st.success(f"Trades: {stats['n']}, Win Rate: {stats['winrate']:.1f}%")
                        st.dataframe(result['trades'].tail(10), use_container_width=True)
                    else:
                        st.warning("Nessun trade generato nel periodo")
                else:
                    st.error("Dati insufficienti")

        st.divider()
        st.subheader("AutoTrader (simulazione)")
        if st.button("▶️ Avvia simulazione AutoTrader (5 trade)", use_container_width=True):
            if 'test_auto_trader' not in st.session_state:
                st.session_state.test_auto_trader = AutoTrader()
            trades = []
            capital = 10000
            for i in range(5):
                pnl_pct = np.random.normal(0.5, 2)
                pnl = capital * pnl_pct / 100
                capital += pnl
                trades.append({
                    "Trade": i+1,
                    "PnL %": f"{pnl_pct:.2f}%",
                    "Capitale": f"${capital:.2f}"
                })
            st.table(pd.DataFrame(trades))

    # ==================== TAB 4: SISTEMA ====================
    with tab4:
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.subheader("Session State")
            if st.button("🔄 Mostra stato", use_container_width=True):
                state = {k: str(v) for k, v in st.session_state.items() if not k.startswith('_')}
                st.json(state)

            if st.button("🧹 Svuota cache", use_container_width=True):
                st.cache_data.clear()
                st.success("Cache svuotata!")

        with col_s2:
            st.subheader("API Usage")
            stats = tracker.get_provider_stats()
            for stat in stats:
                st.metric(stat['name'], f"{stat['today']}/{stat['limit'] if stat['limit'] else '∞'}",
                          help=stat['description'])

        st.divider()
        st.subheader("Test Watchlist")
        wl = st.session_state.watchlist
        st.write(f"**Attuale ({len(wl)} asset):** {', '.join(wl)}")
        col_w1, col_w2 = st.columns(2)
        with col_w1:
            if st.button("➕ Aggiungi TEST", use_container_width=True):
                if "TEST" not in wl:
                    wl.append("TEST")
                    save_watchlist(wl)
                    st.success("✅ TEST aggiunto")
                    st.rerun()
        with col_w2:
            if st.button("❌ Rimuovi TEST", use_container_width=True):
                if "TEST" in wl:
                    wl.remove("TEST")
                    save_watchlist(wl)
                    st.success("✅ TEST rimosso")
                    st.rerun()

        st.divider()
        st.subheader("Validazione dati")
        if st.button("📊 Test validazione su BTC", use_container_width=True):
            with st.spinner("Caricamento..."):
                df15, _ = fetch_td_15m("BTC/USD")
                df1h, _ = fetch_td_1h("BTC/USD")
                df4h, _ = fetch_td_4h("BTC/USD")
                if df15 is not None:
                    val = validate_data_quality(df15, df1h, df4h)
                    st.metric("Qualità", f"{val['quality_score']:.1f}%")
                    with st.expander("Dettaglio"):
                        for item in val['ok']:
                            st.success(item)
                        for item in val['warnings']:
                            st.warning(item)
                        for item in val['issues']:
                            st.error(item)
                else:
                    st.error("Dati non disponibili")

    # ==================== TAB 5: MONEY MANAGER ====================
    with tab5:
        st.subheader("Money Manager interattivo")
        st.caption("I pulsanti aggiornano il capitale in tempo reale (salvato in sessione).")

        if 'test_money_manager' not in st.session_state:
            st.session_state.test_money_manager = MoneyManager(initial_capital=10000)

        mm = st.session_state.test_money_manager

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            if st.button("➕ +500", use_container_width=True):
                mm.update_after_trade(500)
                st.rerun()
        with col_m2:
            if st.button("➖ -300", use_container_width=True):
                mm.update_after_trade(-300)
                st.rerun()
        with col_m3:
            if st.button("🔄 Reset", use_container_width=True):
                st.session_state.test_money_manager = MoneyManager(10000)
                st.rerun()
        with col_m4:
            if st.button("📊 Mostra metriche", use_container_width=True):
                metrics = mm.get_metrics()
                st.json(metrics)

        metrics = mm.get_metrics()
        col_show1, col_show2, col_show3 = st.columns(3)
        with col_show1:
            st.metric("Capitale", f"${metrics['current_capital']:.2f}", delta=f"{metrics['total_pnl_pct']:.2f}%")
        with col_show2:
            st.metric("Drawdown attuale", f"{metrics['current_drawdown']:.2f}%")
        with col_show3:
            st.metric("Max Drawdown", f"{metrics['max_drawdown']:.2f}%")

        if metrics['trades'] > 0:
            st.metric("Sharpe Ratio", f"{metrics['sharpe']:.2f}")

    # ==================== TAB 6: ALTRI TEST ====================
    with tab6:
        st.subheader("Test componenti UI")
        if st.button("🃏 Mostra card esempio", use_container_width=True):
            fake_result = {
                'symbol': 'BTC-USD',
                'price': 51234.56,
                'change': 2.34,
                'volume': 12345678,
                'level': 5,
                'score': 85
            }
            render_result_card(fake_result)

        st.divider()
        st.subheader("Test notifiche Telegram")
        if st.button("📨 Invia test Telegram", use_container_width=True):
            success = send_telegram_alert("🧪 Test dal Diagnostic Center")
            if success:
                st.success("Messaggio inviato!")
            else:
                st.error("Invio fallito (controlla i secrets)")

        st.divider()
        st.subheader("Test performance")
        if st.button("⏱️ Cronometra fetch BTC", use_container_width=True):
            start = time.time()
            df, src = fetch_td_15m("BTC/USD")
            elapsed = time.time() - start
            if df is not None:
                st.success(f"TwelveData: {elapsed:.2f}s")
            else:
                st.error(f"Fallito in {elapsed:.2f}s")
            start = time.time()
            df2 = fetch_yf_ohlcv("BTC-USD", interval="15m", period="1d")
            elapsed = time.time() - start
            if df2 is not None:
                st.success(f"Yahoo: {elapsed:.2f}s")
            else:
                st.error(f"Fallito in {elapsed:.2f}s")

        st.divider()
        st.subheader("Test helpers")
        if st.button("🛠️ Test get_market_status"):
            status = get_market_status("BTC-USD")
            st.json(status)
        if st.button("🛠️ Test convert_symbol_to_yfinance (BTC/USD)"):
            conv = convert_symbol_to_yfinance("BTC/USD")
            st.info(f"BTC/USD → {conv}")
