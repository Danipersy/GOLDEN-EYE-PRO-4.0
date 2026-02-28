# ui_streamlit/pages/__init__.py
"""Pages package for Golden Eye Pro"""

# Importa tutte le funzioni dalle pagine
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

# Dizionario per il routing facile
PAGE_FUNCTIONS = {
    "SCAN": show_scan,
    "DETTAGLIO": show_dettaglio,
    "WATCHLIST": show_watchlist,
    "VALIDAZIONE": render_validazione,
    "OTTIMIZZAZIONE": render_ottimizzazione,
    "MONEY": render_money,
    "PAPER": render_paper,
    "AUTO": render_auto,
    "API": render_api,
    "INFO": render_info,
    "SETTINGS": render_settings,
}

# Esponi tutto
__all__ = list(PAGE_FUNCTIONS.keys()) + ['PAGE_FUNCTIONS']

print("✅ Pages package loaded with functions:", list(PAGE_FUNCTIONS.keys()))
