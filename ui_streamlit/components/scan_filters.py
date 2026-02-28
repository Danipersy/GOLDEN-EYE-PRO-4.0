import streamlit as st

def render_scan_filters():
    defaults = {
        'filter_min_confidence': 1,
        'filter_show_neutral': True,
        'filter_show_trend': True,
        'filter_show_momentum': True,
        'filter_show_medium': True,
        'filter_show_strong': True,
        'filter_min_score': 0
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    with st.expander("🔧 Filtri Avanzati", expanded=False):
        st.slider("Livello minimo", 1, 5, key="filter_min_confidence", format="L%d")
        st.slider("Score minimo", 0, 100, key="filter_min_score")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("⚪ Laterale (L1)", key="filter_show_neutral")
            st.checkbox("📈 Tendenza (L2)", key="filter_show_trend")
            st.checkbox("📊 Momentum (L3)", key="filter_show_momentum")
        with col2:
            st.checkbox("🟡 Medio (L4)", key="filter_show_medium")
            st.checkbox("🔥 Forte (L5)", key="filter_show_strong")
        st.divider()
        st.caption("Preset rapidi:")
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
