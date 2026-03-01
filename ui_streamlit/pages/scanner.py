import streamlit as st
import pandas as pd
import time
from datetime import datetime
from providers.polygon_provider import polygon_provider
from indicators.robust_ta import compute_indicators_15m, decide_signal
from ui_streamlit.components.scan_filters import render_scan_filters

# Liste predefinite per scansione
MARKET_LISTS = {
    "Crypto Top 10": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", "ADA-USD", "AVAX-USD", "DOGE-USD", "DOT-USD", "MATIC-USD"],
    "S&P 500 Top 10": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "JPM", "V"],
    "Nasdaq 100": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AMD", "INTC", "NFLX"],
    "Forex Majors": ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "USD/CAD", "NZD/USD"]
}

def show_page():
    st.subheader("🔎 Scanner di mercato")
    st.caption("Cerca asset promettenti in liste predefinite utilizzando i nostri indicatori.")
    
    # Selezione mercato
    market = st.selectbox("Scegli mercato", list(MARKET_LISTS.keys()))
    symbols = MARKET_LISTS[market]
    
    # Filtri
    filters = render_scan_filters()
    
    if st.button("🚀 Avvia scansione", use_container_width=True, type="primary"):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, symbol in enumerate(symbols):
            status_text.text(f"Scansione {i+1}/{len(symbols)}: {symbol}")
            progress_bar.progress((i+1)/len(symbols))
            
            # Adatta simbolo per Polygon (BTC-USD → X:BTCUSD)
            poly_symbol = symbol
            if "-" in symbol:
                base, quote = symbol.split("-")
                if quote == "USD":
                    poly_symbol = f"X:{base}USD"
            elif "/" in symbol:
                base, quote = symbol.split("/")
                poly_symbol = f"C:{base}{quote}"
            
            # Fetch dati 15m
            df, src = polygon_provider.fetch_aggregates(
                poly_symbol, timespan='minute', multiplier=15, limit=300
            )
            
            if df is not None and len(df) > 50:
                df_ind = compute_indicators_15m(df)
                signal = decide_signal(df_ind, mtf_long=False, mtf_short=False)
                current_price = float(df['close'].iloc[-1])
                change = ((current_price - df['close'].iloc[-50]) / df['close'].iloc[-50]) * 100 if len(df) > 50 else 0
                
                # Livello in base alla forza del segnale e alla variazione
                if signal['strength'] == 'STRONG' or abs(change) > 2:
                    level = 5
                elif signal['strength'] == 'WEAK' or abs(change) > 1:
                    level = 4
                elif abs(change) > 0.5:
                    level = 3
                elif abs(change) > 0.1:
                    level = 2
                else:
                    level = 1
                
                score = min(100, abs(change) * 10)
                
                results.append({
                    'symbol': symbol,
                    'price': current_price,
                    'change': change,
                    'level': level,
                    'score': score,
                    'signal': signal['display'],
                    'volume': df['volume'].iloc[-1] if 'volume' in df.columns else 0
                })
            
            time.sleep(0.5)  # Per non superare rate limit
        
        progress_bar.empty()
        status_text.empty()
        
        if results:
            st.success(f"Scansione completata: {len(results)} risultati")
            
            # Filtra per livello minimo
            min_confidence = filters.get('min_confidence', 1)
            filtered = [r for r in results if r['level'] >= min_confidence]
            
            if filtered:
                df_results = pd.DataFrame(filtered)
                st.dataframe(df_results, use_container_width=True)
                
                # Pulsanti per aggiungere alla watchlist
                st.subheader("Aggiungi alla watchlist")
                for r in filtered[:5]:  # Solo primi 5 per non appesantire
                    cols = st.columns([2, 1, 1, 1])
                    with cols[0]:
                        st.write(f"{r['symbol']} (L{r['level']})")
                    with cols[1]:
                        st.write(f"${r['price']:.2f}")
                    with cols[2]:
                        st.write(f"{r['change']:+.2f}%")
                    with cols[3]:
                        if st.button(f"Aggiungi", key=f"add_{r['symbol']}"):
                            add_symbol = r['symbol']
                            if add_symbol not in st.session_state.watchlist:
                                st.session_state.watchlist.append(add_symbol)
                                from storage.watchlist_store import save_watchlist
                                save_watchlist(st.session_state.watchlist)
                                st.success(f"{add_symbol} aggiunto alla watchlist!")
                                st.rerun()
            else:
                st.info("Nessun risultato con i filtri selezionati.")
        else:
            st.warning("Nessun dato ottenuto durante la scansione.")
