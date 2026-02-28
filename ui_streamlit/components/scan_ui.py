# ui_streamlit/components/scan_ui.py
import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime
from urllib.parse import quote_plus

from ui_streamlit.components.scan_engine import run_scan, apply_ui_filters, pick_best
from config import VERSION

def _sentiment_label(x):
    """Etichetta sentiment"""
    if x is None or not np.isfinite(x):
        return "N/D"
    if x > 0.10:
        return "Positivo"
    if x < -0.10:
        return "Negativo"
    return "Neutro"

def _init_filter_defaults(wl):
    """Inizializza valori default filtri"""
    st.session_state.setdefault("preset_choice", "Conservativo")
    st.session_state.setdefault("only_trade_ok", True)
    st.session_state.setdefault("show_wait", True)
    st.session_state.setdefault("show_error", False)
    st.session_state.setdefault("show_nodata", False)
    st.session_state.setdefault("min_score", 50)
    st.session_state.setdefault("debug_on", True)
    st.session_state.setdefault("auto_expand_best", True)

def debug_show_panel(df_raw: pd.DataFrame, view_final: pd.DataFrame, flags_df: pd.DataFrame):
    """Pannello debug"""
    with st.expander("🛠️ Debug filtri", expanded=False):
        if df_raw is None or df_raw.empty:
            st.info("Nessun dato")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Raw data")
            st.dataframe(df_raw, use_container_width=True, height=200)
        
        with col2:
            st.markdown("### Vista finale")
            if view_final.empty:
                st.info("Vuota - filtri stanno eliminando tutto")
            else:
                st.dataframe(view_final, use_container_width=True, height=200)
        
        if flags_df is not None and not flags_df.empty:
            st.markdown("### Motivi esclusione")
            st.dataframe(flags_df, use_container_width=True, height=200)

def apply_preset(name: str, wl):
    """Applica preset"""
    if name == "Aggressivo":
        st.session_state["only_trade_ok"] = False
        st.session_state["show_wait"] = True
        st.session_state["show_error"] = True
        st.session_state["show_nodata"] = True
        st.session_state["min_score"] = 40
    elif name == "Conservativo":
        st.session_state["only_trade_ok"] = True
        st.session_state["show_wait"] = True
        st.session_state["show_error"] = False
        st.session_state["show_nodata"] = False
        st.session_state["min_score"] = 60

def preset_bar(wl):
    """Barra preset"""
    with st.container(border=True):
        cols = st.columns([1, 1, 1, 1.2])
        cols[0].selectbox("Preset", ["Aggressivo", "Conservativo"], key="preset_choice")
        cols[1].toggle("Debug", key="debug_on")
        
        if cols[2].button("Applica", use_container_width=True):
            apply_preset(st.session_state.get("preset_choice", "Conservativo"), wl)
            st.rerun()
        
        cols[3].caption("Aggressivo = più segnali, Conservativo = selettivo")
    
    return bool(st.session_state.get("debug_on", True))

def read_filters(wl):
    """Leggi filtri UI"""
    _init_filter_defaults(wl)
    
    with st.container(border=True):
        st.markdown("### 🔧 Filtri")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.toggle("Solo TRADE_OK", key="only_trade_ok")
        
        with col2:
            st.toggle("Mostra WAIT", key="show_wait")
        
        with col3:
            st.toggle("Mostra ERRORI", key="show_error")
        
        with col4:
            st.toggle("Mostra NO_DATA", key="show_nodata")
        
        st.slider("Score minimo", 0, 100, key="min_score")
        st.toggle("Apri automaticamente dettaglio", key="auto_expand_best")
    
    return {
        "only_trade_ok": bool(st.session_state["only_trade_ok"]),
        "show_wait": bool(st.session_state["show_wait"]),
        "show_error": bool(st.session_state["show_error"]),
        "show_nodata": bool(st.session_state["show_nodata"]),
        "min_score": int(st.session_state["min_score"]),
        "auto_expand_best": bool(st.session_state["auto_expand_best"])
    }

def render_best_card(best: dict):
    """Render della card miglior segnale"""
    if not best:
        st.error("Nessun best candidato")
        return
    
    asset = str(best.get("asset", "N/A"))
    action = str(best.get("azione", "WAIT"))
    score = best.get("score", 0)
    
    cols = st.columns([1, 1, 1, 1, 1])
    
    with cols[0]:
        st.markdown(f"### {asset}")
        st.caption(action)
    
    with cols[1]:
        st.metric("Score", f"{score:.0f}/100")
    
    with cols[2]:
        price = best.get("last", 0)
        st.metric("Prezzo", f"${price:.2f}" if price else "N/A")
    
    with cols[3]:
        flow = best.get("flow", "N/A")
        st.metric("Flow", flow)
    
    with cols[4]:
        trade_ok = best.get("TRADE_OK", False)
        st.metric("TRADE_OK", "✅" if trade_ok else "❌")
    
    # Dettaglio
    col_d1, col_d2, col_d3, col_d4 = st.columns(4)
    
    with col_d1:
        st.markdown(f"**RSI:** {best.get('rsi', 0):.1f}")
        st.markdown(f"**ADX:** {best.get('adx', 0):.1f}")
    
    with col_d2:
        sl = best.get('sl')
        tp = best.get('tp')
        st.markdown(f"**SL:** ${sl:.2f}" if sl else "**SL:** N/A")
        st.markdown(f"**TP:** ${tp:.2f}" if tp else "**TP:** N/A")
    
    with col_d3:
        st.markdown(f"**Rischio:** {best.get('rischio_sl', 'N/A')}")
        st.markdown(f"**ATR:** ${best.get('atr', 0):.4f}")
    
    # Bottone posizione
    if st.button(f"📌 Apri posizione {asset}", use_container_width=True):
        st.session_state['position'] = {
            'active': True,
            'asset': asset,
            'action': action,
            'flow': best.get('flow'),
            'entry': best.get('last'),
            'sl': best.get('sl'),
            'tp': best.get('tp'),
            'timestamp': datetime.now().isoformat()
        }
        st.success(f"Posizione {asset} aperta!")
        st.rerun()

