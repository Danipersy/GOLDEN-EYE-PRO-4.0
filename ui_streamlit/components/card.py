import streamlit as st

def render_result_card(result):
    """Card professionale per i risultati scan"""
    symbol = result.get('symbol', 'N/A')
    price = result.get('price', 0)
    change = result.get('change', 0)
    volume = result.get('volume', 0)
    level = result.get('level', 1)
    score = result.get('score', 0)

    # Configurazione badge in base al livello
    if level == 5:
        badge_text = "🔥 FORTE"
        badge_color = "#00ff88"
        text_color = "black"
    elif level == 4:
        badge_text = "🟡 MEDIO"
        badge_color = "#f0b90b"
        text_color = "black"
    elif level == 3:
        badge_text = "📊 MOMENTUM"
        badge_color = "#3b82f6"
        text_color = "white"
    elif level == 2:
        badge_text = "📈 TENDENZA"
        badge_color = "#8b5cf6"
        text_color = "white"
    else:
        badge_text = "⚪ LATERALE"
        badge_color = "#94a3b8"
        text_color = "black"

    # HTML minimale per il badge (solo questo, nient'altro)
    badge_html = f"""
    <span style="
        background-color: {badge_color};
        color: {text_color};
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        display: inline-block;
    ">{badge_text}</span>
    """

    # Container con bordo
    with st.container(border=True):
        # Riga 1: simbolo e badge
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"### {symbol}")
        with col2:
            st.markdown(badge_html, unsafe_allow_html=True)

        # Riga 2: metriche
        cols = st.columns(3)
        with cols[0]:
            st.metric("Prezzo", f"${price:,.2f}")
        with cols[1]:
            delta = f"{change:+.2f}%"
            st.metric("Variazione", delta, delta_color="normal")
        with cols[2]:
            st.metric("Score AI", f"{score:.0f}")

        # Riga 3: volume
        st.caption(f"📊 Volume: {volume:,.0f}")

        # Riga 4: bottone analisi centrato
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"📊 Analizza {symbol}", key=f"btn_{symbol}", use_container_width=True):
                st.session_state.selected_asset = symbol
                st.session_state.radar_select = symbol
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
