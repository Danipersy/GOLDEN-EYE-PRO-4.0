import streamlit as st
import time
from datetime import datetime
from providers.multi_provider import scan_symbol
from ui_streamlit.components.scan_filters import render_scan_filters
from ui_streamlit.components.header import render_header
from ui_streamlit.components.card import render_result_card

def show_page():
    # Header DEVE essere chiamato qui
    render_header("RADAR SCAN", "🔍")
    
    # Filtri e scan button
    col_f1, col_f2 = st.columns([3, 1])
    
    with col_f1:
        filters = render_scan_filters()
    
    with col_f2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 AVVIA SCAN COMPLETO", use_container_width=True, type="primary"):
            with st.spinner("🔄 Scansionando mercati..."):
                results = []
                progress_bar = st.progress(0)
                
                for i, symbol in enumerate(st.session_state.watchlist):
                    progress_bar.progress((i + 1) / len(st.session_state.watchlist), 
                                         text=f"📡 Scan {i+1}/{len(st.session_state.watchlist)}: {symbol}")
                    
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
    
    st.markdown("---")
    
    # Risultati scan
    if st.session_state.get('scan_results'):
        st.markdown("### 🎯 Risultati in Tempo Reale")
        
        # Filtra per livello
        filtered_results = [
            r for r in st.session_state.scan_results 
            if r.get('level', 1) >= filters.get('min_confidence', 1)
        ]
        
        for result in filtered_results:
            render_result_card(result, f"card_{result['symbol']}")
            
            if st.button(f"📊 Analizza {result['symbol']}", key=f"btn_{result['symbol']}", use_container_width=True):
                st.session_state.selected_asset = result['symbol']
                st.session_state.radar_select = result['symbol']
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
    else:
        st.info("👆 Clicca 'AVVIA SCAN COMPLETO' per iniziare")
