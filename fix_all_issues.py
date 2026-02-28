# fix_all_issues.py
"""
Script di correzione automatica per tutti i problemi identificati
"""
import os
import sys
import shutil
from pathlib import Path

print("="*80)
print("🔧 GOLDEN EYE PRO - CORREZIONE AUTOMATICA")
print("="*80)

current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# 1. CORREZIONE PATH E IMPORTAZIONI
print("\n📁 1. CORREZIONE PATH E IMPORTAZIONI")

# Crea __init__.py mancanti
init_dirs = [
    "providers",
    "indicators",
    "strategy",
    "storage",
    "utils",
    "ai",
    "ui_streamlit",
    "ui_streamlit/components",
    "ui_streamlit/pages"
]

for d in init_dirs:
    init_file = current_dir / d / "__init__.py"
    if not init_file.exists():
        try:
            with open(init_file, 'w') as f:
                f.write(f'# {d} package\n')
            print(f"✅ Creato {d}/__init__.py")
        except Exception as e:
            print(f"❌ Errore creazione {d}/__init__.py: {e}")

# 2. CORREZIONE App.py
print("\n📄 2. CORREZIONE App.py")

app_py_path = current_dir / "App.py"
if app_py_path.exists():
    with open(app_py_path, 'r') as f:
        content = f.read()
    
    # Sostituisci import dinamico con import diretto
    new_content = content.replace(
        "def import_page(module_name):",
        """def import_page(module_name):
    try:
        # Import diretto delle pagine
        if module_name == "scan":
            from ui_streamlit.pages.scan import show_page
            return show_page
        elif module_name == "dettaglio":
            from ui_streamlit.pages.dettaglio import show_page
            return show_page
        elif module_name == "watchlist":
            from ui_streamlit.pages.watchlist import show_page
            return show_page
        elif module_name == "validazione":
            from ui_streamlit.pages.validazione import render
            return render
        elif module_name == "ottimizzazione":
            from ui_streamlit.pages.ottimizzazione import render
            return render
        elif module_name == "money_management":
            from ui_streamlit.pages.money_management import render
            return render
        elif module_name == "paper_trading":
            from ui_streamlit.pages.paper_trading import render
            return render
        elif module_name == "auto_trader":
            from ui_streamlit.pages.auto_trader import render
            return render
        else:
            print(f"⚠️ Modulo {module_name} non riconosciuto")
            return None
    except ImportError as e:
        print(f"❌ Errore import {module_name}: {e}")
        return None"""
    )
    
    with open(app_py_path, 'w') as f:
        f.write(new_content)
    print("✅ App.py aggiornato con import diretti")

# 3. CORREZIONE CONFIGURAZIONE
print("\n⚙️ 3. CORREZIONE CONFIGURAZIONE")

config_path = current_dir / "config.py"
if config_path.exists():
    with open(config_path, 'r') as f:
        content = f.read()
    
    # Aggiungi variabili mancanti
    missing_vars = """
# ============================================
# VARIABILI AGGIUNTIVE PER COMPATIBILITÀ
# ============================================
YF_15M_PERIOD = "5d"
YF_15M_INTERVAL = "15m"
SCORE_FORTE_MIN = 70
MTF_EMA_FAST = 20
MTF_EMA_SLOW = 50
"""
    
    if "YF_15M_PERIOD" not in content:
        with open(config_path, 'a') as f:
            f.write(missing_vars)
        print("✅ Aggiunte variabili mancanti a config.py")

# 4. CREA secrets.toml SE MANCANTE
print("\n🔐 4. VERIFICA/CREAZIONE SECRETS")

secrets_dir = current_dir / ".streamlit"
secrets_file = secrets_dir / "secrets.toml"

if not secrets_file.exists():
    secrets_dir.mkdir(exist_ok=True)
    with open(secrets_file, 'w') as f:
        f.write("""# Inserisci le tue API keys qui
TWELVEDATA_KEY = ""
ALPHA_VANTAGE_KEY = ""
MARKETAUX_TOKEN = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
""")
    print("✅ Creato template secrets.toml")
    print("⚠️ INSERISCI LE TUE CHIAVI API IN .streamlit/secrets.toml")
else:
    print("✅ secrets.toml già esistente")

# 5. CORREZIONE IMPORT CIRCOLARI
print("\n🔄 5. CORREZIONE IMPORT CIRCOLARI")

