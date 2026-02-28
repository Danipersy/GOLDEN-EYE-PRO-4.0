import streamlit as st
import time
from datetime import datetime
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
            with st.spinner("🔄 Scansionando mercati in tempo reale..."):
                results = []
                progress_bar = st.progress(0, text="Inizializzazione scan...")
                
                for i, symbol in enumerate(st.session_state.watchlist):
                    progress_text = f"📡 Scan {i+1}/{len(st.session_state.watchlist)}: **{symbol}**"
                    progress_bar.progress((i + 1) / len(st.session_state.watchlist), text=progress_text)
                    
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
        # Statistiche in cards
        level_counts = {}
        for r in st.session_state.scan_results:
            level = r.get('level', 1)
            level_counts[level] = level_counts.get(level, 0) + 1
        
        st.markdown("### 📊 Riepilogo Scan")
        
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        
        with col_m1:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <span style="color: #94a3b8;">🔍 TOTALE</span>
                <div style="font-size: 2rem; font-weight: 800; color: #fff;">{len(st.session_state.scan_results)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m2:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; border-left-color: #00ff88;">
                <span style="color: #94a3b8;">🔥 FORTE</span>
                <div style="font-size: 2rem; font-weight: 800; color: #00ff88;">{level_counts.get(5, 0)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m3:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; border-left-color: #f0b90b;">
                <span style="color: #94a3b8;">🟡 MEDIO</span>
                <div style="font-size: 2rem; font-weight: 800; color: #f0b90b;">{level_counts.get(4, 0)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m4:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; border-left-color: #3b82f6;">
                <span style="color: #94a3b8;">📊 MOMENTUM</span>
                <div style="font-size: 2rem; font-weight: 800; color: #3b82f6;">{level_counts.get(3, 0)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_m5:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center; border-left-color: #8b5cf6;">
                <span style="color: #94a3b8;">📈 TENDENZA</span>
                <div style="font-size: 2rem; font-weight: 800; color: #8b5cf6;">{level_counts.get(2, 0) + level_counts.get(1, 0)}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 🎯 Risultati in Tempo Reale")
        
        # Filtra per livello
        filtered_results = [
            r for r in st.session_state.scan_results 
            if r.get('level', 1) >= filters.get('min_confidence', 1)
        ]
        
        if not filtered_results:
            st.info("📭 Nessun risultato con i filtri selezionati")
        else:
            for result in filtered_results:
                render_result_card(result, f"card_{result['symbol']}")
                
                col1, col2, col3 = st.columns([1, 1, 5])
                with col2:
                    if st.button(f"📊 Analizza {result['symbol']}", key=f"btn_{result['symbol']}", use_container_width=True):
                        st.session_state.selected_asset = result['symbol']
                        st.session_state.radar_select = result['symbol']
                        st.session_state.current_page = "DETTAGLIO"
                        st.rerun()
    
    else:
        # Schermata iniziale animata
        st.markdown("""
        <div style="
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(135deg, #1a1f2e, #16213e);
            border-radius: 40px;
            margin: 40px 0;
            border: 2px dashed rgba(240, 185, 11, 0.3);
            animation: pulse 2s infinite;
        ">
            <div style="font-size: 6rem; margin-bottom: 20px; animation: float 3s ease-in-out infinite;">📡</div>
            <h2 style="color: #f0b90b; font-size: 2.5rem; margin-bottom: 15px;">Pronto per lo Scan!</h2>
            <p style="color: #94a3b8; font-size: 1.2rem; margin-bottom: 20px;">Clicca "AVVIA SCAN COMPLETO" per iniziare il monitoraggio</p>
            <div style="
                background: rgba(240, 185, 11, 0.1);
                border-radius: 40px;
                padding: 15px 30px;
                display: inline-block;
                border: 1px solid #f0b90b;
            ">
                <span style="color: #f0b90b; font-weight: 600;">📊 Monitorerai {} asset in tempo reale</span>
            </div>
        </div>
        
        <style>
            @keyframes float {
                0% { transform: translateY(0px); }
                50% { transform: translateY(-20px); }
                100% { transform: translateY(0px); }
            }
            @keyframes pulse {
                0% { border-color: rgba(240, 185, 11, 0.3); }
                50% { border-color: rgba(240, 185, 11, 0.8); }
                100% { border-color: rgba(240, 185, 11, 0.3); }
            }
        </style>
        """.format(len(st.session_state.watchlist)), unsafe_allow_html=True)
