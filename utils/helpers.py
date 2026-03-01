# utils/helpers.py
import requests
import pandas as pd
from datetime import datetime, timezone
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

def convert_symbol_to_yfinance(symbol: str):
    """Converte simbolo generico in formato Yahoo Finance"""
    s = (symbol or "").upper().strip()
    mapping = {
        "XAU/USD": "GC=F",
        "XAG/USD": "SI=F",
        "EUR/USD": "EURUSD=X",
        "GBP/USD": "GBPUSD=X",
        "USD/JPY": "JPY=X",
        "USD/CHF": "CHF=X",
        "AUD/USD": "AUDUSD=X",
        "NZD/USD": "NZDUSD=X",
        "USD/CAD": "CAD=X",
        "BTC/USD": "BTC-USD",
        "ETH/USD": "ETH-USD",
        "BTC/USDT": "BTC-USD",
        "ETH/USDT": "ETH-USD",
        "BNB/USD": "BNB-USD",
        "ADA/USD": "ADA-USD",
        "SOL/USD": "SOL-USD",
        "XRP/USD": "XRP-USD",
    }
    return mapping.get(s, s)

def http_session():
    """Crea sessione HTTP con retry"""
    s = requests.Session()
    retry_strategy = Retry(
        total=2,
        status_forcelist=[500, 502, 503, 504],
        backoff_factor=0.8
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    s.mount("https://", adapter)
    return s

def normalize_ohlcv_df(df: pd.DataFrame):
    """Normalizza DataFrame OHLCV"""
    if df is None or df.empty:
        return None
    x = df.copy()
    x.columns = [c.lower() for c in x.columns]
    
    if "date" in x.columns and "datetime" not in x.columns:
        x.rename(columns={"date": "datetime"}, inplace=True)
    if "datetime" not in x.columns:
        return None
    
    x["datetime"] = pd.to_datetime(x["datetime"], errors="coerce")
    x = x.dropna(subset=["datetime"]).sort_values("datetime").reset_index(drop=True)
    
    if x["datetime"].dt.tz is None:
        x["datetime"] = x["datetime"].dt.tz_localize("UTC")
    else:
        x["datetime"] = x["datetime"].dt.tz_convert("UTC")

    for c in ["open", "high", "low", "close", "volume"]:
        if c not in x.columns:
            if c == "volume":
                x[c] = 0.0
            else:
                return None
        x[c] = pd.to_numeric(x[c], errors="coerce")

    x = x.dropna(subset=["open", "high", "low", "close"]).reset_index(drop=True)
    return x

def get_market_status(symbol: str, last_candle_time=None):
    """Determina stato mercato (aperto/chiuso)"""
    s = (symbol or "").upper().strip()
    crypto_keywords = ["BTC", "ETH", "BNB", "ADA", "SOL", "XRP", "DOGE", "USDT"]
    
    if any(kw in s for kw in crypto_keywords):
        age = 0
        if last_candle_time is not None:
            age = (datetime.now(timezone.utc) - last_candle_time).total_seconds() / 60
        return {
            "status": "APERTO",
            "class": "market-open",
            "descr": f"CRYPTO 24/7 | Ultimo dato: {int(age)}m fa"
        }

    if last_candle_time is not None:
        age = (datetime.now(timezone.utc) - last_candle_time).total_seconds() / 60
        if age <= 30:
            return {
                "status": "APERTO",
                "class": "market-open",
                "descr": f"Dati aggiornati {int(age)}m fa"
            }
        return {
            "status": "CHIUSO",
            "class": "market-closed",
            "descr": f"Ultimo dato: {int(age)}m fa"
        }

    return {
        "status": "?",
        "class": "market-unknown",
        "descr": "Stato non determinabile"
    }

def pick_col_by_prefix(df: pd.DataFrame, prefix: str):
    """Trova colonna per prefisso"""
    if df is None or df.empty:
        return None
    p = prefix.upper()
    for c in df.columns:
        if str(c).upper().startswith(p):
            return c
    return None

def safe_last(df: pd.DataFrame, col: str, default=None):
    """Ultimo valore sicuro di una colonna"""
    if df is None or df.empty or (col is None) or (col not in df.columns):
        return default
    v = df[col].iloc[-1]
    return float(v) if pd.notna(v) else default
    
def convert_symbol_for_polygon(symbol: str) -> str:
    """Converte simboli generici in formato Polygon.
    Esempi:
    - BTC-USD → X:BTCUSD
    - AAPL → AAPL
    - EUR/USD → C:EURUSD (per forex)
    """
    s = symbol.upper().strip()
    if ':' in s:
        return s
    if '-' in s and s.endswith('USD'):
        base = s[:-4]
        return f"X:{base}USD"
    if '/' in s:
        base, quote = s.split('/')
        return f"C:{base}{quote}"
    return s
