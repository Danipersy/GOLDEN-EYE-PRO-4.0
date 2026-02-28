# providers/multi_provider.py
import yfinance as yf
import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from config import ALPHA_VANTAGE_KEY, TWELVEDATA_KEY

# Cache per evitare chiamate duplicate
_data_cache = {}
_cache_timestamp = {}

def fetch_with_fallback(symbol, interval="15m", period="1mo"):
    """
    Prova più provider in sequenza fino a ottenere dati
    """
    
    # Controlla cache (5 minuti)
    cache_key = f"{symbol}_{interval}_{period}"
    if cache_key in _data_cache:
        cache_age = time.time() - _cache_timestamp.get(cache_key, 0)
        if cache_age < 300:  # 5 minuti
            print(f"📦 Usando cache per {symbol}")
            return _data_cache[cache_key]
    
    # Lista provider in ordine di preferenza
    providers = [
        ("yahoo", fetch_yahoo),
        ("alphavantage", fetch_alphavantage),
        ("twelvedata", fetch_twelvedata)
    ]
    
    for provider_name, provider_func in providers:
        print(f"🔄 Tentativo {provider_name} per {symbol}...")
        
        try:
            df = provider_func(symbol, interval, period)
            
            if df is not None and len(df) >= 30:  # Almeno 30 candles
                print(f"✅ {provider_name} successo: {len(df)} candles")
                
                # Salva in cache
                _data_cache[cache_key] = df
                _cache_timestamp[cache_key] = time.time()
                
                return df
                
        except Exception as e:
            print(f"⚠️ {provider_name} fallito: {e}")
            continue
    
    print(f"❌ Tutti i provider falliti per {symbol}")
    return None

# ============================================
# PROVIDER 1: YAHOO
# ============================================
def fetch_yahoo(symbol, interval="15m", period="1mo"):
    """Yahoo Finance"""
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

# ============================================
# PROVIDER 2: ALPHA VANTAGE
# ============================================
def fetch_alphavantage(symbol, interval="15m", period="1mo"):
    """Alpha Vantage API"""
    
    if not ALPHA_VANTAGE_KEY:
        print("⚠️ Alpha Vantage KEY mancante")
        return None
    
    try:
        # Mappa intervalli
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
            "apikey": ALPHA_VANTAGE_KEY
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

# ============================================
# PROVIDER 3: TWELVEDATA
# ============================================
def fetch_twelvedata(symbol, interval="15m", period="1mo"):
    """TwelveData API"""
    
    if not TWELVEDATA_KEY:
        print("⚠️ TwelveData KEY mancante")
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
            "apikey": TWELVEDATA_KEY
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

# ============================================
# FUNZIONI SCAN
# ============================================
def run_radar_scan(symbols, interval="15m", period="1mo"):
    """Esegue scansione radar con multi-provider"""
    results = []
    
    for i, symbol in enumerate(symbols):
        print(f"\n📡 [{i+1}/{len(symbols)}] {symbol}")
        
        df = fetch_with_fallback(symbol, interval, period)
        
        if df is not None and not df.empty:
            current_price = df['close'].iloc[-1]
            prev_price = df['close'].iloc[-2] if len(df) > 1 else current_price
            change = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
            
            results.append({
                'symbol': symbol,
                'price': current_price,
                'change': change,
                'volume': df['volume'].iloc[-1],
                'timestamp': datetime.now()
            })
            print(f"  ✅ ${current_price:.2f}")
        else:
            print(f"  ❌ Nessun dato per {symbol}")
        
        time.sleep(1)
    
    return results

# ============================================
# FUNZIONI COMPATIBILI CON IL TUO CODICE
# ============================================

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

# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("🔍 TEST MULTI-PROVIDER")
    print("="*60)
    
    symbols = ["BTCUSDT", "ETHUSDT"]
    results = run_radar_scan(symbols)
    
    for r in results:
        print(f"✅ {r['symbol']}: ${r['price']:.2f} ({r['change']:.2f}%)")