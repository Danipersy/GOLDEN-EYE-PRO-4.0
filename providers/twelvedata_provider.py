# providers/twelvedata_provider.py
import pandas as pd
import streamlit as st
import requests
from typing import Optional, Tuple, List, Dict, Any
from utils.error_handler import error_handler
from providers.base_provider import BaseProvider
from config import TWELVEDATA_KEY
from utils.helpers import http_session, normalize_ohlcv_df

class TwelveDataProvider(BaseProvider):
    """Provider TwelveData con caching su disco (SENZA st.cache_data)"""
    
    def __init__(self):
        super().__init__("twelvedata", ttl=600)
    
    def _fetch_time_series(self, symbol: str, interval: str, outputsize: int):
        """Fetch interno senza decoratori"""
        if not TWELVEDATA_KEY:
            return None, "NO_KEY"
        
        url = f"https://api.twelvedata.com/time_series"
        params = {
            "symbol": symbol,
            "interval": interval,
            "outputsize": outputsize,
            "apikey": TWELVEDATA_KEY,
            "timezone": "UTC"
        }
        
        try:
            session = http_session()
            response = session.get(url, params=params, timeout=10)
            
            if response.status_code == 429:
                return None, "RATE_LIMIT"
            
            data = response.json()
            
            if data.get("status") == "error":
                return None, "ERROR"
            
            values = data.get("values")
            if not values:
                return None, "NO_DATA"
            
            df = pd.DataFrame(values)
            df = normalize_ohlcv_df(df)
            
            return df, "TwelveData"
            
        except Exception as e:
            error_handler.logger.error(f"TwelveData error: {e}")
            return None, "ERROR"
    
    def fetch_15m(self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 15m con caching manuale"""
        result = self.fetch(self._fetch_time_series, symbol, "15min", 420)
        if result is None:
            return None, "ERROR"
        return result
    
    def fetch_1h(self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 1h con caching manuale"""
        result = self.fetch(self._fetch_time_series, symbol, "1h", 320)
        if result is None:
            return None, "ERROR"
        return result
    
    def fetch_4h(self, symbol: str) -> Tuple[Optional[pd.DataFrame], str]:
        """Fetch 4h con caching manuale"""
        result = self.fetch(self._fetch_time_series, symbol, "4h", 220)
        if result is None:
            return None, "ERROR"
        return result
    
    def search_symbols(self, query: str, outputsize: int = 20) -> List[Dict[str, str]]:
        """Cerca simboli con caching"""
        if not TWELVEDATA_KEY:
            return []
        if not query or len(query.strip()) < 3:
            return []
        
        # Usa caching manuale
        cache_key = self.get_cache_key("search", query, outputsize)
        cached = self.get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        url = f"https://api.twelvedata.com/symbol_search"
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
            
            if not isinstance(items, list):
                return []
            
            results = []
            for item in items:
                sym = item.get("symbol")
                if not sym:
                    continue
                name = item.get("instrument_name") or item.get("name") or ""
                exch = item.get("exchange") or ""
                label = sym
                extra = [x for x in [name, exch] if x]
                if extra:
                    label += " - " + " | ".join(extra)
                results.append({"symbol": sym, "label": label})
            
            # Salva in cache
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