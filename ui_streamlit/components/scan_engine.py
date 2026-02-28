# ui_streamlit/components/scan_engine.py
import time
import numpy as np
import pandas as pd
import streamlit as st
from typing import List, Dict, Any, Optional, Tuple, Callable
from datetime import datetime

from config import (
    TTL_YF, YF_15M_PERIOD, YF_15M_INTERVAL,
    SL_ATR, TP_ATR, ADX_MIN, RSI_LONG_MAX, RSI_SHORT_MIN, SCORE_FORTE_MIN
)
from providers.yahoo_provider import fetch_yahoo_ohlcv
from indicators.robust_ta import compute_basic_ta
from ui_streamlit.components.indicators import atr_wilder_last, rischio_stopout

def _norm_ohlcv(df: pd.DataFrame) -> pd.DataFrame:
    """Normalizza colonne OHLCV"""
    if df is None or df.empty:
        return df
    
    out = df.copy()
    out.columns = [str(c).strip().lower() for c in out.columns]
    
    # Gestione indice
    if "time" not in out.columns and out.index.name:
        out = out.reset_index()
        out.columns = [str(c).strip().lower() for c in out.columns]
    
    # Rinomina colonne comuni
    rename_map = {
        'open': 'open', 'high': 'high', 'low': 'low',
        'close': 'close', 'volume': 'volume',
        'adj close': 'close', 'adj_close': 'close'
    }
    
    for old, new in rename_map.items():
        if old in out.columns and new not in out.columns:
            out = out.rename(columns={old: new})
    
    return out

@st.cache_data(ttl=TTL_YF)
def cached_yahoo_fast(symbol: str, period: str, interval: str) -> Optional[pd.DataFrame]:
    """Versione cached di fetch_yahoo_ohlcv"""
    return fetch_yahoo_ohlcv(symbol, period=period, interval=interval)

def _compute_signal(sym: str, df: pd.DataFrame) -> Dict[str, Any]:
    """Calcola segnale per un asset"""
    if df is None or len(df) < 30:
        return {
            "asset": sym,
            "azione": "NO_DATA",
            "score": 0,
            "TRADE_OK": False,
            "last": 0,
            "sl": None,
            "tp": None,
            "rischio_sl": "N/D",
            "flow": None,
            "atr": 0,
            "rsi": 0,
            "adx": 0
        }
    
    try:
        ta = compute_basic_ta(df)
        if not ta:
            raise ValueError("No TA data")
        
        last = float(df['close'].iloc[-1])
        ema20 = float(ta['ema_fast'].iloc[-1])
        ema200 = float(ta['ema_trend'].iloc[-1])
        rsi = float(ta['rsi'].iloc[-1])
        adx = float(ta['adx'].iloc[-1])
        
        # Calcola ATR
        atr = atr_wilder_last(df)
        
        action = "WAIT"
        flow = None
        score = 50.0
        
        # Condizioni LONG
        if adx >= ADX_MIN:
            if last > ema200 and ema20 > ema200 and rsi < RSI_LONG_MAX:
                action = "BUY"
                flow = "LONG"
            elif last < ema200 and ema20 < ema200 and rsi > RSI_SHORT_MIN:
                action = "SELL"
                flow = "SHORT"
        
        # Calcolo score
        if action != "WAIT":
            score = 60.0
            dist = abs(last - ema200) / ema200 * 100
            score += min(20, dist)
            score += min(20, adx - ADX_MIN)
        
        score = max(0, min(100, score))
        trade_ok = score >= SCORE_FORTE_MIN
        
        # SL/TP
        sl = None
        tp = None
        if atr > 0 and flow:
            if flow == "LONG":
                sl = last - (SL_ATR * atr)
                tp = last + (TP_ATR * atr)
            else:
                sl = last + (SL_ATR * atr)
                tp = last - (TP_ATR * atr)
        
        # Livello rischio
        rischio_sl = "N/D"
        if sl:
            stop_dist = abs(last - sl) / last * 100
            if stop_dist < 1.5:
                rischio_sl = "ALTO"
            elif stop_dist < 3.0:
                rischio_sl = "MEDIO"
            else:
                rischio_sl = "BASSO"
        
        return {
            "asset": sym,
            "azione": action,
            "score": score,
            "TRADE_OK": trade_ok,
            "last": last,
            "sl": sl,
            "tp": tp,
            "rischio_sl": rischio_sl,
            "flow": flow,
            "atr": atr,
            "rsi": rsi,
            "adx": adx
        }
        
    except Exception as e:
        return {
            "asset": sym,
            "azione": "ERROR",
            "score": 0,
            "TRADE_OK": False,
            "last": 0,
            "sl": None,
            "tp": None,
            "rischio_sl": "N/D",
            "flow": None,
            "atr": 0,
            "rsi": 0,
            "adx": 0,
            "error": str(e)
        }

