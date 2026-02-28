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
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Watchlist", len(st.session_state.watchlist))
        with col2:
            if st.session_state.get('radar_results'):
                st.metric("Risultati", len(st.session_state.radar_results))
        with col3:
            last_scan = st.session_state.get('last_scan_time')
            st.metric("Ultimo scan", last_scan.strftime("%H:%M") if last_scan else "—")
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🔄 Refresh", use_container_width=True, key="refresh_scan"):
                st.rerun()
        with col_btn2:
            if st.button("📡 AVVIA SCAN", use_container_width=True, type="primary", key="start_scan"):
                with st.spinner("Scansionando..."):
                    progress_bar = st.progress(0, text="Avvio scan...")
                    results = []
                    total = len(st.session_state.watchlist)
                    
                    st.session_state.last_scan_time = datetime.now()
                    
                    for i, symbol in enumerate(st.session_state.watchlist):
                        progress_text = f"📡 Scan {i+1}/{total}: {symbol}"
                        progress_bar.progress((i + 1) / total, text=progress_text)
                        
                        result = scan_symbol(symbol, "15m", "1mo")
                        results.append(result)
                        time.sleep(0.5)
                    
                    progress_bar.empty()
                    st.session_state.radar_results = results
                    st.rerun()
        
        filters = render_scan_filters()
        
        if st.session_state.get('radar_results'):
            st.markdown("---")
            st.markdown("### 🎯 RISULTATI SCAN")
            
            filtered = []
            for r in st.session_state.radar_results:
                if 'error' in r:
                    continue
                level = r.get('level', 1)
                if level < filters.get('min_confidence', 1):
                    continue
                filtered.append(r)
            
            if filtered:
                for idx, r in enumerate(filtered[:10]):
                    change = r.get('change', 0)
                    if change > 2:
                        color = "#00ff88"
                        badge = "🟢 FORTE"
                    elif change > 1:
                        color = "#88ff88"
                        badge = "🟡 MEDIO"
                    elif change > 0:
                        color = "#f0b90b"
                        badge = "⚪ DEBOLE"
                    elif change > -1:
                        color = "#ff8888"
                        badge = "🔴 DEBOLE"
                    else:
                        color = "#ff3344"
                        badge = "🔴 FORTE"
                    
                    st.markdown(f"""
                    <div style="
                        padding:12px; 
                        margin:8px 0; 
                        background:#1e1e2e; 
                        border-radius:10px;
                        border-left:5px solid {color};
                        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                    ">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-size:1.2rem; font-weight:bold;">{r['symbol']}</span>
                            <span style="background:{color}20; color:{color}; padding:4px 8px; border-radius:12px; font-size:0.8rem;">
                                {badge}
                            </span>
                        </div>
                        <div style="display:flex; justify-content:space-between; margin-top:10px;">
                            <div>
                                <span style="color:#94a3b8;">Prezzo</span><br>
                                <span style="font-size:1.3rem; font-weight:bold;">${r.get('price', 0):,.2f}</span>
                            </div>
                            <div style="text-align:right;">
                                <span style="color:{color}; font-weight:bold; font-size:1.3rem;">
                                    {r.get('change', 0):+.2f}%
                                </span><br>
                                <span style="color:#94a3b8;">VOL: {r.get('volume', 0):,.0f}</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button(f"📊 Analizza {r['symbol']}", key=f"detail_{idx}", use_container_width=True):
                        st.session_state.radar_select = r['symbol']
                        st.session_state.current_view = "detail"
                        st.rerun()
                
                if len(filtered) < len(st.session_state.radar_results):
                    st.caption(f"📊 Mostrati {len(filtered)} di {len(st.session_state.radar_results)} totali")
            else:
                st.info("Nessun risultato dopo i filtri")
        else:
            st.info("👆 Clicca AVVIA SCAN per cercare segnali")
    
    with col_add:
        st.markdown("### ➕ GESTIONE ASSET")
        
        with st.container(border=True):
            st.markdown("**🔍 Cerca nuovi simboli**")
            search = st.text_input("Simbolo", placeholder="Es: bitcoin, apple, BTC...", key="search_symbol_input", label_visibility="collapsed")
            
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
        
        with st.container(border=True):
            st.markdown("**✏️ Aggiunta manuale**")
            manual = st.text_input("Simbolo", placeholder="Es: BTC-USD, AAPL, MSFT", key="manual_symbol_input", label_visibility="collapsed").upper().strip()
            
            if st.button("➕ Aggiungi manuale", use_container_width=True, key="add_manual") and manual:
                if manual not in st.session_state.watchlist:
                    st.session_state.watchlist.append(manual)
                    save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                    st.success(f"✅ {manual} aggiunto!")
                    st.rerun()
                else:
                    st.warning(f"⚠️ {manual} già presente")
        
        with st.expander("📋 Watchlist attuale", expanded=False):
            st.write(", ".join(st.session_state.watchlist))
            st.caption(f"Totale: {len(st.session_state.watchlist)} asset")
            
            if st.button("🔄 Reset a default", use_container_width=True, key="reset_watchlist"):
                st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
                save_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)
                st.rerun()