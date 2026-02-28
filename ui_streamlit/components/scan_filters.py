# ui_streamlit/components/scan_filters.py
import streamlit as st
from typing import Dict

def render_scan_filters():
    """Filtri a 5 livelli - Grafica migliorata"""
    
    # Inizializzazione
    defaults = {
        'filter_min_confidence': 1,
        'filter_show_neutral': True,
        'filter_show_trend': True,
        'filter_show_momentum': True,
        'filter_show_medium': True,
        'filter_show_strong': True
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    # Gestione preset
    if 'preset_requested' in st.session_state:
        preset = st.session_state.preset_requested
        if preset == 'tutti':
            st.session_state.filter_min_confidence = 1
        elif preset == 'trend':
            st.session_state.filter_min_confidence = 2
        elif preset == 'medi':
            st.session_state.filter_min_confidence = 4
        elif preset == 'forti':
            st.session_state.filter_min_confidence = 5
        del st.session_state.preset_requested
    
    with st.expander("🔧 Filtri Avanzati", expanded=False):
        # Livello minimo
        st.markdown("#### 🎯 Livello minimo")
        
        level = st.select_slider(
            "Filtra per confidenza:",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.filter_min_confidence,
            format_func=lambda x: {
                1: "⚪ TUTTI",
                2: "📈 TENDENZA",
                3: "📊 MOMENTUM",
                4: "🟡 MEDI",
                5: "🟢 SOLO FORTI"
            }[x],
            key="confidence_slider"
        )
        st.session_state.filter_min_confidence = level
        
        # Checkbox categorie
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("⚪ Laterale", key="filter_show_neutral", 
                       disabled=level > 1,
                       help="Mercato laterale - solo informativo")
            st.checkbox("📈 Tendenza", key="filter_show_trend",
                       disabled=level > 2,
                       help="Posizione rispetto a EMA200")
            st.checkbox("📊 Momentum", key="filter_show_momentum",
                       disabled=level > 3,
                       help="Pendenza significativa")
        
        with col2:
            st.checkbox("🟡 Acquisto/Vendita", key="filter_show_medium",
                       disabled=level > 4,
                       help="Segnali di trading medi")
            st.checkbox("🟢 Forti", key="filter_show_strong",
                       disabled=level > 5,
                       help="Segnali di trading forti")
        
        # Preset rapidi
        st.markdown("#### ⚡ Preset")
        cols = st.columns(4)
        with cols[0]:
            if st.button("📊 Tutti", use_container_width=True):
                st.session_state.preset_requested = 'tutti'
                st.rerun()
        with cols[1]:
            if st.button("📈 Trend", use_container_width=True):
                st.session_state.preset_requested = 'trend'
                st.rerun()
        with cols[2]:
            if st.button("🟡 Medi", use_container_width=True):
                st.session_state.preset_requested = 'medi'
                st.rerun()
        with cols[3]:
            if st.button("🔥 Forti", use_container_width=True):
                st.session_state.preset_requested = 'forti'
                st.rerun()
    
    return {
        "min_confidence": st.session_state.filter_min_confidence,
        "show_neutral": st.session_state.filter_show_neutral,
        "show_trend": st.session_state.filter_show_trend,
        "show_momentum": st.session_state.filter_show_momentum,
        "show_medium": st.session_state.filter_show_medium,
        "show_strong": st.session_state.filter_show_strong
    }