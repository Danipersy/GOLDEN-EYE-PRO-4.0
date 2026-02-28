# test_twelvedata.py
import streamlit as st
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h

print("🔍 TEST TWELVEDATA")
print("="*60)

# Leggi chiave
td_key = st.secrets.get("TWELVEDATA_KEY", "")
print(f"📌 TwelveData KEY: {'✅ Presente' if td_key else '❌ MANCANTE'}")
if td_key:
    print(f"   Inizia con: {td_key[:4]}...")
print()

# Simboli da testare
symbols = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "ADAUSDT"]

for symbol in symbols:
    print(f"\n📡 Test {symbol}:")
    
    df15, src = fetch_td_15m(symbol)
    print(f"  15m: {len(df15) if df15 is not None else 0} candles")
    
    df1h, src = fetch_td_1h(symbol)
    print(f"  1h: {len(df1h) if df1h is not None else 0} candles")
    
    df4h, src = fetch_td_4h(symbol)
    print(f"  4h: {len(df4h) if df4h is not None else 0} candles")

print("\n" + "="*60)
print("✅ TEST COMPLETATO")
