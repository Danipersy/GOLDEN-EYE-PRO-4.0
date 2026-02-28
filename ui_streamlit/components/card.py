import streamlit as st

def render_result_card(result, on_click_key):
    """Renderizza una card risultato unificata"""
    
    level = result.get('level', 1)
    change = result.get('change', 0)
    score = result.get('score', 0)
    
    # Configurazione livelli
    level_config = {
        5: {"color": "#00ff88", "text": "🔥 FORTE", "bg": "#00ff8815"},
        4: {"color": "#f0b90b", "text": "🟡 MEDIO", "bg": "#f0b90b15"},
        3: {"color": "#3b82f6", "text": "📊 MOMENTUM", "bg": "#3b82f615"},
        2: {"color": "#8b5cf6", "text": "📈 TENDENZA", "bg": "#8b5cf615"},
        1: {"color": "#94a3b8", "text": "⚪ LATERALE", "bg": "#94a3b815"},
    }
    
    cfg = level_config.get(level, level_config[1])
    
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {cfg['bg']}, transparent);
        border-left: 8px solid {cfg['color']};
        border-radius: 20px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        position: relative;
        overflow: hidden;
    ">
        <div style="position: absolute; top: 0; right: 0; background: {cfg['color']}; padding: 5px 15px; border-radius: 0 20px 0 20px;">
            <span style="color: #000; font-weight: 700;">{cfg['text']}</span>
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div>
                <span style="font-size: 1.5rem; font-weight: 800; color: #fff;">{result['symbol']}</span>
                <div style="display: flex; gap: 20px; margin-top: 8px; flex-wrap: wrap;">
                    <span style="color: #94a3b8;">💰 Prezzo: <span style="color: #fff; font-weight: 600;">${result.get('price', 0):,.2f}</span></span>
                    <span style="color: #94a3b8;">📊 Volume: <span style="color: #fff; font-weight: 600;">{result.get('volume', 0):,.0f}</span></span>
                    <span style="color: #94a3b8;">🎯 Score: <span style="color: {cfg['color']}; font-weight: 700;">{score:.0f}</span></span>
                </div>
            </div>
            
            <div style="display: flex; gap: 15px; align-items: center;">
                <div style="text-align: right;">
                    <span style="color: #94a3b8; font-size: 0.8rem;">VARIAZIONE</span>
                    <div style="font-size: 1.8rem; font-weight: 800; color: {'#00ff88' if change > 0 else '#ff3344'};">
                        {change:+.2f}%
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <style>
        div[style*="border-left: 8px solid"]:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 30px {cfg['color']}40;
        }}
    </style>
    """, unsafe_allow_html=True)
