import streamlit as st
import time
from datetime import datetime
from providers.multi_provider import scan_symbol
from ui_streamlit.components.scan_filters import render_scan_filters
from ui_streamlit.components.card import render_result_card

def show_page():
    st.markdown("## 🔍 RADAR SCAN")
    
    # Info orario
    col1, col2 = st.columns([3, 1])
    with col2:
        st.caption(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
    
    # Filtri
    filters = render_scan_filters()
    
    # Bottone scan
    if st.button("🚀 AVVIA SCAN", use_container_width=True, type="primary"):
        with st.spinner("Scansionando..."):
            results = []
            progress_bar = st.progress(0)
            
            for i, symbol in enumerate(st.session_state.watchlist):
                progress_bar.progress((i + 1) / len(st.session_state.watchlist), 
                                     text=f"Scan {i+1}/{len(st.session_state.watchlist)}: {symbol}")
                
                result = scan_symbol(symbol, "15m", "1d")
                if result and 'error' not in result:
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
                    result['score'] = min(100, abs(change) * 10)
                    results.append(result)
                
                time.sleep(0.3)
            
            progress_bar.empty()
            st.session_state.scan_results = results
            st.session_state.last_scan_time = datetime.now()
            st.rerun()
    
    st.divider()
    
    # Risultati
    if st.session_state.get('scan_results'):
        st.markdown("### 📊 Risultati")
        
        # Statistiche
        level_counts = {}
        for r in st.session_state.scan_results:
            level = r.get('level', 1)
            level_counts[level] = level_counts.get(level, 0) + 1
        
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Totale", len(st.session_state.scan_results))
        col2.metric("🔥 L5", level_counts.get(5, 0))
        col3.metric("🟡 L4", level_counts.get(4, 0))
        col4.metric("📊 L3", level_counts.get(3, 0))
        col5.metric("📈 L2", level_counts.get(2, 0) + level_counts.get(1, 0))
        
        st.divider()
        
        # Filtra risultati
        filtered = [
            r for r in st.session_state.scan_results 
            if r.get('level', 1) >= filters.get('min_confidence', 1)
        ]
        
        for result in filtered:
            # ✅ CORRETTO: un solo argomento
            render_result_card(result)
            
            if st.button(f"📊 Analizza {result['symbol']}", key=f"btn_{result['symbol']}"):
                st.session_state.selected_asset = result['symbol']
                st.session_state.radar_select = result['symbol']
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
    
    else:
        st.info("👆 Clicca 'AVVIA SCAN' per iniziare")
