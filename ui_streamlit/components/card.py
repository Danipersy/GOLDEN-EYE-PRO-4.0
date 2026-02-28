import streamlit as st

def render_result_card(result):
    symbol = result.get('symbol', 'N/A')
    price = result.get('price', 0)
    change = result.get('change', 0)
    volume = result.get('volume', 0)
    level = result.get('level', 1)
    score = result.get('score', 0)

    # Mappa badge
    badge_map = {
        5: ("🔥 FORTE", "badge-l5"),
        4: ("🟡 MEDIO", "badge-l4"),
        3: ("📊 MOMENTUM", "badge-l3"),
        2: ("📈 TENDENZA", "badge-l2"),
        1: ("⚪ LATERALE", "badge-l1"),
    }
    badge_text, badge_class = badge_map.get(level, ("⚪ LATERALE", "badge-l1"))

    # Colore bordo sinistro in base al livello
    border_colors = {5: "#00ff88", 4: "#f0b90b", 3: "#3b82f6", 2: "#8b5cf6", 1: "#94a3b8"}
    border_color = border_colors.get(level, "#94a3b8")

    card_html = f'''
    <div class="custom-card" style="border-left-color: {border_color};">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span style="font-size: 1.8rem; font-weight: 700; color: white;">{symbol}</span>
            <span class="badge {badge_class}">{badge_text}</span>
        </div>
        <div style="display: flex; gap: 2rem; flex-wrap: wrap;">
            <div>
                <span style="color: #94a3b8; font-size: 0.8rem;">💰 PREZZO</span>
                <div style="font-size: 1.6rem; font-weight: 700; color: white;">${price:,.2f}</div>
            </div>
            <div>
                <span style="color: #94a3b8; font-size: 0.8rem;">📊 VOLUME</span>
                <div style="font-size: 1.2rem; font-weight: 600; color: white;">{volume:,.0f}</div>
            </div>
            <div>
                <span style="color: #94a3b8; font-size: 0.8rem;">🎯 SCORE AI</span>
                <div style="font-size: 1.6rem; font-weight: 700; color: {border_color};">{score}</div>
            </div>
            <div style="margin-left: auto; text-align: right;">
                <span style="color: #94a3b8; font-size: 0.8rem;">📈 VARIAZIONE</span>
                <div style="font-size: 1.8rem; font-weight: 800; color: {'#00ff88' if change >= 0 else '#ff3344'};">
                    {'▲' if change >= 0 else '▼'} {abs(change):.2f}%
                </div>
            </div>
        </div>
    </div>
    '''
    st.markdown(card_html, unsafe_allow_html=True)

    # Bottone analisi centrato
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(f"📊 Analizza {symbol}", key=f"btn_{symbol}", use_container_width=True):
            st.session_state.selected_asset = symbol
            st.session_state.radar_select = symbol
            st.session_state.current_page = "DETTAGLIO"
            st.rerun()
