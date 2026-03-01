import streamlit as st
from datetime import datetime
from config import VERSION

def render():
    st.markdown("## ℹ️ Golden Eye Pro 4.0 – Informazioni")
    st.caption("Trading Intelligence Platform • Tutti i dati sono in tempo reale")

    # Sezione introduzione
    with st.container(border=True):
        st.markdown("""
        ### 🦅 Cos'è Golden Eye Pro?
        **Golden Eye Pro** è una piattaforma professionale di **trading intelligence** progettata per fornire analisi multi‑asset in tempo reale.  
        Combina fonti dati affidabili (Yahoo Finance, TwelveData, Marketaux) con un motore di **indicatori tecnici**, un **AI Suggeritore** a 5 livelli e strumenti avanzati come backtest, ottimizzazione e paper trading.

        L'obiettivo è offrire a trader e investitori un quadro chiaro e immediato dei mercati, facilitando decisioni consapevoli.
        """)

    # Funzionalità principali
    with st.container(border=True):
        st.markdown("### ✨ Funzionalità principali")
        cols = st.columns(2)
        with cols[0]:
            st.markdown("""
            - **📡 Radar SCAN** – Monitoraggio automatico della watchlist con segnali a 5 livelli (L1‑L5)
            - **📊 Dettaglio Asset** – Grafici interattivi, indicatori (RSI, ADX, ATR), analisi MTF (1h/4h)
            - **🤖 AI Suggeritore** – Analisi contestuale con punteggio e suggerimenti operativi
            - **📰 News Sentiment** – Integrazione Marketaux per valutare il sentiment delle notizie
            """)
        with cols[1]:
            st.markdown("""
            - **📈 Backtest & Validazione** – Test della strategia su dati storici, anche multi‑asset
            - **⚙️ Ottimizzazione** – Ricerca automatica dei parametri ottimali per ogni asset
            - **💰 Money Management** – Calcolo posizione, rischio, drawdown
            - **📝 Paper Trading** – Simulazione di trading con capitale virtuale
            - **🤖 AutoTrader** – Bot automatico basato su livelli di confidenza
            - **📊 Dashboard API** – Monitoraggio dei consumi e dei limiti delle API
            """)

    # Sistema a 5 livelli
    with st.container(border=True):
        st.markdown("### 🔥 Sistema a 5 livelli di confidenza")
        st.markdown("""
        I segnali vengono classificati in base alla forza del trend e degli indicatori:

        | Livello | Descrizione | Azione consigliata |
        |---------|-------------|---------------------|
        | **L5 – FORTE** | Condizioni ottimali: trend forte, RSI ≤ 55, ADX ≥ 25, allineamento MTF | ✅ Trading attivo con SL/TP standard |
        | **L4 – MEDIO** | Trend presente ma condizioni meno stringenti | 🟡 Trading cauto, attendere conferma |
        | **L3 – MOMENTUM** | Pendenza significativa, ma RSI/ADX non allineati | 📊 Monitorare, non ancora un segnale |
        | **L2 – TENDENZA** | Posizione rispetto a EMA200, senza conferma | ℹ️ Informativo |
        | **L1 – LATERALE** | Mercato senza direzione chiara | ⚪ Attendere movimento |
        """)

    # Tecnologie
    with st.container(border=True):
        st.markdown("### 🛠️ Tecnologie utilizzate")
        st.markdown("""
        - **Frontend**: Streamlit (Python)
        - **Dati di mercato**: Yahoo Finance (gratuito), TwelveData (800 chiamate/giorno), Alpha Vantage (500/giorno)
        - **News**: Marketaux (100 chiamate/giorno)
        - **Analisi tecnica**: pandas-ta / ta, numpy, pandas
        - **Grafici**: Plotly
        - **AI**: Modello proprietario basato su regole e pesi calibrati
        - **Storage**: JSON locale per watchlist, caching su disco
        """)

    # Versione e aggiornamenti
    with st.container(border=True):
        st.markdown(f"### 📦 Versione attuale: **{VERSION}**")
        st.markdown("""
        **Data di rilascio**: Marzo 2026  
        **Ultimo aggiornamento**: 01/03/2026

        **Novità della versione 4.0**:
        - Sistema a 5 livelli di confidenza
        - AI Suggeritore integrato
        - Nuova dashboard API
        - Ottimizzatore parametri automatico
        - Validazione multi‑asset
        - Paper trading interattivo
        - AutoTrader con soglie configurabili
        - Grafica rinnovata e responsive
        """)

    # Disclaimer legale
    with st.container(border=True):
        st.markdown("### ⚠️ Disclaimer importante")
        st.markdown("""
        **Golden Eye Pro** è uno strumento di analisi e simulazione **a scopo puramente educativo e informativo**.  
        - I dati forniti non costituiscono consulenza finanziaria né raccomandazioni di investimento.
        - Le performance passate non garantiscono risultati futuri.
        - Il trading reale comporta rischi significativi di perdita; si raccomanda di consultare un consulente finanziario professionista.
        - L'uso delle API è soggetto ai termini di servizio dei rispettivi provider.
        - L'autore declina ogni responsabilità per eventuali perdite finanziarie derivanti dall'uso dell'applicazione.

        *Investi in modo responsabile.*
        """)

    # Crediti e contatti
    with st.container(border=True):
        st.markdown("### 👨‍💻 Crediti e contatti")
        st.markdown("""
        **Sviluppatore**: Danipersy  
        **Progetto**: [GitHub – Golden Eye Pro 4.0](https://github.com/Danipersy/GOLDEN-EYE-PRO-4.0)  
        **Segnalazione bug / suggerimenti**: aprire una issue su GitHub o contattare via [email](mailto:danipersy@example.com) (placeholder)

        *Se apprezzi il progetto, lascia una ⭐ su GitHub!*
        """)

    # Footer con data
    st.divider()
    st.caption(f"Documentazione aggiornata il {datetime.now().strftime('%d/%m/%Y %H:%M')}")
