import streamlit as st

def render():
    st.subheader("ℹ️ Informazioni sull'App")
    st.markdown("""
    **GOLDEN EYE PRO 4.0** è una piattaforma di trading intelligence progettata per fornire analisi multi-asset in tempo reale.

    ### Funzionalità principali
    - **Radar SCAN**: monitoraggio automatico di oltre 20 asset con filtri a 5 livelli
    - **Dettaglio asset**: analisi tecnica con RSI, ADX, ATR, MTF e AI Suggeritore
    - **Watchlist**: gestione personalizzata degli asset
    - **Strumenti avanzati**: validazione strategia, ottimizzazione parametri, money management
    - **Trading**: paper trading e AutoTrader
    - **Dashboard API**: monitoraggio consumi e limiti

    ### Tecnologie utilizzate
    - Python, Streamlit, Pandas, Plotly
    - Yahoo Finance, TwelveData, Marketaux
    - AI integrata con sistema a 5 livelli

    ### Versione
    4.0.0 - Marzo 2026

    ### Disclaimer
    Questo strumento è per soli scopi educativi. Non costituisce consulenza finanziaria.
    """)
