import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from config import (
    DEFAULT_WATCHLIST, RSI_LEN, ATR_LEN, ADX_LEN, ADX_MIN,
    RSI_LONG_MAX, RSI_SHORT_MIN, SL_ATR, TP_ATR,
    WEAK_SIGNALS_ENABLED, ENABLE_SIGNAL_CLASSIFICATION
)
from storage.watchlist_store import save_watchlist
from providers.base_provider import tracker

def render():
    st.subheader("⚙️ Configurazione Applicazione")
    st.caption("Modifica parametri, chiavi API e preferenze")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Indicatori", "💰 Risk Management", "🔑 API Keys", "🖥️ Avanzate"])

    with tab1:
        st.markdown("### Parametri indicatori")
        col1, col2 = st.columns(2)
        with col1:
            rsi_len = st.number_input("RSI Length", min_value=2, max_value=50, value=st.session_state.get('rsi_len', RSI_LEN))
            atr_len = st.number_input("ATR Length", min_value=2, max_value=50, value=st.session_state.get('atr_len', ATR_LEN))
            adx_len = st.number_input("ADX Length", min_value=2, max_value=50, value=st.session_state.get('adx_len', ADX_LEN))
        with col2:
            adx_min = st.number_input("ADX Min", min_value=10.0, max_value=50.0, value=float(st.session_state.get('adx_min', ADX_MIN)), step=1.0)
            rsi_long_max = st.number_input("RSI Long Max", min_value=30.0, max_value=80.0, value=float(st.session_state.get('rsi_long_max', RSI_LONG_MAX)), step=1.0)
            rsi_short_min = st.number_input("RSI Short Min", min_value=20.0, max_value=70.0, value=float(st.session_state.get('rsi_short_min', RSI_SHORT_MIN)), step=1.0)

        if st.button("Salva parametri indicatori", use_container_width=True):
            st.session_state.rsi_len = rsi_len
            st.session_state.atr_len = atr_len
            st.session_state.adx_len = adx_len
            st.session_state.adx_min = adx_min
            st.session_state.rsi_long_max = rsi_long_max
            st.session_state.rsi_short_min = rsi_short_min
            st.success("Parametri salvati per questa sessione (non permanenti)")

    with tab2:
        st.markdown("### Stop Loss / Take Profit")
        col1, col2 = st.columns(2)
        with col1:
            sl_atr = st.number_input("SL (ATR multiplo)", min_value=0.5, max_value=5.0, value=float(st.session_state.get('sl_atr', SL_ATR)), step=0.1)
        with col2:
            tp_atr = st.number_input("TP (ATR multiplo)", min_value=0.5, max_value=10.0, value=float(st.session_state.get('tp_atr', TP_ATR)), step=0.1)

        st.markdown("### Gestione segnali deboli")
        weak_enabled = st.checkbox("Abilita segnali deboli (WEAK)", value=st.session_state.get('weak_signals_enabled', WEAK_SIGNALS_ENABLED))
        classification_enabled = st.checkbox("Abilita classificazione segnali", value=st.session_state.get('classification_enabled', ENABLE_SIGNAL_CLASSIFICATION))

        if st.button("Salva Risk Management", use_container_width=True):
            st.session_state.sl_atr = sl_atr
            st.session_state.tp_atr = tp_atr
            st.session_state.weak_signals_enabled = weak_enabled
            st.session_state.classification_enabled = classification_enabled
            st.success("Parametri salvati per questa sessione")

    with tab3:
        st.markdown("### Chiavi API (solo per questa sessione)")
        st.info("Le chiavi sono normalmente caricate dai secrets di Streamlit. Qui puoi sovrascriverle temporaneamente.")

        default_td = st.secrets.get("TWELVEDATA_KEY", "")
        default_av = st.secrets.get("ALPHA_VANTAGE_KEY", "")
        default_mk = st.secrets.get("MARKETAUX_TOKEN", "")
        default_finnhub = st.secrets.get("FINNHUB_KEY", "")

        td_key = st.text_input("TwelveData API Key", value=st.session_state.get('twelvedata_key', default_td), type="password")
        av_key = st.text_input("Alpha Vantage API Key", value=st.session_state.get('alphavantage_key', default_av), type="password")
        mk_key = st.text_input("Marketaux Token", value=st.session_state.get('marketaux_token', default_mk), type="password")
        finnhub_key = st.text_input("Finnhub API Key", value=st.session_state.get('finnhub_key', default_finnhub), type="password", 
                                   help="Registrati su finnhub.io per una chiave gratuita (60 chiamate/minuto)")

        if st.button("Salva chiavi (sessione corrente)", use_container_width=True):
            st.session_state.twelvedata_key = td_key
            st.session_state.alphavantage_key = av_key
            st.session_state.marketaux_token = mk_key
            st.session_state.finnhub_key = finnhub_key
            st.success("Chiavi temporanee impostate (valide fino al refresh)")

        st.divider()
        st.markdown("### Stato consumi API oggi")
        stats = tracker.get_provider_stats()
        for stat in stats:
            st.metric(stat['name'], f"{stat['today']}/{stat['limit'] if stat['limit'] else '∞'}",
                     help=stat['description'])

    with tab4:
        st.markdown("### Watchlist predefinita")
        default_wl = st.text_area("Elenco simboli separati da virgola", value=", ".join(DEFAULT_WATCHLIST))
        new_default = [s.strip() for s in default_wl.split(",") if s.strip()]
        if st.button("Salva come default (sessione)", use_container_width=True):
            st.session_state.default_watchlist = new_default
            st.success("Watchlist predefinita aggiornata per questa sessione")

        st.markdown("### Reset")
        if st.button("🔄 Ripristina tutti i valori di default", use_container_width=True):
            for key in list(st.session_state.keys()):
                if key not in ['watchlist', 'selected_asset', 'radar_select', 'current_page', 'last_scan_time', 'scan_results']:
                    del st.session_state[key]
            st.rerun()

        st.markdown("### Info di sistema")
        st.json({
            "streamlit_version": st.__version__,
            "pandas_version": pd.__version__,
            "numpy_version": np.__version__,
            "session_keys": list(st.session_state.keys())
        })
