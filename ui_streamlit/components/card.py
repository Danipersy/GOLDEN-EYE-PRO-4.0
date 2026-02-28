import streamlit as st

def render_result_card(result, key):
    """Renderizza una card risultato con grafica professionale"""
    
    level = result.get('level', 1)
    change = result.get('change', 0)
    score = result.get('score', 0)
    
    # Configurazione livelli
    level_config = {
        5: {
            "color": "#00ff88",
            "text": "🔥 FORTE",
            "bg": "linear-gradient(135deg, #00ff8815, #00ff8805)",
        },
        4: {
            "color": "#f0b90b",
            "text": "🟡 MEDIO",
            "bg": "linear-gradient(135deg, #f0b90b15, #f0b90b05)",
        },
        3: {
            "color": "#3b82f6",
            "text": "📊 MOMENTUM",
            "bg": "linear-gradient(135deg, #3b82f615, #3b82f605)",
        },
        2: {
            "color": "#8b5cf6",
            "text": "📈 TENDENZA",
            "bg": "linear-gradient(135deg, #8b5cf615, #8b5cf605)",
        },
        1: {
            "color": "#94a3b8",
            "text": "⚪ LATERALE",
            "bg": "linear-gradient(135deg, #94a3b815, #94a3b805)",
        },
    }
    
    cfg = level_config.get(level, level_config[1])
    
    # Determina colore variazione
    change_color = "#00ff88" if change > 0 else "#ff3344"
    change_icon = "▲" if change > 0 else "▼"
    
    card_html = f"""
    <div style="
        background: {cfg['bg']};
        border-left: 8px solid {cfg['color']};
        border-radius: 24px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    ">
        <!-- Badge livello -->
        <div style="
            position: absolute;
            top: 0;
            right: 0;
            background: {cfg['color']};
            padding: 8px 24px;
            border-radius: 0 24px 0 24px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        ">
            <span style="color: #000; font-weight: 700; font-size: 0.9rem;">{cfg['text']}</span>
        </div>
        
        <!-- Contenuto principale -->
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div>
                <span style="font-size: 1.8rem; font-weight: 800; color: #fff;">{result['symbol']}</span>
                <div style="display: flex; gap: 25px; margin-top: 12px; flex-wrap: wrap;">
                    <div>
                        <span style="color: #94a3b8; font-size: 0.8rem;">💰 PREZZO</span>
                        <div style="font-size: 1.4rem; font-weight: 700; color: #fff;">${result.get('price', 0):,.2f}</div>
                    </div>
                    <div>
                        <span style="color: #94a3b8; font-size: 0.8rem;">📊 VOLUME</span>
                        <div style="font-size: 1.2rem; font-weight: 600; color: #fff;">{result.get('volume', 0):,.0f}</div>
                    </div>
                    <div>
                        <span style="color: #94a3b8; font-size: 0.8rem;">🎯 SCORE</span>
                        <div style="font-size: 1.4rem; font-weight: 700; color: {cfg['color']};">{score:.0f}</div>
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
        
        <!-- Hover effect overlay (CORRETTO) -->
        <div style="
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, transparent, rgba(255,255,255,0.05));
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
        "></div>
    </div>
    
    <style>
        div[style*="border-left: 8px solid"]:hover {{
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0 15px 30px {cfg['color']}40;
        }}
        div[style*="border-left: 8px solid"]:hover div[style*="pointer-events: none"] {{
            opacity: 1;
        }}
    </style>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)
    
