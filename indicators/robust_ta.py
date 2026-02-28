# indicators/robust_ta.py
import pandas as pd
import pandas_ta as ta
from config import (
    RSI_LEN, ATR_LEN, ADX_LEN, ST_LEN, ST_MULT,
    SQUEEZE_BB_LEN, SQUEEZE_KC_LEN, ADX_MIN,
    RSI_LONG_MAX, RSI_SHORT_MIN,
    WEAK_RSI_LONG_MAX, WEAK_RSI_SHORT_MIN,
    WEAK_ADX_MIN, WEAK_SLOPE_MIN,
    ENABLE_SIGNAL_CLASSIFICATION, WEAK_SIGNALS_ENABLED,
    COLOR_STRONG_LONG, COLOR_WEAK_LONG,
    COLOR_STRONG_SHORT, COLOR_WEAK_SHORT,
    COLOR_NEUTRAL,
    EMOJI_STRONG_LONG, EMOJI_WEAK_LONG,
    EMOJI_STRONG_SHORT, EMOJI_WEAK_SHORT,
    EMOJI_NEUTRAL
)
from utils.helpers import pick_col_by_prefix, safe_last

def compute_indicators_15m(df_15m: pd.DataFrame):
    """Calcola tutti gli indicatori per timeframe 15m"""
    df = df_15m.copy()
    
    # EMA
    df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
    df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
    df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()

    # RSI
    df["rsi"] = ta.rsi(df["close"], length=RSI_LEN)
    
    # ATR
    df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=ATR_LEN)

    # ADX
    adx_df = ta.adx(df["high"], df["low"], df["close"], length=ADX_LEN)
    if isinstance(adx_df, pd.DataFrame) and not adx_df.empty:
        df = df.join(adx_df)

    # SuperTrend
    st_df = ta.supertrend(df["high"], df["low"], df["close"], length=ST_LEN, multiplier=ST_MULT)
    if isinstance(st_df, pd.DataFrame) and not st_df.empty:
        df = df.join(st_df)

    # Squeeze
    sqz_df = ta.squeeze(df["high"], df["low"], df["close"], 
                        bb_length=SQUEEZE_BB_LEN, kc_length=SQUEEZE_KC_LEN)
    if isinstance(sqz_df, pd.DataFrame) and not sqz_df.empty:
        df = df.join(sqz_df)

    return df

