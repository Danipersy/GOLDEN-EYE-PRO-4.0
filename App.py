# App.py - Golden Eye Pro 2026 ULTIMATE
import streamlit as st
import os
from datetime import datetime
from config import TITLE, VERSION, DEFAULT_WATCHLIST, WATCHLIST_FILE
from storage.watchlist_store import load_watchlist
from ui_streamlit.styles import apply_styles
from utils.lazy_loader import lazy
from utils.error_handler import error_handler
# ============================================================
# DIAGNOSI RAPIDA - RIMUOVI DOPO
# ============================================================
if st.button("🔍 TEST SCANNER"):
    st.write("### Test connessione Yahoo...")
    try:
        import yfinance as yf
        ticker = yf.Ticker("BTCUSDT")
        df = ticker.history(period="1mo", interval="15m")
        st.write(f"✅ Yahoo funziona: {len(df)} candles")
    except Exception as e:
        st.error(f"❌ Yahoo errore: {e}")
    
    st.write("### Test pandas_ta...")
    try:
        import pandas_ta as ta
        st.write(f"✅ pandas_ta {ta.__version__} OK")
    except Exception as e:
        st.error(f"❌ pandas_ta errore: {e}")
    
    st.write("### Test configurazione...")
    from config import MIN_DATA_POINTS, MIN_VOLUME
    st.write(f"MIN_DATA_POINTS: {MIN_DATA_POINTS}")
    st.write(f"MIN_VOLUME: {MIN_VOLUME}")
# Configurazione pagina
st.set_page_config(
    page_title=TITLE,
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Applica stili
apply_styles()

# ============================================================
# INIZIALIZZAZIONE SESSION STATE
# ============================================================
if "watchlist" not in st.session_state:
    st.session_state.watchlist = load_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)

if "radar_select" not in st.session_state:
    st.session_state.radar_select = st.session_state.watchlist[0] if st.session_state.watchlist else ""

if "radar_results" not in st.session_state:
    st.session_state.radar_results = []

if "show_neutral_sentiment" not in st.session_state:
    st.session_state.show_neutral_sentiment = False

if "last_update" not in st.session_state:
    st.session_state.last_update = None

if "last_data_timestamp" not in st.session_state:
    st.session_state.last_data_timestamp = None

if "data_source" not in st.session_state:
    st.session_state.data_source = "N/D"

if "validation_log" not in st.session_state:
    st.session_state.validation_log = None

if "open_pos" not in st.session_state:
    st.session_state.open_pos = {
        "direzione": "Long",
        "entry": 0.0,
        "size": 1.0,
        "sl": 0.0,
        "tp": 0.0
    }

if "menu_key" not in st.session_state:
    st.session_state.menu_key = 0

if "debug_mode" not in st.session_state:
    st.session_state.debug_mode = False

# ============================================================
# SIDEBAR - NAVIGAZIONE
# ============================================================
with st.sidebar:
    st.markdown(f"## {TITLE}")
    st.markdown(f"v{VERSION}")
    st.divider()
    
    page = st.radio(
        "Navigazione",
        ["🔍 Trading View", "⚙️ Impostazioni"],  # INFO è nel tab 6
        key="navigation"
    )
    
    st.divider()
    
    # Statistiche rapide
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Watchlist", len(st.session_state.watchlist))
    with col2:
        last = st.session_state.last_update
        st.metric("Ultimo update", last.strftime("%H:%M") if last else "Mai")
    
    # Bottone debug (opzionale)
    if st.button("🔧 Debug Mode", use_container_width=True):
        st.session_state.debug_mode = not st.session_state.debug_mode
        st.rerun()

# ============================================================
# CARICAMENTO PAGINE CON LAZY LOADING
# ============================================================
if page == "🔍 Trading View":
    render_main_view = lazy.get_function('ui_streamlit.pages', 'render_main_view')
    if render_main_view:
        render_main_view()
    else:
        st.error("Errore caricamento pagina Trading View")
else:  # ⚙️ Impostazioni
    render_settings = lazy.get_function('ui_streamlit.pages', 'render_settings')
    if render_settings:
        render_settings()
    else:
        st.error("Errore caricamento impostazioni")

# ============================================================
# DEBUG PANEL (solo se attivato)
# ============================================================
if st.session_state.debug_mode:
    st.sidebar.divider()
    st.sidebar.markdown("### 🔍 DEBUG INFO")
    st.sidebar.write(f"**Asset selezionato:** {st.session_state.radar_select}")
    st.sidebar.write(f"**Menu key:** {st.session_state.menu_key}")
    st.sidebar.write(f"**Scan results:** {len(st.session_state.get('radar_results', []))}")
    
    if st.button("🧪 TEST DATI", key="test_btn"):
        st.sidebar.write("**Watchlist:**", st.session_state.watchlist)
        if st.session_state.get('detail_data'):
            d = st.session_state.detail_data
            st.sidebar.write(f"**Detail:** {d.get('asset')} @ ${d.get('p', 0):.2f}")
    
    error_handler.show_error_summary()
    lazy.show_loading_stats()

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.caption(f"🕒 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
with col_f2:
    st.caption(f"📊 Watchlist: {len(st.session_state.watchlist)} assets")
with col_f3:
    st.caption("⚠️ Educational purpose only")