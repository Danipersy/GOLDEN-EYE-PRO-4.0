import streamlit as st
from strategy.money_manager import render_money_manager_panel
from providers.twelvedata_provider import fetch_td_15m
from providers.multi_provider import fetch_yf_ohlcv
from indicators.robust_ta import compute_indicators_15m, decide_signal

def render():
    st.subheader("💰 Money Management")
    st.caption("Calcola dimensionamento posizioni e gestione del capitale per un asset.")

    watchlist = st.session_state.watchlist
    if not watchlist:
        st.warning("La watchlist è vuota. Aggiungi degli asset nella pagina WATCHLIST.")
        return

    # Selettore asset
    default_asset = st.session_state.radar_select if st.session_state.radar_select in watchlist else watchlist[0]
    selected_asset = st.selectbox("Asset", options=watchlist, index=watchlist.index(default_asset))

    # Opzione fonte dati
    use_td = st.checkbox("Usa TwelveData (più preciso)", value=True)

    price = None
    atr = None
    signal_score = 50
    error = None

    def load_data(asset):
        nonlocal price, atr, signal_score, error
        with st.spinner(f"Caricamento dati per {asset}..."):
            if use_td:
                df, src = fetch_td_15m(asset)
            else:
                df = fetch_yf_ohlcv(asset, interval="15m", period="5d")
            if df is not None and not df.empty:
                df_ind = compute_indicators_15m(df)
                # Per il money management ci serve principalmente ATR, usiamo un MTF fittizio
                signal = decide_signal(df_ind, mtf_long=False, mtf_short=False)
                price = float(df['close'].iloc[-1])
                atr = signal['atr']
                # Calcoliamo uno score semplice basato su RSI e ADX (opzionale)
                rsi = signal['rsi']
                adx = signal['adx']
                # Score fittizio: più RSI vicino a 50 e ADX alto -> più alto
                score = 50 + (abs(rsi - 50) * 0.5) + (adx * 0.5)
                signal_score = min(100, max(0, score))
            else:
                error = f"Impossibile caricare dati per {asset}"

    # Controlla se abbiamo già dati validi in session_state
    if 'detail_data' in st.session_state and st.session_state.detail_data is not None:
        data = st.session_state.detail_data
        if data.get('symbol') == selected_asset:
            price = data.get('p')
            atr = data.get('atr')
            signal_score = data.get('score', 50)
        else:
            load_data(selected_asset)
    else:
        load_data(selected_asset)

    if error:
        st.error(error)
        return

    if price is not None and atr is not None and atr > 0:
        render_money_manager_panel(price, atr, signal_score)
    else:
        st.warning("Dati insufficienti per calcolare il money management.")
