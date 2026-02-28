# ui_streamlit/components/radar_panel.py
import streamlit as st
from datetime import datetime
from providers.yahoo_provider import run_radar_scan_yahoo
from providers.twelvedata_provider import search_symbols_td
from storage.watchlist_store import save_watchlist
from ui_streamlit.components.scan_filters import render_scan_filters
from config import WATCHLIST_FILE

def render_radar_panel():
    """Pannello radar - Versione grafica migliorata"""
    col_rad, col_new = st.columns([1.35, 1.65])
    
    # Inizializzazione
    if 'radar_select' not in st.session_state:
        st.session_state.radar_select = st.session_state.watchlist[0] if st.session_state.watchlist else ""
    if 'menu_key' not in st.session_state:
        st.session_state.menu_key = 0
    
    with col_rad:
        st.markdown("### 📡 RADAR YAHOO")
        
        # Menu a tendina con chiave dinamica
        menu_key = f"asset_menu_{st.session_state.menu_key}"
        selected = st.selectbox(
            "Seleziona asset",
            options=st.session_state.watchlist,
            index=st.session_state.watchlist.index(st.session_state.radar_select) 
                if st.session_state.radar_select in st.session_state.watchlist else 0,
            key=menu_key
        )
        
        if selected != st.session_state.radar_select:
            st.session_state.radar_select = selected
            st.session_state.menu_key += 1
            st.rerun()

        # Bottoni azione
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔄 Refresh", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("🗑️ Rimuovi", use_container_width=True):
                if len(st.session_state.watchlist) > 1:
                    st.session_state.watchlist.remove(st.session_state.radar_select)
                    save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                    st.session_state.radar_select = st.session_state.watchlist[0]
                    st.session_state.menu_key += 1
                    st.rerun()
        with col3:
            if st.button("📡 SCAN", use_container_width=True, type="primary"):
                with st.spinner("Scansionando..."):
                    st.session_state.radar_results = run_radar_scan_yahoo(st.session_state.watchlist)
                    st.rerun()
        
        # Filtri
        filters = render_scan_filters()
        
        # Risultati scan
        if st.session_state.get('radar_results'):
            st.markdown("---")
            st.markdown("### 🎯 SEGNALI")
            
            # Applica filtri
            filtered = []
            for r in st.session_state.radar_results:
                level = r.get('level', 1)
                if level < filters['min_confidence']: continue
                if level == 1 and not filters['show_neutral']: continue
                if level == 2 and not filters['show_trend']: continue
                if level == 3 and not filters['show_momentum']: continue
                if level == 4 and not filters['show_medium']: continue
                if level == 5 and not filters['show_strong']: continue
                filtered.append(r)
            
            for idx, r in enumerate(filtered):
                # Card segnale
                st.markdown(f"""
                <div style="
                    padding:12px; 
                    margin:8px 0; 
                    background:#1e1e2e; 
                    border-radius:10px;
                    border-left:5px solid {r['color']};
                    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
                ">
                    <div style="display:flex; justify-content:space-between;">
                        <span style="font-size:1.1rem; font-weight:bold;">{r['asset']}</span>
                        <span style="color:{r['color']}; font-weight:bold;">{r['signal']}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-top:5px;">
                        <span>💰 ${r['price']:,.2f}</span>
                        <span>📊 RSI: {r['rsi']}</span>
                        <span>📈 {r['var']:+.2f}%</span>
                        <span>⚡ L{r['level']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Bottone selezione
                if st.button(f"✅ Seleziona {r['asset']}", key=f"select_{idx}", use_container_width=True):
                    st.session_state.radar_select = r['asset']
                    st.session_state.menu_key += 1
                    st.rerun()
        else:
            st.info("Clicca SCAN per cercare segnali")

    with col_new:
        st.markdown("### ➕ AGGIUNGI ASSET")
        
        # Ricerca TwelveData
        search = st.text_input("🔍 Cerca", placeholder="Es: bitcoin, tesla...")
        if search and len(search) >= 3:
            results = search_symbols_td(search, 20)
            if results:
                labels = [x["label"] for x in results]
                symbols = [x["symbol"] for x in results]
                sel = st.selectbox("Risultati", labels)
                idx = labels.index(sel)
                if st.button("➕ Aggiungi", use_container_width=True):
                    sym = symbols[idx].upper()
                    if sym not in st.session_state.watchlist:
                        st.session_state.watchlist.append(sym)
                        save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                    st.session_state.radar_select = sym
                    st.session_state.menu_key += 1
                    st.rerun()
            else:
                st.caption("Nessun risultato")
        
        # Ticker manuale
        manual = st.text_input("✏️ Ticker", placeholder="Es: AAPL").upper().strip()
        if st.button("➕ Aggiungi manuale", use_container_width=True) and manual:
            if manual not in st.session_state.watchlist:
                st.session_state.watchlist.append(manual)
                save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
            st.session_state.radar_select = manual
            st.session_state.menu_key += 1
            st.rerun()