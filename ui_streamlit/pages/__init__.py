# ui_streamlit/pages/__init__.py
"""
Package pages - Contiene tutte le pagine dell'applicazione
"""

from ui_streamlit.pages.trading_view import render_trading_view

__all__ = [
    'render_trading_view',
]

print(f"✅ Pages package caricato")