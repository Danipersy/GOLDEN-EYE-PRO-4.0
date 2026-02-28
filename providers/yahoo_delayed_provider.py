# providers/yahoo_delayed_provider.py
import yfinance as yf
import pandas as pd
import time
import random
from datetime import datetime

# Coda per gestire le richieste
request_timestamps = []

def wait_for_rate_limit():
    """Aspetta il tempo necessario per non superare il rate limit"""
    global request_timestamps
    
    # Pulisci timestamp più vecchi di 60 secondi
    now = time.time()
    request_timestamps = [t for t in request_timestamps if now - t < 60]
    
    # Se abbiamo fatto più di 5 richieste nell'ultimo minuto, aspetta
    if len(request_timestamps) >= 5:
        wait_time = 60 - (now - request_timestamps[0]) + random.uniform(1, 3)
        print(f"⏳ Rate limit: aspetto {wait_time:.1f} secondi...")
        time.sleep(wait_time)
    
    # Aggiungi questa richiesta
    request_timestamps.append(time.time())

def fetch_yf_delayed(symbol, interval="15m", period="1mo", tail=None):
    """Fetch dati Yahoo con delay per evitare rate limit"""
    
    # Aspetta se necessario
    wait_for_rate_limit()
    
    try:
        print(f"📥 Yahoo: {symbol}...")
        
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df is None or df.empty:
            print(f"⚠️ Nessun dato per {symbol}")
            return None
        
        print(f"✅ {symbol}: {len(df)} candles")
        
        # Rinomina colonne
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        
        df = df.reset_index()
        df = df.rename(columns={'Datetime': 'datetime', 'Date': 'datetime'})
        
        if tail:
            df = df.tail(tail)
        
        return df
        
    except Exception as e:
        print(f"❌ Errore {symbol}: {e}")
        time.sleep(5)  # Attendi di più dopo un errore
        return None

def run_radar_scan_delayed(symbols, interval="15m", period="1mo"):
    """Esegue scansione con delay tra ogni richiesta"""
    results = []
    
    print(f"📡 Avvio scan per {len(symbols)} simboli...")
    
    for i, symbol in enumerate(symbols):
        print(f"\n📊 [{i+1}/{len(symbols)}] {symbol}")
        
        df = fetch_yf_delayed(symbol, interval, period)
        
        if df is not None and not df.empty:
            current_price = df['close'].iloc[-1]
            prev_price = df['close'].iloc[-2] if len(df) > 1 else current_price
            change = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
            
            avg_volume = df['volume'].tail(20).mean()
            current_volume = df['volume'].iloc[-1]
            
            results.append({
                'symbol': symbol,
                'price': current_price,
                'change': change,
                'volume': current_volume,
                'volume_ratio': current_volume / avg_volume if avg_volume > 0 else 1,
                'timestamp': datetime.now()
            })
            
            print(f"  ✅ ${current_price:.2f} ({change:.2f}%)")
        else:
            print(f"  ❌ Nessun dato")
            results.append({
                'symbol': symbol,
                'price': 0,
                'change': 0,
                'volume': 0,
                'volume_ratio': 0,
                'timestamp': datetime.now(),
                'error': 'No data'
            })
        
        # Delay FISSO tra le richieste (12 secondi = 5 al minuto)
        if i < len(symbols) - 1:  # Non dopo l'ultimo
            print(f"⏳ Attendo 12 secondi prima del prossimo...")
            time.sleep(12)
    
    return results

# ============================================
# FUNZIONI COMPATIBILI
# ============================================

def fetch_yf(symbol, interval="15m", period="1mo", tail=None):
    return fetch_yf_delayed(symbol, interval, period, tail)

def fetch_yf_ohlcv(symbol, interval="15m", period="1mo"):
    return fetch_yf_delayed(symbol, interval, period)

def run_radar_scan_yahoo(symbols, interval="15m", period="1mo"):
    return run_radar_scan_delayed(symbols, interval, period)

def test_connection():
    """Test veloce"""
    try:
        ticker = yf.Ticker("BTCUSDT")
        df = ticker.history(period="1d", interval="15m")
        return df is not None and not df.empty
    except:
        return False

# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("🔍 TEST YAHOO CON DELAY")
    print("="*60)
    
    symbols = ["BTCUSDT", "ETHUSDT"]
    results = run_radar_scan_delayed(symbols)
    
    for r in results:
        if 'error' in r:
            print(f"❌ {r['symbol']}: {r['error']}")
        else:
            print(f"✅ {r['symbol']}: ${r['price']:.2f} ({r['change']:.2f}%)")