import streamlit as st
from strategy.money_manager import render_money_manager_panel

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

    if selected_asset != st.session_state.radar_select:
        st.session_state.radar_select = selected_asset

    if 'detail_data' in st.session_state and st.session_state.detail_data is not None:
        data = st.session_state.detail_data
        if data.get('symbol') != selected_asset:
            st.info(f"I dati visualizzati si riferiscono a {data.get('symbol', 'un asset')}. Seleziona '{selected_asset}' nella pagina DETTAGLIO per aggiornare.")
            use_manual = st.checkbox("Inserisci manualmente i dati")
            if use_manual:
                with st.form("manual_input"):
                    price = st.number_input("Prezzo", min_value=0.0, value=100.0, step=0.01, format="%.2f")
                    atr = st.number_input("ATR", min_value=0.0, value=1.0, step=0.01, format="%.2f")
                    signal_score = st.number_input("Score AI", min_value=0, max_value=100, value=65)
                    submitted = st.form_submit_button("Calcola")
                    if submitted:
                        render_money_manager_panel(price, atr, signal_score)
            else:
                if st.button("📊 Vai a Dettaglio"):
                    st.session_state.selected_asset = selected_asset
                    st.session_state.current_page = "DETTAGLIO"
                    st.rerun()
        else:
            # Dati presenti e corretti
            signal_score = data.get('score', 65)
            render_money_manager_panel(data.get('p', 0), data.get('atr', 0), signal_score)
    else:
        st.info("Nessun dato disponibile. Puoi inserirli manualmente o andare su DETTAGLIO.")
        use_manual = st.checkbox("Inserisci manualmente i dati")
        if use_manual:
            with st.form("manual_input"):
                price = st.number_input("Prezzo", min_value=0.0, value=100.0, step=0.01, format="%.2f")
                atr = st.number_input("ATR", min_value=0.0, value=1.0, step=0.01, format="%.2f")
                signal_score = st.number_input("Score AI", min_value=0, max_value=100, value=65)
                submitted = st.form_submit_button("Calcola")
                if submitted:
                    render_money_manager_panel(price, atr, signal_score)
        else:
            if st.button("📊 Vai a Dettaglio"):
                st.session_state.selected_asset = selected_asset
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
