import streamlit as st
from datetime import datetime
from ui_streamlit.styles import apply_styles  # Importa gli stili

def get_market_status():
    """Determina stato mercati con grafica avanzata"""
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    
    # Cripto 24/7
    crypto_status = "APERTO 24/7"
    crypto_color = "#00ff88"
    crypto_icon = "🪙"
    
    # Mercati tradizionali
    if weekday < 5 and 9 <= hour <= 16:
        stock_status = "APERTO"
        stock_color = "#00ff88"
        stock_icon = "📈"
    elif weekday < 5:
        stock_status = "CHIUSO"
        stock_color = "#ff3344"
        stock_icon = "📉"
    else:
        stock_status = "CHIUSO (Weekend)"
        stock_color = "#ff3344"
        stock_icon = "🔒"
    
    # Forex
    if weekday < 5:
        forex_status = "APERTO"
        forex_color = "#00ff88"
        forex_icon = "💱"
    else:
        forex_status = "CHIUSO"
        forex_color = "#ff3344"
        forex_icon = "🔒"
    
    return {
        'crypto': {'status': crypto_status, 'color': crypto_color, 'icon': crypto_icon},
        'stocks': {'status': stock_status, 'color': stock_color, 'icon': stock_icon},
        'forex': {'status': forex_status, 'color': forex_color, 'icon': forex_icon}
    }

def render_header(page_title, page_icon):
    """Renderizza header unificato con grafica professionale"""
    
    # Applica gli stili globali (se non già applicati in App.py)
    # apply_styles()
    
    market = get_market_status()
    
    # TOP BAR con classi CSS
    st.markdown(f"""
    <div class="market-bar">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">
            <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                <!-- Ora -->
                <div class="market-item">
                    <span class="market-label">🕒 Ora</span>
                    <div style="font-size: 1.8rem; font-weight: 800; color: #f0b90b; line-height: 1.2;">
                        {datetime.now().strftime("%H:%M")}
                    </div>
                    <span style="color: #94a3b8; font-size: 0.8rem;">{datetime.now().strftime("%d %b %Y")}</span>
                </div>
                
                <!-- Crypto -->
                <div class="market-item">
                    <span class="market-label">🪙 Crypto</span>
                    <div class="market-value">
                        <span style="font-size: 1.2rem;">{market['crypto']['icon']}</span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: {market['crypto']['color']};">{market['crypto']['status']}</span>
                    </div>
                </div>
                
                <!-- Azioni -->
                <div class="market-item">
                    <span class="market-label">📈 Azioni</span>
                    <div class="market-value">
                        <span style="font-size: 1.2rem;">{market['stocks']['icon']}</span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: {market['stocks']['color']};">{market['stocks']['status']}</span>
                    </div>
                </div>
                
                <!-- Forex -->
                <div class="market-item">
                    <span class="market-label">💱 Forex</span>
                    <div class="market-value">
                        <span style="font-size: 1.2rem;">{market['forex']['icon']}</span>
                        <span style="font-size: 1.1rem; font-weight: 600; color: {market['forex']['color']};">{market['forex']['status']}</span>
                    </div>
                </div>
            </div>
            
            <!-- Badge versione -->
            <div class="badge" style="padding: 8px 20px;">
                <span style="color: #f0b90b; font-weight: 700;">⚡ GOLDEN EYE PRO 4.0</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # HEADER PAGINA
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <h1 class="text-gradient" style="font-size: 2.5rem;">{page_icon} {page_title}</h1>
            <div class="badge-green" style="padding: 4px 16px;">
                <span style="color: #00ff88; font-weight: 600;">LIVE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">📊 WATCHLIST</span>
            <div class="metric-value" style="color: #f0b90b;">{len(st.session_state.watchlist)}</div>
            <span style="color: #94a3b8; font-size: 0.7rem;">asset monitorati</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        last_scan = st.session_state.get('last_scan_time')
        if last_scan:
            time_diff = (datetime.now() - last_scan).seconds // 60
            scan_text = f"{time_diff} min fa" if time_diff < 60 else f"{time_diff//60} ore fa"
        else:
            scan_text = "Mai"
        
        st.markdown(f"""
        <div class="metric-card">
            <span class="metric-label">⏱️ ULTIMO SCAN</span>
            <div style="font-size: 1.3rem; font-weight: 700; color: #94a3b8;">{scan_text}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
