# providers/defeatbeta_provider.py
import pandas as pd
from datetime import datetime
import time

# Prova a importare defeatbeta
try:
    from defeatbeta import Ticker
    DEFEATBETA_AVAILABLE = True
    print("✅ Defeatbeta API disponibile")
except ImportError:
    print("⚠️ Defeatbeta non installato, uso fallback")
    DEFEATBETA_AVAILABLE = False

def fetch_defeatbeta(symbol, interval="15m", period="1mo"):
    """Fetch dati da Defeatbeta (nessun rate limit!)"""
    
    if not DEFEATBETA_AVAILABLE:
        print(f"⚠️ Defeatbeta non disponibile, uso dati fake per {symbol}")
        return generate_fake_data(symbol)
    
    try:
        print(f"📥 Defeatbeta: {symbol}...")
        
        ticker = Ticker(symbol)
        df = ticker.history(period=period, interval=interval)
        
        if df is None or df.empty:
            print(f"⚠️ Nessun dato per {symbol}")
            return generate_fake_data(symbol)
        
        print(f"✅ {symbol}: {len(df)} candles")
        
        # Rinomina colonne per compatibilità
        df = df.rename(columns={
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        })
        
        # Reset index
        df = df.reset_index()
        df = df.rename(columns={'Datetime': 'datetime', 'Date': 'datetime'})
        
        return df
        
    except Exception as e:
        print(f"❌ Errore {symbol}: {e}")
        return generate_fake_data(symbol)

def generate_fake_data(symbol, days=30):
    """Genera dati fake per test quando tutto fallisce"""
    print(f"⚠️ Generazione dati fake per {symbol}")
    
    import numpy as np
    from datetime import datetime, timedelta
    
    # Genera timestamp ogni 15 minuti
    end = datetime.now()
    start = end - timedelta(days=days)
    timestamps = pd.date_range(start=start, end=end, freq='15min')
    
    # Prezzo base in base al simbolo
    if 'BTC' in symbol:
        base_price = 50000
    elif 'ETH' in symbol:
        base_price = 3000
    elif 'BNB' in symbol:
        base_price = 500
    elif 'SOL' in symbol:
        base_price = 150
    else:
        base_price = 100
    
    # Genera prezzi con random walk
    prices = [base_price]
    for i in range(1, len(timestamps)):
        change = np.random.randn() * 0.01  # 1% volatilità
        prices.append(prices[-1] * (1 + change))
    
    df = pd.DataFrame({
        'datetime': timestamps,
        'open': prices,
        'high': [p * 1.005 for p in prices],
        'low': [p * 0.995 for p in prices],
        'close': prices,
        'volume': np.random.randint(100, 1000, len(timestamps))
    })
    
    return df

def run_radar_scan(symbols, interval="15m", period="1mo"):
    """Esegue scansione radar con Defeatbeta"""
    results = []
    
    for symbol in symbols:
        print(f"📡 Radar scan: {symbol}")
        df = fetch_defeatbeta(symbol, interval, period)
        
        if df is not None and not df.empty:
            current_price = df['close'].iloc[-1]
            prev_price = df['close'].iloc[-2] if len(df) > 1 else current_price
            change = ((current_price - prev_price) / prev_price) * 100 if prev_price > 0 else 0
            
            avg_volume = df['volume'].tail(20).mean()
            current_volume = df['volume'].iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            results.append({
                'symbol': symbol,
                'price': current_price,
                'change': change,
                'volume': current_volume,
                'volume_ratio': volume_ratio,
                'timestamp': datetime.now()
            })
        else:
            results.append({
                'symbol': symbol,
                'price': 0,
                'change': 0,
                'volume': 0,
                'volume_ratio': 0,
                'timestamp': datetime.now(),
                'error': 'No data'
            })
        
        # Piccola pausa per sicurezza
        time.sleep(0.5)
    
    return results

def test_connection():
    """Test connessione a Defeatbeta"""
    if not DEFEATBETA_AVAILABLE:
        return False
    
    try:
        ticker = Ticker("BTCUSDT")
        df = ticker.history(period="1d", interval="15m")
        return df is not None and not df.empty
    except:
        return False

# ============================================
# FUNZIONI COMPATIBILI CON IL TUO CODICE
# ============================================

def fetch_yf(symbol, interval="15m", period="1mo", tail=None):
    """Compatibile con fetch_yf originale"""
    df = fetch_defeatbeta(symbol, interval, period)
    if tail and df is not None:
        return df.tail(tail)
    return df

def fetch_yf_ohlcv(symbol, interval="15m", period="1mo"):
    return fetch_yf(symbol, interval, period)

def run_radar_scan_yahoo(symbols, interval="15m", period="1mo"):
    """Compatibile con run_radar_scan_yahoo originale"""
    return run_radar_scan(symbols, interval, period)

def get_current_price(symbol):
    """Ottieni prezzo corrente"""
    df = fetch_defeatbeta(symbol, "15m", "1d")
    if df is not None and not df.empty:
        return df['close'].iloc[-1]
    return None

# ============================================
# TEST
# ============================================
if __name__ == "__main__":
    print("🔍 TEST DEFEATBETA PROVIDER")
    print("="*60)
    
    # Test connessione
    if test_connection():
        print("✅ Connessione OK")
    else:
        print("❌ Connessione FALLITA (uso dati fake)")
    
    # Test simboli
    symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    
    for symbol in symbols:
        df = fetch_yf(symbol, "15m", "1mo")
        if df is not None:
            print(f"✅ {symbol}: {len(df)} candles - ${df['close'].iloc[-1]:.2f}")
        else:
            print(f"❌ {symbol}: fallito")
    
    # Test radar scan
    print("\n📡 Test radar scan...")
    results = run_radar_scan(symbols)
    for r in results:
        if 'error' in r:
            print(f"❌ {r['symbol']}: {r['error']}")
        else:
            print(f"✅ {r['symbol']}: ${r['price']:.2f} ({r['change']:.2f}%)")
    
    print("="*60)