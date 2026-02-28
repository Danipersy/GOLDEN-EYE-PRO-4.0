import streamlit as st
from storage.watchlist_store import save_watchlist
from config import DEFAULT_WATCHLIST, WATCHLIST_FILE

def show_page():
    st.subheader("📋 Gestione Watchlist", divider="blue")

    # Mostra watchlist attuale
    st.write("**Watchlist attuale:**")
    for i, asset in enumerate(st.session_state.watchlist):
        cols = st.columns([3, 1, 1])
        with cols[0]:
            st.write(f"{i+1}. {asset}")
        with cols[1]:
            if st.button("📊", key=f"view_{i}"):
                st.session_state.selected_asset = asset
                st.session_state.radar_select = asset
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
        with cols[2]:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.watchlist.pop(i)
                save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                st.rerun()

    # Aggiungi nuovo asset
    st.divider()
    new_asset = st.text_input("Nuovo simbolo (es. BTC-USD)").upper().strip()
    if st.button("➕ Aggiungi") and new_asset:
        if new_asset not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_asset)
            save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
            st.success(f"{new_asset} aggiunto!")
            st.rerun()
        else:
            st.warning("Già presente")

    if st.button("🔄 Reset a default"):
        st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
        save_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)
        st.rerun()
