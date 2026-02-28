# ui_streamlit/components/radar_panel.py
import streamlit as st
import time
from datetime import datetime
from providers.multi_provider import scan_symbol
from providers.twelvedata_provider import search_symbols_td
from storage.watchlist_store import save_watchlist
from ui_streamlit.components.scan_filters import render_scan_filters
from config import WATCHLIST_FILE

def render_radar_panel():
    """Pannello radar per la pagina SCAN"""
    
    st.markdown("### 📡 RADAR")
    
    # Selezione asset
    if st.session_state.watchlist:
        st.selectbox(
            "Seleziona asset",
            options=st.session_state.watchlist,
            index=st.session_state.watchlist.index(st.session_state.radar_select) 
                if st.session_state.radar_select in st.session_state.watchlist else 0,
            key="radar_select_box",
            on_change=lambda: setattr(st.session_state, 'radar_select', st.session_state.radar_select_box)
        )
    
    # Bottone SCAN
    if st.button("🔍 AVVIA SCAN", use_container_width=True, type="primary"):
        with st.spinner("Scansionando..."):
            results = []
            total = len(st.session_state.watchlist)
            progress_bar = st.progress(0, text="Avvio scan...")
            
            for i, symbol in enumerate(st.session_state.watchlist):
                progress_bar.progress((i + 1) / total, text=f"📡 Scan {i+1}/{total}: {symbol}")
                results.append(scan_symbol(symbol, "15m", "1mo"))
                time.sleep(0.5)
            
            progress_bar.empty()
            st.session_state.radar_results = results
    
    # Filtri
    render_scan_filters()
    
    st.markdown("---")
    st.markdown("### 🔍 RICERCA ASSET")
    
    search = st.text_input("Cerca simbolo", placeholder="Es: bitcoin, apple, BTC...")
    if search and len(search) >= 2:
        results = search_symbols_td(search, 10)
        if results:
            labels = [r["label"] for r in results]
            selected = st.selectbox("Risultati:", labels, key="search_results")
            idx = labels.index(selected)
            symbol = results[idx]["symbol"].replace("/", "-")
            
            if st.button("➕ Aggiungi alla watchlist", use_container_width=True):
                if symbol not in st.session_state.watchlist:
                    st.session_state.watchlist.append(symbol)
                    save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                    st.success(f"✅ {symbol} aggiunto!")
                    st.rerun()
