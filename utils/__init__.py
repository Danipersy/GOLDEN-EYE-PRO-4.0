# utils/__init__.py
"""
Utility package per Golden Eye Pro
Contiene funzioni di supporto, gestione errori e loader
"""

from utils.error_handler import error_handler, ErrorHandler
from utils.helpers import (
    convert_symbol_to_yfinance,
    http_session,
    normalize_ohlcv_df,
    get_market_status,
    pick_col_by_prefix,
    safe_last
)
from utils.lazy_loader import lazy, LazyLoader

__all__ = [
    # Error Handler
    'error_handler',
    'ErrorHandler',
    
    # Helpers
    'convert_symbol_to_yfinance',
    'http_session',
    'normalize_ohlcv_df',
    'get_market_status',
    'pick_col_by_prefix',
    'safe_last',
    
    # Lazy Loader
    'lazy',
    'LazyLoader'
]

print("✅ Utils package loaded")
