import streamlit as st

def show_page():
    st.title("🔍 SCAN")
    st.markdown("Pannello di scansione mercati")
    
    # Mock data per test
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("BTC-USD", "$52,345", "+2.3%")
    with col2:
        st.metric("ETH-USD", "$3,124", "+1.2%")
    with col3:
        st.metric("BNB-USD", "$412", "-0.5%")
