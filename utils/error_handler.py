# utils/error_handler.py
import streamlit as st
import logging
import traceback
from datetime import datetime
from functools import wraps
from typing import Any, Callable, Optional

class ErrorHandler:
    """
    Gestione centralizzata degli errori
    """
    
    def __init__(self):
        self.log = []
        self.setup_logging()
    
    def setup_logging(self):
        """Configura logging"""
        logging.basicConfig(
            filename='golden_eye.log',
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def safe_execute(self, func: Callable, fallback: Any = None, 
                     error_msg: str = "Errore imprevisto", 
                     show_error: bool = True) -> Any:
        """
        Esegue una funzione in modo sicuro con gestione errori
        """
        try:
            return func()
        except Exception as e:
            error_detail = {
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'traceback': traceback.format_exc(),
                'function': func.__name__
            }
            self.log.append(error_detail)
            self.logger.error(f"{error_msg}: {str(e)}\n{traceback.format_exc()}")
            
            if show_error:
                if "rate limit" in str(e).lower():
                    st.warning("⏳ Rate limit raggiunto. Attendi qualche secondo.")
                elif "timeout" in str(e).lower():
                    st.warning("⏱️ Timeout della richiesta. Riprova.")
                elif "api key" in str(e).lower():
                    st.error("🔑 Errore di autenticazione. Verifica le API keys.")
                else:
                    st.error(f"⚠️ {error_msg}")
            
            return fallback
    
    def safe_fetch(self, fallback_msg: str = "Dati non disponibili"):
        """Decorator per fetch sicuri"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    self.logger.error(f"Errore in {func.__name__}: {str(e)}")
                    st.caption(fallback_msg)
                    return None
            return wrapper
        return decorator
    
    def show_error_summary(self):
        """Mostra riepilogo errori (per debug)"""
        if self.log:
            with st.expander("🔧 Debug Errori", expanded=False):
                for i, err in enumerate(self.log[-5:]):
                    st.markdown(f"**{i+1}. {err['timestamp']}**")
                    st.code(err['error'])
                    if st.checkbox(f"Mostra traceback {i+1}", key=f"tb_{i}"):
                        st.code(err['traceback'])

# Istanza globale
error_handler = ErrorHandler()
