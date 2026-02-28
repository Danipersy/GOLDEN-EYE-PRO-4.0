# ui_streamlit/pages/test.py
import streamlit as st
import platform
import sys
from datetime import datetime
from providers.multi_provider import scan_symbol
from providers.twelvedata_provider import fetch_td_15m, convert_symbol_for_twelvedata

def render():
    """Pagina Test e Debug"""
    
    st.markdown("## 🧪 Test e Debug")
    st.caption("Verifica il corretto funzionamento di tutti i componenti")
    
    # TEST RAPIDI
    st.markdown("### ⚡ Test Rapidi")
    col_q1, col_q2, col_q3, col_q4 = st.columns(4)
    
    with col_q1:
        if st.button("📊 Test BTC-USD", use_container_width=True, key="test_btc"):
            result = scan_symbol("BTC-USD", "15m", "1d")
            if result and 'error' not in result:
                st.success(f"BTC: ${result['price']:.2f} ({result['change']:+.2f}%)")
            else:
                st.error("❌ Fallito")
    
    with col_q2:
        if st.button("📊 Test ETH-USD", use_container_width=True, key="test_eth"):
            result = scan_symbol("ETH-USD", "15m", "1d")
            if result and 'error' not in result:
                st.success(f"ETH: ${result['price']:.2f} ({result['change']:+.2f}%)")
            else:
                st.error("❌ Fallito")
    
    with col_q3:
        if st.button("📊 Test AAPL", use_container_width=True, key="test_aapl"):
            result = scan_symbol("AAPL", "15m", "1d")
            if result and 'error' not in result:
                st.success(f"AAPL: ${result['price']:.2f} ({result['change']:+.2f}%)")
            else:
                st.error("❌ Fallito")
    
    with col_q4:
        if st.button("📊 Test MSFT", use_container_width=True, key="test_msft"):
            result = scan_symbol("MSFT", "15m", "1d")
            if result and 'error' not in result:
                st.success(f"MSFT: ${result['price']:.2f} ({result['change']:+.2f}%)")
            else:
                st.error("❌ Fallito")
    
    st.markdown("---")
    
    # TEST AVANZATI
    col_test1, col_test2 = st.columns(2)
    
    with col_test1:
        # TEST PROVIDER
        with st.container(border=True):
            st.markdown("### 📡 Test Provider")
            
            col_y, col_td = st.columns(2)
            
            with col_y:
                if st.button("🟢 Test Yahoo", use_container_width=True, key="test_yahoo"):
                    try:
                        import yfinance as yf
                        ticker = yf.Ticker("BTC-USD")
                        df = ticker.history(period="1d", interval="15m")
                        if df is not None and not df.empty:
                            st.success(f"✅ Yahoo OK: {len(df)} candles")
                        else:
                            st.error("❌ Yahoo: nessun dato")
                    except Exception as e:
                        st.error(f"❌ Errore: {str(e)[:50]}...")
            
            with col_td:
                if st.button("🔵 Test TwelveData", use_container_width=True, key="test_td"):
                    df, src = fetch_td_15m("BTC-USD")
                    if df is not None:
                        st.success(f"✅ TwelveData OK: {len(df)} candles")
                    else:
                        st.error(f"❌ TwelveData: {src}")
        
        # TEST CONVERSIONE
        with st.container(border=True):
            st.markdown("### 🔄 Test Conversione")
            test_symbol = st.text_input("Simbolo", value="BTC-USD", key="test_symbol")
            if st.button("🔄 Converti", use_container_width=True):
                converted = convert_symbol_for_twelvedata(test_symbol)
                st.info(f"📌 {test_symbol} → {converted}")
                df, src = fetch_td_15m(test_symbol)
                if df is not None:
                    st.success(f"✅ Successo: {len(df)} candles")
                else:
                    st.error(f"❌ Fallito: {src}")
    
    with col_test2:
        # DEBUG MODE
        with st.container(border=True):
            st.markdown("### 🐛 Debug Mode")
            if st.button("🔄 Toggle Debug Mode", use_container_width=True, key="debug_toggle"):
                st.session_state.debug_mode = not st.session_state.debug_mode
                st.rerun()
            if st.session_state.debug_mode:
                st.success("✅ Debug Mode: ATTIVO")
            else:
                st.info("⚪ Debug Mode: DISATTIVO")
        
        # STATO SESSIONE
        with st.container(border=True):
            st.markdown("### 🔍 Stato Sessione")
            st.json({
                "watchlist_size": len(st.session_state.watchlist),
                "radar_select": st.session_state.radar_select,
                "scan_results": len(st.session_state.radar_results),
                "debug_mode": st.session_state.debug_mode,
                "menu_key": st.session_state.get('menu_key', 0),
                "app_uptime": str(datetime.now() - st.session_state.app_start_time).split('.')[0]
            })
    
    # TEST SISTEMA
    st.markdown("### 🔧 Test Sistema")
    col_sys1, col_sys2, col_sys3, col_sys4 = st.columns(4)
    
    with col_sys1:
        if st.button("🧪 Test Cache", use_container_width=True):
            from providers.multi_provider import _data_cache
            st.write(f"Items in cache: {len(_data_cache)}")
    
    with col_sys2:
        if st.button("🧪 Test Watchlist", use_container_width=True):
            st.write(f"Items: {len(st.session_state.watchlist)}")
            st.write(f"Primi 5: {st.session_state.watchlist[:5]}")
    
    with col_sys3:
        if st.button("🧪 Test Session", use_container_width=True):
            keys = list(st.session_state.keys())
            st.write(f"Total keys: {len(keys)}")
            st.write(f"Keys: {keys[:10]}...")
    
    with col_sys4:
        if st.button("🧪 Test Python", use_container_width=True):
            st.write(f"Python: {sys.version[:30]}...")
            st.write(f"Platform: {platform.platform()}")