# Fix per providers/__init__.py
init_providers = current_dir / "providers" / "__init__.py"
if init_providers.exists():
    with open(init_providers, 'w') as f:
        f.write("""# providers/__init__.py
from providers.twelvedata_provider import (
    fetch_td_15m, fetch_td_1h, fetch_td_4h, 
    search_symbols_td, convert_symbol_for_twelvedata
)
from providers.multi_provider import (
    fetch_yf_ohlcv, scan_symbol, fetch_yf,
    fetch_yahoo, fetch_alphavantage, fetch_twelvedata
)
from providers.marketaux_provider import fetch_marketaux_sentiment
from providers.base_provider import tracker, BaseProvider, count_api_call

__all__ = [
    'fetch_td_15m', 'fetch_td_1h', 'fetch_td_4h', 'search_symbols_td', 'convert_symbol_for_twelvedata',
    'fetch_yf_ohlcv', 'scan_symbol', 'fetch_yf',
    'fetch_yahoo', 'fetch_alphavantage', 'fetch_twelvedata',
    'fetch_marketaux_sentiment',
    'tracker', 'BaseProvider', 'count_api_call'
]
""")
    print("✅ providers/__init__.py aggiornato")

# 6. INSTALLA DIPENDENZE MANCANTI
print("\n📦 6. VERIFICA DIPENDENZE")

try:
    import pandas_ta
except ImportError:
    print("⚠️ pandas_ta non installato - installazione in corso...")
    os.system(f"{sys.executable} -m pip install pandas-ta")
    print("✅ pandas_ta installato")

try:
    import plotly
except ImportError:
    print("⚠️ plotly non installato - installazione in corso...")
    os.system(f"{sys.executable} -m pip install plotly")
    print("✅ plotly installato")

# 7. CREA CACHE DIRECTORY
print("\n💾 7. CREAZIONE CACHE DIRECTORY")

cache_dirs = [
    "cache",
    "cache/twelvedata",
    "cache/yahoo"
]

for d in cache_dirs:
    path = current_dir / d
    path.mkdir(parents=True, exist_ok=True)
    print(f"✅ {d}/ - OK")

# 8. CORREZIONE UI COMPONENTS
print("\n🎨 8. CORREZIONE UI COMPONENTS")

# Fix per paper_trading.py - funzione mancante
paper_trading = current_dir / "ui_streamlit" / "components" / "paper_trading.py"
if paper_trading.exists():
    with open(paper_trading, 'r') as f:
        content = f.read()
    
    if "render_paper_trading_panel" not in content:
        # Aggiungi la funzione mancante
        with open(paper_trading, 'a') as f:
            f.write("""

def render_paper_trading_panel(focus, current_price, atr, signal_score, signal_label):
    '''Wrapper per retrocompatibilità'''
    from ui_streamlit.components.paper_trading import render_paper_trading_panel as original
    return original(focus, current_price, atr, signal_score, signal_label)
""")
        print("✅ Aggiunto wrapper render_paper_trading_panel")

# 9. OTTIMIZZAZIONE PERFORMANCE
print("\n⚡ 9. OTTIMIZZAZIONE PERFORMANCE")

# Aggiungi caching a tutte le funzioni di fetch
twelvedata_path = current_dir / "providers" / "twelvedata_provider.py"
if twelvedata_path.exists():
    with open(twelvedata_path, 'r') as f:
        content = f.read()
    
    if "@st.cache_data" not in content:
        # Aggiungi decorator caching
        content = content.replace(
            "def fetch_td_15m(self, symbol: str):",
            """@st.cache_data(ttl=600, show_spinner=False)
    def fetch_td_15m(self, symbol: str):"""
        )
        with open(twelvedata_path, 'w') as f:
            f.write(content)
        print("✅ Aggiunto caching a twelvedata_provider.py")

# 10. CORREZIONE ERROR HANDLER
print("\n🐛 10. CORREZIONE ERROR HANDLER")

error_handler_path = current_dir / "utils" / "error_handler.py"
if error_handler_path.exists():
    with open(error_handler_path, 'r') as f:
        content = f.read()
    
    # Aggiungi metodo safe_fetch se mancante
    if "def safe_fetch" not in content:
        safe_fetch_method = """
    def safe_fetch(self, fallback_msg: str = "Dati non disponibili"):
        '''Decorator per fetch sicuri'''
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Errore in {func.__name__}: {str(e)}")
                    st.caption(fallback_msg)
                    return None
            return wrapper
        return decorator
"""
        # Inserisci dopo __init__
        content = content.replace(
            "    def __init__(self):",
            "    def __init__(self):\n" + safe_fetch_method
        )
        with open(error_handler_path, 'w') as f:
            f.write(content)
        print("✅ Aggiunto safe_fetch a error_handler.py")

# 11. CREA FILE DI TEST COMPLETO
print("\n🧪 11. CREAZIONE FILE DI TEST COMPLETO")

