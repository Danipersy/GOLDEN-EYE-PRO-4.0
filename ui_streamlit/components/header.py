# ui_streamlit/components/header.py
import streamlit as st
from datetime import datetime

def render_header():
    """Header con orario e watchlist"""
    
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"## 🦅 GOLDEN EYE PRO")
        st.caption(f"v{st.session_state.get('version', '1.0.0')}")
    
    with col2:
        st.markdown(f"### 🕒 {datetime.now().strftime('%H:%M:%S')}")
    
    with col3:
        st.markdown(f"### 📊 {len(st.session_state.watchlist)} assets")
    
    st.markdown("---")
