# ui_streamlit/pages/watchlist.py
import streamlit as st

def show_page():
    st.title("📋 Gestione Watchlist")
    
    # Watchlist corrente
    st.subheader("Watchlist Attuale")
    
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD']
    
    for i, asset in enumerate(st.session_state.watchlist):
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.write(f"{i+1}. {asset}")
        with col2:
            if st.button("📊", key=f"view_{i}"):
                st.session_state.selected_asset = asset
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
        with col3:
            if st.button("❌", key=f"del_{i}"):
                st.session_state.watchlist.pop(i)
                st.rerun()
    
    # Aggiungi nuovo asset
    st.markdown("---")
    st.subheader("➕ Aggiungi Asset")
    
    new_asset = st.text_input("Simbolo (es. BTC-USD, AAPL, MSFT)", key="new_asset")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Aggiungi", use_container_width=True) and new_asset:
            if new_asset not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_asset.upper())
                st.rerun()
            else:
                st.warning("Asset già presente")
    
    with col2:
        if st.button("Reset a Default", use_container_width=True):
            st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
            st.rerun()
            
