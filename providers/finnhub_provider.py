import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from providers.base_provider import BaseProvider, count_api_call

FINNHUB_KEY = st.secrets.get("FINNHUB_KEY", "")

class FinnhubProvider(BaseProvider):
    """Provider Finnhub per dati di mercato in tempo reale e storici"""
    
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
                'previous_close': data.get('pc', 0),
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
    
    @count_api_call('finnhub', 'candle')
    def get_historical_candles(self, symbol: str, resolution: str = '15', count: int = 500):
        """
        Ottieni dati storici OHLCV da Finnhub
        resolution: '1', '5', '15', '30', '60', 'D', 'W', 'M'
        count: numero di candles da restituire (max 5000)
        """
        if not FINNHUB_KEY:
            return None, "NO_KEY"
        
        url = f"{self.base_url}/stock/candle"
        params = {
            "symbol": symbol,
            "resolution": resolution,
            "count": count,
            "token": FINNHUB_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 429:
                return None, "RATE_LIMIT"
            if response.status_code != 200:
                return None, f"HTTP_{response.status_code}"
            
            data = response.json()
            
            if data.get('s') != 'ok':
                return None, f"ERROR: {data.get('s')}"
            
            # Finnhub restituisce array di timestamp, open, high, low, close, volume
            df = pd.DataFrame({
                'timestamp': data['t'],
                'open': data['o'],
                'high': data['h'],
                'low': data['l'],
                'close': data['c'],
                'volume': data['v']
            })
            
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='s', utc=True)
            df = df.sort_values('datetime').reset_index(drop=True)
            
            return df, "Finnhub"
            
        except Exception as e:
            return None, f"ERROR: {str(e)[:50]}"
    
    @count_api_call('finnhub', 'crypto_candle')
    def get_crypto_historical(self, symbol: str, resolution: str = '15', count: int = 500):
        """Per crypto, Finnhub richiede simboli nel formato BINANCE:BTCUSDT"""
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
        return self.get_historical_candles(finnhub_symbol, resolution, count)
    
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
                data = response.json()
                return {
                    'name': data.get('name'),
                    'ticker': data.get('ticker'),
                    'market_cap': data.get('marketCapitalization'),
                    'share_outstanding': data.get('shareOutstanding'),
                    'ipo': data.get('ipo'),
                    'logo': data.get('logo'),
                    'weburl': data.get('weburl'),
                    'industry': data.get('finnhubIndustry'),
                    'exchange': data.get('exchange')
                }
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
                news_list = response.json()
                # Formatta e limita a 10 news
                formatted_news = []
                for item in news_list[:10]:
                    formatted_news.append({
                        'headline': item.get('headline'),
                        'summary': item.get('summary'),
                        'source': item.get('source'),
                        'url': item.get('url'),
                        'datetime': datetime.fromtimestamp(item.get('datetime')).strftime('%Y-%m-%d %H:%M'),
                        'sentiment': item.get('sentiment', 0)
                    })
                return formatted_news
        except:
            pass
        return []
    
    @count_api_call('finnhub', 'news_sentiment')
    def get_news_sentiment(self, symbol: str):
        """Ottieni sentiment delle news per un simbolo"""
        if not FINNHUB_KEY:
            return None
        
        url = f"{self.base_url}/news-sentiment"
        params = {
            "symbol": symbol,
            "token": FINNHUB_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                data = response.json()
                return {
                    'sentiment': data.get('sentiment', {}).get('score', 0.5),
                    'bearish': data.get('sentiment', {}).get('bearish', 0),
                    'bullish': data.get('sentiment', {}).get('bullish', 0),
                    'mentions': data.get('mentionCount', 0),
                    'positive_mentions': data.get('positiveMentionCount', 0),
                    'negative_mentions': data.get('negativeMentionCount', 0),
                    'source': 'Finnhub'
                }
        except:
            pass
        return None
    
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
                        'currency': 'USD',
                        'display': f"{item.get('symbol')} - {item.get('description')}"
                    })
                return results
        except Exception as e:
            print(f"Finnhub search error: {e}")
        return []
    
    @count_api_call('finnhub', 'market_news')
    def get_market_news(self, category: str = 'general', limit: int = 10):
        """
        Ottieni news di mercato generali
        category: 'general', 'forex', 'crypto', 'merger'
        """
        if not FINNHUB_KEY:
            return []
        
        url = f"{self.base_url}/news"
        params = {
            "category": category,
            "token": FINNHUB_KEY,
            "minId": 0
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                news_list = response.json()
                return news_list[:limit]
        except:
            pass
        return []
    
    @count_api_call('finnhub', 'economic_code')
    def get_economic_calendar(self, from_date: str = None, to_date: str = None):
        """Calendario economico"""
        if not FINNHUB_KEY:
            return []
        
        if from_date is None:
            from_date = datetime.now().strftime('%Y-%m-%d')
            to_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/calendar/economic"
        params = {
            "from": from_date,
            "to": to_date,
            "token": FINNHUB_KEY
        }
        
        try:
            response = requests.get(url, params=params, timeout=5)
            if response.status_code == 200:
                return response.json().get('economicCalendar', [])
        except:
            pass
        return []

# Istanza globale
finnhub_provider = FinnhubProvider()
