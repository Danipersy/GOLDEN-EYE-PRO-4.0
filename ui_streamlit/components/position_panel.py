# ui_streamlit/components/position_panel.py
import streamlit as st
from datetime import datetime, timedelta

def calculate_position_timeout_from_sl_tp(asset_type: str, atr: float, current_price: float, 
                                          sl: float, tp: float, entry: float) -> dict:
    """
    Calcola tempo stimato basato su SL/TP EFFETTIVI della posizione
    """
    if atr <= 0 or current_price <= 0 or sl <= 0 or tp <= 0:
        return {"ore": "N/D", "chiusura": "N/D", "mercato": "N/D", "color": "#999999"}
    
    # Calcola distanze effettive
    dist_sl = abs(entry - sl)
    dist_tp = abs(tp - entry)
    distanza_minore = min(dist_sl, dist_tp)
    
    if distanza_minore <= 0:
        return {"ore": "N/D", "chiusura": "N/D", "mercato": "N/D", "color": "#999999"}
    
    # Volatilità oraria
    hourly_volatility = atr / 24
    
    if hourly_volatility <= 0:
        return {"ore": "N/D", "chiusura": "N/D", "mercato": "N/D", "color": "#999999"}
    
    # Tempo stimato in ore
    ore_stimate = distanza_minore / hourly_volatility
    ore_stimate = min(ore_stimate, 168)  # Max 7 giorni
    
    # Calcola orario di chiusura
    now = datetime.now()
    expiry = now + timedelta(hours=ore_stimate)
    
    # Determina mercato
    asset_upper = asset_type.upper()
    if "BTC" in asset_upper or "ETH" in asset_upper or "USD" in asset_upper:
        market_hours = "24/7"
    else:
        market_hours = "09:30-16:00"
        if expiry.hour < 9 or expiry.hour > 16:
            expiry = expiry.replace(hour=16, minute=0) if expiry.hour < 9 else expiry
    
    # Colore in base al tempo
    if ore_stimate < 4:
        color = "#ff3344"  # Rosso - breve
    elif ore_stimate < 12:
        color = "#f0b90b"  # Giallo - medio
    else:
        color = "#00ff88"  # Verde - lungo
    
    # Determina cosa è più probabile
    if dist_sl < dist_tp:
        probabilita = f"SL più probabile ({(dist_tp/dist_sl):.1f}:1)"
    else:
        probabilita = f"TP più probabile ({(dist_sl/dist_tp):.1f}:1)"
    
    return {
        "ore": f"{ore_stimate:.1f}h",
        "chiusura": expiry.strftime("%d/%m %H:%M"),
        "mercato": market_hours,
        "color": color,
        "probabilita": probabilita
    }

