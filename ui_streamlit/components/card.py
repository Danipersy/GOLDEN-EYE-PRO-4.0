import streamlit as st

def render_result_card(result, key):
    """Renderizza una card risultato con grafica professionale - SENZA DIV VISIBILI"""
    
    level = result.get('level', 1)
    change = result.get('change', 0)
    score = result.get('score', 0)
    symbol = result.get('symbol', 'N/A')
    price = result.get('price', 0)
    volume = result.get('volume', 0)
    
    # Configurazione livelli
    if level == 5:
        level_color = "#00ff88"
        level_text = "🔥 FORTE"
        level_bg = "#00ff8815"
    elif level == 4:
        level_color = "#f0b90b"
        level_text = "🟡 MEDIO"
        level_bg = "#f0b90b15"
    elif level == 3:
        level_color = "#3b82f6"
        level_text = "📊 MOMENTUM"
        level_bg = "#3b82f615"
    elif level == 2:
        level_color = "#8b5cf6"
        level_text = "📈 TENDENZA"
        level_bg = "#8b5cf615"
    else:
        level_color = "#94a3b8"
        level_text = "⚪ LATERALE"
        level_bg = "#94a3b815"
    
    # Determina colore variazione
    if change > 0:
        change_color = "#00ff88"
        change_icon = "▲"
    else:
        change_color = "#ff3344"
        change_icon = "▼"
    
    # Costruisci HTML della card - UNA SOLA STRINGA
    card_html = f'''
    <div style="
        background: linear-gradient(135deg, {level_bg}, transparent);
        border-left: 8px solid {level_color};
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    ">
        <!-- Badge livello -->
        <div style="
            position: absolute;
            top: 0;
            right: 0;
            background: {level_color};
            padding: 8px 24px;
            border-radius: 0 24px 0 24px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        ">
            <span style="color: #000; font-weight: 700; font-size: 0.9rem;">{level_text}</span>
        </div>
        
        <!-- Contenuto principale -->
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div>
                <span style="font-size: 1.8rem; font-weight: 800; color: #fff;">{symbol}</span>
                <div style="display: flex; gap: 25px; margin-top: 12px; flex-wrap: wrap;">
                    <div>
                        <span style="color: #94a3b8; font-size: 0.8rem;">💰 PREZZO</span>
                        <div style="font-size: 1.4rem; font-weight: 700; color: #fff;">${price:,.2f}</div>
                    </div>
                    <div>
                        <span style="color: #94a3b8; font-size: 0.8rem;">📊 VOLUME</span>
                        <div style="font-size: 1.2rem; font-weight: 600; color: #fff;">{volume:,.0f}</div>
                    </div>
                    <div>
                        <span style="color: #94a3b8; font-size: 0.8rem;">🎯 SCORE</span>
                        <div style="font-size: 1.4rem; font-weight: 700; color: {level_color};">{score:.0f}</div>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; gap: 20px; align-items: center;">
                <div style="text-align: right;">
                    <span style="color: #94a3b8; font-size: 0.8rem;">VARIAZIONE</span>
                    <div style="font-size: 2.2rem; font-weight: 800; color: {change_color};">
                        {change_icon} {abs(change):.2f}%
                    </div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    # Usa st.markdown per renderizzare l'HTML
    st.markdown(card_html, unsafe_allow_html=True)
