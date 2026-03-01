import streamlit as st
import pandas as pd
from datetime import datetime
from providers.multi_scanner import multi_scanner
from ui_streamlit.components.scan_filters import render_scan_filters

# Liste predefinite (ampliate!)
MARKET_LISTS = {
    "Crypto Top 20": ["BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "XRP-USD", 
                      "ADA-USD", "AVAX-USD", "DOGE-USD", "DOT-USD", "MATIC-USD",
                      "LINK-USD", "UNI-USD", "ATOM-USD", "LTC-USD", "BCH-USD",
                      "ALGO-USD", "VET-USD", "FIL-USD", "ICP-USD", "NEAR-USD"],
    "S&P 50": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B",
               "JPM", "V", "JNJ", "WMT", "PG", "MA", "UNH", "HD", "DIS", "BAC",
               "NFLX", "ADBE", "CRM", "PFE", "TMO", "ABT", "NKE"],
    "Nasdaq 100": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", 
                   "AMD", "INTC", "NFLX", "ADBE", "CRM", "CSCO", "PEP"],
    "Forex Majors": ["EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", 
                     "AUD/USD", "USD/CAD", "NZD/USD"],
    "Meme Stocks": ["GME", "AMC", "BB", "KOSS", "NOK"],
}

def show_page():
    st.subheader("🔎 Scanner Multi-Provider")
    st.caption("Cerca asset promettenti usando Yahoo Finance + Finnhub (real-time)")
    
    # Verifica chiave Finnhub
    finnhub_key = st.secrets.get("FINNHUB_KEY", "")
    if not finnhub_key:
        st.warning("⚠️ Chiave Finnhub non trovata. Aggiungila in Configurazione o nei secrets per dati real-time.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        market = st.selectbox("Scegli mercato", list(MARKET_LISTS.keys()))
        symbols = MARKET_LISTS[market]
    
    with col2:
        use_finnhub = st.checkbox("Usa Finnhub (dati real-time)", value=True,
                                 help="Arricchisce i dati con quote in tempo reale")
        st.caption(f"📊 {len(symbols)} asset da analizzare")
    
    filters = render_scan_filters()
    
    if st.button("🚀 Avvia scansione", use_container_width=True, type="primary"):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Mostra quali provider useremo
        providers = ["Yahoo Finance"]
        if use_finnhub and finnhub_key:
            providers.append("Finnhub (real-time)")
        
        status_text.info(f"Provider attivi: {', '.join(providers)}")
        
        # Esegui scan
        with st.spinner("Scansionando mercati..."):
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
            
            progress_bar.progress(1.0)
            status_text.success(f"✅ Scansione completata! {len(results)} risultati")
        
        if results:
            # Statistiche
            st.subheader("📊 Riepilogo")
            col_s1, col_s2, col_s3 = st.columns(3)
            with col_s1:
                st.metric("Totale asset", len(results))
            with col_s2:
                sources = pd.DataFrame(results)['source'].value_counts()
                st.write("**Fonti:**")
                for src, count in sources.items():
                    st.caption(f"• {src}: {count}")
            with col_s3:
                avg_change = pd.DataFrame(results)['change'].mean()
                st.metric("Variazione media", f"{avg_change:+.2f}%")
            
            # Filtra per livello
            min_confidence = filters.get('min_confidence', 1)
            filtered = [r for r in results if r['level'] >= min_confidence]
            
            if filtered:
                st.subheader("🎯 Risultati")
                df_results = pd.DataFrame(filtered)
                
                # Formatta per visualizzazione
                display_df = df_results[['symbol', 'price', 'change', 'level', 'score', 'source']].copy()
                display_df['price'] = display_df['price'].map('${:,.2f}'.format)
                display_df['change'] = display_df['change'].map('{:+.2f}%'.format)
                
                st.dataframe(display_df, use_container_width=True,
                           column_config={
                               "symbol": "Simbolo",
                               "price": "Prezzo",
                               "change": "Variazione",
                               "level": "Livello",
                               "score": "Score",
                               "source": "Fonte"
                           })
                
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
                            add_symbol = r['symbol']
                            if add_symbol not in st.session_state.watchlist:
                                st.session_state.watchlist.append(add_symbol)
                                from storage.watchlist_store import save_watchlist
                                save_watchlist(st.session_state.watchlist)
                                st.success(f"✅ {add_symbol} aggiunto!")
                                st.rerun()
            else:
                st.warning("Nessun risultato con i filtri selezionati")
