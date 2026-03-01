import json
import os
from config import DEFAULT_WATCHLIST, WATCHLIST_FILE

def load_watchlist():
    """Carica la watchlist dal file JSON."""
    if os.path.exists(WATCHLIST_FILE):
        try:
            with open(WATCHLIST_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, list) and data:
                return [str(x).strip().upper() for x in data if str(x).strip()]
        except Exception:
            pass
    return DEFAULT_WATCHLIST.copy()

def save_watchlist(wl):
    """Salva la watchlist su file JSON."""
    try:
        with open(WATCHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(wl, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
