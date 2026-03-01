# ui_streamlit/pages/info.py
import streamlit as st

def render():
    st.subheader("ℹ️ Informazioni sull'App")
    st.markdown("""
    **GOLDEN EYE PRO 4.0** è una piattaforma di trading intelligence progettata per fornire analisi multi-asset in tempo reale.
    
    # Layout a colonne
    col_info1, col_info2 = st.columns(2)
    
    with col_info1:
        # STATISTICHE
        with st.container(border=True):
            st.markdown("### 📊 Statistiche Sistema")
            
            # Metriche in colonne
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Watchlist", len(st.session_state.watchlist))
                st.metric("Scan eseguiti", len(st.session_state.radar_results))
            
            with col_m2:
                uptime = str(datetime.now() - st.session_state.app_start_time).split('.')[0]
                st.metric("Uptime", uptime)
                st.metric("Menu Key", st.session_state.get('menu_key', 0))
            
            # Asset corrente
            if st.session_state.radar_select:
                st.info(f"📌 **Asset attuale:** {st.session_state.radar_select}")
    
    with col_info2:
        # PROVIDER
        with st.container(border=True):
            st.markdown("### 📡 Provider Dati")
            st.markdown("""
            | Provider | Utilizzo |
            |----------|----------|
            | **TwelveData** | Dati principali (5000 candles) |
            | **Yahoo Finance** | Fallback e scan rapido |
            | **Marketaux** | News e sentiment |
            """)
            
            # Fonte dati attuale
            if st.session_state.get('data_source'):
                st.success(f"Fonte attuale: {st.session_state.data_source}")
    
    # RIGA 2: Cache e Debug
    col_cache, col_debug = st.columns(2)
    
    with col_cache:
        # CACHE
        with st.container(border=True):
            st.markdown("### 💾 Cache")
            
            # Mostra items in cache
            cache_items = len(_data_cache)
            st.metric("Items in cache", cache_items)
            
            # Ultime chiavi cache
            if cache_items > 0:
                with st.expander("📋 Ultime chiavi cache"):
                    keys = list(_data_cache.keys())[-5:]
                    for k in keys:
                        st.code(k)
            
            # Bottone svuota cache
            if st.button("🗑️ Svuota Cache", use_container_width=True):
                _data_cache.clear()
                st.success("✅ Cache svuotata!")
                st.rerun()
    
    with col_debug:
        # DEBUG
        with st.container(border=True):
            st.markdown("### 🐛 Debug Mode")
            
            # Stato debug
            debug_status = "✅ ATTIVO" if st.session_state.debug_mode else "❌ DISATTIVO"
            st.info(f"Debug: {debug_status}")
            
            # Toggle debug
            if st.button("🔄 Toggle Debug", use_container_width=True):
                st.session_state.debug_mode = not st.session_state.debug_mode
                st.rerun()
            
            # Info aggiuntive se debug attivo
            if st.session_state.debug_mode:
                st.warning("Debug mode attivo - info extra visibili")
    
    # RIGA 3: Session State (collassabile)
    with st.container(border=True):
        st.markdown("### 📋 Session State")
        
        if st.checkbox("Mostra session state", key="show_session"):
            # Filtra chiavi private
            public_keys = {k: v for k, v in st.session_state.items() if not k.startswith('_')}
            st.json(public_keys)
            
            # Download session state
            import json
            session_json = json.dumps({k: str(v) for k, v in public_keys.items()}, indent=2)
            st.download_button(
                "📥 Download Session State",
                session_json,
                "session_state.json",
                "application/json"
            )
    
    # RIGA 4: Ultimo aggiornamento
    st.markdown("---")
    col_up1, col_up2, col_up3 = st.columns(3)
    with col_up1:
        if st.session_state.last_update:
            st.caption(f"🕒 Ultimo update: {st.session_state.last_update.strftime('%d/%m/%Y %H:%M:%S')}")
    with col_up2:
        if st.session_state.last_data_timestamp:
            st.caption(f"📅 Ultimo dato: {st.session_state.last_data_timestamp.strftime('%d/%m/%Y %H:%M:%S')}")
    with col_up3:
        st.caption(f"⚙️ Versione: {st.session_state.get('version', '1.0.0')}")
