# strategy/backtest.py
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from indicators.robust_ta import compute_indicators_15m, decide_signal
from utils.helpers import pick_col_by_prefix
from config import (
    BT_SL_ATR, BT_TP_ATR, ADX_MIN, RSI_LONG_MAX, RSI_SHORT_MIN,
    STRONG_SL_ATR, STRONG_TP_ATR, WEAK_SL_ATR, WEAK_TP_ATR,
    POSITION_SIZE_PCT
)

def backtest_engine(df_15m: pd.DataFrame, use_mtf: bool, df_1h=None, df_4h=None):
    """Motore di backtest completo con supporto weak/strong signals"""
    if df_15m is None or len(df_15m) < 260:
        return None

    # Inizializzazione serie MTF
    mtf_long_series = pd.Series(True, index=df_15m.index)
    mtf_short_series = pd.Series(True, index=df_15m.index)

    if use_mtf and df_1h is not None and df_4h is not None and not df_1h.empty and not df_4h.empty:
        df1 = df_1h.copy().set_index("datetime")
        df4 = df_4h.copy().set_index("datetime")
        
        # Logica Trend MTF
        ema1h = df1["close"].ewm(span=50, adjust=False).mean()
        up_1h = (df1["close"] > ema1h)
        
        ema4h = df4["close"].ewm(span=20, adjust=False).mean()
        up_4h = (df4["close"] > ema4h)

        # Riallineamento timeframe su 15m
        df1m = pd.DataFrame({"up_1h": up_1h}, index=df1.index).resample("15min").ffill()
        df4m = pd.DataFrame({"up_4h": up_4h}, index=df4.index).resample("15min").ffill()

        df15 = df_15m.set_index("datetime")
        joined = df15.join(df1m, how="left").join(df4m, how="left")
        joined["up_1h"] = joined["up_1h"].ffill().fillna(False)
        joined["up_4h"] = joined["up_4h"].ffill().fillna(False)

        mtf_long_series = (joined["up_1h"] & joined["up_4h"]).reset_index(drop=True)
        mtf_short_series = ((~joined["up_1h"]) & (~joined["up_4h"])).reset_index(drop=True)

    # Calcolo indicatori su 15m
    df_ind = compute_indicators_15m(df_15m)
    
    # Aggiungi colonne per tracciare la forza del segnale
    df_ind['signal_strength'] = 'none'
    df_ind['signal_type'] = 'none'

    adx_col = pick_col_by_prefix(df_ind, "ADX_")
    dmp_col = pick_col_by_prefix(df_ind, "DMP_")
    dmn_col = pick_col_by_prefix(df_ind, "DMN_")
    st_dir_col = pick_col_by_prefix(df_ind, "SUPERTD_")

    in_pos = False
    side = None
    entry = sl = tp = None
    trades = []
    current_signal_info = None  # Per tracciare info del segnale corrente
    capital = 10000  # Capitale iniziale fittizio per calcoli

    for i in range(len(df_ind)):
        if i < 210:
            continue

        p_close = float(df_ind["close"].iloc[i])
        p_high = float(df_ind["high"].iloc[i])
        p_low = float(df_ind["low"].iloc[i])
        ts = df_ind["datetime"].iloc[i]
        atr = float(df_ind["atr"].iloc[i])

        # Ottieni info segnale per questo punto
        signal_info = decide_signal(
            df_ind.iloc[:i+1],  # Dati fino a questo punto
            mtf_long_series.iloc[i] if i < len(mtf_long_series) else True,
            mtf_short_series.iloc[i] if i < len(mtf_short_series) else True
        )
        
        # Salva nel dataframe
        df_ind.loc[df_ind.index[i], 'signal_strength'] = signal_info['strength']
        df_ind.loc[df_ind.index[i], 'signal_type'] = signal_info['signal']

        # Gestione uscita
        if in_pos:
            exit_price = None
            exit_reason = None

            if side == "LONG":
                if p_low <= sl:
                    exit_price, exit_reason = sl, "SL"
                elif p_high >= tp:
                    exit_price, exit_reason = tp, "TP"
            else:  # SHORT
                if p_high >= sl:
                    exit_price, exit_reason = sl, "SL"
                elif p_low <= tp:
                    exit_price, exit_reason = tp, "TP"

            if exit_price is not None:
                pnl = (exit_price - entry) if side == "LONG" else (entry - exit_price)
                pnl_pct = (pnl / entry) * 100
                
                trades.append({
                    "time_exit": ts,
                    "side": side,
                    "entry": entry,
                    "exit": exit_price,
                    "reason": exit_reason,
                    "pnl_pct": pnl_pct,
                    "signal_strength": current_signal_info['strength'] if current_signal_info else 'unknown',
                    "signal_type": current_signal_info['signal'] if current_signal_info else 'unknown',
                    "rsi_entry": current_signal_info['rsi'] if current_signal_info else None,
                    "adx_entry": current_signal_info['adx'] if current_signal_info else None,
                    "slope_entry": current_signal_info['slope'] if current_signal_info else None,
                    "atr_entry": atr
                })
                in_pos = False
                side = entry = sl = tp = None
                current_signal_info = None
            
            continue

        # Gestione entrata - usa signal_info
        if signal_info['signal'] in ["LONG", "SHORT"]:
            # Determina moltiplicatori SL/TP in base alla forza
            if signal_info['strength'] == "STRONG":
                sl_mult = STRONG_SL_ATR
                tp_mult = STRONG_TP_ATR
            elif signal_info['strength'] == "WEAK":
                sl_mult = WEAK_SL_ATR
                tp_mult = WEAK_TP_ATR
            else:
                sl_mult = BT_SL_ATR
                tp_mult = BT_TP_ATR

            # Calcola dimensione posizione (simulata)
            position_size = capital * POSITION_SIZE_PCT
            quantity = position_size / p_close if p_close > 0 else 0

            in_pos = True
            side = signal_info['signal']
            entry = p_close
            current_signal_info = signal_info.copy() if signal_info else None
            
            if side == "LONG":
                sl = entry - (atr * sl_mult)
                tp = entry + (atr * tp_mult)
            else:  # SHORT
                sl = entry + (atr * sl_mult)
                tp = entry - (atr * tp_mult)

    # Report
    tdf = pd.DataFrame(trades)
    if tdf.empty:
        return {
            "trades": tdf, 
            "stats": {
                "n": 0, 
                "wins": 0,
                "winrate": 0, 
                "avg_pnl_pct": 0, 
                "total_pnl_pct": 0
            }
        }

    wins = int((tdf["pnl_pct"] > 0).sum())
    n = len(tdf)
    
    # Statistiche per tipo segnale
    strong_trades = tdf[tdf['signal_strength'] == 'STRONG'] if 'signal_strength' in tdf.columns else pd.DataFrame()
    weak_trades = tdf[tdf['signal_strength'] == 'WEAK'] if 'signal_strength' in tdf.columns else pd.DataFrame()
    
    stats = {
        "n": n,
        "wins": wins,
        "winrate": (wins / n) * 100 if n > 0 else 0,
        "avg_pnl_pct": float(tdf["pnl_pct"].mean()),
        "total_pnl_pct": float(tdf["pnl_pct"].sum()),
        "strong_trades": len(strong_trades),
        "strong_winrate": (len(strong_trades[strong_trades["pnl_pct"] > 0]) / len(strong_trades) * 100) if len(strong_trades) > 0 else 0,
        "weak_trades": len(weak_trades),
        "weak_winrate": (len(weak_trades[weak_trades["pnl_pct"] > 0]) / len(weak_trades) * 100) if len(weak_trades) > 0 else 0,
    }
    
    return {"trades": tdf, "stats": stats, "df_indicators": df_ind}

def load_history_for_backtest(symbol: str, days: int, source: str, fetch_yf, fetch_td_15m):
    """Carica storico per backtest"""
    if source == "Yahoo (gratis)":
        period = f"{days}d"
        return fetch_yf(symbol, "15m", period, tail=days*24*4), "Yahoo"
    else:
        df_15m, src = fetch_td_15m(symbol)
        if df_15m is not None and len(df_15m) >= days*24*4:
            df_15m = df_15m.tail(days*24*4)
        return df_15m, src or "TwelveData"
    return None, "ERROR"
