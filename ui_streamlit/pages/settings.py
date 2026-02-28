# ui_streamlit/pages/settings.py
import streamlit as st
from storage.watchlist_store import save_watchlist
from config import DEFAULT_WATCHLIST, WATCHLIST_FILE

def render():
    """Pagina Impostazioni - SENZA RADAR"""
    
    st.markdown("## ⚙️ Impostazioni")
    
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("### 📋 Watchlist Attuale")
            st.write(", ".join(st.session_state.watchlist))
            st.caption(f"Totale: {len(st.session_state.watchlist)} asset")
            
            if st.button("🔄 Reset a default", use_container_width=True):
                st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
                save_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)
                st.session_state.radar_select = DEFAULT_WATCHLIST[0]
                st.rerun()
    
    with col2:
        with st.container(border=True):
            st.markdown("### 🗑️ Rimuovi Asset")
            if st.session_state.watchlist:
                to_remove = st.selectbox("Seleziona asset", st.session_state.watchlist)
                if st.button("❌ Rimuovi", use_container_width=True) and len(st.session_state.watchlist) > 1:
                    st.session_state.watchlist.remove(to_remove)
                    save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                    if st.session_state.radar_select == to_remove:
                        st.session_state.radar_select = st.session_state.watchlist[0]
                    st.rerun()
        
        with st.container(border=True):
            st.markdown("### ➕ Aggiungi Manuale")
            manual = st.text_input("Simbolo", placeholder="BTC-USD").upper().strip()
            if st.button("➕ Aggiungi", use_container_width=True) and manual:
                if manual not in st.session_state.watchlist:
                    st.session_state.watchlist.append(manual)
                    save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                    st.session_state.radar_select = manual
                    st.rerun()
                    
