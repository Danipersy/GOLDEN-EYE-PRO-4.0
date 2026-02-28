import streamlit as st
import numpy as np

def show_page():
    st.title("📋 Watchlist")
    
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = ['BTC-USD', 'ETH-USD', 'BNB-USD', 'SOL-USD', 'ADA-USD']
    
    for asset in st.session_state.watchlist:
        col1, col2, col3, col4 = st.columns([2,2,1,1])
        with col1:
            st.write(asset)
        with col2:
            price = np.random.randn()*1000 + 1000
            st.write(f"${price:.2f}")
        with col3:
            change = np.random.normal(0, 2)
            color = "🟢" if change > 0 else "🔴"
            st.write(f"{color} {change:.1f}%")
        with col4:
            if st.button("📊 Dettaglio", key=f"btn_{asset}"):
                st.session_state.selected_asset = asset
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
