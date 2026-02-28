# debug_twelvedata.py
import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# Forza la lettura dei secrets
print("🔍 DEBUG TWELVEDATA")
print("="*60)

# 1. Verifica che la chiave esista
try:
    td_key = st.secrets.get("TWELVEDATA_KEY", "")
    print(f"📌 TWELVEDATA_KEY: {'✅ TROVATA' if td_key else '❌ MANCANTE'}")
    if td_key:
        print(f"   Inizia con: {td_key[:4]}...")
        print(f"   Lunghezza: {len(td_key)} caratteri")
except Exception as e:
    print(f"❌ Errore lettura secrets: {e}")
    td_key = ""

if not td_key:
    print("❌ Impossibile proseguire senza chiave")
    exit(1)

# 2. Test chiamata diretta API
print("\n📡 TEST CHIAMATA API DIRETTA")
symbol = "BTCUSDT"
url = "https://api.twelvedata.com/time_series"
params = {
    "symbol": symbol,
    "interval": "15min",
    "outputsize": 10,
    "apikey": td_key
}

try:
    print(f"📤 Richiesta a: {url}")
    print(f"📤 Parametri: {params}")
    
    response = requests.get(url, params=params, timeout=15)
    print(f"📥 Status code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"📥 Risposta JSON keys: {list(data.keys())}")
        
        if "values" in data:
            print(f"✅ Trovati {len(data['values'])} valori")
            print(f"📊 Primo valore: {data['values'][0]}")
        else:
            print(f"❌ 'values' non trovato nella risposta")
            print(f"Messaggio: {data.get('message', 'N/A')}")
            print(f"Status: {data.get('status', 'N/A')}")
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        print(f"Risposta: {response.text[:200]}")
        
except Exception as e:
    print(f"❌ Eccezione: {e}")

print("\n" + "="*60)
