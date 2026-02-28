# ui_streamlit/components/scan_panel.py
import streamlit as st
import time
from datetime import datetime
from providers.multi_provider import scan_symbol
from providers.twelvedata_provider import search_symbols_td
from storage.watchlist_store import save_watchlist
from ui_streamlit.components.scan_filters import render_scan_filters
from config import WATCHLIST_FILE, DEFAULT_WATCHLIST

def render_scan_panel():
    """Pannello scan con risultati cliccabili"""
    
    col_scan, col_add = st.columns([1.35, 1.65])
    
    with col_scan:
        st.markdown("### 🔍 SCAN ASSET")
        
        # Bottoni azione
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Refresh Watchlist", use_container_width=True, key="refresh_watchlist"):
                st.rerun()
        with col2:
            if st.button("📡 AVVIA SCAN", use_container_width=True, type="primary", key="start_scan"):
                with st.spinner("Scansionando..."):
                    progress_bar = st.progress(0, text="Avvio scan...")
                    results = []
                    total = len(st.session_state.watchlist)
                    
                    for i, symbol in enumerate(st.session_state.watchlist):
                        progress_text = f"📡 Scan {i+1}/{total}: {symbol}"
                        progress_bar.progress((i + 1) / total, text=progress_text)
                        
                        result = scan_symbol(symbol, "15m", "1mo")
                        results.append(result)
                        time.sleep(0.5)
                    
                    progress_bar.empty()
                    st.session_state.radar_results = results
                    st.rerun()
        
        # Filtri
        filters = render_scan_filters()
        
        # Risultati scan
        if st.session_state.get('radar_results'):
            st.markdown("---")
            st.markdown("### 🎯 RISULTATI SCAN")
            
            # Applica filtri
            filtered = []
            for r in st.session_state.radar_results:
                if 'error' in r:
                    continue
                filtered.append(r)
            
            for idx, r in enumerate(filtered[:10]):
                change = r.get('change', 0)
                if change > 1:
                    color = "#00ff88"
                elif change > 0:
                    color = "#88ff88"
                elif change > -1:
                    color = "#ff8888"
                else:
                    color = "#ff3344"
                
                # Card risultato
                st.markdown(f"""
                <div style="
                    padding:12px; 
                    margin:8px 0; 
                    background:#1e1e2e; 
                    border-radius:10px;
                    border-left:5px solid {color};
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                ">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:1.1rem; font-weight:bold;">{r['symbol']}</span>
                        <span style="color:{color}; font-weight:bold;">
                            {r.get('change', 0):+.2f}%
                        </span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:5px;">
                        <span>💰 ${r.get('price', 0):,.2f}</span>
                        <span>📊 VOL: {r.get('volume', 0):,.0f}</span>
                        <span>⏱️ {r.get('timestamp', datetime.now()).strftime('%H:%M')}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Bottone per aprire dettaglio
                if st.button(f"📊 Analizza {r['symbol']}", key=f"detail_{idx}", use_container_width=True):
                    st.session_state.radar_select = r['symbol']
                    st.session_state.current_view = "detail"
                    st.rerun()
            
            if len(filtered) < len(st.session_state.radar_results):
                st.caption(f"📊 Mostrati {len(filtered)} di {len(st.session_state.radar_results)} totali")
        else:
            st.info("👆 Clicca AVVIA SCAN per cercare segnali")
    
    with col_add:
        st.markdown("### ➕ AGGIUNGI ASSET")
        
        search = st.text_input("Cerca simbolo", placeholder="Es: bitcoin, apple, BTC...", key="search_symbol_input")
        
        if search and len(search) >= 2:
            with st.spinner("Ricerca in corso..."):
                results = search_symbols_td(search, 15)
            
            if results:
                labels = [r["label"] for r in results]
                selected_label = st.selectbox("Risultati:", options=labels, key="search_results_select")
                
                idx = labels.index(selected_label)
                selected_symbol = results[idx]["symbol"]
                
                if st.button("➕ Aggiungi", use_container_width=True, type="primary", key="add_from_search"):
                    add_symbol = selected_symbol.replace("/", "-")
                    if add_symbol not in st.session_state.watchlist:
                        st.session_state.watchlist.append(add_symbol)
                        save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                        st.success(f"✅ {add_symbol} aggiunto!")
                        st.rerun()
                    else:
                        st.warning(f"⚠️ Già presente")
            else:
                st.caption("❌ Nessun risultato")