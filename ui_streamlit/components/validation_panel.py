# ui_streamlit/components/validation_panel.py
import streamlit as st
import pandas as pd
from datetime import datetime, timezone

def validate_data_quality(df_15m, df_1h, df_4h):
    """Valida qualità dati"""
    issues, warnings, ok = [], [], []
    
    if df_15m is None or len(df_15m) < 210:
        issues.append(f"❌ Storico 15m insufficiente: {0 if df_15m is None else len(df_15m)} (min 210)")
    else:
        ok.append(f"✅ Storico 15m OK: {len(df_15m)} candele")

    if df_15m is not None and len(df_15m) > 5:
        diffs = df_15m["datetime"].diff().dt.total_seconds() / 60
        gaps = int((diffs > 30).sum())
        if gaps > 5:
            warnings.append(f"⚠️ Gap temporali: {gaps}")
        else:
            ok.append(f"✅ Continuità OK (gap: {gaps})")

        invalid_ohlc = int(
            ((df_15m["high"] < df_15m["low"]) |
             (df_15m["close"] > df_15m["high"]) |
             (df_15m["close"] < df_15m["low"])).sum()
        )
        if invalid_ohlc:
            issues.append(f"❌ OHLC inconsistente: {invalid_ohlc}")
        else:
            ok.append("✅ Coerenza OHLC OK")

        last_candle = df_15m["datetime"].iloc[-1]
        age_min = (datetime.now(timezone.utc) - last_candle).total_seconds() / 60
        if age_min > 60:
            warnings.append(f"⚠️ Ultimo dato vecchio: {int(age_min)}m")
        else:
            ok.append(f"✅ Dati freschi: {int(age_min)}m")

    if df_1h is None:
        warnings.append("⚠️ 1H non caricato")
    elif len(df_1h) >= 60:
        ok.append(f"✅ 1H OK: {len(df_1h)}")
    else:
        warnings.append(f"⚠️ 1H corto: {len(df_1h)}")

    if df_4h is None:
        warnings.append("⚠️ 4H non caricato")
    elif len(df_4h) >= 40:
        ok.append(f"✅ 4H OK: {len(df_4h)}")
    else:
        warnings.append(f"⚠️ 4H corto: {len(df_4h)}")

    denom = (len(ok) + len(warnings) + len(issues))
    score = (len(ok) / denom * 100) if denom else 0.0
    
    return {
        "issues": issues,
        "warnings": warnings,
        "ok": ok,
        "quality_score": score
    }

def render_validation_panel(val):
    """Renderizza pannello validazione"""
    if not val:
        return
    
    score = val["quality_score"]
    
    if score >= 80:
        css_class, icon, status_text = "validation-ok", "✅", "ECCELLENTE"
    elif score >= 60:
        css_class, icon, status_text = "validation-warn", "⚠️", "ACCETTABILE"
    else:
        css_class, icon, status_text = "validation-error", "❌", "DUBBIO"

    with st.expander(f"{icon} Validazione Dati - Qualità: {score:.0f}% ({status_text})"):
        st.markdown(f'<div class="{css_class}"><b>QUALITÀ DATI: {score:.1f}%</b></div>', unsafe_allow_html=True)
        
        for item in val.get("ok", []):
            st.markdown(f"- {item}")
        
        if val.get("warnings"):
            st.markdown("**⚠️ Attenzioni:**")
            for item in val["warnings"]:
                st.markdown(f"- {item}")
        
        if val.get("issues"):
            st.markdown("**❌ Problemi critici:**")
            for item in val["issues"]:
                st.markdown(f"- {item}")
