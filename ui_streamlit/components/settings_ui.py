# ui_streamlit/components/settings_ui.py
import streamlit as st
from config import DEFAULT_WATCHLIST, WATCHLIST_FILE, MAX_WATCHLIST_SIZE
from storage.watchlist_store import load_watchlist, save_watchlist

def render_settings_page():
    """Pagina impostazioni"""
    st.markdown("## ⚙️ Impostazioni")
    
    with st.container(border=True):
        st.markdown("### 📋 Watchlist")
        
        if "watchlist" not in st.session_state:
            st.session_state.watchlist = load_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)
        
        wl = [x.upper() for x in st.session_state.watchlist if x.strip()]
        wl = list(dict.fromkeys(wl))[:MAX_WATCHLIST_SIZE]
        st.session_state.watchlist = wl
        
        st.markdown("**Watchlist attuale:**")
        st.write(", ".join(wl) if wl else "Vuota")
        
        if st.button("🔄 Reset a default", use_container_width=True):
            st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
            save_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)
            st.rerun()
    
    with st.container(border=True):
        st.markdown("### ℹ️ Info")
        st.markdown(f"""
        - **Max asset:** {MAX_WATCHLIST_SIZE}
        - **Fonte dati:** TwelveData + Yahoo Finance
        - **Cache:** 60-600 secondi
        """)
