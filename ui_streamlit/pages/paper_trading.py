import streamlit as st
from ui_streamlit.components.paper_trading import render_paper_trading_panel

def render():
    st.subheader("📝 Paper Trading")
    st.caption("Simula trading con capitale virtuale.")

    watchlist = st.session_state.watchlist
    if not watchlist:
        st.warning("La watchlist è vuota. Aggiungi degli asset nella pagina WATCHLIST.")
        return

    # Selettore asset
    default_asset = st.session_state.radar_select if st.session_state.radar_select in watchlist else watchlist[0]
    selected_asset = st.selectbox("Asset", options=watchlist, index=watchlist.index(default_asset))

    # Aggiorna la sessione per coerenza
    if selected_asset != st.session_state.radar_select:
        st.session_state.radar_select = selected_asset

    # Verifica disponibilità dati di dettaglio
    if 'detail_data' in st.session_state and st.session_state.detail_data is not None:
        data = st.session_state.detail_data
        if data.get('symbol') != selected_asset:
            st.info(f"I dati visualizzati si riferiscono a {data.get('symbol', 'un asset')}. Seleziona '{selected_asset}' nella pagina DETTAGLIO per aggiornare.")
            # Offri la possibilità di inserire manualmente i dati
            use_manual = st.checkbox("Inserisci manualmente i dati per questo asset")
            if use_manual:
                with st.form("manual_input"):
                    price = st.number_input("Prezzo", min_value=0.0, value=100.0, step=0.01, format="%.2f")
                    atr = st.number_input("ATR", min_value=0.0, value=1.0, step=0.01, format="%.2f")
                    signal_label = st.selectbox("Tipo segnale", ["FORTE", "MEDIO", "DEBOLE", "NEUTRALE"])
                    signal_score = {"FORTE": 85, "MEDIO": 75, "DEBOLE": 60, "NEUTRALE": 50}[signal_label]
                    submitted = st.form_submit_button("Avvia paper trading")
                    if submitted:
                        render_paper_trading_panel(selected_asset, price, atr, signal_score, signal_label)
            else:
                st.info("Vai su DETTAGLIO per caricare i dati di questo asset.")
                if st.button("📊 Vai a Dettaglio"):
                    st.session_state.selected_asset = selected_asset
                    st.session_state.current_page = "DETTAGLIO"
                    st.rerun()
        else:
            # Dati presenti e corretti
            signal_label = data.get('sig', 'SEGNALE')
            signal_score = data.get('score', 50)
            render_paper_trading_panel(selected_asset, data.get('p', 0), data.get('atr', 0), signal_score, signal_label)
    else:
        # Nessun dato di dettaglio
        st.info("Nessun dato disponibile. Puoi inserirli manualmente o andare su DETTAGLIO.")
        use_manual = st.checkbox("Inserisci manualmente i dati")
        if use_manual:
            with st.form("manual_input"):
                price = st.number_input("Prezzo", min_value=0.0, value=100.0, step=0.01, format="%.2f")
                atr = st.number_input("ATR", min_value=0.0, value=1.0, step=0.01, format="%.2f")
                signal_label = st.selectbox("Tipo segnale", ["FORTE", "MEDIO", "DEBOLE", "NEUTRALE"])
                signal_score = {"FORTE": 85, "MEDIO": 75, "DEBOLE": 60, "NEUTRALE": 50}[signal_label]
                submitted = st.form_submit_button("Avvia paper trading")
                if submitted:
                    render_paper_trading_panel(selected_asset, price, atr, signal_score, signal_label)
        else:
            if st.button("📊 Vai a Dettaglio"):
                st.session_state.selected_asset = selected_asset
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
