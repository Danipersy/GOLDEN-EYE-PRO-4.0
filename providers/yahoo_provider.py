# providers/yahoo_provider.py
# Wrapper per multi_provider

from providers.multi_provider import fetch_with_fallback, run_radar_scan

def fetch_yf(symbol, interval="15m", period="1mo", tail=None):
    """Compatibile con fetch_yf originale"""
    df = fetch_with_fallback(symbol, interval, period)
    if tail and df is not None:
        return df.tail(tail)
    return df

def fetch_yf_ohlcv(symbol, interval="15m", period="1mo"):
    return fetch_with_fallback(symbol, interval, period)

def run_radar_scan_yahoo(symbols, interval="15m", period="1mo"):
    """Compatibile con vecchio nome"""
    return run_radar_scan(symbols, interval, period)

__all__ = ['fetch_yf', 'fetch_yf_ohlcv', 'run_radar_scan_yahoo']