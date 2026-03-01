import streamlit as st

def render_result_card(result):
    symbol = result.get('symbol', 'N/A')
    price = result.get('price', 0)
    change = result.get('change', 0)
    volume = result.get('volume', 0)
    level = result.get('level', 1)
    score = result.get('score', 0)

    # Mappa badge
    if level == 5:
        badge_class = "badge-l5"
        badge_text = "🔥 FORTE"
    elif level == 4:
        badge_class = "badge-l4"
        badge_text = "🟡 MEDIO"
    elif level == 3:
        badge_class = "badge-l3"
        badge_text = "📊 MOMENTUM"
    elif level == 2:
        badge_class = "badge-l2"
        badge_text = "📈 TENDENZA"
    else:
        badge_class = "badge-l1"
        badge_text = "⚪ LATERALE"

    change_color = "#10B981" if change >= 0 else "#EF4444"
    change_icon = "▲" if change >= 0 else "▼"

    with st.container(border=True):
        cols = st.columns([1, 4])
        with cols[0]:
            st.markdown(f"**{symbol}**")
        with cols[1]:
            st.markdown(f'<span class="{badge_class}">{badge_text}</span>', unsafe_allow_html=True)

        cols = st.columns(3)
        with cols[0]:
            st.metric("Prezzo", f"${price:,.2f}")
        with cols[1]:
            st.metric("Variazione", f"{change_icon} {abs(change):.2f}%")
        with cols[2]:
            st.metric("Score AI", f"{score:.0f}")

        st.caption(f"📊 Volume: {volume:,.0f}")

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"📊 Analizza {symbol}", key=f"btn_{symbol}", use_container_width=True):
                st.session_state.selected_asset = symbol
                st.session_state.radar_select = symbol
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
