import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from providers.base_provider import BaseProvider, count_api_call

POLYGON_KEY = st.secrets.get("POLYGON_KEY", "")

class PolygonProvider(BaseProvider):
    """Provider Polygon.io per dati azionari e crypto"""
    
    def __init__(self):
        super().__init__("polygon", ttl=300)
        self.base_url = "https://api.polygon.io"
    
    @count_api_call('polygon', 'aggregates')
    def fetch_aggregates(self, symbol: str, timespan: str = 'minute', multiplier: int = 15, from_date: str = None, to_date: str = None, limit: int = 5000):
        """
        Fetch OHLCV data from Polygon aggregates endpoint.
        timespan: minute, hour, day
        multiplier: 1, 5, 15, etc.
        """
        if not POLYGON_KEY:
            return None, "NO_KEY"
        
        if from_date is None:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=30)
        
        to_str = to_date.strftime('%Y-%m-%d')
        from_str = from_date.strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/v2/aggs/ticker/{symbol}/range/{multiplier}/{timespan}/{from_str}/{to_str}"
        params = {
            "adjusted": "true",
            "sort": "asc",
            "limit": limit,
            "apiKey": POLYGON_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 429:
                return None, "RATE_LIMIT"
            if response.status_code != 200:
                return None, f"HTTP_{response.status_code}"
            
            data = response.json()
            if data.get('status') != 'OK':
                return None, "ERROR"
            
            results = data.get('results', [])
            if not results:
                return None, "NO_DATA"
            
            df = pd.DataFrame(results)
            df = df.rename(columns={
                't': 'timestamp',
                'o': 'open',
                'h': 'high',
                'l': 'low',
                'c': 'close',
                'v': 'volume'
            })
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
            df = df.sort_values('datetime').reset_index(drop=True)
            
            return df, "Polygon"
            
        except Exception as e:
            print(f"Polygon error: {e}")
            return None, "ERROR"
    
    @count_api_call('polygon', 'tickers')
    def search_symbols(self, query: str, limit: int = 20):
        """Cerca simboli per nome o ticker"""
        if not POLYGON_KEY:
            return []
        
        url = f"{self.base_url}/v3/reference/tickers"
        params = {
            "search": query,
            "active": "true",
            "limit": limit,
            "apiKey": POLYGON_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code != 200:
                return []
            
            data = response.json()
            results = data.get('results', [])
            
            out = []
            for item in results:
                out.append({
                    "symbol": item.get('ticker'),
                    "name": item.get('name'),
                    "market": item.get('market'),
                    "locale": item.get('locale'),
                    "currency": item.get('currency_name', 'USD')
                })
            return out
        except Exception as e:
            print(f"Polygon search error: {e}")
            return []

# Istanza globale
polygon_provider = PolygonProvider()
