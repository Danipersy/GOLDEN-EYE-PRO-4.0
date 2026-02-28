import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
from providers.multi_provider import scan_symbol
from ui_streamlit.components.scan_filters import render_scan_filters

def show_page():
    st.title("🔍 RADAR SCAN")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.metric("Watchlist", len(st.session_state.watchlist))
        if st.button("🔄 Aggiorna", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    # Filtri avanzati
    filters = render_scan_filters()
    
    # Bottone scan
    if st.button("📡 AVVIA SCAN COMPLETO", use_container_width=True, type="primary"):
        with st.spinner("Scansionando mercati..."):
            results = []
            progress_bar = st.progress(0)
            
            for i, symbol in enumerate(st.session_state.watchlist):
                progress_bar.progress((i + 1) / len(st.session_state.watchlist), 
                                     text=f"Scan {i+1}/{len(st.session_state.watchlist)}: {symbol}")
                
                result = scan_symbol(symbol, "15m", "1d")
                if result and 'error' not in result:
                    # Calcola livello segnale
                    change = result.get('change', 0)
                    if abs(change) > 2:
                        level = 5
                    elif abs(change) > 1:
                        level = 4
                    elif abs(change) > 0.5:
                        level = 3
                    elif abs(change) > 0.1:
                        level = 2
                    else:
                        level = 1
                    
                    result['level'] = level
                    result['score'] = abs(change) * 10
                    results.append(result)
                
                time.sleep(0.5)
            
            progress_bar.empty()
            st.session_state.scan_results = results
    
    # Mostra risultati
    if st.session_state.get('scan_results'):
        st.markdown("---")
        st.subheader("🎯 Risultati Scan")
        
        # Filtra per livello
        filtered_results = [
            r for r in st.session_state.scan_results 
            if r.get('level', 1) >= filters.get('min_confidence', 1)
        ]
        
        # Card per ogni risultato
        for result in filtered_results:
            level = result.get('level', 1)
            change = result.get('change', 0)
            
            # Colori in base al livello
            if level == 5:
                color = "#00ff88"
                badge = "🔥 FORTE"
            elif level == 4:
                color = "#f0b90b"
                badge = "🟡 MEDIO"
            elif level == 3:
                color = "#3b82f6"
                badge = "📊 MOMENTUM"
            elif level == 2:
                color = "#8b5cf6"
                badge = "📈 TENDENZA"
            else:
                color = "#94a3b8"
                badge = "⚪ LATERALE"
            
            with st.container():
                cols = st.columns([2, 1, 1, 1, 1])
                
                with cols[0]:
                    st.markdown(f"**{result['symbol']}**")
                    st.caption(badge)
                
                with cols[1]:
                    st.metric("Prezzo", f"${result.get('price', 0):,.2f}")
                
                with cols[2]:
                    delta_color = "normal" if change > 0 else "inverse"
                    st.metric("Variazione", f"{change:+.2f}%", delta_color=delta_color)
                
                with cols[3]:
                    st.metric("Volume", f"{result.get('volume', 0):,.0f}")
                
                with cols[4]:
                    if st.button(f"📊 Dettaglio", key=f"detail_{result['symbol']}"):
                        st.session_state.selected_asset = result['symbol']
                        st.session_state.radar_select = result['symbol']
                        st.session_state.current_page = "DETTAGLIO"
                        st.rerun()
                
                st.divider()
