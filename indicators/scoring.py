# indicators/scoring.py
import numpy as np
from typing import Dict, Any

def calculate_score(signal_data: Dict[str, Any]) -> float:
    """Calcola score di confidenza (0-100)"""
    base_score = 50.0
    
    if signal_data.get('action') in ['BUY', 'SELL']:
        base_score = 60.0
        
        # Bonus per ADX
        adx = signal_data.get('adx', 0)
        base_score += min(20, adx - 20) * 2
        
        # Bonus per trend strength
        trend_strength = signal_data.get('trend_strength', 0)
        base_score += min(15, abs(trend_strength) * 5)
        
        # Penalità per squeeze
        if signal_data.get('sqz_on', False):
            base_score -= 20
    
    return max(0, min(100, base_score))
