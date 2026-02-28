# utils/lazy_loader.py
import importlib
import streamlit as st
from typing import Any, Dict
from functools import lru_cache

class LazyLoader:
    def __init__(self):
        self._loaded_modules: Dict[str, Any] = {}
        self._loading_time: Dict[str, float] = {}
    
    @lru_cache(maxsize=32)
    def load(self, module_path: str, function_name: str = None):
        import time
        start = time.time()
        
        try:
            module = importlib.import_module(module_path)
            
            if function_name:
                if hasattr(module, function_name):
                    result = getattr(module, function_name)
                else:
                    available = [attr for attr in dir(module) if not attr.startswith('_')]
                    st.error(f"Funzione {function_name} non trovata in {module_path}")
                    st.error(f"Disponibili: {available}")
                    return None
            else:
                result = module
            
            load_time = time.time() - start
            self._loading_time[f"{module_path}.{function_name if function_name else ''}"] = load_time
            return result
            
        except ImportError as e:
            st.error(f"Errore caricamento modulo {module_path}: {e}")
            return None
    
    def get_function(self, module_path: str, function_name: str):
        def wrapper(*args, **kwargs):
            func = self.load(module_path, function_name)
            if func:
                return func(*args, **kwargs)
            return None
        return wrapper
    
    def show_loading_stats(self):
        if self._loading_time:
            with st.expander("⚡ Statistiche Caricamento", expanded=False):
                total = sum(self._loading_time.values())
                st.metric("Tempo totale", f"{total:.2f}s")
                
                for name, time in sorted(self._loading_time.items(), 
                                         key=lambda x: x[1], reverse=True)[:5]:
                    st.caption(f"{name}: {time:.3f}s")

lazy = LazyLoader()