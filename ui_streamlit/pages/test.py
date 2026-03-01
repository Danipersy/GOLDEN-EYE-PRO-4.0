import streamlit as st
import platform
import sys
import pandas as pd
import numpy as np
from datetime import datetime

# Provider
from providers.multi_provider import scan_symbol, fetch_yf_ohlcv
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h, search_symbols_td
from providers.marketaux_provider import fetch_marketaux_sentiment
from providers.base_provider import tracker

# Indicatori
from indicators.robust_ta import compute_indicators_15m, decide_signal

# AI
from ai.asset_analyzer import AssetAIAnalyzer

# Strategia
from strategy.backtest import backtest_engine
from strategy.money_manager import MoneyManager

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
    tab1, tab2, tab3, tab4 = st.tabs(["📡 Provider", "📊 Indicatori", "🤖 AI & Strategia", "⚙️ Sistema"])

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
            if st.button("🔵 Test BTC/USD", use_container_width=True):
                df, src = fetch_td_15m("BTC/USD")
                if df is not None:
                    st.success(f"✅ {len(df)} candles da {src}, prezzo ${df['close'].iloc[-1]:,.2f}")
                else:
                    st.error(f"❌ {src}")

            if st.button("🔵 Test ETH/USD", use_container_width=True):
                df, src = fetch_td_15m("ETH/USD")
                if df is not None:
                    st.success(f"✅ {len(df)} candles da {src}, prezzo ${df['close'].iloc[-1]:,.2f}")
                else:
                    st.error(f"❌ {src}")

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
            st.subheader("Ricerca simboli")
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

    # ==================== TAB 2: INDICATORI ====================
    with tab2:
        st.subheader("Calcolo indicatori su dati sintetici")
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

        if st.button("🧮 Calcola RSI, ADX, ATR", use_container_width=True):
            df_ind = compute_indicators_15m(df_fake)
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

        st.divider()
        st.subheader("Classificazione segnale")
        if st.button("🎯 Genera segnale casuale", use_container_width=True):
            df_ind = compute_indicators_15m(df_fake)
            mtf_long = np.random.choice([True, False])
            mtf_short = np.random.choice([True, False])
            signal = decide_signal(df_ind, mtf_long, mtf_short)
            st.info(f"**{signal['display']}** (forza: {signal['strength']})")
            col1, col2, col3 = st.columns(3)
            col1.metric("RSI", f"{signal['rsi']:.1f}")
            col2.metric("ADX", f"{signal['adx']:.1f}")
            col3.metric("ATR", f"${signal['atr']:.2f}")

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
        st.subheader("Backtest rapido")
        if st.button("📊 Esegui backtest sintetico", use_container_width=True):
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
                st.success(f"Trades: {stats['n']}, Win Rate: {stats['winrate']:.1f}%")
            else:
                st.warning("Nessun trade generato (normale con dati casuali)")

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
        st.subheader("Watchlist")
        wl = st.session_state.watchlist
        st.write(f"**{len(wl)} asset**: {', '.join(wl)}")
