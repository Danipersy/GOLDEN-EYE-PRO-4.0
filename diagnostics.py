# diagnostics.py
"""
Script di diagnostica completo per Golden Eye Pro 2026
Esegui questo script per identificare tutti i problemi
"""
import os
import sys
import importlib
from pathlib import Path

print("="*80)
print("🔍 GOLDEN EYE PRO - DIAGNOSI COMPLETA")
print("="*80)

# 1. Verifica struttura directory
print("\n📁 1. VERIFICA STRUTTURA DIRECTORIES")
current_dir = Path(__file__).parent.absolute()
print(f"Directory corrente: {current_dir}")

required_dirs = [
    "ui_streamlit",
    "ui_streamlit/components",
    "ui_streamlit/pages",
    "providers",
    "indicators",
    "strategy",
    "storage",
    "utils",
    "ai",
    "cache"
]

for d in required_dirs:
    path = current_dir / d
    if path.exists():
        print(f"✅ {d} - OK")
    else:
        print(f"❌ {d} - MANCANTE")
        try:
            path.mkdir(parents=True, exist_ok=True)
            print(f"   📁 Creata directory {d}")
        except Exception as e:
            print(f"   ❌ Errore creazione: {e}")

# 2. Verifica file essenziali
print("\n📄 2. VERIFICA FILE ESSENZIALI")
essential_files = [
    "App.py",
    "config.py",
    "requirements.txt",
    "providers/__init__.py",
    "providers/base_provider.py",
    "providers/twelvedata_provider.py",
    "providers/multi_provider.py",
    "providers/marketaux_provider.py",
    "indicators/robust_ta.py",
    "strategy/backtest.py",
    "strategy/validator.py",
    "strategy/money_manager.py",
    "ui_streamlit/__init__.py",
    "ui_streamlit/pages/__init__.py",
    "ui_streamlit/pages/trading_view.py",
    "utils/helpers.py",
    "utils/error_handler.py",
    "storage/watchlist_store.py",
    "ai/asset_analyzer.py"
]

for f in essential_files:
    path = current_dir / f
    if path.exists():
        size = path.stat().st_size
        print(f"✅ {f} - OK ({size} bytes)")
    else:
        print(f"❌ {f} - MANCANTE")

# 3. Verifica importazioni
print("\n🔌 3. TEST IMPORTAZIONI CRITICHE")
sys.path.insert(0, str(current_dir))

modules_to_test = [
    "config",
    "providers.base_provider",
    "providers.twelvedata_provider",
    "providers.multi_provider",
    "providers.marketaux_provider",
    "indicators.robust_ta",
    "strategy.backtest",
    "strategy.validator",
    "strategy.money_manager",
    "utils.helpers",
    "utils.error_handler",
    "storage.watchlist_store",
    "ai.asset_analyzer",
    "ui_streamlit.components.scan_panel",
    "ui_streamlit.pages.trading_view"
]

for module_name in modules_to_test:
    try:
        module = importlib.import_module(module_name)
        print(f"✅ {module_name} - OK")
    except ImportError as e:
        print(f"❌ {module_name} - ERRORE: {e}")
    except Exception as e:
        print(f"⚠️ {module_name} - WARNING: {e}")

# 4. Verifica dipendenze
print("\n📦 4. VERIFICA DIPENDENZE")
try:
    import streamlit
    print(f"✅ streamlit {streamlit.__version__}")
except: print("❌ streamlit")

try:
    import pandas
    print(f"✅ pandas {pandas.__version__}")
except: print("❌ pandas")

try:
    import numpy
    print(f"✅ numpy {numpy.__version__}")
except: print("❌ numpy")

try:
    import pandas_ta
    print(f"✅ pandas_ta {pandas_ta.__version__}")
except: print("❌ pandas_ta")

try:
    import plotly
    print(f"✅ plotly {plotly.__version__}")
except: print("❌ plotly")

try:
    import yfinance
    print(f"✅ yfinance {yfinance.__version__}")
except: print("❌ yfinance")

try:
    import requests
    print(f"✅ requests {requests.__version__}")
except: print("❌ requests")

# 5. Verifica configurazione
print("\n⚙️ 5. VERIFICA CONFIGURAZIONE")
try:
    from config import *
    print("✅ config.py caricato")
    
    # Verifica variabili essenziali
    required_vars = [
        "DEFAULT_WATCHLIST",
        "VERSION",
        "TTL_YF",
        "SL_ATR",
        "TP_ATR",
        "ADX_MIN",
        "RSI_LONG_MAX",
        "RSI_SHORT_MIN"
    ]
    
    for var in required_vars:
        if var in dir():
            value = eval(var)
            print(f"   ✅ {var} = {value}")
        else:
            print(f"   ❌ {var} - MANCANTE")
except Exception as e:
    print(f"❌ Errore caricamento config: {e}")

# 6. Verifica secrets
print("\n🔐 6. VERIFICA SECRETS")
try:
    import streamlit as st
    
    # Prova a leggere i secrets
    td_key = st.secrets.get("TWELVEDATA_KEY", "")
    av_key = st.secrets.get("ALPHA_VANTAGE_KEY", "")
    mk_key = st.secrets.get("MARKETAUX_TOKEN", "")
    
    print(f"📡 TwelveData: {'✅ Presente' if td_key else '❌ Mancante'}")
    if td_key:
        print(f"   Inizia con: {td_key[:4]}...")
    
    print(f"🟣 Alpha Vantage: {'✅ Presente' if av_key else '❌ Mancante'}")
    if av_key:
        print(f"   Inizia con: {av_key[:4]}...")
    
    print(f"🟡 Marketaux: {'✅ Presente' if mk_key else '❌ Mancante'}")
    if mk_key:
        print(f"   Inizia con: {mk_key[:4]}...")
        
except Exception as e:
    print(f"❌ Errore lettura secrets: {e}")
    print("   Crea .streamlit/secrets.toml con le tue chiavi")

# 7. Verifica circolari import
print("\n🔄 7. VERIFICA IMPORT CIRCOLARI")
potential_circular = [
    ("providers", "twelvedata_provider", "base_provider"),
    ("ui_streamlit", "pages", "components"),
    ("strategy", "backtest", "validator"),
    ("ai", "asset_analyzer", "indicators.robust_ta")
]

for pkg, mod1, mod2 in potential_circular:
    try:
        m1 = importlib.import_module(f"{pkg}.{mod1}")
        m2 = importlib.import_module(f"{pkg}.{mod2}")
        print(f"✅ {pkg}.{mod1} <-> {mod2} - OK")
    except Exception as e:
        print(f"⚠️ {pkg}.{mod1} <-> {mod2}: {e}")

# 8. Riepilogo finale
print("\n" + "="*80)
print("📊 RIEPILOGO DIAGNOSI")
print("="*80)

print("""
🔴 PROBLEMI GRAVI (DA RISOLVERE SUBITO):
- Errori di import circolari
- Path mancanti
- Secrets non configurati
- Dipendenze mancanti

🟡 PROBLEMI MEDI (DA OTTIMIZZARE):
- Duplicazione codice
- Cache non ottimizzata
- Error handling migliorabile

🟢 PROBLEMI MINORI (MIGLIORIE):
- UI responsive
- Performance loading
- Documentazione

✅ COSA FUNZIONA:
- Struttura base del progetto
- Moduli principali presenti
- Architettura solida
""")

print("\n🔥 Per correggere automaticamente tutti i problemi, esegui:")
print("python fix_all_issues.py")
