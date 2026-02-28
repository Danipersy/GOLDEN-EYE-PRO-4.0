import streamlit as st
import time
from datetime import datetime
from providers.multi_provider import scan_symbol
from ui_streamlit.components.scan_filters import render_scan_filters
from ui_streamlit.components.card import render_result_card

def show_page():
    st.subheader("🔍 RADAR SCAN", divider="orange")

    col_f1, col_f2 = st.columns([3, 1])
    with col_f1:
        filters = render_scan_filters()
    with col_f2:
        st.write("")
        st.write("")
        if st.button("🚀 AVVIA SCAN", use_container_width=True, type="primary"):
            with st.spinner("Scansionando mercati..."):
                results = []
                progress_bar = st.progress(0)
                for i, symbol in enumerate(st.session_state.watchlist):
                    progress_bar.progress((i+1)/len(st.session_state.watchlist),
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
                        result['score'] = min(100, abs(change)*10)
                        results.append(result)
                    time.sleep(0.3)
                progress_bar.empty()
                st.session_state.scan_results = results
                st.session_state.last_scan_time = datetime.now()
                st.rerun()

    st.divider()

    if st.session_state.get('scan_results'):
        # Statistiche riepilogo
        level_counts = {}
        for r in st.session_state.scan_results:
            level = r.get('level', 1)
            level_counts[level] = level_counts.get(level, 0) + 1

        st.subheader("📊 Riepilogo")
        cols = st.columns(5)
        with cols[0]:
            st.metric("Totale", len(st.session_state.scan_results))
        with cols[1]:
            st.metric("🔥 L5", level_counts.get(5, 0))
        with cols[2]:
            st.metric("🟡 L4", level_counts.get(4, 0))
        with cols[3]:
            st.metric("📊 L3", level_counts.get(3, 0))
        with cols[4]:
            st.metric("📈 L2", level_counts.get(2, 0) + level_counts.get(1, 0))

        st.divider()
        st.subheader("🎯 Segnali")

        filtered = [r for r in st.session_state.scan_results
                    if r.get('level', 1) >= filters.get('min_confidence', 1)]

        for result in filtered:
            render_result_card(result)
    else:
        st.info("👆 Clicca 'AVVIA SCAN' per iniziare")
