"""Pages package for Golden Eye Pro"""

import streamlit as st

# Importa tutte le funzioni dalle pagine
try:
    from ui_streamlit.pages.scan import show_page as show_scan
    from ui_streamlit.pages.dettaglio import show_page as show_dettaglio
    from ui_streamlit.pages.watchlist import show_page as show_watchlist
    from ui_streamlit.pages.validazione import render as render_validazione
    from ui_streamlit.pages.ottimizzazione import render as render_ottimizzazione
    from ui_streamlit.pages.money_management import render as render_money
    from ui_streamlit.pages.paper_trading import render as render_paper
    from ui_streamlit.pages.auto_trader import render as render_auto
    from ui_streamlit.pages.api_dashboard import render as render_api
    from ui_streamlit.pages.info import render as render_info
    from ui_streamlit.pages.settings import render as render_settings
    
    print("✅ Pagine importate con successo")
except ImportError as e:
    print(f"⚠️ Errore import pagine: {e}")

# Funzione principale richiesta da App.py
def render_main_view():
    """Vista principale"""
    current_page = st.session_state.get('current_page', 'SCAN')
    
    if current_page == "SCAN" and 'show_scan' in dir():
        show_scan()
    elif current_page == "DETTAGLIO" and 'show_dettaglio' in dir():
        asset = st.session_state.get('selected_asset', 'BTC-USD')
        show_dettaglio(asset)
    elif current_page == "WATCHLIST" and 'show_watchlist' in dir():
        show_watchlist()
    else:
        st.info(f"Pagina {current_page} in caricamento...")

# Dizionario per routing facile
PAGE_FUNCTIONS = {
    "SCAN": show_scan if 'show_scan' in dir() else None,
    "DETTAGLIO": show_dettaglio if 'show_dettaglio' in dir() else None,
    "WATCHLIST": show_watchlist if 'show_watchlist' in dir() else None,
    "VALIDAZIONE": render_validazione if 'render_validazione' in dir() else None,
    "OTTIMIZZAZIONE": render_ottimizzazione if 'render_ottimizzazione' in dir() else None,
    "MONEY": render_money if 'render_money' in dir() else None,
    "PAPER": render_paper if 'render_paper' in dir() else None,
    "AUTO": render_auto if 'render_auto' in dir() else None,
    "API": render_api if 'render_api' in dir() else None,
    "INFO": render_info if 'render_info' in dir() else None,
    "SETTINGS": render_settings if 'render_settings' in dir() else None,
}

# Esportazioni
__all__ = [
    'render_main_view',
    'show_scan', 'show_dettaglio', 'show_watchlist',
    'render_validazione', 'render_ottimizzazione', 'render_money',
    'render_paper', 'render_auto', 'render_api',
    'render_info', 'render_settings',
    'PAGE_FUNCTIONS'
]

print("✅ Pages package caricato - render_main_view disponibile")
