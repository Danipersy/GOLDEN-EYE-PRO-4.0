import streamlit as st
import time
from datetime import datetime
from providers.multi_provider import scan_symbol
from ui_streamlit.components.scan_filters import render_scan_filters
from ui_streamlit.components.card import render_result_card

def show_page():
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px;">
        <h1 style="margin:0; font-size: 2.5rem; background: linear-gradient(135deg, #fff, #f0f6fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🔍 RADAR SCAN
        </h1>
        <div class="live-badge">
            <span style="color: #00ff88;">●</span> LIVE
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filtri e scan button
    col_f1, col_f2 = st.columns([3, 1])
    
    with col_f1:
        filters = render_scan_filters()
    
    with col_f2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 AVVIA SCAN PREMIUM", use_container_width=True, type="primary"):
            with st.spinner("🔄 Scansionando mercati globali..."):
                results = []
                progress_bar = st.progress(0)
                
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
    
    # Risultati
    if st.session_state.get('scan_results'):
        # Statistiche in card PRO
        level_counts = {}
        for r in st.session_state.scan_results:
            level = r.get('level', 1)
            level_counts[level] = level_counts.get(level, 0) + 1
        
        st.markdown("### 📊 Panoramica Scan")
        
        cols = st.columns(5)
        metrics = [
            ("🔍 TOTALE", len(st.session_state.scan_results), "#f0b90b"),
            ("🔥 FORTE", level_counts.get(5, 0), "#00ff88"),
            ("🟡 MEDIO", level_counts.get(4, 0), "#f0b90b"),
            ("📊 MOMENTUM", level_counts.get(3, 0), "#3b82f6"),
            ("📈 TENDENZA", level_counts.get(2, 0) + level_counts.get(1, 0), "#8b5cf6"),
        ]
        
        for col, (label, value, color) in zip(cols, metrics):
            with col:
                st.markdown(f"""
                <div class="metric-card-pro" style="text-align: center;">
                    <div style="color: #94a3b8; font-size: 0.8rem;">{label}</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: {color};">{value}</div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Segnali in Tempo Reale")
        
        # Filtra risultati
        filtered = [
            r for r in st.session_state.scan_results 
            if r.get('level', 1) >= filters.get('min_confidence', 1)
        ]
        
        for result in filtered:
            render_result_card(result)
    
    else:
        # Schermata iniziale elegante
        st.markdown(f"""
        <div style="
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(135deg, rgba(26, 31, 58, 0.5), rgba(18, 23, 40, 0.5));
            border-radius: 40px;
            margin: 40px 0;
            border: 2px dashed rgba(240, 185, 11, 0.3);
        ">
            <div style="font-size: 5rem; margin-bottom: 20px;">📡</div>
            <h2 style="color: #f0b90b; font-size: 2rem;">Pronto per lo Scan Premium</h2>
            <p style="color: #94a3b8; font-size: 1.1rem;">Clicca "AVVIA SCAN PREMIUM" per iniziare il monitoraggio</p>
            <div style="
                background: rgba(240, 185, 11, 0.1);
                border-radius: 40px;
                padding: 15px 30px;
                display: inline-block;
                margin-top: 20px;
                border: 1px solid #f0b90b;
            ">
                <span style="color: #f0b90b;">📊 Monitorerai {len(st.session_state.watchlist)} asset in tempo reale</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
