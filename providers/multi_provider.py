# providers/multi_provider.py
import yfinance as yf
import requests
import pandas as pd
import time
import streamlit as st
from datetime import datetime
from providers.base_provider import count_api_call

# Cache per evitare chiamate duplicate
_data_cache = {}
_cache_timestamp = {}

def get_api_keys():
    """Recupera chiavi API da st.secrets"""
    alpha_key = st.secrets.get("ALPHA_VANTAGE_KEY", "")
    td_key = st.secrets.get("TWELVEDATA_KEY", "")
    return alpha_key, td_key

def fetch_with_fallback(symbol, interval="15m", period="1mo"):
    """Prova più provider in sequenza"""
    
    # Controlla cache (5 minuti)
    cache_key = f"{symbol}_{interval}_{period}"
    if cache_key in _data_cache:
        cache_age = time.time() - _cache_timestamp.get(cache_key, 0)
        if cache_age < 300:  # 5 minuti
            return _data_cache[cache_key]
    
    # Prova Yahoo
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if not df.empty:
            df = df.rename(columns={
                'Open': 'open', 'High': 'high', 'Low': 'low',
                'Close': 'close', 'Volume': 'volume'
            })
            df = df.reset_index()
            df = df.rename(columns={'Datetime': 'datetime', 'Date': 'datetime'})
            
            # Salva in cache
            _data_cache[cache_key] = df
            _cache_timestamp[cache_key] = time.time()
            
            return df
    except Exception as e:
        pass
    
    return None

@count_api_call('yahoo', 'history')
def fetch_yahoo(symbol, interval="15m", period="1mo"):
    """Fetch dati da Yahoo Finance"""
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return None
        
        df = df.rename(columns={
            'Open': 'open', 'High': 'high', 'Low': 'low',
            'Close': 'close', 'Volume': 'volume'
        })
        df = df.reset_index()
        df = df.rename(columns={'Datetime': 'datetime', 'Date': 'datetime'})
        
        return df
    except Exception as e:
        print(f"Yahoo errore: {e}")
        return None

@count_api_call('alphavantage', 'time_series')
def fetch_alphavantage(symbol, interval="15m", period="1mo", api_key=None):
    """Fetch dati da Alpha Vantage"""
    if not api_key:
        return None
    
    try:
        interval_map = {
            "15m": "15min",
            "1h": "60min",
            "4h": "60min"
        }
        av_interval = interval_map.get(interval, "15min")
        
        url = "https://www.alphavantage.co/query"
        params = {
            "function": "TIME_SERIES_INTRADAY",
            "symbol": symbol.replace("USDT", "USD"),
            "interval": av_interval,
            "outputsize": "compact",
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        time_key = f"Time Series ({av_interval})"
        if time_key not in data:
            return None
        
        records = []
        for timestamp, values in list(data[time_key].items())[:500]:
            records.append({
                'datetime': pd.to_datetime(timestamp),
                'open': float(values['1. open']),
                'high': float(values['2. high']),
                'low': float(values['3. low']),
                'close': float(values['4. close']),
                'volume': int(values['5. volume'])
            })
        
        df = pd.DataFrame(records)
        df = df.sort_values('datetime')
        
        return df
        
    except Exception as e:
        print(f"Alpha Vantage errore: {e}")
        return None

@count_api_call('twelvedata', 'time_series')
def fetch_twelvedata(symbol, interval="15m", period="1mo", api_key=None):
    """Fetch dati da TwelveData"""
    if not api_key:
        return None
    
    try:
        interval_map = {
            "15m": "15min",
            "1h": "1h",
            "4h": "4h"
        }
        td_interval = interval_map.get(interval, "15min")
        
        url = "https://api.twelvedata.com/time_series"
        params = {
            "symbol": symbol,
            "interval": td_interval,
            "outputsize": 500,
            "apikey": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if "values" not in data:
            return None
        
        df = pd.DataFrame(data["values"])
        df = df.rename(columns={
            'datetime': 'datetime',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume'
        })
        
        for col in ['open', 'high', 'low', 'close', 'volume']:
            df[col] = pd.to_numeric(df[col])
        
        df = df.iloc[::-1].reset_index(drop=True)
        df['datetime'] = pd.to_datetime(df['datetime'])
        
        return df
        
    except Exception as e:
        print(f"TwelveData errore: {e}")
        return None

def scan_symbol(symbol, interval="15m", period="1mo"):
    """Scansione singolo simbolo"""
    alpha_key, td_key = get_api_keys()
    
    # Prova Yahoo prima
    df = fetch_yahoo(symbol, interval, period)
    
    # Se Yahoo fallisce, prova Alpha Vantage
    if df is None and alpha_key:
        df = fetch_alphavantage(symbol, interval, period, alpha_key)
    
    # Se Alpha Vantage fallisce, prova TwelveData
    if df is None and td_key:
        df = fetch_twelvedata(symbol, interval, period, td_key)
    
    if df is not None and not df.empty:
        current_price = df['close'].iloc[-1]
        prev_price = df['close'].iloc[-2] if len(df) > 1 else current_price
        change = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
        
        return {
            'symbol': symbol,
            'price': current_price,
            'change': change,
            'volume': df['volume'].iloc[-1],
            'timestamp': datetime.now()
        }
    
    return {
        'symbol': symbol,
        'price': 0,
        'change': 0,
        'volume': 0,
        'timestamp': datetime.now(),
        'error': 'No data'
    }

def fetch_yf(symbol, interval="15m", period="1mo", tail=None):
    """Compatibile con fetch_yf originale"""
    df = scan_symbol(symbol, interval, period)
    if df and 'error' not in df and tail and df.get('price'):
        # Questo è un placeholder - non abbiamo il dataframe completo
        return None
    return None  # Da migliorare

def fetch_yf_ohlcv(symbol, interval="15m", period="1mo"):
    """Compatibile con fetch_yf_ohlcv originale"""
    return scan_symbol(symbol, interval, period)

def run_radar_scan_yahoo(symbols, interval="15m", period="1mo"):
    """Esegue scansione radar"""
    results = []
    
    for symbol in symbols:
        result = scan_symbol(symbol, interval, period)
        results.append(result)
        time.sleep(1)  # Evita rate limiting
    
    return results