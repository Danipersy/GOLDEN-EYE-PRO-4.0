import streamlit as st

def render_scan_filters():
    """Filtri a 5 livelli con grafica PRO"""
    
    # Inizializzazione
    defaults = {
        'filter_min_confidence': 1,
        'filter_show_neutral': True,
        'filter_show_trend': True,
        'filter_show_momentum': True,
        'filter_show_medium': True,
        'filter_show_strong': True,
        'filter_min_score': 0
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
    
    with st.expander("🔧 FILTRI AVANZATI", expanded=False):
        # Livello minimo
        st.markdown("#### 🎯 Livello di Confidenza")
        
        level = st.select_slider(
            "Seleziona livello minimo:",
            options=[1, 2, 3, 4, 5],
            value=st.session_state.filter_min_confidence,
            format_func=lambda x: {
                1: "⚪ TUTTI (L1+)",
                2: "📈 TENDENZA (L2+)",
                3: "📊 MOMENTUM (L3+)",
                4: "🟡 MEDI (L4+)",
                5: "🔥 SOLO FORTI (L5)"
            }[x],
            key="confidence_slider"
        )
        st.session_state.filter_min_confidence = level
        
        # Score minimo
        st.session_state.filter_min_score = st.slider(
            "Score AI minimo",
            0, 100, 
            st.session_state.filter_min_score,
            help="Filtra per score dell'AI (0-100)"
        )
        
        st.divider()
        
        # Categorie
        col1, col2 = st.columns(2)
        
        with col1:
            st.checkbox("⚪ Laterale (L1)", key="filter_show_neutral",
                       disabled=level > 1,
                       help="Mercato laterale - solo informativo")
            st.checkbox("📈 Tendenza (L2)", key="filter_show_trend",
                       disabled=level > 2,
                       help="Posizione rispetto a EMA200")
            st.checkbox("📊 Momentum (L3)", key="filter_show_momentum",
                       disabled=level > 3,
                       help="Pendenza significativa")
        
        with col2:
            st.checkbox("🟡 Trading Medio (L4)", key="filter_show_medium",
                       disabled=level > 4,
                       help="Segnali di trading medi")
            st.checkbox("🔥 Trading Forte (L5)", key="filter_show_strong",
                       disabled=level > 5,
                       help="Segnali di trading forti")
        
        st.divider()
        
        # Preset rapidi
        st.markdown("#### ⚡ Preset Rapidi")
        cols = st.columns(4)
        with cols[0]:
            if st.button("📊 Tutti", use_container_width=True):
                st.session_state.filter_min_confidence = 1
                st.session_state.filter_min_score = 0
                st.rerun()
        with cols[1]:
            if st.button("📈 Trend", use_container_width=True):
                st.session_state.filter_min_confidence = 2
                st.session_state.filter_min_score = 30
                st.rerun()
        with cols[2]:
            if st.button("🟡 Medi", use_container_width=True):
                st.session_state.filter_min_confidence = 4
                st.session_state.filter_min_score = 50
                st.rerun()
        with cols[3]:
            if st.button("🔥 Forti", use_container_width=True):
                st.session_state.filter_min_confidence = 5
                st.session_state.filter_min_score = 70
                st.rerun()
    
    return {
        "min_confidence": st.session_state.filter_min_confidence,
        "min_score": st.session_state.filter_min_score,
        "show_neutral": st.session_state.filter_show_neutral,
        "show_trend": st.session_state.filter_show_trend,
        "show_momentum": st.session_state.filter_show_momentum,
        "show_medium": st.session_state.filter_show_medium,
        "show_strong": st.session_state.filter_show_strong
    }
