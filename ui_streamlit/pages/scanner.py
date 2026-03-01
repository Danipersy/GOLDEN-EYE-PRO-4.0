import streamlit as st
import pandas as pd
from providers.market_scanner import market_scanner
from providers.multi_scanner import multi_scanner
from ui_streamlit.components.scan_filters import render_scan_filters

def show_page():
    st.subheader("🔎 Market Scanner - Top Movers")
    st.caption("Cerca i migliori e peggiori performer del mercato in tempo reale")
    
    # Verifica chiave Finnhub
    finnhub_key = st.secrets.get("FINNHUB_KEY", "") or st.session_state.get('finnhub_key', '')
    if not finnhub_key:
        st.warning("⚠️ Chiave Finnhub non trovata. Aggiungila in Configurazione per dati real-time.")
    
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Top Gainers", "📉 Top Losers", "📊 Most Active", "🔍 Scanner Personalizzato"])
    
    filters = render_scan_filters()
    
    col1, col2 = st.columns([3, 1])
    with col2:
        use_finnhub = st.checkbox("Usa Finnhub (real-time)", value=True)
    
    if st.button("🚀 Avvia scansione mercato", use_container_width=True, type="primary"):
        with st.spinner("Scansionando i mercati..."):
            results = market_scanner.scan_top_movers(limit=30)
            
            if results['gainers']:
                with tab1:
                    st.subheader("📈 Top Gainers")
                    df = pd.DataFrame(results['gainers'])
                    st.dataframe(
                        df[['symbol', 'name', 'price', 'change', 'volume', 'sector']],
                        column_config={
                            "symbol": "Simbolo",
                            "name": "Nome",
                            "price": st.column_config.NumberColumn("Prezzo", format="$%.2f"),
                            "change": st.column_config.NumberColumn("Variazione %", format="%+.2f%%"),
                            "volume": st.column_config.NumberColumn("Volume", format="%d"),
                            "sector": "Settore"
                        },
                        use_container_width=True
                    )
                    
                    # Aggiungi alla watchlist
                    for r in results['gainers'][:5]:
                        cols = st.columns([2, 1, 1, 1])
                        with cols[0]:
                            st.write(f"**{r['symbol']}**")
                        with cols[1]:
                            st.write(f"${r['price']:.2f}")
                        with cols[2]:
                            st.write(f"{r['change']:+.2f}%")
                        with cols[3]:
                            if st.button(f"Aggiungi", key=f"add_gainer_{r['symbol']}"):
                                if r['symbol'] not in st.session_state.watchlist:
                                    st.session_state.watchlist.append(r['symbol'])
                                    from storage.watchlist_store import save_watchlist
                                    save_watchlist(st.session_state.watchlist)
                                    st.success(f"✅ {r['symbol']} aggiunto!")
                                    st.rerun()
            
            if results['losers']:
                with tab2:
                    st.subheader("📉 Top Losers")
                    df = pd.DataFrame(results['losers'])
                    st.dataframe(
                        df[['symbol', 'name', 'price', 'change', 'volume', 'sector']],
                        column_config={
                            "symbol": "Simbolo",
                            "name": "Nome",
                            "price": st.column_config.NumberColumn("Prezzo", format="$%.2f"),
                            "change": st.column_config.NumberColumn("Variazione %", format="%+.2f%%"),
                            "volume": st.column_config.NumberColumn("Volume", format="%d"),
                            "sector": "Settore"
                        },
                        use_container_width=True
                    )
            
            if results['most_active']:
                with tab3:
                    st.subheader("📊 Most Active")
                    df = pd.DataFrame(results['most_active'])
                    st.dataframe(
                        df[['symbol', 'name', 'price', 'volume', 'market_cap', 'sector']],
                        column_config={
                            "symbol": "Simbolo",
                            "name": "Nome",
                            "price": st.column_config.NumberColumn("Prezzo", format="$%.2f"),
                            "volume": st.column_config.NumberColumn("Volume", format="%d"),
                            "market_cap": st.column_config.NumberColumn("Market Cap", format="$%d"),
                            "sector": "Settore"
                        },
                        use_container_width=True
                    )
    
    # Scanner personalizzato
    with tab4:
        st.subheader("🔍 Scanner Personalizzato")
        st.caption("Cerca asset da liste predefinite")
        
        market_lists = {
            "Crypto Top 20": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", 
                              "ADA-USD", "AVAX-USD", "DOGE-USD", "DOT-USD", "MATIC-USD",
                              "LINK-USD", "UNI-USD", "ATOM-USD", "LTC-USD", "BCH-USD"],
            "S&P 50": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
                       "JPM", "V", "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "BAC"],
            "Nasdaq 100": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", 
                           "AMD", "INTC", "NFLX", "ADBE", "CRM", "CSCO", "PEP"]
        }
        
        market = st.selectbox("Scegli mercato", list(market_lists.keys()))
        symbols = market_lists[market]
        
        if st.button("🔎 Scansiona lista", use_container_width=True):
            with st.spinner("Scansionando..."):
                results = multi_scanner.enhanced_scan(symbols, use_finnhub=use_finnhub)
                
                # Calcola livelli
                for r in results:
                    change = r.get('change', 0)
                    if abs(change) > 2:
                        level = 5
                    elif abs(change) > 1:
                        level = 4
                    elif abs(change) > 0.5:
                        level = 3
                    elif abs(change) > 0.1:
                        level = 2
                    else:
                        level = 1
                    r['level'] = level
                    r['score'] = min(100, abs(change) * 10)
                
                if results:
                    df_results = pd.DataFrame(results)
                    st.dataframe(
                        df_results[['symbol', 'price', 'change', 'level', 'score', 'source']],
                        column_config={
                            "symbol": "Simbolo",
                            "price": st.column_config.NumberColumn("Prezzo", format="$%.2f"),
                            "change": st.column_config.NumberColumn("Variazione", format="%+.2f%%"),
                            "level": "Livello",
                            "score": "Score",
                            "source": "Fonte"
                        },
                        use_container_width=True
                    )
