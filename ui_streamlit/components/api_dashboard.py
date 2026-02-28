# ui_streamlit/components/api_dashboard.py
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, date
from providers.base_provider import tracker

def render_api_dashboard():
    """Dashboard completa per monitoraggio e gestione API"""
    
    st.markdown("## 📊 Dashboard API")
    st.caption("Monitoraggio utilizzo e gestione chiavi")
    
    # Tabs per separare monitoraggio e configurazione
    tab_monitor, tab_config = st.tabs(["📈 Monitoraggio", "🔧 Configurazione API"])
    
    with tab_monitor:
        render_monitoring_tab()
    
    with tab_config:
        render_config_tab()

def render_monitoring_tab():
    """Tab di monitoraggio utilizzo API"""
    
    # Statistiche generali
    stats = tracker.get_provider_stats()
    total_today = tracker.get_today_total()
    
    # Metriche principali
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Chiamate Oggi", total_today)
    with col2:
        st.metric("Provider Attivi", len([s for s in stats if s['today'] > 0]))
    with col3:
        st.metric("Totale Complessivo", sum(s['total'] for s in stats))
    with col4:
        st.metric("Ultimo Reset", date.today().strftime("%d/%m/%Y"))
    
    st.divider()
    
    # Barre di progresso per ogni provider
    st.markdown("### 📊 Utilizzo per Provider")
    
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
                    st.markdown(f"<span style='color:{color}; font-weight:bold;'>{stat['percent']:.0f}%</span>", 
                              unsafe_allow_html=True)
                else:
                    st.markdown("∞")
            
            with cols[3]:
                st.caption(stat['description'])
    
    # Log chiamate recenti
    with st.expander("📋 Log Chiamate Recenti", expanded=False):
        if st.session_state.get('api_calls_log'):
            # Filtri per provider
            providers = list(set(call['provider'] for call in st.session_state.api_calls_log))
            selected_provider = st.selectbox("Filtra per provider", ["Tutti"] + providers)
            
            for call in reversed(st.session_state.api_calls_log[-50:]):
                if selected_provider != "Tutti" and call['provider'] != selected_provider:
                    continue
                    
                provider_data = st.session_state.api_usage.get(call['provider'], {})
                icon = provider_data.get('icon', '🔹')
                st.caption(f"{icon} {call['time'].strftime('%H:%M:%S')} - "
                          f"{call['provider'].title()} - {call['symbol']} - "
                          f"{call['endpoint']} (#{call['cumulative_today']} oggi)")
        else:
            st.caption("Nessuna chiamata registrata")
    
    # Grafico distribuzione
    if total_today > 0:
        st.markdown("### 📈 Distribuzione Chiamate")
        
        fig = go.Figure(data=[go.Pie(
            labels=[s['name'] for s in stats if s['today'] > 0],
            values=[s['today'] for s in stats if s['today'] > 0],
            hole=.3,
            marker_colors=[s['color'] for s in stats if s['today'] > 0],
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            template='plotly_dark',
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Bottone reset log
    if st.button("🗑️ Resetta Log", use_container_width=True):
        st.session_state.api_calls_log = []
        st.rerun()

def render_config_tab():
    """Tab di configurazione API keys"""
    
    st.markdown("### 🔑 Gestione API Keys")
    st.caption("Modifica le chiavi dei provider (salvate in secrets.toml)")
    
    # Mostra chiavi attuali (censurate)
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container(border=True):
            st.markdown("**📡 TwelveData**")
            current_td = st.secrets.get("TWELVEDATA_KEY", "")
            if current_td:
                masked = current_td[:4] + "*" * (len(current_td) - 8) + current_td[-4:]
                st.code(masked)
            else:
                st.warning("❌ Non configurata")
            
            new_td = st.text_input("Nuova chiave TwelveData", type="password", key="td_key_input")
            if st.button("Aggiorna TwelveData", key="update_td"):
                st.warning("⚠️ Le chiavi si modificano in .streamlit/secrets.toml")
                st.code(f"TWELVEDATA_KEY=\"{new_td}\"")
        
        with st.container(border=True):
            st.markdown("**🟣 Alpha Vantage**")
            current_av = st.secrets.get("ALPHA_VANTAGE_KEY", "")
            if current_av:
                masked = current_av[:4] + "*" * (len(current_av) - 8) + current_av[-4:]
                st.code(masked)
            else:
                st.warning("❌ Non configurata")
            
            new_av = st.text_input("Nuova chiave Alpha Vantage", type="password", key="av_key_input")
            if st.button("Aggiorna Alpha Vantage", key="update_av"):
                st.warning("⚠️ Le chiavi si modificano in .streamlit/secrets.toml")
                st.code(f"ALPHA_VANTAGE_KEY=\"{new_av}\"")
    
    with col2:
        with st.container(border=True):
            st.markdown("**🟡 Marketaux**")
            current_mk = st.secrets.get("MARKETAUX_TOKEN", "")
            if current_mk:
                masked = current_mk[:4] + "*" * (len(current_mk) - 8) + current_mk[-4:]
                st.code(masked)
            else:
                st.warning("❌ Non configurata")
            
            new_mk = st.text_input("Nuova chiave Marketaux", type="password", key="mk_key_input")
            if st.button("Aggiorna Marketaux", key="update_mk"):
                st.warning("⚠️ Le chiavi si modificano in .streamlit/secrets.toml")
                st.code(f"MARKETAUX_TOKEN=\"{new_mk}\"")
        
        with st.container(border=True):
            st.markdown("**📄 secrets.toml completo**")
            st.code("""
# .streamlit/secrets.toml
TWELVEDATA_KEY="your_key_here"
ALPHA_VANTAGE_KEY="your_key_here"
MARKETAUX_TOKEN="your_key_here"
            """)
    
    # Link per ottenere chiavi
    st.divider()
    st.markdown("### 🔗 Dove ottenere le chiavi")
    
    col_l1, col_l2, col_l3 = st.columns(3)
    
    with col_l1:
        st.markdown("""
        **📡 TwelveData**
        - [twelvedata.com/apikey](https://twelvedata.com/apikey)
        - 800 chiamate/giorno
        - Gratis
        """)
    
    with col_l2:
        st.markdown("""
        **🟣 Alpha Vantage**
        - [alphavantage.co](https://www.alphavantage.co/support/#api-key)
        - 500 chiamate/giorno
        - Gratis
        """)
    
    with col_l3:
        st.markdown("""
        **🟡 Marketaux**
        - [marketaux.com](https://www.marketaux.com/)
        - 100 chiamate/giorno
        - Gratis
        """)
    
    # Istruzioni
    with st.expander("📖 Istruzioni per aggiornare le chiavi"):
        st.markdown("""
        ### Come aggiornare le API keys su Streamlit Cloud
        
        1. Vai su [share.streamlit.io](https://share.streamlit.io)
        2. Seleziona la tua app
        3. Clicca su **"Manage app"** (menu in alto a destra)
        4. Vai su **"Settings"** → **"Secrets"**
        5. Incolla il contenuto aggiornato:
        
        ```toml
        TWELVEDATA_KEY = "nuova_chiave"
        ALPHA_VANTAGE_KEY = "nuova_chiave"
        MARKETAUX_TOKEN = "nuova_chiave"
        ```
        
        6. Clicca **"Save"**
        7. Riavvia l'app
        """)