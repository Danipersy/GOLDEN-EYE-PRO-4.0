# ui_streamlit/components/indicators.py
import numpy as np
import pandas as pd
from typing import Dict, Any, Optional

def atr_wilder_last(df: pd.DataFrame, period: int = 14) -> float:
    """Calcola l'ultimo valore ATR"""
    if df is None or df.empty or len(df) < period + 5:
        return 0.0
    
    # Assicura che ci siano le colonne necessarie
    high = df['high'].values if 'high' in df.columns else df['close'].values
    low = df['low'].values if 'low' in df.columns else df['close'].values
    close = df['close'].values
    
    tr = np.zeros_like(close)
    tr[0] = high[0] - low[0]
    
    for i in range(1, len(close)):
        tr[i] = max(
            high[i] - low[i],
            abs(high[i] - close[i-1]),
            abs(low[i] - close[i-1])
        )
    
    atr = np.zeros_like(close)
    atr[period-1] = np.mean(tr[:period])
    
    for i in range(period, len(close)):
        atr[i] = (atr[i-1] * (period-1) + tr[i]) / period
    
    return float(atr[-1]) if len(atr) > 0 else 0.0

def rischio(entry: Optional[float], sl: Optional[float], tp: Optional[float], atr: float = 0.0) -> Dict[str, Any]:
    """Calcola metriche di rischio"""
    out = {"r": 0.0, "rr": 0.0, "atr": float(atr or 0.0)}
    
    if entry is None or entry == 0:
        return out
    
    if sl is not None and sl != 0:
        risk_abs = abs(entry - sl)
        out["r"] = float((risk_abs / abs(entry)) * 100.0)
        
        if tp is not None and tp != 0:
            reward_abs = abs(tp - entry)
            out["rr"] = float(reward_abs / risk_abs) if risk_abs > 0 else 0.0
    
    return out

def rischio_stopout(entry: Optional[float], sl: Optional[float], last: Optional[float] = None,
                   atr: float = 0.0, flow: Optional[str] = None) -> Dict[str, Any]:
    """Verifica se lo stop è stato hit"""
    out = {"stop_dist_pct": 0.0, "stop_dist_atr": 0.0, "stop_hit": False}
    
    if entry is None or entry == 0 or sl is None:
        return out
    
    ref = last if last is not None and last != 0 else entry
    
    dist_abs = abs(ref - sl)
    out["stop_dist_pct"] = float((dist_abs / abs(ref)) * 100.0)
    
    if atr > 0:
        out["stop_dist_atr"] = float(dist_abs / atr)
    
    if last is not None and flow:
        if flow.upper() == "LONG":
            out["stop_hit"] = bool(last <= sl)
        elif flow.upper() == "SHORT":
            out["stop_hit"] = bool(last >= sl)
    
    return out

def tp_eta_minutes(last: Optional[float], tp: Optional[float], atr: float,
                  minutes_per_bar: int = 15, speed_atr_per_bar: float = 0.35) -> Optional[int]:
    """Stima tempo per raggiungere TP"""
    if last is None or tp is None or atr <= 0:
        return None
    
    dist = abs(tp - last)
    if dist <= 0:
        return 0
    
    per_bar = atr * speed_atr_per_bar
    if per_bar <= 0:
        return None
    
    bars = dist / per_bar
    return int(round(bars * minutes_per_bar))
