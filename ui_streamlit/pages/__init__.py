"""Pages package for Golden Eye Pro"""

from ui_streamlit.pages.scan import show_page as show_scan
from ui_streamlit.pages.dettaglio import show_page as show_dettaglio
from ui_streamlit.pages.watchlist import show_page as show_watchlist
from ui_streamlit.pages.validazione import render as render_validazione
from ui_streamlit.pages.ottimizzazione import render as render_ottimizzazione
from ui_streamlit.pages.money_management import render as render_money
from ui_streamlit.pages.paper_trading import render as render_paper
from ui_streamlit.pages.auto_trader import render as render_auto
from ui_streamlit.pages.info import render as render_info
from ui_streamlit.pages.settings import render as render_settings
from ui_streamlit.pages.test import render as render_test

__all__ = [
    'show_scan', 'show_dettaglio', 'show_watchlist',
    'render_validazione', 'render_ottimizzazione', 'render_money',
    'render_paper', 'render_auto', 'render_info', 'render_settings',
    'render_test'
]