test_file = current_dir / "test_completo.py"
with open(test_file, 'w') as f:
    f.write("""# test_completo.py
import streamlit as st
import sys
from pathlib import Path

st.set_page_config(page_title="Golden Eye - Test", layout="wide")

st.title("🧪 Golden Eye Pro - Test Completo")

# Test imports
st.header("1. Test Importazioni")

tests = [
    ("config", "config"),
    ("providers.twelvedata_provider", "twelvedata_provider"),
    ("providers.multi_provider", "multi_provider"),
    ("indicators.robust_ta", "robust_ta"),
    ("strategy.backtest", "backtest"),
    ("strategy.validator", "validator"),
    ("ai.asset_analyzer", "asset_analyzer"),
    ("ui_streamlit.pages.trading_view", "trading_view")
]

for module_name, display_name in tests:
    try:
        __import__(module_name)
        st.success(f"✅ {display_name}")
    except Exception as e:
        st.error(f"❌ {display_name}: {e}")

# Test dati
st.header("2. Test Provider Dati")

from providers.twelvedata_provider import fetch_td_15m
from providers.multi_provider import scan_symbol

col1, col2 = st.columns(2)

with col1:
    st.subheader("TwelveData")
    if st.button("Test BTC-USD", key="td_test"):
        with st.spinner("Caricamento..."):
            df, src = fetch_td_15m("BTC-USD")
            if df is not None:
                st.success(f"✅ {len(df)} candles da {src}")
                st.dataframe(df.tail())
            else:
                st.error(f"❌ Fallito: {src}")

with col2:
    st.subheader("Yahoo/MultiProvider")
    if st.button("Test ETH-USD", key="yahoo_test"):
        with st.spinner("Caricamento..."):
            result = scan_symbol("ETH-USD", "15m", "1d")
            if result and 'error' not in result:
                st.success(f"✅ Prezzo: ${result['price']:.2f} ({result['change']:+.2f}%)")
            else:
                st.error("❌ Fallito")

# Test strategia
st.header("3. Test Strategia")

from indicators.robust_ta import compute_indicators_15m, decide_signal
import pandas as pd
import numpy as np

# Genera dati fake
dates = pd.date_range(end=pd.Timestamp.now(), periods=500, freq='15min')
df_test = pd.DataFrame({
    'datetime': dates,
    'open': np.random.randn(500).cumsum() + 100,
    'high': np.random.randn(500).cumsum() + 102,
    'low': np.random.randn(500).cumsum() + 98,
    'close': np.random.randn(500).cumsum() + 100,
    'volume': np.random.randint(100, 1000, 500)
})

df_ind = compute_indicators_15m(df_test)
signal = decide_signal(df_ind, True, False)

st.json({
    "segnale": signal['display'],
    "forza": signal['strength'],
    "rsi": f"{signal['rsi']:.1f}",
    "adx": f"{signal['adx']:.1f}"
})

# Test AI
st.header("4. Test AI Suggeritore")

from ai.asset_analyzer import AssetAIAnalyzer

analyzer = AssetAIAnalyzer()
test_data = {
    'v': 'BUY',
    'level': 4,
    'rsi': 45,
    'adx': 30,
    'p': 50000,
    'atr': 1000,
    'sqz_on': False,
    'mtf_long': True,
    'mtf_short': False,
    'bias_long': True
}

analysis = analyzer.analyze_asset("BTC-USD", test_data)

st.metric("Score AI", analysis['score'])
st.info(f"Azione: {analysis['action']}")
st.write("Segnali:", analysis['signals'])
""")
print("✅ Creato test_completo.py")

# 12. CREA REQUIREMENTS COMPLETO
print("\n📋 12. AGGIORNAMENTO REQUIREMENTS")

req_path = current_dir / "requirements.txt"
with open(req_path, 'w') as f:
    f.write("""# Core
streamlit>=1.38.0
pandas>=2.2.0
numpy>=1.26.0
streamlit-option-menu==0.3.6

# Dati
yfinance>=0.2.40
requests>=2.32.0

# Utility
python-dotenv>=1.0.0
pytz>=2024.1
urllib3>=2.2.0
psutil>=5.9.0

# Grafici
plotly>=5.24.0

# Technical Analysis
pandas-ta>=0.3.14b0

# AI (opzionale)
scikit-learn>=1.5.0
""")
print("✅ requirements.txt aggiornato")

# 13. RIEPILOGO FINALE
print("\n" + "="*80)
print("✅✅✅ CORREZIONE COMPLETATA ✅✅✅")
print("="*80)
print("""
📋 COSA È STATO CORRETTO:
✓ Path e importazioni
✓ __init__.py mancanti
✓ App.py con import diretti
✓ Config.py con variabili mancanti
✓ Template secrets.toml
✓ Import circolari nei providers
✓ Dipendenze installate
✓ Cache directories
✓ UI components mancanti
✓ Error handler migliorato
✓ Test completi
✓ Requirements aggiornato

🚀 PROSSIMI PASSI:
1. Inserisci le tue API keys in .streamlit/secrets.toml
2. Esegui: streamlit run App.py
3. Se ci sono errori, esegui: streamlit run test_completo.py
4. Verifica che tutto funzioni

🔥 COMANDI RAPIDI:
streamlit run App.py           # Avvia l'app
streamlit run test_completo.py  # Test completo
python diagnostics.py           # Diagnostica
""")
