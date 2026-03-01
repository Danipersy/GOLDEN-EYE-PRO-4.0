import streamlit as st
import time
from providers.twelvedata_provider import search_symbols_td
from storage.watchlist_store import save_watchlist
from config import WATCHLIST_FILE, DEFAULT_WATCHLIST

def show_page():
    st.subheader("📋 Gestione Watchlist", divider="blue")

    # Layout a due colonne: watchlist attuale a sinistra, ricerca a destra
    col_lista, col_ricerca = st.columns([1, 1])

    with col_lista:
        st.markdown("### 📌 Watchlist attuale")
        if not st.session_state.watchlist:
            st.info("La watchlist è vuota")
        else:
            for i, asset in enumerate(st.session_state.watchlist):
                cols = st.columns([3, 1, 1])
                with cols[0]:
                    st.write(f"{i+1}. **{asset}**")
                with cols[1]:
                    if st.button("📊", key=f"view_{i}", help="Vedi dettaglio"):
                        st.session_state.selected_asset = asset
                        st.session_state.radar_select = asset
                        st.session_state.current_page = "DETTAGLIO"
                        st.rerun()
                with cols[2]:
                    if st.button("❌", key=f"del_{i}", help="Rimuovi"):
                        st.session_state.watchlist.pop(i)
                        save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                        st.rerun()
            st.caption(f"Totale: {len(st.session_state.watchlist)} asset")

        if st.button("🔄 Reset a default", use_container_width=True):
            st.session_state.watchlist = DEFAULT_WATCHLIST.copy()
            save_watchlist(WATCHLIST_FILE, DEFAULT_WATCHLIST)
            st.rerun()

    with col_ricerca:
        st.markdown("### 🔍 Cerca nuovi asset")
        search_term = st.text_input(
            "Simbolo o nome",
            placeholder="Es: bitcoin, apple, BTC-USD...",
            key="search_input",
            help="Inizia a scrivere per cercare automaticamente"
        )

        if search_term and len(search_term) >= 2:
            with st.spinner(f"Ricerca '{search_term}' in corso..."):
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

        st.markdown("---")
        st.markdown("### ✏️ Aggiunta manuale")
        manual_symbol = st.text_input(
            "Simbolo",
            placeholder="Es: BTC-USD, AAPL, MSFT",
            key="manual_symbol"
        ).upper().strip()

        if st.button("➕ Aggiungi manuale", use_container_width=True) and manual_symbol:
            if manual_symbol not in st.session_state.watchlist:
                st.session_state.watchlist.append(manual_symbol)
                save_watchlist(WATCHLIST_FILE, st.session_state.watchlist)
                st.success(f"✅ {manual_symbol} aggiunto!")
                st.rerun()
            else:
                st.warning(f"⚠️ {manual_symbol} già presente")
