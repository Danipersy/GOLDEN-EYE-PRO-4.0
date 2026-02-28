import streamlit as st
import time
from providers.multi_provider import scan_symbol
from ui_streamlit.components.scan_filters import render_scan_filters
from ui_streamlit.components.header import render_header
from ui_streamlit.components.card import render_result_card

def show_page():
    # Header unificato
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
                progress_bar = st.progress(0, text="Inizializzazione scan...")
                
                for i, symbol in enumerate(st.session_state.watchlist):
                    progress_bar.progress((i + 1) / len(st.session_state.watchlist), 
                                         text=f"📡 Scan {i+1}/{len(st.session_state.watchlist)}: **{symbol}**")
                    
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
        # Statistiche
        level_counts = {}
        for r in st.session_state.scan_results:
            level = r.get('level', 1)
            level_counts[level] = level_counts.get(level, 0) + 1
        
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        with col_m1:
            st.metric("🔍 TOTALE", len(st.session_state.scan_results), border=True)
        with col_m2:
            st.metric("🔥 L5", level_counts.get(5, 0), border=True)
        with col_m3:
            st.metric("🟡 L4", level_counts.get(4, 0), border=True)
        with col_m4:
            st.metric("📊 L3", level_counts.get(3, 0), border=True)
        with col_m5:
            st.metric("📈 L2+", level_counts.get(2, 0) + level_counts.get(1, 0), border=True)
        
        st.markdown("---")
        st.subheader("🎯 Risultati Scan")
        
        # Filtra per livello
        filtered_results = [
            r for r in st.session_state.scan_results 
            if r.get('level', 1) >= filters.get('min_confidence', 1)
        ]
        
        for result in filtered_results:
            render_result_card(result, f"detail_{result['symbol']}")
            
            if st.button(f"📊 Analizza {result['symbol']}", key=f"btn_{result['symbol']}", use_container_width=True):
                st.session_state.selected_asset = result['symbol']
                st.session_state.radar_select = result['symbol']
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
    
    else:
        st.markdown("""
        <div style="
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #1a1f2e, #16213e);
            border-radius: 30px;
            margin: 30px 0;
            border: 2px dashed #f0b90b40;
        ">
            <div style="font-size: 5rem; margin-bottom: 20px;">📡</div>
            <h2 style="color: #f0b90b; margin-bottom: 10px;">Pronto per lo Scan!</h2>
            <p style="color: #94a3b8; margin-bottom: 20px;">Clicca "AVVIA SCAN COMPLETO" per iniziare</p>
        </div>
        """, unsafe_allow_html=True)