def decide_signal(df_ind: pd.DataFrame, mtf_long: bool, mtf_short: bool):
    """
    Decide il segnale con classificazione STRONG/WEAK
    
    Returns:
        dict con chiavi:
        - signal: "LONG", "SHORT", o "NONE"
        - strength: "STRONG", "WEAK", o "NONE"
        - display: testo da mostrare UI
        - color: colore esadecimale
        - emoji: emoji da mostrare
        - is_long: True/False/None
        - rsi, atr, slope, adx, sqz_on: valori indicatori
    """
    # Estrai valori correnti
    p = float(df_ind["close"].iloc[-1])
    ema20 = float(df_ind["ema20"].iloc[-1])
    ema50 = float(df_ind["ema50"].iloc[-1])
    ema200 = float(df_ind["ema200"].iloc[-1])

    rsi = safe_last(df_ind, "rsi", 50.0)
    atr = safe_last(df_ind, "atr", 0.0)

    # Calcola pendenza EMA20
    sw = min(5, len(df_ind) - 1)
    if sw > 0:
        slope = float((df_ind["ema20"].iloc[-1] - df_ind["ema20"].iloc[-sw]) / sw)
    else:
        slope = 0.0

    # Trend di base
    up_15m = (p > ema200) and (ema20 > ema50)
    dw_15m = (p < ema200) and (ema20 < ema50)

    # ADX e DI
    adx_col = pick_col_by_prefix(df_ind, "ADX_")
    dmp_col = pick_col_by_prefix(df_ind, "DMP_")
    dmn_col = pick_col_by_prefix(df_ind, "DMN_")
    
    adx = safe_last(df_ind, adx_col, 0.0)
    dmp = safe_last(df_ind, dmp_col, 0.0)
    dmn = safe_last(df_ind, dmn_col, 0.0)
    
    di_long = (dmp > dmn)
    di_short = (dmn > dmp)

    # SuperTrend
    st_dir_col = pick_col_by_prefix(df_ind, "SUPERTD_")
    st_dir = None
    if st_dir_col:
        try:
            st_dir = int(df_ind[st_dir_col].iloc[-1])
        except Exception:
            st_dir = None
    
    st_long_ok = (st_dir == 1) if st_dir is not None else True
    st_short_ok = (st_dir == -1) if st_dir is not None else True

    # Squeeze
    sqz_on = False
    if "SQZ_ON" in df_ind.columns and pd.notna(df_ind["SQZ_ON"].iloc[-1]):
        sqz_on = bool(int(df_ind["SQZ_ON"].iloc[-1]) == 1)
    elif "NO_SQZ" in df_ind.columns and pd.notna(df_ind["NO_SQZ"].iloc[-1]):
        sqz_on = not bool(int(df_ind["NO_SQZ"].iloc[-1]) == 1)

    # Se la classificazione è disabilitata, usa solo la logica base
    if not ENABLE_SIGNAL_CLASSIFICATION:
        long_ok = up_15m and slope > 0 and rsi <= RSI_LONG_MAX and adx >= ADX_MIN and di_long and st_long_ok and not sqz_on and mtf_long
        short_ok = dw_15m and slope < 0 and rsi >= RSI_SHORT_MIN and adx >= ADX_MIN and di_short and st_short_ok and not sqz_on and mtf_short
        
        if long_ok:
            return {
                'signal': "LONG",
                'strength': "STRONG",
                'display': f"{EMOJI_STRONG_LONG} FORTE ACQUISTO",
                'color': COLOR_STRONG_LONG,
                'emoji': EMOJI_STRONG_LONG,
                'is_long': True,
                'rsi': rsi,
                'atr': atr,
                'slope': slope,
                'adx': adx,
                'sqz_on': sqz_on
            }
        if short_ok:
            return {
                'signal': "SHORT",
                'strength': "STRONG",
                'display': f"{EMOJI_STRONG_SHORT} FORTE VENDITA",
                'color': COLOR_STRONG_SHORT,
                'emoji': EMOJI_STRONG_SHORT,
                'is_long': False,
                'rsi': rsi,
                'atr': atr,
                'slope': slope,
                'adx': adx,
                'sqz_on': sqz_on
            }
        return {
            'signal': "NONE",
            'strength': "NONE",
            'display': f"{EMOJI_NEUTRAL} ATTENDI / LATERALE",
            'color': COLOR_NEUTRAL,
            'emoji': EMOJI_NEUTRAL,
            'is_long': None,
            'rsi': rsi,
            'atr': atr,
            'slope': slope,
            'adx': adx,
            'sqz_on': sqz_on
        }

    # LOGICA COMPLETA CON CLASSIFICAZIONE STRONG/WEAK
    
    # Condizioni per STRONG LONG (più restrittive)
    strong_long = (
        up_15m and 
        slope > 1.0 and              # Pendenza significativa
        rsi <= RSI_LONG_MAX and       # RSI ≤ 55
        adx >= ADX_MIN and             # ADX ≥ 25
        di_long and 
        st_long_ok and 
        not sqz_on and 
        mtf_long
    )
    
    # Condizioni per WEAK LONG (più lasche)
    weak_long = (
        up_15m and 
        slope >= WEAK_SLOPE_MIN and    # Pendenza minima 0.2
        rsi <= WEAK_RSI_LONG_MAX and    # RSI ≤ 65
        adx >= WEAK_ADX_MIN and          # ADX ≥ 20
        di_long and 
        st_long_ok and 
        not sqz_on and 
        mtf_long and
        WEAK_SIGNALS_ENABLED            # Solo se abilitati
    )
    
    # Condizioni per STRONG SHORT
    strong_short = (
        dw_15m and 
        slope < -1.0 and               # Pendenza negativa significativa
        rsi >= RSI_SHORT_MIN and        # RSI ≥ 45
        adx >= ADX_MIN and 
        di_short and 
        st_short_ok and 
        not sqz_on and 
        mtf_short
    )
    
    # Condizioni per WEAK SHORT
    weak_short = (
        dw_15m and 
        slope <= -WEAK_SLOPE_MIN and    # Pendenza negativa minima
        rsi >= WEAK_RSI_SHORT_MIN and    # RSI ≥ 35
        adx >= WEAK_ADX_MIN and 
        di_short and 
        st_short_ok and 
        not sqz_on and 
        mtf_short and
        WEAK_SIGNALS_ENABLED
    )

    # Classificazione con priorità: STRONG > WEAK > NIENTE
    if strong_long:
        return {
            'signal': "LONG",
            'strength': "STRONG",
            'display': f"{EMOJI_STRONG_LONG} FORTE ACQUISTO",
            'color': COLOR_STRONG_LONG,
            'emoji': EMOJI_STRONG_LONG,
            'is_long': True,
            'rsi': rsi,
            'atr': atr,
            'slope': slope,
            'adx': adx,
            'sqz_on': sqz_on
        }
    elif weak_long:
        return {
            'signal': "LONG",
            'strength': "WEAK",
            'display': f"{EMOJI_WEAK_LONG} ACQUISTO DEBOLE",
            'color': COLOR_WEAK_LONG,
            'emoji': EMOJI_WEAK_LONG,
            'is_long': True,
            'rsi': rsi,
            'atr': atr,
            'slope': slope,
            'adx': adx,
            'sqz_on': sqz_on
        }
    elif strong_short:
        return {
            'signal': "SHORT",
            'strength': "STRONG",
            'display': f"{EMOJI_STRONG_SHORT} FORTE VENDITA",
            'color': COLOR_STRONG_SHORT,
            'emoji': EMOJI_STRONG_SHORT,
            'is_long': False,
            'rsi': rsi,
            'atr': atr,
            'slope': slope,
            'adx': adx,
            'sqz_on': sqz_on
        }
    elif weak_short:
        return {
            'signal': "SHORT",
            'strength': "WEAK",
            'display': f"{EMOJI_WEAK_SHORT} VENDITA DEBOLE",
            'color': COLOR_WEAK_SHORT,
            'emoji': EMOJI_WEAK_SHORT,
            'is_long': False,
            'rsi': rsi,
            'atr': atr,
            'slope': slope,
            'adx': adx,
            'sqz_on': sqz_on
        }
    else:
        return {
            'signal': "NONE",
            'strength': "NONE",
            'display': f"{EMOJI_NEUTRAL} ATTENDI / LATERALE",
            'color': COLOR_NEUTRAL,
            'emoji': EMOJI_NEUTRAL,
            'is_long': None,
            'rsi': rsi,
            'atr': atr,
            'slope': slope,
            'adx': adx,
            'sqz_on': sqz_on
        }
