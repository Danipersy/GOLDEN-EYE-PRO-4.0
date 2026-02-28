import streamlit as st

def render_result_card(result, key=None):  # key è opzionale
    """Renderizza una card risultato"""
    
    # Estrai dati
    symbol = result.get('symbol', 'N/A')
    price = result.get('price', 0)
    change = result.get('change', 0)
    volume = result.get('volume', 0)
    level = result.get('level', 1)
    score = result.get('score', 0)
    
    # Configurazione livello
    if level == 5:
        color = "#00ff88"
        badge = "🔥 FORTE"
    elif level == 4:
        color = "#f0b90b"
        badge = "🟡 MEDIO"
    elif level == 3:
        color = "#3b82f6"
        badge = "📊 MOMENTUM"
    elif level == 2:
        color = "#8b5cf6"
        badge = "📈 TENDENZA"
    else:
        color = "#94a3b8"
        badge = "⚪ LATERALE"
    
    # Colore variazione
    change_color = "#00ff88" if change > 0 else "#ff3344"
    change_icon = "▲" if change > 0 else "▼"
    
    # Crea container Streamlit
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        
        with col1:
            st.markdown(f"**{symbol}**")
            st.caption(badge)
        
        with col2:
            st.metric("Prezzo", f"${price:,.2f}")
        
        with col3:
            st.metric("Variazione", f"{change:+.2f}%", delta_color="off")
        
        with col4:
            st.metric("Score", f"{score:.0f}")
        
        st.caption(f"📊 Volume: {volume:,.0f}")
        st.divider()
