import streamlit as st
from datetime import datetime

def render_market_bar():
    """Renderizza la barra con orari e stati mercato"""
    
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    
    # Determina stati mercato
    # Crypto 24/7
    crypto_status = "APERTO 24/7"
    crypto_color = "#00ff88"
    
    # Azioni (9:30-16:00 ET, lun-ven)
    if weekday < 5 and 9 <= hour <= 16:
        stock_status = "APERTO"
        stock_color = "#00ff88"
        stock_icon = "📈"
    elif weekday < 5:
        stock_status = "CHIUSO"
        stock_color = "#ff3344"
        stock_icon = "📉"
    else:
        stock_status = "CHIUSO (WEEKEND)"
        stock_color = "#ff3344"
        stock_icon = "🔒"
    
    # Forex (24/5)
    if weekday < 5:
        forex_status = "APERTO"
        forex_color = "#00ff88"
        forex_icon = "💱"
    else:
        forex_status = "CHIUSO"
        forex_color = "#ff3344"
        forex_icon = "🔒"
    
    # Prezzi indici
    sp500 = "+0.8%"
    nasdaq = "+1.2%"
    dax = "-0.3%"
    
    # HTML della barra
    html = f'''
    <div class="market-bar">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 30px;">
            <!-- Ora e Data -->
            <div style="display: flex; align-items: center; gap: 30px;">
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem; text-transform: uppercase;">🕒 Ora Locale</div>
                    <div style="font-size: 2.2rem; font-weight: 800; color: #f0b90b; line-height: 1.2;">{now.strftime("%H:%M")}</div>
                    <div style="color: #94a3b8; font-size: 0.9rem;">{now.strftime("%d %b %Y")}</div>
                </div>
                
                <!-- Crypto -->
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem; text-transform: uppercase;">🪙 Crypto</div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">🪙</span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: {crypto_color};">{crypto_status}</span>
                    </div>
                </div>
                
                <!-- Azioni -->
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem; text-transform: uppercase;">📈 Azioni</div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">{stock_icon}</span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: {stock_color};">{stock_status}</span>
                    </div>
                </div>
                
                <!-- Forex -->
                <div>
                    <div style="color: #94a3b8; font-size: 0.7rem; text-transform: uppercase;">💱 Forex</div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.2rem;">{forex_icon}</span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: {forex_color};">{forex_status}</span>
                    </div>
                </div>
            </div>
            
            <!-- Indici in tempo reale -->
            <div style="display: flex; gap: 20px;">
                <div style="text-align: right;">
                    <div style="color: #94a3b8; font-size: 0.7rem;">S&P 500</div>
                    <div style="color: #00ff88; font-weight: 600;">{sp500}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #94a3b8; font-size: 0.7rem;">NASDAQ</div>
                    <div style="color: #00ff88; font-weight: 600;">{nasdaq}</div>
                </div>
                <div style="text-align: right;">
                    <div style="color: #94a3b8; font-size: 0.7rem;">DAX</div>
                    <div style="color: #ff3344; font-weight: 600;">{dax}</div>
                </div>
            </div>
        </div>
    </div>
    '''
    
    st.markdown(html, unsafe_allow_html=True)
