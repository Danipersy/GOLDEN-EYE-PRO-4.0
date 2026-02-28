# providers/base_provider.py
import streamlit as st
import json
import os
import pickle
import hashlib
from datetime import datetime, date, timedelta
from utils.error_handler import error_handler

class APIUsageTracker:
    """Traccia l'utilizzo delle API con supporto per tutti i provider"""
    
    def __init__(self):
        if 'api_usage' not in st.session_state:
            st.session_state.api_usage = {
                'twelvedata': {
                    'today': 0, 
                    'total': 0, 
                    'last_reset': date.today(),
                    'name': 'TwelveData',
                    'icon': '🔵',
                    'color': '#3b82f6'
                },
                'alphavantage': {
                    'today': 0, 
                    'total': 0, 
                    'last_reset': date.today(),
                    'name': 'Alpha Vantage',
                    'icon': '🟣',
                    'color': '#a855f7'
                },
                'yahoo': {
                    'today': 0, 
                    'total': 0, 
                    'last_reset': date.today(),
                    'name': 'Yahoo Finance',
                    'icon': '🟢',
                    'color': '#10b981'
                },
                'marketaux': {
                    'today': 0, 
                    'total': 0, 
                    'last_reset': date.today(),
                    'name': 'Marketaux',
                    'icon': '🟡',
                    'color': '#f59e0b'
                }
            }
        
        if 'api_calls_log' not in st.session_state:
            st.session_state.api_calls_log = []
    
    def _check_reset(self, provider):
        """Resetta il contatore giornaliero se necessario"""
        today = date.today()
        if st.session_state.api_usage[provider]['last_reset'] != today:
            st.session_state.api_usage[provider]['today'] = 0
            st.session_state.api_usage[provider]['last_reset'] = today
    
    def increment(self, provider, endpoint="", symbol=""):
        """Incrementa contatore per un provider con log dettagliato"""
        if provider not in st.session_state.api_usage:
            return
        
        self._check_reset(provider)
        st.session_state.api_usage[provider]['today'] += 1
        st.session_state.api_usage[provider]['total'] += 1
        
        # Log della chiamata
        st.session_state.api_calls_log.append({
            'time': datetime.now(),
            'provider': provider,
            'endpoint': endpoint,
            'symbol': symbol,
            'cumulative_today': st.session_state.api_usage[provider]['today']
        })
        
        # Mantieni solo ultime 100 chiamate nel log
        if len(st.session_state.api_calls_log) > 100:
            st.session_state.api_calls_log = st.session_state.api_calls_log[-100:]
    
    def get_usage(self, provider):
        """Ottieni utilizzo per provider"""
        self._check_reset(provider)
        return st.session_state.api_usage[provider]
    
    def get_all_usage(self):
        """Ottieni tutti gli utilizzi"""
        for provider in st.session_state.api_usage:
            self._check_reset(provider)
        return st.session_state.api_usage
    
    def get_limits(self, provider):
        """Restituisce i limiti per provider"""
        limits = {
            'twelvedata': {
                'daily': 800, 
                'minute': 8, 
                'cost_per_call': 1,
                'description': '800 chiamate/giorno, 8/minuto'
            },
            'alphavantage': {
                'daily': 500, 
                'minute': 5, 
                'cost_per_call': 1,
                'description': '500 chiamate/giorno, 5/minuto'
            },
            'yahoo': {
                'daily': 'Illimitato', 
                'minute': 'Variabile', 
                'cost_per_call': 0,
                'description': 'Rate limit variabile, usare con cautela'
            },
            'marketaux': {
                'daily': 100, 
                'minute': 10, 
                'cost_per_call': 1,
                'description': '100 chiamate/giorno, 10/minuto (gratis)'
            }
        }
        return limits.get(provider, {'daily': '?', 'minute': '?', 'cost_per_call': 0})
    
    def get_today_total(self):
        """Totale chiamate oggi"""
        total = 0
        for provider in st.session_state.api_usage:
            self._check_reset(provider)
            total += st.session_state.api_usage[provider]['today']
        return total
    
    def get_provider_stats(self):
        """Statistiche per provider"""
        stats = []
        for provider, data in self.get_all_usage().items():
            limits = self.get_limits(provider)
            percent = 0
            if isinstance(limits['daily'], int) and limits['daily'] > 0:
                percent = (data['today'] / limits['daily']) * 100
            
            stats.append({
                'provider': provider,
                'name': data.get('name', provider.title()),
                'icon': data.get('icon', '🔹'),
                'color': data.get('color', '#94a3b8'),
                'today': data['today'],
                'total': data['total'],
                'limit': limits['daily'],
                'percent': percent,
                'description': limits['description']
            })
        return stats

# Istanza globale
tracker = APIUsageTracker()

# Decorator per contare chiamate
def count_api_call(provider, endpoint=""):
    """Decorator per contare le chiamate API"""
    from functools import wraps
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Estrai symbol se presente (per log più dettagliato)
            symbol = ""
            if args and len(args) > 0:
                symbol = str(args[0])
            elif 'symbol' in kwargs:
                symbol = kwargs['symbol']
            
            tracker.increment(provider, endpoint, symbol)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# ============================================
# BASE PROVIDER (esistente)
# ============================================
class BaseProvider:
    """
    Classe base per tutti i provider con caching su disco
    """
    
    def __init__(self, name: str, ttl: int = 300):
        self.name = name
        self.ttl = ttl
        self.cache_dir = os.path.join("cache", name)
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_cache_key(self, *args, **kwargs) -> str:
        """Genera chiave cache univoca"""
        key_str = f"{self.name}_{str(args)}_{str(kwargs)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_from_cache(self, key: str):
        """Legge dal cache su disco"""
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        if not os.path.exists(cache_file):
            return None
        
        # Verifica TTL
        mod_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
        if datetime.now() - mod_time > timedelta(seconds=self.ttl):
            os.remove(cache_file)
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            error_handler.logger.error(f"Cache read error: {e}")
            return None
    
    def save_to_cache(self, key: str, data):
        """Salva su cache su disco"""
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            error_handler.logger.error(f"Cache write error: {e}")
    
    def fetch(self, func, *args, **kwargs):
        """Fetch con caching manuale"""
        cache_key = self.get_cache_key(*args, **kwargs)
        
        # Prova cache
        cached = self.get_from_cache(cache_key)
        if cached is not None:
            return cached
        
        # Esegui funzione
        result = error_handler.safe_execute(
            lambda: func(*args, **kwargs),
            fallback=None,
            error_msg=f"Errore in {self.name}"
        )
        
        # Salva in cache
        if result is not None:
            self.save_to_cache(cache_key, result)
        
        return result