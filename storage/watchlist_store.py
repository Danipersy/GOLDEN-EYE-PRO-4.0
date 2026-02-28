# storage/watchlist_store.py
import json
import os
from typing import List
from config import WATCHLIST_FILE  # se vuoi usare la costante

def load_watchlist(filename: str, default: List[str]) -> List[str]:
    """Carica watchlist da file JSON"""
    try:
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Errore caricamento watchlist: {e}")
    
    return default.copy()

def save_watchlist(filename: str, watchlist: List[str]) -> bool:
    """Salva watchlist su file JSON"""
    try:
        with open(filename, 'w') as f:
            json.dump(watchlist, f, indent=2)
        return True
    except Exception as e:
        print(f"Errore salvataggio watchlist: {e}")
        return False
