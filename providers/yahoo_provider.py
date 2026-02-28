# providers/yahoo_provider.py
# Wrapper per multi_provider

from providers.multi_provider import (
    fetch_yf as multi_fetch_yf,
    fetch_yf_ohlcv as multi_fetch_ohlcv,
    run_radar_scan_yahoo as multi_run_scan
)

def fetch_yf(symbol, interval="15m", period="1mo", tail=None):
    """Compatibile con fetch_yf originale"""
    return multi_fetch_yf(symbol, interval, period, tail)

def fetch_yf_ohlcv(symbol, interval="15m", period="1mo"):
    return multi_fetch_ohlcv(symbol, interval, period)

def run_radar_scan_yahoo(symbols, interval="15m", period="1mo"):
    """Compatibile con vecchio nome"""
    return multi_run_scan(symbols, interval, period)

__all__ = ['fetch_yf', 'fetch_yf_ohlcv', 'run_radar_scan_yahoo']
