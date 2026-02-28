import pandas as pd
import streamlit as st
import requests
import time
from typing import Optional, Tuple, List, Dict, Any
from utils.error_handler import error_handler
from providers.base_provider import BaseProvider, count_api_call
from utils.helpers import http_session, normalize_ohlcv_df

# Leggi chiave da secrets
TWELVEDATA_KEY = st.secrets.get("TWELVEDATA_KEY", "")

def convert_symbol_for_twelvedata(symbol: str) -> str:
    """
    Converte simbolo da formato Yahoo (BTC-USD) a TwelveData (BTC/USD)
    """
    if "/" in symbol:
        return symbol
    if "-" in symbol:
        return symbol.replace("-", "/")
    if "USDT" in symbol:
        return symbol.replace("USDT", "/USDT")
    if "USD" in symbol and len(symbol) > 3:
        base = symbol[:-3]
        return f"{base}/USD"
    return symbol

class TwelveDataProvider(BaseProvider):
    """Provider TwelveData con caching"""
    
    def __init__(self, ttl: int = 600, max_retries: int = 3):
        super().__init__("twelvedata", ttl=ttl)
        self.max_retries = max_retries
    
    @count_api_call('twelvedata', 'time_series')
    def _fetch_time_series(self, symbol: str, interval: str, outputsize: int):
        """Fetch interno con retry automatico"""
        if not TWELVEDATA_KEY:
            return None, "NO_KEY"
        
        td_symbol = convert_symbol_for_twelvedata(symbol)
        
        url = "https://api.twelvedata.com/time_series"
        params = {
            "symbol": td_symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": TWELVEDATA_KEY,
            "timezone": "UTC"
        }
        
        for attempt in range(self.max_retries):
            try:
                session = http_session()
                response = session.get(url, params=params, timeout=15)
                
                if response.status_code == 429:
                    wait_time = 60 * (attempt + 1)
                    if attempt < self.max_retries - 1:
                        time.sleep(wait_time)
                        continue
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
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                    continue
                return None, "TIMEOUT"
            except requests.exceptions.ConnectionError:
                if attempt < self.max_retries - 1:
                    time.sleep(2)
                    continue
                return None, "CONNECTION_ERROR"
            except Exception as e:
                error_handler.logger.error(f"TwelveData error: {e}")
                return None, "ERROR"
        
        return None, "MAX_RETRIES"
    
    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_15m(_self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 15m con caching - NOTA: _self per evitare hashing"""
        return _self.fetch(_self._fetch_time_series, symbol, "15min", 5000)
    
    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_1h(_self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 1h con caching - NOTA: _self per evitare hashing"""
        return _self.fetch(_self._fetch_time_series, symbol, "1h", 2000)
    
    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_4h(_self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 4h con caching - NOTA: _self per evitare hashing"""
        return _self.fetch(_self._fetch_time_series, symbol, "4h", 1000)
    
    @st.cache_data(ttl=3600, show_spinner=False)
    def search_symbols(_self, query: str, outputsize: int = 20) -> List[Dict[str, str]]:
        """Cerca simboli con caching - NOTA: _self per evitare hashing"""
        if not TWELVEDATA_KEY or not query or len(query.strip()) < 2:
            return []
        
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
