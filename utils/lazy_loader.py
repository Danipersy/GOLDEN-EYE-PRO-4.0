# utils/lazy_loader.py
import importlib
import streamlit as st
from typing import Any, Dict
from functools import lru_cache

class LazyLoader:
    """
    Caricamento lazy dei moduli per ottimizzare l'avvio
    """
    
    def __init__(self):
        self._loaded_modules: Dict[str, Any] = {}
        self._loading_time: Dict[str, float] = {}
    
    @lru_cache(maxsize=32)
    def load(self, module_path: str, function_name: str = None):
        """
        Carica un modulo solo quando serve
        """
        import time
        start = time.time()
        
        try:
            # Importa il modulo
            module = importlib.import_module(module_path)
            
            if function_name:
                result = getattr(module, function_name)
            else:
                result = module
            
            # Log tempo di caricamento
            load_time = time.time() - start
            self._loading_time[f"{module_path}.{function_name if function_name else ''}"] = load_time
            
            return result
            
        except ImportError as e:
            st.error(f"Errore caricamento modulo {module_path}: {e}")
            return None
    
    def get_function(self, module_path: str, function_name: str):
        """
        Restituisce una funzione da caricare lazy
        """
        def wrapper(*args, **kwargs):
            func = self.load(module_path, function_name)
            if func:
                return func(*args, **kwargs)
            return None
        return wrapper
    
    def show_loading_stats(self):
        """Mostra statistiche di caricamento (debug)"""
        if self._loading_time:
            with st.expander("⚡ Statistiche Caricamento", expanded=False):
                total = sum(self._loading_time.values())
                st.metric("Tempo totale caricamento", f"{total:.2f}s")
                
                for name, time in sorted(self._loading_time.items(), 
                                         key=lambda x: x[1], reverse=True)[:5]:
                    st.caption(f"{name}: {time:.3f}s")

# Istanza globale
lazy = LazyLoader()