# providers/base_provider.py
import streamlit as st
from utils.error_handler import error_handler
from config import DISK_CACHE_ENABLED, DISK_CACHE_DIR
import json
import os
from datetime import datetime, timedelta
import hashlib
import pickle

class BaseProvider:
    """
    Classe base per tutti i provider con caching su disco (SENZA st.cache_data)
    """
    
    def __init__(self, name: str, ttl: int = 300):
        self.name = name
        self.ttl = ttl
        self.cache_dir = os.path.join(DISK_CACHE_DIR, name)
        if DISK_CACHE_ENABLED:
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_cache_key(self, *args, **kwargs) -> str:
        """Genera chiave cache univoca"""
        key_str = f"{self.name}_{str(args)}_{str(kwargs)}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get_from_cache(self, key: str):
        """Legge dal cache su disco"""
        if not DISK_CACHE_ENABLED:
            return None
        
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
        if not DISK_CACHE_ENABLED:
            return
        
        cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(data, f)
        except Exception as e:
            error_handler.logger.error(f"Cache write error: {e}")
    
    def fetch(self, func, *args, **kwargs):
        """Fetch con caching manuale (SENZA st.cache_data)"""
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