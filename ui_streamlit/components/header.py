import streamlit as st
from datetime import datetime

def get_market_status():
    """Determina stato mercati"""
    now = datetime.now()
    weekday = now.weekday()
    hour = now.hour
    
    # Cripto 24/7
    crypto_status = "🟢 APERTO 24/7"
    crypto_color = "#00ff88"
    
    # Mercati tradizionali (9:30-16:00 ET, lun-ven)
    if weekday < 5 and 9 <= hour <= 16:
        stock_status = "🟢 APERTO"
        stock_color = "#00ff88"
    elif weekday < 5:
        stock_status = "🔴 CHIUSO"
        stock_color = "#ff3344"
    else:
        stock_status = "🔴 CHIUSO (Weekend)"
        stock_color = "#ff3344"
    
    # Forex (24/5)
    if weekday < 5:
        forex_status = "🟢 APERTO"
        forex_color = "#00ff88"
    else:
        forex_status = "🔴 CHIUSO"
        forex_color = "#ff3344"
    
    return {
        'crypto': {'status': crypto_status, 'color': crypto_color},
        'stocks': {'status': stock_status, 'color': stock_color},
        'forex': {'status': forex_status, 'color': forex_color}
    }

def render_header(page_title, page_icon):
    """Renderizza header unificato per tutte le pagine"""
    
    market = get_market_status()
    
    # TOP BAR - STATO MERCATI E ORARI
    st.markdown(f"""
    <div style="
        background: linear-gradient(90deg, #1a1f2e, #16213e);
        border-radius: 16px;
        padding: 12px 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(240, 185, 11, 0.2);
        border-left: 5px solid #f0b90b;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    ">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
            <div style="display: flex; gap: 25px; flex-wrap: wrap;">
                <div>
                    <span style="color: #94a3b8; font-size: 0.8rem;">🕒 ORARIO</span>
                    <div style="font-size: 1.3rem; font-weight: 700; color: #f0b90b;">
                        {datetime.now().strftime("%H:%M:%S")}
                    </div>
                    <span style="color: #94a3b8; font-size: 0.7rem;">{datetime.now().strftime("%d/%m/%Y")}</span>
                </div>
                <div>
                    <span style="color: #94a3b8; font-size: 0.8rem;">📈 CRYPTO</span>
                    <div style="font-size: 1.1rem; font-weight: 600; color: {market['crypto']['color']};">
                        {market['crypto']['status']}
                    </div>
                </div>
                <div>
                    <span style="color: #94a3b8; font-size: 0.8rem;">📊 AZIONI</span>
                    <div style="font-size: 1.1rem; font-weight: 600; color: {market['stocks']['color']};">
                        {market['stocks']['status']}
                    </div>
                </div>
                <div>
                    <span style="color: #94a3b8; font-size: 0.8rem;">💱 FOREX</span>
                    <div style="font-size: 1.1rem; font-weight: 600; color: {market['forex']['color']};">
                        {market['forex']['status']}
                    </div>
                </div>
            </div>
            <div style="
                background: rgba(240, 185, 11, 0.1);
                border-radius: 30px;
                padding: 6px 15px;
                border: 1px solid rgba(240, 185, 11, 0.3);
            ">
                <span style="color: #f0b90b; font-weight: 600;">⚡ GOLDEN EYE PRO 4.0</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # HEADER PAGINA
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px;">
            <h1 style="margin:0; background: linear-gradient(135deg, #f0b90b, #fbbf24); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {page_icon} {page_title}
            </h1>
            <div style="
                background: linear-gradient(135deg, #00ff8820, #00ff8805);
                border: 1px solid #00ff88;
                border-radius: 20px;
                padding: 4px 12px;
            ">
                <span style="color: #00ff88; font-weight: 600;">LIVE</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="
            background: #1e1e2e;
            border-radius: 16px;
            padding: 12px;
            text-align: center;
            border: 1px solid #3c3c4a;
        ">
            <span style="color: #94a3b8; font-size: 0.7rem;">📊 WATCHLIST</span>
            <div style="font-size: 2rem; font-weight: 800; color: #f0b90b;">
                {len(st.session_state.watchlist)}
            </div>
            <span style="color: #94a3b8; font-size: 0.7rem;">asset monitorati</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        last_scan = st.session_state.get('last_scan_time')
        if last_scan:
            time_diff = (datetime.now() - last_scan).seconds // 60
            scan_text = f"{time_diff}m fa" if time_diff < 60 else f"{time_diff//60}h fa"
        else:
            scan_text = "Mai"
        
        st.markdown(f"""
        <div style="
            background: #1e1e2e;
            border-radius: 16px;
            padding: 12px;
            text-align: center;
            border: 1px solid #3c3c4a;
        ">
            <span style="color: #94a3b8; font-size: 0.7rem;">⏱️ ULTIMO SCAN</span>
            <div style="font-size: 1.2rem; font-weight: 600; color: #94a3b8;">
                {scan_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
