# providers/twelvedata_provider.py
import pandas as pd
import streamlit as st
import requests
from typing import Optional, Tuple, List, Dict, Any
from utils.error_handler import error_handler
from providers.base_provider import BaseProvider, count_api_call
from utils.helpers import http_session, normalize_ohlcv_df

# Leggi chiave da secrets
TWELVEDATA_KEY = st.secrets.get("TWELVEDATA_KEY", "")

def convert_symbol_for_twelvedata(symbol: str) -> str:
    """
    Converte simbolo da formato Yahoo (BTC-USD) a TwelveData (BTC/USD)
    
    Esempi:
    - BTC-USD → BTC/USD
    - ETH-USD → ETH/USD
    - BTCUSDT → BTC/USDT (non supportato, ma gestito)
    - AAPL → AAPL (azioni)
    """
    # Se è già nel formato con slash, lascia stare
    if "/" in symbol:
        return symbol
    
    # Se è nel formato BTC-USD, converti in BTC/USD
    if "-" in symbol:
        return symbol.replace("-", "/")
    
    # Se è BTCUSDT, prova a convertire in BTC/USDT
    if "USDT" in symbol:
        return symbol.replace("USDT", "/USDT")
    
    # Se è BTCUSD, converti in BTC/USD
    if "USD" in symbol and len(symbol) > 3:
        base = symbol[:-3]
        return f"{base}/USD"
    
    # Altrimenti lascia com'è
    return symbol

class TwelveDataProvider(BaseProvider):
    """Provider TwelveData con caching su disco"""
    
    def __init__(self):
        super().__init__("twelvedata", ttl=600)
    
    @count_api_call('twelvedata', 'time_series')
    def _fetch_time_series(self, symbol: str, interval: str, outputsize: int):
        """Fetch interno senza decoratori"""
        if not TWELVEDATA_KEY:
            return None, "NO_KEY"
        
        # Converti simbolo per TwelveData
        td_symbol = convert_symbol_for_twelvedata(symbol)
        
        url = "https://api.twelvedata.com/time_series"
        params = {
            "symbol": td_symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": TWELVEDATA_KEY,
            "timezone": "UTC"
        }
        
        try:
            session = http_session()
            response = session.get(url, params=params, timeout=15)
            
            if response.status_code == 429:
                return None, "RATE_LIMIT"
            
            if response.status_code != 200:
                return None, f"HTTP_{response.status_code}"
            
            data = response.json()
            
            if "values" not in data:
                return None, "NO_VALUES"
            
            values = data.get("values")
            if not values:
                return None, "NO_DATA"
            
            df = pd.DataFrame(values)
            df = normalize_ohlcv_df(df)
            
            return df, "TwelveData"
            
        except requests.exceptions.Timeout:
            return None, "TIMEOUT"
        except requests.exceptions.ConnectionError:
            return None, "CONNECTION_ERROR"
        except Exception as e:
            error_handler.logger.error(f"TwelveData error: {e}")
            return None, "ERROR"
    
    def fetch_15m(self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 15m con 5000 candles"""
        return self.fetch(self._fetch_time_series, symbol, "15min", 5000)
    
    def fetch_1h(self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 1h con 2000 candles"""
        return self.fetch(self._fetch_time_series, symbol, "1h", 2000)
    
    def fetch_4h(self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 4h con 1000 candles"""
        return self.fetch(self._fetch_time_series, symbol, "4h", 1000)
    
    def search_symbols(self, query: str, outputsize: int = 20) -> List[Dict[str, str]]:
        """Cerca simboli su TwelveData"""
        if not TWELVEDATA_KEY or not query or len(query.strip()) < 2:
            return []
        
        cache_key = self.get_cache_key("search", query, outputsize)
        cached = self.get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        url = "https://api.twelvedata.com/symbol_search"
        params = {
            "symbol": query.strip(),
            "outputsize": outputsize,
            "apikey": TWELVEDATA_KEY
        }
        
        try:
            session = http_session()
            response = session.get(url, params=params, timeout=8)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            items = data.get("data", [])
            
            results = []
            for item in items:
                sym = item.get("symbol")
                if not sym:
                    continue
                name = item.get("instrument_name") or item.get("name") or ""
                exch = item.get("exchange") or ""
                currency = item.get("currency") or ""
                
                # Costruisci label informativa
                label = sym
                details = []
                if name:
                    details.append(name)
                if exch:
                    details.append(exch)
                if currency and currency != "USD":
                    details.append(currency)
                
                if details:
                    label += f" - {' | '.join(details)}"
                
                results.append({
                    "symbol": sym,
                    "label": label,
                    "name": name,
                    "exchange": exch,
                    "currency": currency
                })
            
            self.save_to_cache(cache_key, results)
            return results
            
        except Exception as e:
            error_handler.logger.error(f"TwelveData search error: {e}")
            return []

# Istanza globale
td_provider = TwelveDataProvider()

# Funzioni di compatibilità
def fetch_td_15m(symbol: str):
    return td_provider.fetch_15m(symbol)

def fetch_td_1h(symbol: str):
    return td_provider.fetch_1h(symbol)

def fetch_td_4h(symbol: str):
    return td_provider.fetch_4h(symbol)

def search_symbols_td(query: str, outputsize: int = 20):
    return td_provider.search_symbols(query, outputsize)