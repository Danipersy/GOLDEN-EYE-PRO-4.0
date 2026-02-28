# strategy/scoring.py
import numpy as np
from typing import Dict, Any

def calculate_score(signal: Dict[str, Any]) -> float:
    """
    Calcola score (placeholder - da implementare)
    """
    return signal.get('score', 50.0)
