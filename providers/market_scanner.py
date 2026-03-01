import streamlit as st
import yfinance as yf
import pandas as pd
import time
from datetime import datetime, timedelta
from providers.base_provider import count_api_call

class MarketScanner:
    """
    Scanner avanzato che cerca top mover nel mercato usando Yahoo Finance
    """
    
    def __init__(self):
        self.popular_tickers = [
            # S&P 500 top 50 per volume
            "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
            "JPM", "V", "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "BAC",
            "NFLX", "ADBE", "CRM", "PFE", "TMO", "ABT", "NKE", "INTC", "AMD",
            "CSCO", "PEP", "COST", "CVX", "WFC", "ABBV", "ACN", "AVGO",
            "DHR", "LIN", "TXN", "PM", "QCOM", "HON", "UPS", "UNP", "MS", "BLK",
            # Crypto
            "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD",
            "DOGE-USD", "DOT-USD", "MATIC-USD", "AVAX-USD", "LINK-USD", "UNI-USD",
            # Forex
            "EURUSD=X", "GBPUSD=X", "JPY=X", "AUDUSD=X", "USDCAD=X", "NZDUSD=X"
        ]
    
    @count_api_call('scanner', 'scan_movers')
    def scan_top_movers(self, limit=50, min_volume=1000000, min_price=1.0):
        """
        Cerca i top mover del mercato:
        - Top gainers (maggiori rialzi %)
        - Top losers (maggiori ribassi %)
        - Most active (maggior volume)
        """
        results = {
            'gainers': [],
            'losers': [],
            'most_active': []
        }
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Raccogli dati
        data = []
        for i, symbol in enumerate(self.popular_tickers):
            status_text.text(f"Scanning {i+1}/{len(self.popular_tickers)}: {symbol}")
            progress_bar.progress((i+1)/len(self.popular_tickers))
            
            try:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                
                # Ottieni prezzo e variazioni
                current_price = info.get('regularMarketPrice', 0)
                prev_close = info.get('regularMarketPreviousClose', 0)
                volume = info.get('volume', 0)
                
                if current_price > min_price and volume > min_volume and prev_close > 0:
                    change_percent = ((current_price - prev_close) / prev_close) * 100
                    
                    data.append({
                        'symbol': symbol,
                        'name': info.get('shortName', symbol),
                        'price': current_price,
                        'change': change_percent,
                        'volume': volume,
                        'market_cap': info.get('marketCap', 0),
                        'sector': info.get('sector', 'N/A')
                    })
                
                time.sleep(0.1)  # Rate limiting
                
            except Exception as e:
                continue
        
        progress_bar.empty()
        status_text.empty()
        
        # Converti in DataFrame e ordina
        if data:
            df = pd.DataFrame(data)
            
            # Top gainers
            gainers = df[df['change'] > 0].sort_values('change', ascending=False).head(limit)
            results['gainers'] = gainers.to_dict('records')
            
            # Top losers
            losers = df[df['change'] < 0].sort_values('change', ascending=True).head(limit)
            results['losers'] = losers.to_dict('records')
            
            # Most active (volume)
            most_active = df.sort_values('volume', ascending=False).head(limit)
            results['most_active'] = most_active.to_dict('records')
        
        return results
    
    def search_by_criteria(self, min_change=2, max_change=None, min_volume=1000000, 
                          sector=None, limit=20):
        """
        Cerca asset per criteri specifici
        """
        all_data = self.scan_top_movers(limit=100)
        
        results = []
        for category in ['gainers', 'losers']:
            for item in all_data[category]:
                change = abs(item['change'])
                if change >= min_change:
                    if max_change is None or change <= max_change:
                        if sector is None or item.get('sector') == sector:
                            results.append(item)
        
        return sorted(results, key=lambda x: abs(x['change']), reverse=True)[:limit]

# Istanza globale
market_scanner = MarketScanner()
