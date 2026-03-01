import streamlit as st
import time
from datetime import datetime
from providers.multi_provider import fetch_yf_ohlcv
from providers.finnhub_provider import finnhub_provider
from providers.base_provider import count_api_call

class MultiScanner:
    """
    Scanner multi-provider che combina Yahoo (primario) e Finnhub (real-time)
    """
    
    def __init__(self):
        pass
    
    @count_api_call('scanner', 'scan_symbols_yahoo')
    def scan_symbols_yahoo(self, symbols, interval="15m", period="1d"):
        """Scanner primario usando Yahoo Finance (gratuito e robusto)"""
        results = []
        for i, symbol in enumerate(symbols):
            try:
                df = fetch_yf_ohlcv(symbol, interval, period)
                if df is not None and not df.empty:
                    change = ((df['close'].iloc[-1] - df['close'].iloc[0]) / df['close'].iloc[0]) * 100
                    results.append({
                        'symbol': symbol,
                        'price': df['close'].iloc[-1],
                        'change': change,
                        'volume': df['volume'].iloc[-1],
                        'source': 'Yahoo',
                        'timestamp': datetime.now()
                    })
                time.sleep(0.2)  # Rate limiting gentile
            except Exception as e:
                print(f"Yahoo error {symbol}: {e}")
        return results
    
    def enhance_with_finnhub(self, results):
        """Arricchisce i risultati con dati Finnhub (quote real-time)"""
        enhanced = []
        finnhub_key = st.secrets.get("FINNHUB_KEY", "")
        
        if not finnhub_key:
            return results  # Non possiamo arricchire
        
        for res in results:
            symbol = res['symbol']
            try:
                # Per crypto, usa endpoint specifico
                if symbol.endswith('USD') and len(symbol) > 4 and symbol not in ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 'USD/CAD', 'NZD/USD']:
                    quote_data, src = finnhub_provider.get_crypto_quote(symbol)
                else:
                    quote_data, src = finnhub_provider.get_quote(symbol)
                
                if quote_data:
                    # Aggiorna con dati Finnhub (più freschi)
                    res['price'] = quote_data.get('price', res['price'])
                    res['change'] = quote_data.get('change_percent', res['change'])
                    res['volume'] = quote_data.get('volume', res['volume'])
                    res['source'] = 'Finnhub'
                time.sleep(0.5)
            except Exception as e:
                print(f"Finnhub enhance error {symbol}: {e}")
            enhanced.append(res)
        
        return enhanced
    
    def enhanced_scan(self, market_list, use_finnhub=True):
        """
        Scanner potenziato che usa Yahoo come base e Finnhub per arricchimento
        """
        # Passo 1: Scan base con Yahoo
        results = self.scan_symbols_yahoo(market_list)
        
        # Passo 2: Arricchisci con Finnhub se richiesto e disponibile
        if use_finnhub and st.secrets.get("FINNHUB_KEY", ""):
            results = self.enhance_with_finnhub(results)
        
        return results

# Istanza globale
multi_scanner = MultiScanner()
