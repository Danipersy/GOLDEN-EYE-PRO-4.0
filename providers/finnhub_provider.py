import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from providers.base_provider import BaseProvider, count_api_call

FINNHUB_KEY = st.secrets.get("FINNHUB_KEY", "")

class FinnhubProvider(BaseProvider):
    """Provider Finnhub per dati di mercato in tempo reale"""
    
    def __init__(self):
        super().__init__("finnhub", ttl=60)  # Cache più breve per dati real-time
        self.base_url = "https://finnhub.io/api/v1"
    
    @count_api_call('finnhub', 'quote')
    def get_quote(self, symbol: str):
        """Ottieni quotazione in tempo reale"""
        if not FINNHUB_KEY:
            return None, "NO_KEY"
        
        url = f"{self.base_url}/quote"
        params = {
            "symbol": symbol,
            "token": FINNHUB_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 429:
                return None, "RATE_LIMIT"
            if response.status_code != 200:
                return None, f"HTTP_{response.status_code}"
            
            data = response.json()
            
            # Finnhub restituisce: c=current, d=change, dp=percent change, h=high, l=low, o=open, v=volume
            return {
                'price': data.get('c', 0),
                'change': data.get('d', 0),
                'change_percent': data.get('dp', 0),
                'high': data.get('h', 0),
                'low': data.get('l', 0),
                'open': data.get('o', 0),
                'volume': data.get('v', 0),
                'timestamp': datetime.now()
            }, "Finnhub"
            
        except Exception as e:
            return None, f"ERROR: {str(e)[:50]}"
    
    @count_api_call('finnhub', 'crypto_quote')
    def get_crypto_quote(self, symbol: str):
        """Per crypto, Finnhub usa un formato diverso (es. BINANCE:BTCUSDT)"""
        # Converti simboli comuni
        symbol_map = {
            "BTC-USD": "BINANCE:BTCUSDT",
            "ETH-USD": "BINANCE:ETHUSDT",
            "BNB-USD": "BINANCE:BNBUSDT",
            "SOL-USD": "BINANCE:SOLUSDT",
            "ADA-USD": "BINANCE:ADAUSDT",
            "XRP-USD": "BINANCE:XRPUSDT",
            "DOGE-USD": "BINANCE:DOGEUSDT",
            "DOT-USD": "BINANCE:DOTUSDT",
            "LINK-USD": "BINANCE:LINKUSDT",
            "MATIC-USD": "BINANCE:MATICUSDT",
            "AVAX-USD": "BINANCE:AVAXUSDT",
            "UNI-USD": "BINANCE:UNIUSDT",
            "ATOM-USD": "BINANCE:ATOMUSDT",
            "LTC-USD": "BINANCE:LTCUSDT",
            "BCH-USD": "BINANCE:BCHUSDT",
        }
        finnhub_symbol = symbol_map.get(symbol, symbol)
        return self.get_quote(finnhub_symbol)
    
    @count_api_call('finnhub', 'company_profile')
    def get_company_profile(self, symbol: str):
        """Ottieni informazioni sull'azienda"""
        if not FINNHUB_KEY:
            return None
        
        url = f"{self.base_url}/stock/profile2"
        params = {
            "symbol": symbol,
            "token": FINNHUB_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        return None
    
    @count_api_call('finnhub', 'news')
    def get_news(self, symbol: str, from_date: str = None, to_date: str = None):
        """Ottieni news per un simbolo"""
        if not FINNHUB_KEY:
            return []
        
        if from_date is None:
            to_date = datetime.now()
            from_date = to_date - timedelta(days=7)
        
        url = f"{self.base_url}/company-news"
        params = {
            "symbol": symbol,
            "from": from_date.strftime('%Y-%m-%d'),
            "to": to_date.strftime('%Y-%m-%d'),
            "token": FINNHUB_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()[:5]  # Ultime 5 news
        except:
            pass
        return []
    
    @count_api_call('finnhub', 'search')
    def search_symbols(self, query: str, limit: int = 20):
        """Cerca simboli per nome"""
        if not FINNHUB_KEY:
            return []
        
        url = f"{self.base_url}/search"
        params = {
            "q": query,
            "token": FINNHUB_KEY,
            "limit": limit
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get('result', []):
                    results.append({
                        'symbol': item.get('symbol'),
                        'name': item.get('description'),
                        'type': item.get('type'),
                        'currency': 'USD'
                    })
                return results
        except Exception as e:
            print(f"Finnhub search error: {e}")
        return []

# Istanza globale
finnhub_provider = FinnhubProvider()
