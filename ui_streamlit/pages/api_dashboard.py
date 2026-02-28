# ui_streamlit/pages/api_dashboard.py
import streamlit as st
from providers.base_provider import tracker

def render():
    """Pagina Dashboard API"""
    st.title("📊 Monitoraggio API")
    
    stats = tracker.get_provider_stats()
    total_today = tracker.get_today_total()
    
    # Metriche principali
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Chiamate Oggi", total_today)
    with col2:
        st.metric("Provider Attivi", len([s for s in stats if s['today'] > 0]))
    with col3:
        st.metric("Ultimo Reset", "Oggi")
    with col4:
        st.metric("Limiti", "800/500/100")
    
    st.divider()
    
    # Barre di progresso per provider
    for stat in stats:
        with st.container(border=True):
            cols = st.columns([1, 3, 1, 2])
            
            with cols[0]:
                st.markdown(f"{stat['icon']} **{stat['name']}**")
            
            with cols[1]:
                if isinstance(stat['limit'], int):
                    progress = stat['percent'] / 100
                    st.progress(min(progress, 1.0), 
                              text=f"{stat['today']}/{stat['limit']}")
                else:
                    st.progress(0.1, text=f"{stat['today']} chiamate")
            
            with cols[2]:
                if isinstance(stat['limit'], int):
                    color = "#00ff88" if stat['percent'] < 50 else "#f0b90b" if stat['percent'] < 80 else "#ff3344"
                    st.markdown(f"<span style='color:{color};'>{stat['percent']:.0f}%</span>", 
                              unsafe_allow_html=True)
            
            with cols[3]:
                st.caption(stat['description'])
    
    # Log chiamate
    with st.expander("📋 Log Chiamate Recenti"):
        if st.session_state.get('api_calls_log'):
            for call in reversed(st.session_state.api_calls_log[-20:]):
                provider_data = st.session_state.api_usage.get(call['provider'], {})
                icon = provider_data.get('icon', '🔹')
                st.caption(f"{icon} {call['time'].strftime('%H:%M:%S')} - {call['provider']} - {call['symbol']}")
        else:
            st.caption("Nessuna chiamata registrata")