def run_scan(assets: List[str], refresh_tick: int = 0, f: Optional[Dict] = None) -> pd.DataFrame:
    """Esegue scan completo"""
    rows = []
    total = len(assets)
    
    for i, sym in enumerate(assets, 1):
        try:
            df = cached_yahoo_fast(sym, period=YF_15M_PERIOD, interval=YF_15M_INTERVAL)
            
            if df is None or df.empty:
                rows.append({
                    "asset": sym,
                    "azione": "NO_DATA",
                    "score": 0,
                    "TRADE_OK": False,
                    "rischio_sl": "N/D",
                    "last": 0,
                    "sl": None,
                    "tp": None,
                    "flow": None,
                    "atr": 0,
                    "rsi": 0,
                    "adx": 0
                })
                continue
            
            df = _norm_ohlcv(df)
            signal = _compute_signal(sym, df)
            rows.append(signal)
            
        except Exception as e:
            rows.append({
                "asset": sym,
                "azione": "ERROR",
                "score": 0,
                "TRADE_OK": False,
                "rischio_sl": "N/D",
                "last": 0,
                "sl": None,
                "tp": None,
                "flow": None,
                "atr": 0,
                "rsi": 0,
                "adx": 0,
                "error": str(e)
            })
    
    return pd.DataFrame(rows)

def apply_ui_filters(df: pd.DataFrame, f: Dict) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Applica filtri UI"""
    if df is None or df.empty:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    
    df_raw = df.copy()
    df_filtered = df_raw.copy()
    flags = []
    
    for idx, row in df_raw.iterrows():
        kept = True
        reasons = []
        
        # Filtro TRADE_OK
        if f.get('only_trade_ok', False) and not row.get('TRADE_OK', False):
            kept = False
            reasons.append("trade_ok_false")
        
        # Filtro azione
        show_wait = f.get('show_wait', True)
        action = row.get('azione', '')
        
        if action == 'WAIT' and not show_wait:
            kept = False
            reasons.append("wait_excluded")
        elif action == 'ERROR' and not f.get('show_error', False):
            kept = False
            reasons.append("error_excluded")
        elif action == 'NO_DATA' and not f.get('show_nodata', False):
            kept = False
            reasons.append("nodata_excluded")
        
        # Filtro score minimo
        min_score = f.get('min_score', 0)
        if min_score > 0 and row.get('score', 0) < min_score:
            kept = False
            reasons.append(f"score<{min_score}")
        
        flags.append({
            'asset': row.get('asset', ''),
            'kept': kept,
            'reasons': ', '.join(reasons),
            'action': action,
            'score': row.get('score', 0)
        })
    
    flags_df = pd.DataFrame(flags)
    
    # Applica filtri
    if not df_filtered.empty:
        kept_assets = flags_df[flags_df['kept']]['asset'].tolist()
        df_filtered = df_filtered[df_filtered['asset'].isin(kept_assets)]
    
    # Ordina per score
    if 'score' in df_filtered.columns and not df_filtered.empty:
        df_filtered = df_filtered.sort_values('score', ascending=False)
    
    return df_raw, df_filtered, flags_df

def pick_best(df: pd.DataFrame) -> Tuple[Dict, str, str]:
    """Seleziona il miglior segnale"""
    if df is None or df.empty:
        return {}, "", "NO_DATA"
    
    # Priorità a TRADE_OK
    if 'TRADE_OK' in df.columns:
        ok_df = df[df['TRADE_OK'] == True]
        if not ok_df.empty:
            best = ok_df.iloc[0].to_dict()
            return best, str(best.get('asset', '')), str(best.get('azione', 'WAIT'))
    
    best = df.iloc[0].to_dict()
    return best, str(best.get('asset', '')), str(best.get('azione', 'WAIT'))
