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
    
    # Aggiorna la sessione per coerenza
    if selected_asset != st.session_state.radar_select:
        st.session_state.radar_select = selected_asset
        # Opzionale: ricarica i dati di dettaglio per l'asset selezionato? Non lo facciamo per evitare chiamate API automatiche.
        # L'utente dovrà andare su DETTAGLIO per caricare i dati.
    
    if 'detail_data' in st.session_state and st.session_state.detail_data is not None:
        data = st.session_state.detail_data
        # Verifica che i dati si riferiscano all'asset selezionato (se no, avvisa)
        if data.get('symbol') != selected_asset:
            st.info(f"I dati visualizzati si riferiscono a {data.get('symbol', 'un asset')}. Seleziona '{selected_asset}' nella pagina DETTAGLIO per aggiornare.")
            # Usiamo comunque i dati disponibili? Potremmo non farlo per evitare errori.
            # Meglio mostrare un messaggio e non chiamare il pannello.
            st.info("Vai su DETTAGLIO per caricare i dati di questo asset.")
        else:
            signal_score = data.get('score', 65)
            render_money_manager_panel(
                data.get('p', 0),
                data.get('atr', 0),
                signal_score
            )
    else:
        st.info("ℹ️ Nessun dato disponibile. Vai su DETTAGLIO e seleziona un asset per visualizzarne i dettagli.")
