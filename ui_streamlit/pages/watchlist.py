import streamlit as st
import time
from providers.twelvedata_provider import search_symbols_td
from storage.watchlist_store import save_watchlist
from config import WATCHLIST_FILE, DEFAULT_WATCHLIST

def show_page():
    st.title("📋 Gestione Watchlist")
    
    # Assicurati che la watchlist esista
    if 'watchlist' not in st.session_state:
        st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
    
    # Layout a 2 colonne
    col_lista, col_ricerca = st.columns([1, 1])
    
    with col_lista:
        st.subheader("📌 Watchlist Attuale")
        
        if not st.session_state.watchlist:
            st.info("Watchlist vuota")
        else:
            for i, asset in enumerate(st.session_state.watchlist):
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                
                with col1:
                    st.write(f"{i+1}. **{asset}**")
                
                with col2:
                    if st.button("📊", key=f"view_{i}", help="Vedi dettaglio"):
                        st.session_state.selected_asset = asset
                        st.session_state.radar_select = asset
                        st.session_state.current_page = "DETTAGLIO"
                        st.rerun()
                
                with col3:
                    if st.button("🔄", key=f"refresh_{i}", help="Aggiorna"):
                        st.cache_data.clear()
                        st.rerun()
                
                with col4:
                    if st.button("❌", key=f"del_{i}", help="Rimuovi"):
                        st.session_state.watchlist.pop(i)
                        save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                        st.rerun()
            
            st.caption(f"Totale: {len(st.session_state.watchlist)} asset")
            
            # Bottone reset
            if st.button("🔄 Reset a Default", use_container_width=True):
                st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
                save_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)
                st.rerun()
    
    with col_ricerca:
        st.subheader("🔍 Cerca Nuovi Asset")
        
        # Ricerca automatica mentre scrivi
        search_term = st.text_input(
            "Simbolo o nome",
            placeholder="Es: bitcoin, apple, BTC-USD...",
            key="search_input",
            help="Inizia a scrivere per cercare automaticamente"
        )
        
        if search_term and len(search_term) >= 2:
            with st.spinner(f"Ricerca '{search_term}' in corso..."):
                # Usa TwelveData per la ricerca
                results = search_symbols_td(search_term, 10)
                
                if results:
                    st.success(f"✅ Trovati {len(results)} risultati")
                    
                    for idx, r in enumerate(results):
                        symbol = r.get('symbol', '')
                        name = r.get('name', '')
                        exchange = r.get('exchange', '')
                        currency = r.get('currency', '')
                        
                        # Crea label descrittiva
                        label = symbol
                        details = []
                        if name:
                            details.append(name)
                        if exchange:
                            details.append(exchange)
                        if currency and currency != 'USD':
                            details.append(currency)
                        
                        if details:
                            label += f" - {' | '.join(details)}"
                        
                        col_btn1, col_btn2, col_btn3 = st.columns([3, 1, 1])
                        
                        with col_btn1:
                            st.markdown(f"**{label}**")
                        
                        with col_btn2:
                            # Converti per compatibilità
                            display_symbol = symbol.replace("/", "-")
                            st.caption(f"📌 {display_symbol}")
                        
                        with col_btn3:
                            if st.button("➕", key=f"add_{idx}", help="Aggiungi alla watchlist"):
                                add_symbol = symbol.replace("/", "-")
                                if add_symbol not in st.session_state.watchlist:
                                    st.session_state.watchlist.append(add_symbol)
                                    save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                                    st.success(f"✅ {add_symbol} aggiunto!")
                                    time.sleep(1)
                                    st.rerun()
                                else:
                                    st.warning(f"⚠️ {add_symbol} già presente")
                        
                        st.divider()
                else:
                    st.warning("❌ Nessun risultato trovato")
        
        elif search_term and len(search_term) == 1:
            st.caption("🔤 Scrivi almeno 2 caratteri...")
        
        # Aggiunta manuale
        st.markdown("---")
        st.subheader("✏️ Aggiunta Manuale")
        
        manual_symbol = st.text_input(
            "Simbolo",
            placeholder="Es: BTC-USD, AAPL, MSFT",
            key="manual_symbol"
        ).upper().strip()
        
        col_man1, col_man2 = st.columns(2)
        
        with col_man1:
            if st.button("➕ Aggiungi Manuale", use_container_width=True):
                if manual_symbol and manual_symbol not in st.session_state.watchlist:
                    st.session_state.watchlist.append(manual_symbol)
                    save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                    st.success(f"✅ {manual_symbol} aggiunto!")
                    st.rerun()
                elif manual_symbol in st.session_state.watchlist:
                    st.warning(f"⚠️ {manual_symbol} già presente")
                else:
                    st.warning("⚠️ Inserisci un simbolo valido")
        
        with col_man2:
            if st.button("🧹 Pulisci", use_container_width=True):
                st.session_state.search_input = ""
                st.rerun()