def render_position_panel(current_price, prec=2, atr_value=0, asset_symbol=""):
    """Renderizza pannello gestione posizione con stima tempo"""
    
    current_asset = st.session_state.get('radar_select', asset_symbol or "")
    
    st.markdown("---")
    st.markdown("## 💼 Gestione Posizione")

    with st.expander("Apri pannello posizione", expanded=False):
        # RIMOSSO IL BOTTONE RESET DA QUI - ERA DUPLICATO
        
        c1, c2 = st.columns(2)
        
        open_pos = st.session_state.get('open_pos', {
            "direzione": "Long",
            "entry": 0.0,
            "size": 1.0,
            "sl": 0.0,
            "tp": 0.0
        })
        
        with c1:
            direzione = st.selectbox(
                "Direzione",
                ["Long", "Short"],
                index=0 if open_pos.get("direzione", "Long") == "Long" else 1,
                key="pos_direction_unique"  # Chiave unica
            )
            
            entry_pos = st.number_input(
                "Entry",
                min_value=0.0,
                value=float(open_pos.get("entry", 0) or current_price),
                format=f"%.{prec}f",
                key="pos_entry_unique"  # Chiave unica
            )
            
            size_pos = st.number_input(
                "Size",
                min_value=0.0,
                value=float(open_pos.get("size", 1.0) or 1.0),
                format="%.4f",
                key="pos_size_unique"  # Chiave unica
            )
        
        with c2:
            sl_pos = st.number_input(
                "Stop Loss",
                min_value=0.0,
                value=float(open_pos.get("sl", 0) or 0.0),
                format=f"%.{prec}f",
                key="pos_sl_unique"  # Chiave unica
            )
            
            tp_pos = st.number_input(
                "Take Profit",
                min_value=0.0,
                value=float(open_pos.get("tp", 0) or 0.0),
                format=f"%.{prec}f",
                key="pos_tp_unique"  # Chiave unica
            )
            
            # AGGIUNTO BOTTONE RESET QUI (solo uno!)
            if st.button("🔄 Reset Posizione", key="reset_position_unique", use_container_width=True):
                st.session_state.open_pos = {
                    "direzione": "Long",
                    "entry": 0.0,
                    "size": 1.0,
                    "sl": 0.0,
                    "tp": 0.0
                }
                st.rerun()

        # Salva in session state
        st.session_state.open_pos = {
            "direzione": direzione,
            "entry": entry_pos,
            "size": size_pos,
            "sl": sl_pos,
            "tp": tp_pos
        }

        # Calcolo PnL
        if entry_pos and size_pos and current_price and current_price > 0:
            if direzione == "Long":
                pnl = (current_price - entry_pos) * size_pos
                pnl_pct = ((current_price - entry_pos) / entry_pos * 100) if entry_pos > 0 else 0
            else:
                pnl = (entry_pos - current_price) * size_pos
                pnl_pct = ((entry_pos - current_price) / entry_pos * 100) if entry_pos > 0 else 0
            
            col_pnl1, col_pnl2, col_pnl3 = st.columns(3)
            with col_pnl1:
                st.metric("PnL", value=f"{pnl:+.4f}", delta=f"{pnl_pct:+.2f}%")
            with col_pnl2:
                st.caption(f"Asset: {current_asset}")
            with col_pnl3:
                st.caption(f"Prezzo: {current_price:.{prec}f}")
            
            # Stima tempo
            if sl_pos > 0 and tp_pos > 0 and atr_value > 0 and entry_pos > 0:
                timeout = calculate_position_timeout_from_sl_tp(
                    current_asset, 
                    atr_value,
                    current_price,
                    sl_pos,
                    tp_pos,
                    entry_pos
                )
                
                st.markdown(f"""
                <div style='
                    margin-top: 15px;
                    padding: 15px;
                    border-radius: 12px;
                    background: linear-gradient(90deg, {timeout['color']}15, {timeout['color']}05);
                    border: 1px solid {timeout['color']}40;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                '>
                    <div>
                        <span style='color:#94a3b8; font-size:0.8rem;'>⏱️ TEMPO STIMATO</span>
                        <div style='font-size:1.4rem; font-weight:700; color:{timeout['color']};'>
                            {timeout['ore']}
                        </div>
                        <div style='font-size:0.8rem; color:#94a3b8;'>
                            {timeout['probabilita']}
                        </div>
                    </div>
                    <div style='text-align:right;'>
                        <span style='color:#94a3b8; font-size:0.8rem;'>📅 CHIUSURA</span>
                        <div style='font-size:1.1rem; font-weight:600;'>
                            {timeout['chiusura']}
                        </div>
                        <div style='font-size:0.7rem; color:#94a3b8;'>
                            {timeout['mercato']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if timeout['ore'] != "N/D":
                    ore_float = float(timeout['ore'].replace('h',''))
                    if ore_float < 2:
                        st.warning("⚠️ Posizione molto rapida - tieni sotto controllo!")
                    elif ore_float > 48:
                        st.info("📊 Posizione a lungo termine - considera trailing stop")
