import streamlit as st
from datetime import datetime

def render_header(page_title, page_icon):
    """Renderizza solo le informazioni di mercato (NON il menu)"""
    
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    
    # Determina stati
    crypto_status = "APERTO 24/7"
    crypto_color = "#00ff88"
    
    if weekday < 5 and 9 <= hour <= 16:
        stock_status = "APERTO"
        stock_color = "#00ff88"
    else:
        stock_status = "CHIUSO" + (" (Weekend)" if weekday >= 5 else "")
        stock_color = "#ff3344"
    
    if weekday < 5:
        forex_status = "APERTO"
        forex_color = "#00ff88"
    else:
        forex_status = "CHIUSO"
        forex_color = "#ff3344"
    
    # HTML info mercato
    html = f'''
    <div style="background: rgba(26, 31, 46, 0.8); border-radius: 20px; padding: 16px 24px; margin-bottom: 24px; border: 1px solid rgba(240, 185, 11, 0.2); border-left: 6px solid #f0b90b;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                <div>
                    <div style="color: #94a3b8; font-size: 0.75rem;">🕒 Ora</div>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #f0b90b;">{now.strftime("%H:%M")}</div>
                    <div style="color: #94a3b8; font-size: 0.8rem;">{now.strftime("%d %b %Y")}</div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.75rem;">🪙 Crypto</div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span>🪙</span>
                        <span style="font-weight: 600; color: {crypto_color};">{crypto_status}</span>
                    </div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.75rem;">📈 Azioni</div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span>{"📈" if "APERTO" in stock_status else "🔒"}</span>
                        <span style="font-weight: 600; color: {stock_color};">{stock_status}</span>
                    </div>
                </div>
                <div>
                    <div style="color: #94a3b8; font-size: 0.75rem;">💱 Forex</div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span>{"💱" if "APERTO" in forex_status else "🔒"}</span>
                        <span style="font-weight: 600; color: {forex_color};">{forex_status}</span>
                    </div>
                </div>
            </div>
            <div style="background: linear-gradient(135deg, #f0b90b20, #f0b90b05); border: 1px solid #f0b90b; border-radius: 40px; padding: 8px 20px;">
                <span style="color: #f0b90b; font-weight: 700;">⚡ GOLDEN EYE PRO 4.0</span>
            </div>
        </div>
    </div>
    
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
        <h1 style="margin:0; font-size: 2.5rem; background: linear-gradient(135deg, #fff, #f0f6fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            {page_icon} {page_title}
        </h1>
        <div style="background: linear-gradient(135deg, #00ff8820, #00ff8805); border: 1px solid #00ff88; border-radius: 30px; padding: 4px 16px;">
            <span style="color: #00ff88; font-weight: 600;">LIVE</span>
        </div>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)
