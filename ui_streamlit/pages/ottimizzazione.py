import streamlit as st
from strategy.optimizer import render_optimizer_panel

def render():
    st.subheader("⚙️ Ottimizzazione Parametri")
    st.caption("Seleziona un asset dalla watchlist per ottimizzare i parametri di trading.")
    
    watchlist = st.session_state.watchlist
    if not watchlist:
        st.warning("La watchlist è vuota. Aggiungi degli asset nella pagina WATCHLIST.")
        return
    
    # Selettore asset
    default_asset = st.session_state.radar_select if st.session_state.radar_select in watchlist else watchlist[0]
    selected_asset = st.selectbox("Asset da ottimizzare", options=watchlist, index=watchlist.index(default_asset))
    
    # Aggiorna la sessione per coerenza
    if selected_asset != st.session_state.radar_select:
        st.session_state.radar_select = selected_asset
        # Non facciamo rerun per evitare di perdere lo stato, ma possiamo farlo se vogliamo aggiornare subito
        # st.rerun()
    
    render_optimizer_panel(selected_asset)
