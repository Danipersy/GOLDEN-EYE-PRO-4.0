import streamlit as st

def render_result_card(result):
    """Renderizza card risultato in versione PRO"""
    
    symbol = result.get('symbol', 'N/A')
    price = result.get('price', 0)
    change = result.get('change', 0)
    volume = result.get('volume', 0)
    level = result.get('level', 1)
    score = result.get('score', 0)
    
    # Configurazione badge livello
    level_config = {
        5: {"color": "#00ff88", "bg": "rgba(0, 255, 136, 0.1)", "text": "🔥 FORTE", "border": "#00ff88"},
        4: {"color": "#f0b90b", "bg": "rgba(240, 185, 11, 0.1)", "text": "🟡 MEDIO", "border": "#f0b90b"},
        3: {"color": "#3b82f6", "bg": "rgba(59, 130, 246, 0.1)", "text": "📊 MOMENTUM", "border": "#3b82f6"},
        2: {"color": "#8b5cf6", "bg": "rgba(139, 92, 246, 0.1)", "text": "📈 TENDENZA", "border": "#8b5cf6"},
        1: {"color": "#94a3b8", "bg": "rgba(148, 163, 184, 0.1)", "text": "⚪ LATERALE", "border": "#94a3b8"},
    }
    
    cfg = level_config.get(level, level_config[1])
    
    # Determina colore variazione
    if change > 0:
        change_color = "#00ff88"
        change_icon = "▲"
        change_text = f"+{change:.2f}%"
    else:
        change_color = "#ff3344"
        change_icon = "▼"
        change_text = f"{change:.2f}%"
    
    # Usa container con stile personalizzato
    with st.container():
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {cfg['bg']}, rgba(26, 31, 58, 0.8));
            border-left: 6px solid {cfg['color']};
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            transition: transform 0.3s ease;
            position: relative;
            overflow: hidden;
        ">
            <div style="position: absolute; top: 10px; right: 20px;">
                <span style="
                    background: {cfg['color']};
                    color: #000;
                    padding: 4px 16px;
                    border-radius: 30px;
                    font-size: 0.8rem;
                    font-weight: 700;
                ">{cfg['text']}</span>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="font-size: 1.8rem; font-weight: 700; color: #fff;">{symbol}</span>
                    <div style="display: flex; gap: 30px; margin-top: 15px;">
                        <div>
                            <span style="color: #94a3b8; font-size: 0.7rem;">PREZZO</span>
                            <div style="font-size: 1.5rem; font-weight: 700; color: #fff;">${price:,.2f}</div>
                        </div>
                        <div>
                            <span style="color: #94a3b8; font-size: 0.7rem;">VOLUME</span>
                            <div style="font-size: 1.2rem; font-weight: 600; color: #fff;">{volume:,.0f}</div>
                        </div>
                        <div>
                            <span style="color: #94a3b8; font-size: 0.7rem;">SCORE AI</span>
                            <div style="font-size: 1.5rem; font-weight: 700; color: {cfg['color']};">{score:.0f}</div>
                        </div>
                    </div>
                </div>
                
                <div style="text-align: right;">
                    <span style="color: #94a3b8; font-size: 0.7rem;">VARIAZIONE 24h</span>
                    <div style="font-size: 2rem; font-weight: 800; color: {change_color};">
                        {change_icon} {abs(change):.2f}%
                    </div>
                </div>
            </div>
        </div>
        
        <style>
            div[style*="border-left: 6px solid"]:hover {{
                transform: translateY(-5px) scale(1.02);
                box-shadow: 0 20px 40px {cfg['color']}40;
            }}
        </style>
        """, unsafe_allow_html=True)
        
        # Bottone analisi separato
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(f"📊 ANALIZZA {symbol}", key=f"btn_{symbol}", use_container_width=True):
                st.session_state.selected_asset = symbol
                st.session_state.radar_select = symbol
                st.session_state.current_page = "DETTAGLIO"
                st.rerun()
