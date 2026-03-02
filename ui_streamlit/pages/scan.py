import streamlit as st
import pandas as pd
import time
from datetime import datetime
from providers.multi_provider import scan_symbol, fetch_yf_ohlcv
from providers.finnhub_provider import finnhub_provider
from providers.market_scanner import market_scanner
from ui_streamlit.components.scan_filters import render_scan_filters
from ui_streamlit.components.card import render_result_card

# Liste predefinite
MARKET_LISTS = {
    "📋 La mia watchlist": "watchlist",
    "📈 Top Gainers": "gainers",
    "📉 Top Losers": "losers",
    "📊 Most Active": "active",
    "🪙 Crypto Top 20": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", 
                         "ADA-USD", "AVAX-USD", "DOGE-USD", "DOT-USD", "MATIC-USD",
                         "LINK-USD", "UNI-USD", "ATOM-USD", "LTC-USD", "BCH-USD"],
    "🏢 S&P 50": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
                  "JPM", "V", "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "BAC"],
    "💱 Forex Majors": ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", 
                        "AUD/USD", "USD/CAD", "NZD/USD"],
}

def show_page():
    st.subheader("🔍 Scanner Unificato")
    st.caption("Cerca, analizza e scopri nuovi asset in tempo reale")
    
    # Modalità di scansione
    col1, col2 = st.columns([2, 1])
    
    with col1:
        scan_mode = st.selectbox(
            "Modalità scansione",
            ["📋 Watchlist personale", "📈 Market Movers", "📊 Liste predefinite", "✏️ Lista personalizzata"]
        )
    
    with col2:
        use_finnhub = st.checkbox("📡 Finnhub Real-time", value=True, 
                                 help="Arricchisci con dati in tempo reale")
    
    # Configurazione in base alla modalità
    symbols_to_scan = []
    source_name = ""
    
    if scan_mode == "📋 Watchlist personale":
        symbols_to_scan = st.session_state.watchlist
        source_name = "watchlist"
        st.info(f"📊 Scansionando la tua watchlist ({len(symbols_to_scan)} asset)")
        
    elif scan_mode == "📈 Market Movers":
        market_type = st.radio(
            "Tipo di movers",
            ["📈 Top Gainers", "📉 Top Losers", "📊 Most Active"],
            horizontal=True
        )
        if st.button("🔄 Aggiorna movers", use_container_width=True):
            with st.spinner("Caricamento top movers..."):
                results = market_scanner.scan_top_movers(limit=30)
                if market_type == "📈 Top Gainers":
                    symbols_to_scan = [r['symbol'] for r in results['gainers']]
                elif market_type == "📉 Top Losers":
                    symbols_to_scan = [r['symbol'] for r in results['losers']]
                else:
                    symbols_to_scan = [r['symbol'] for r in results['most_active']]
                source_name = market_type
                st.success(f"Trovati {len(symbols_to_scan)} {market_type}")
                
    elif scan_mode == "📊 Liste predefinite":
        selected_list = st.selectbox("Scegli lista", list(MARKET_LISTS.keys())[2:])  # Escludi watchlist e movers
        if isinstance(MARKET_LISTS[selected_list], list):
            symbols_to_scan = MARKET_LISTS[selected_list]
            source_name = selected_list
            st.caption(f"📊 {len(symbols_to_scan)} asset nella lista")
        else:
            st.warning("Lista non valida")
            
    else:  # Lista personalizzata
        custom_list = st.text_area(
            "Inserisci simboli (uno per riga o separati da virgola)",
            placeholder="BTC-USD\nETH-USD\nAAPL\nMSFT",
            height=100
        )
        if custom_list:
            # Pulisci input
            symbols_to_scan = [
                s.strip().upper() 
                for s in custom_list.replace(',', ' ').split() 
                if s.strip()
            ]
            source_name = "personalizzata"
            st.caption(f"📊 {len(symbols_to_scan)} asset inseriti")
    
    # Filtri avanzati (sempre visibili)
    filters = render_scan_filters()
    
    # Bottone scan
    if symbols_to_scan and st.button("🚀 Avvia scansione", use_container_width=True, type="primary"):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        providers_used = ["Yahoo Finance"]
        if use_finnhub and st.secrets.get("FINNHUB_KEY", ""):
            providers_used.append("Finnhub")
        
        status_text.info(f"Provider attivi: {', '.join(providers_used)}")
        
        for i, symbol in enumerate(symbols_to_scan[:30]):  # Limite 30 per performance
            status_text.text(f"Scan {i+1}/{min(len(symbols_to_scan),30)}: {symbol}")
            progress_bar.progress((i+1)/min(len(symbols_to_scan),30))
            
            # Scan base con Yahoo
            result = scan_symbol(symbol, "15m", "1d")
            
            if result and 'error' not in result:
                # Arricchisci con Finnhub se richiesto
                if use_finnhub and st.secrets.get("FINNHUB_KEY", ""):
                    try:
                        if symbol.endswith('USD') and len(symbol) > 4:
                            quote, _ = finnhub_provider.get_crypto_quote(symbol)
                        else:
                            quote, _ = finnhub_provider.get_quote(symbol)
                        if quote:
                            result['price'] = quote.get('price', result['price'])
                            result['change'] = quote.get('change_percent', result['change'])
                            result['source'] = 'Finnhub'
                    except:
                        pass
                
                # Calcola livello
                change = result.get('change', 0)
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
                
                result['level'] = level
                result['score'] = min(100, abs(change) * 10)
                results.append(result)
            
            time.sleep(0.2)
        
        progress_bar.empty()
        status_text.empty()
        
        if results:
            st.success(f"✅ Scansione completata! {len(results)} risultati")
            
            # Statistiche
            level_counts = {}
            for r in results:
                level_counts[r['level']] = level_counts.get(r['level'], 0) + 1
            
            cols = st.columns(5)
            with cols[0]:
                st.metric("Totale", len(results))
            with cols[1]:
                st.metric("🔥 L5", level_counts.get(5, 0))
            with cols[2]:
                st.metric("🟡 L4", level_counts.get(4, 0))
            with cols[3]:
                st.metric("📊 L3", level_counts.get(3, 0))
            with cols[4]:
                st.metric("📈 L2", level_counts.get(2, 0) + level_counts.get(1, 0))
            
            # Filtra per livello minimo
            filtered = [r for r in results if r['level'] >= filters['min_confidence']]
            
            if filtered:
                st.subheader("🎯 Risultati")
                
                # Visualizzazione a scelta
                view_mode = st.radio("Visualizzazione", ["📊 Tabella", "🃏 Card"], horizontal=True)
                
                if view_mode == "📊 Tabella":
                    df = pd.DataFrame(filtered)
                    st.dataframe(
                        df[['symbol', 'price', 'change', 'level', 'score', 'source']],
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
                else:
                    for r in filtered:
                        render_result_card(r)
                
                # Aggiungi alla watchlist
                st.subheader("➕ Aggiungi alla watchlist")
                for r in filtered[:10]:
                    cols = st.columns([2, 1, 1, 1, 1])
                    with cols[0]:
                        st.write(f"**{r['symbol']}**")
                    with cols[1]:
                        badge_color = "#00ff88" if r['level'] >= 4 else "#f0b90b" if r['level'] >= 3 else "#94a3b8"
                        st.markdown(f"<span style='background:{badge_color}20; color:{badge_color}; padding:2px 8px; border-radius:12px;'>L{r['level']}</span>", unsafe_allow_html=True)
                    with cols[2]:
                        st.write(f"${r['price']:.2f}")
                    with cols[3]:
                        color = "#00ff88" if r['change'] > 0 else "#ff3344"
                        st.markdown(f"<span style='color:{color};'>{r['change']:+.2f}%</span>", unsafe_allow_html=True)
                    with cols[4]:
                        if st.button(f"Aggiungi", key=f"add_{r['symbol']}"):
                            if r['symbol'] not in st.session_state.watchlist:
                                st.session_state.watchlist.append(r['symbol'])
                                from storage.watchlist_store import save_watchlist
                                save_watchlist(st.session_state.watchlist)
                                st.success(f"✅ {r['symbol']} aggiunto!")
                                st.rerun()
            else:
                st.warning("Nessun risultato con i filtri selezionati")
        else:
            st.warning("Nessun dato ottenuto durante la scansione")
