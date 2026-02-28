# test_indipendente.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import sys

print("="*60)
print("🚀 TEST INDIPENDENTE")
print("="*60)

# Verifica pandas_ta
try:
    import pandas_ta as ta
    print(f"✅ pandas_ta {ta.__version__} installato")
    PANDAS_TA_OK = True
except ImportError:
    print("❌ pandas_ta NON installato")
    PANDAS_TA_OK = False
    sys.exit(1)

# Funzione per calcolare indicatori (copia da robust_ta.py)
def compute_indicators_simple(df_15m):
    """Calcola indicatori (versione semplificata)"""
    df = df_15m.copy()
    
    # EMA
    df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

    # RSI con pandas_ta
    df["rsi"] = ta.rsi(df["close"], length=14)
    
    # ATR con pandas_ta
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)

    # ADX con pandas_ta
    adx_df = ta.adx(df["high"], df["low"], df["close"], length=14)
    if isinstance(adx_df, pd.DataFrame) and not adx_df.empty:
        df = df.join(adx_df)

    return df

# Genera dati di test
print("\n📊 Generazione dati...")
dates = pd.date_range(start='2024-01-01', periods=500, freq='15min')
df = pd.DataFrame({
    'datetime': dates,
    'open': np.random.normal(50000, 100, 500),
    'high': np.random.normal(50100, 100, 500),
    'low': np.random.normal(49900, 100, 500),
    'close': np.random.normal(50000, 100, 500),
    'volume': np.random.randint(100, 1000, 500)
})
print(f"✅ Generati {len(df)} candles")

# Calcola indicatori
print("\n📈 Calcolo indicatori...")
df_ind = compute_indicators_simple(df)
print(f"✅ Colonne: {list(df_ind.columns)}")
print(f"✅ RSI ultimo: {df_ind['rsi'].iloc[-1]:.2f}")
print(f"✅ ATR ultimo: {df_ind['atr'].iloc[-1]:.2f}")

print("\n" + "="*60)
print("✅✅✅ TEST SUPERATO ✅✅✅")
print("="*60)