def render_signals_table(view: pd.DataFrame):
    """Render tabella segnali"""
    if view is None or view.empty:
        st.info("Nessun segnale da mostrare")
        return
    
    # Colonne da mostrare
    display_cols = ['asset', 'azione', 'score', 'TRADE_OK', 'rischio_sl',
                   'last', 'flow', 'rsi', 'adx']
    
    display_df = view[[c for c in display_cols if c in view.columns]].copy()
    
    # Formattazione
    def color_action(val):
        if val == 'BUY':
            return 'background-color: #1E3A3A; color: #4ADE80'
        elif val == 'SELL':
            return 'background-color: #3A1E1E; color: #F87171'
        return ''
    
    def color_score(val):
        if val >= 75:
            return 'color: #4ADE80; font-weight: bold'
        elif val >= 60:
            return 'color: #FBBF24'
        return ''
    
    styled_df = display_df.style.map(color_action, subset=['azione'])
    styled_df = styled_df.map(color_score, subset=['score'])
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "asset": "Asset",
            "azione": "Azione",
            "score": st.column_config.NumberColumn("Score", format="%.0f"),
            "TRADE_OK": "OK?",
            "rischio_sl": "Rischio",
            "last": st.column_config.NumberColumn("Prezzo", format="$%.2f"),
            "flow": "Flow",
            "rsi": st.column_config.NumberColumn("RSI", format="%.1f"),
            "adx": st.column_config.NumberColumn("ADX", format="%.1f")
        }
    )

def render_scan_page(wl, refresh_tick: int, render_asset_detail_fn):
    """Pagina scan principale"""
    _init_filter_defaults(wl)
    
    # Stats bar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"**Watchlist:** {len(wl)} assets")
    with col2:
        st.markdown(f"**Ultimo scan:** {datetime.now().strftime('%H:%M:%S')}")
    with col3:
        st.markdown(f"**Version:** {VERSION}")
    with col4:
        st.markdown("**Data:** Yahoo Finance")
    
    st.divider()
    
    # Preset bar
    debug_on = preset_bar(wl)
    
    # Filtri
    filters = read_filters(wl)
    
    # Bottone scan
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🚀 AVVIA SCAN", use_container_width=True, type="primary"):
            with st.spinner("Scansionando..."):
                results = run_scan(wl, refresh_tick=refresh_tick, f=filters)
                st.session_state['scan_results'] = results
    
    st.divider()
    
    # Recupera risultati
    df = st.session_state.get('scan_results')
    
    if df is None or df.empty:
        st.info("👆 Premi 'AVVIA SCAN' per iniziare")
        return
    
    # Applica filtri
    df_raw, df_filtered, flags_df = apply_ui_filters(df, filters)
    
    # Metriche
    st.markdown("### 📊 Riepilogo")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.metric("Totale Asset", len(df_raw), border=True)
    with m2:
        st.metric("Segnali Attivi", len(df_filtered), border=True)
    with m3:
        trade_ok_count = len(df_filtered[df_filtered['TRADE_OK'] == True]) if 'TRADE_OK' in df_filtered.columns else 0
        st.metric("TRADE_OK", trade_ok_count, border=True)
    with m4:
        buy_count = len(df_filtered[df_filtered['azione'] == 'BUY']) if 'azione' in df_filtered.columns else 0
        sell_count = len(df_filtered[df_filtered['azione'] == 'SELL']) if 'azione' in df_filtered.columns else 0
        st.metric("BUY/SELL", f"{buy_count}/{sell_count}", border=True)
    
    # Debug panel
    if debug_on:
        debug_show_panel(df_raw, df_filtered, flags_df)
    
    # Best signal
    best, best_asset, best_action = pick_best(df_filtered)
    if best:
        st.markdown("### 🏆 Miglior Segnale")
        render_best_card(best)
    else:
        st.info("Nessun segnale con i filtri attuali")
    
    # Tabella segnali
    st.markdown("### 📋 Tabella Segnali")
    render_signals_table(df_filtered)
    
    st.divider()
    
    # Dettaglio asset
    st.markdown("### 🔍 Dettaglio Asset")
    
    if not df_filtered.empty:
        assets = df_filtered['asset'].tolist()
        default_idx = 0
        if best_asset in assets:
            default_idx = assets.index(best_asset)
        
        selected = st.selectbox("Seleziona asset", assets, index=default_idx)
        
        with st.expander(f"📊 Dettaglio {selected}", 
                        expanded=bool(st.session_state.get("auto_expand_best", True))):
            render_asset_detail_fn(selected, refresh_tick)
