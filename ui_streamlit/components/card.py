import streamlit as st

def render_result_card(result):
    """Renderizza card risultato usando SOLO componenti Streamlit"""
    
    symbol = result.get('symbol', 'N/A')
    price = result.get('price', 0)
    change = result.get('change', 0)
    volume = result.get('volume', 0)
    level = result.get('level', 1)
    score = result.get('score', 0)
    
    # Determina badge in base al livello
    if level == 5:
        badge = "🔥 FORTE"
        badge_color = "#00ff88"
    elif level == 4:
        badge = "🟡 MEDIO"
        badge_color = "#f0b90b"
    elif level == 3:
        badge = "📊 MOMENTUM"
        badge_color = "#3b82f6"
    elif level == 2:
        badge = "📈 TENDENZA"
        badge_color = "#8b5cf6"
    else:
        badge = "⚪ LATERALE"
        badge_color = "#94a3b8"
    
    # Crea container con bordo colorato
    with st.container(border=True):
        cols = st.columns([1, 1, 1, 1])
        
        with cols[0]:
            st.markdown(f"**{symbol}**")
            st.caption(badge)
        
        with cols[1]:
            st.metric("Prezzo", f"${price:,.2f}")
        
        with cols[2]:
            delta = f"{change:+.2f}%"
            st.metric("Variazione", delta, delta_color="normal")
        
        with cols[3]:
            st.metric("Score AI", f"{score:.0f}")
        
        st.caption(f"📊 Volume: {volume:,.0f}")
