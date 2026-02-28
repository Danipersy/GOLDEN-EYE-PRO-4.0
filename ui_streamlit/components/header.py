import streamlit as st
from datetime import datetime

def get_market_status():
    """Determina stato mercati"""
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
    """Renderizza header unificato"""
    
    market = get_market_status()
    
    # TOP BAR - COSTRUITA CON STRINGHE SEMPLICI
    html = '<div style="background: rgba(26, 31, 46, 0.8); backdrop-filter: blur(10px); border-radius: 20px; padding: 16px 24px; margin-bottom: 24px; border: 1px solid rgba(240, 185, 11, 0.2); border-left: 6px solid #f0b90b; box-shadow: 0 8px 32px rgba(0,0,0,0.3);">'
    html += '<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 20px;">'
    html += '<div style="display: flex; gap: 30px; flex-wrap: wrap;">'
    
    # Ora
    html += '<div>'
    html += '<div style="color: #94a3b8; font-size: 0.75rem;">🕒 Ora</div>'
    html += f'<div style="font-size: 1.8rem; font-weight: 800; color: #f0b90b;">{datetime.now().strftime("%H:%M")}</div>'
    html += f'<div style="color: #94a3b8; font-size: 0.8rem;">{datetime.now().strftime("%d %b %Y")}</div>'
    html += '</div>'
    
    # Crypto
    html += '<div>'
    html += '<div style="color: #94a3b8; font-size: 0.75rem;">🪙 Crypto</div>'
    html += '<div style="display: flex; align-items: center; gap: 8px;">'
    html += f'<span>{market["crypto"]["icon"]}</span>'
    html += f'<span style="font-weight: 600; color: {market["crypto"]["color"]};">{market["crypto"]["status"]}</span>'
    html += '</div></div>'
    
    # Azioni
    html += '<div>'
    html += '<div style="color: #94a3b8; font-size: 0.75rem;">📈 Azioni</div>'
    html += '<div style="display: flex; align-items: center; gap: 8px;">'
    html += f'<span>{market["stocks"]["icon"]}</span>'
    html += f'<span style="font-weight: 600; color: {market["stocks"]["color"]};">{market["stocks"]["status"]}</span>'
    html += '</div></div>'
    
    # Forex
    html += '<div>'
    html += '<div style="color: #94a3b8; font-size: 0.75rem;">💱 Forex</div>'
    html += '<div style="display: flex; align-items: center; gap: 8px;">'
    html += f'<span>{market["forex"]["icon"]}</span>'
    html += f'<span style="font-weight: 600; color: {market["forex"]["color"]};">{market["forex"]["status"]}</span>'
    html += '</div></div>'
    
    html += '</div>'  # Chiudi flex interno
    
    # Badge versione
    html += '<div style="background: linear-gradient(135deg, #f0b90b20, #f0b90b05); border: 1px solid #f0b90b; border-radius: 40px; padding: 8px 20px;">'
    html += '<span style="color: #f0b90b; font-weight: 700;">⚡ GOLDEN EYE PRO 4.0</span>'
    html += '</div>'
    
    html += '</div></div>'  # Chiudi container principale
    
    # QUESTO È FONDAMENTALE - usa st.markdown
    st.markdown(html, unsafe_allow_html=True)
    
    # HEADER PAGINA
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        title_html = '<div style="display: flex; align-items: center; gap: 15px;">'
        title_html += f'<h1 style="margin:0; font-size: 2.5rem; background: linear-gradient(135deg, #fff, #f0f6fc); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{page_icon} {page_title}</h1>'
        title_html += '<div style="background: linear-gradient(135deg, #00ff8820, #00ff8805); border: 1px solid #00ff88; border-radius: 30px; padding: 4px 16px;">'
        title_html += '<span style="color: #00ff88; font-weight: 600;">LIVE</span>'
        title_html += '</div></div>'
        st.markdown(title_html, unsafe_allow_html=True)
    
    with col2:
        watchlist_html = '<div style="background: linear-gradient(135deg, #1e1e2e, #1a1a2a); border-radius: 16px; padding: 16px; border: 1px solid #3c3c4a; text-align: center;">'
        watchlist_html += '<div style="color: #94a3b8; font-size: 0.8rem;">📊 WATCHLIST</div>'
        watchlist_html += f'<div style="font-size: 2.2rem; font-weight: 800; color: #f0b90b;">{len(st.session_state.watchlist)}</div>'
        watchlist_html += '</div>'
        st.markdown(watchlist_html, unsafe_allow_html=True)
    
    with col3:
        last_scan = st.session_state.get('last_scan_time')
        if last_scan:
            time_diff = (datetime.now() - last_scan).seconds // 60
            scan_text = f"{time_diff} min fa" if time_diff < 60 else f"{time_diff//60} ore fa"
        else:
            scan_text = "Mai"
        
        scan_html = '<div style="background: linear-gradient(135deg, #1e1e2e, #1a1a2a); border-radius: 16px; padding: 16px; border: 1px solid #3c3c4a; text-align: center;">'
        scan_html += '<div style="color: #94a3b8; font-size: 0.8rem;">⏱️ ULTIMO SCAN</div>'
        scan_html += f'<div style="font-size: 1.3rem; font-weight: 700; color: #94a3b8;">{scan_text}</div>'
        scan_html += '</div>'
        st.markdown(scan_html, unsafe_allow_html=True)
    
    st.markdown("---")
