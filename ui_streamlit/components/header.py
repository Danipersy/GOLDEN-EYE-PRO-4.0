# ui_streamlit/components/header.py
import streamlit as st
import pytz
from datetime import datetime
from utils.helpers import get_market_status

def render_header():
    """Renderizza header con badge e info"""
    focus = st.session_state.get('radar_select', st.session_state.watchlist[0] if st.session_state.watchlist else "N/A")
    
    last_update_dt = st.session_state.get('last_update')
    last_update_str = last_update_dt.strftime("%d/%m/%Y %H:%M:%S") if last_update_dt else "N/D"

    last_data_ts = st.session_state.get('last_data_timestamp')
    if last_data_ts:
        tz_it = pytz.timezone("Europe/Rome")
        data_time_str = last_data_ts.astimezone(tz_it).strftime("%H:%M:%S %d/%m/%Y")
    else:
        data_time_str = "N/D"

    src = st.session_state.get('data_source', "N/D")
    if src == "TwelveData":
        source_badge = '<span class="badge source-td">📊 TwelveData</span>'
    elif src == "Yahoo":
        source_badge = '<span class="badge source-yf">📈 Yahoo</span>'
    else:
        source_badge = '<span class="badge source-err">⚠️ N/D</span>'

    market_info = get_market_status(focus, last_data_ts)
    market_badge = f'<span class="badge {market_info["class"]}">{market_info["status"]}</span>'

    st.markdown(f"""
    <div class="main-header">
      <div><b>GOLDEN EYE PRO 2026 ULTIMATE</b> {source_badge} {market_badge}</div>
      <div style="text-align:right;">
        <span class="metric-small">UI: {last_update_str}</span><br>
        <span class="metric-small" style="color:#f0b90b;">📅 Dati: {data_time_str}</span><br>
        <span class="metric-small">Asset: {focus}</span>
      </div>
    </div>
    """, unsafe_allow_html=True)
    
    return focus
