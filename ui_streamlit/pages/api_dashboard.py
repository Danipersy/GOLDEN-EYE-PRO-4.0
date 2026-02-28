import streamlit as st
import plotly.graph_objects as go
from providers.base_provider import tracker
from datetime import datetime

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
        st.metric("Ultimo Reset", datetime.now().strftime("%d/%m/%Y"))
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
                else:
                    st.markdown("∞")
            
            with cols[3]:
                st.caption(stat['description'])
    
    # Grafico a torta se ci sono chiamate
    if total_today > 0:
        st.subheader("📈 Distribuzione Chiamate")
        
        fig = go.Figure(data=[go.Pie(
            labels=[s['name'] for s in stats if s['today'] > 0],
            values=[s['today'] for s in stats if s['today'] > 0],
            hole=.3,
            marker_colors=[s['color'] for s in stats if s['today'] > 0]
        )])
        
        fig.update_layout(
            template='plotly_dark',
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Log chiamate
    with st.expander("📋 Log Chiamate Recenti"):
        if st.session_state.get('api_calls_log'):
            for call in reversed(st.session_state.api_calls_log[-20:]):
                provider_data = st.session_state.api_usage.get(call['provider'], {})
                icon = provider_data.get('icon', '🔹')
                
                # Converti timestamp se è stringa
                time_str = call['time']
                if isinstance(time_str, str):
                    try:
                        time_obj = datetime.fromisoformat(time_str)
                        time_str = time_obj.strftime('%H:%M:%S')
                    except:
                        pass
                
                st.caption(f"{icon} {time_str} - {call['provider']} - {call.get('symbol', 'N/A')}")
        else:
            st.caption("Nessuna chiamata registrata")
    
    # Bottone reset log
    if st.button("🗑️ Resetta Log", use_container_width=True):
        st.session_state.api_calls_log = []
        st.rerun()
