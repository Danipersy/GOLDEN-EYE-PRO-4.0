# ui_streamlit/components/info_ui.py
import streamlit as st
from config import VERSION

def render_info_page():
    """Pagina informazioni aggiornata con tutte le funzionalità"""
    
    st.markdown("## ℹ️ Info - Golden Eye Pro 2026 ULTIMATE")
    
    # Versione in evidenza
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #f0b90b20, #f0b90b05);
        border: 1px solid #f0b90b;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin-bottom: 20px;
    '>
        <span style='color:#94a3b8; font-size:0.9rem;'>VERSIONE ATTUALE</span>
        <div style='font-size:2.5rem; font-weight:900; color:#f0b90b;'>{VERSION}</div>
<span style='color:#94a3b8;'>AI integrata con sistema a 5 livelli - 23 Febbraio 2026</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Panoramica
    with st.container(border=True):
        st.markdown("### 🎯 Panoramica")
        st.markdown("""
        **Golden Eye Pro** è uno scanner multi-asset professionale con sistema a **5 livelli di confidenza**:
        
        **Livelli segnale:**
        - 🔥 **L5 - FORTE** : Veri segnali di trading (condizioni ottimali)
        - 🟡 **L4 - MEDIO** : Segnali di trading con cautela
        - 📊 **L3 - MOMENTUM** : Da monitorare, attendere conferma
        - 📈 **L2 - TENDENZA** : Posizione relativa a EMA200 (informativo)
        - ⚪ **L1 - LATERALE** : Mercato laterale (solo informativo)
        
        **Moduli principali:**
        - 📡 **Radar Yahoo** con filtri per livello di confidenza
        - 📊 **Dettaglio TwelveData** con analisi MTF
        - 📰 **News Marketaux** con sentiment (fino a 5 news)
        - 📈 **Backtest** rapido, annuale e multi-asset
        - 🎯 **Validazione strategia** multi-asset con scoring
        - ⚙️ **Ottimizzazione parametri** automatica
        - 💰 **Money Management** professionale
        - 📝 **Paper Trading** interattivo
        - 🤖 **AI Suggeritore v2.0** con analisi contestuale
        """)
    
    # Sistema a 5 livelli
    with st.container(border=True):
        st.markdown("### 🎯 Sistema a 5 Livelli di Confidenza")
        
        col_l1, col_l2 = st.columns(2)
        
        with col_l1:
            st.markdown("""
            **🟢 LIVELLO 5 - FORTE**
            - Condizioni originali: trend + RSI ottimale
            - ✅ **Segnale di trading vero**
            - 🔥 Alta probabilità di successo
            """)
            
            st.markdown("""
            **🟡 LIVELLO 4 - MEDIO**
            - Solo trend rialzista/ribassista
            - ⚠️ **Segnale di trading con cautela**
            - 📊 Richiede conferma aggiuntiva
            """)
            
            st.markdown("""
            **📊 LIVELLO 3 - MOMENTUM**
            - Pendenza EMA significativa
            - 🔍 **Da monitorare**
            - ⏳ Attendere conferma prima di agire
            """)
        
        with col_l2:
            st.markdown("""
            **📈 LIVELLO 2 - TENDENZA**
            - Posizione rispetto a EMA200
            - ℹ️ **Informativo**
            - 📉 Non è un segnale di trading
            """)
            
            st.markdown("""
            **⚪ LIVELLO 1 - LATERALE**
            - Mercato senza direzione
            - 📋 **Solo informativo**
            - ⏸️ Attendere movimento
            """)
    
    # Novità versione 4.0.0
    with st.container(border=True):
        st.markdown("### ✨ Novità Versione 4.0.0")
        
        col_n1, col_n2 = st.columns(2)
        
        with col_n1:
            st.markdown("""
            **🎯 Sistema a 5 Livelli:**
            - Mai più scan vuoto
            - Gerarchia chiara dei segnali
            - Note esplicative per ogni livello
            - Filtri granulari per confidenza
            
            **🔧 Filtri Avanzati v2.0:**
            - Slider per livello minimo
            - Checkbox per ogni categoria
            - Preset rapidi (Tutti/Trend/Medi/Forti)
            - Tooltip informativi
            """)
        
        with col_n2:
            st.markdown("""
            **📊 Radar Migliorato:**
            - Badge con livello segnale
            - Note contestuali
            - Colori differenziati
            - Sempre risultati visibili
            
            **🤖 AI Suggeritore:**
            - Integrato con nuovo sistema
            - Pesi calibrati
            - Analisi contestuale
            """)
    
    # Filtri e utilizzo
    with st.container(border=True):
        st.markdown("### 🔧 Come usare i filtri")
        
        st.markdown("""
        **1. Scegli il livello minimo** con lo slider:
        - **TUTTI** (L1) → vedi anche laterale (informativo)
        - **TENDENZA** (L2) → vedi solo tendenza e superiori
        - **MOMENTUM** (L3) → vedi momentum e superiori
        - **MEDI** (L4) → vedi solo segnali di trading
        - **FORTI** (L5) → vedi solo segnali forti
        
        **2. Personalizza** con i checkbox:
        - Puoi escludere specifiche categorie
        - Le opzioni si disabilitano automaticamente
        
        **3. Usa i preset** per cambiare rapidamente:
        - 📊 **Tutti** → massime informazioni
        - 📈 **Trend** → solo tendenza e superiori
        - 🟡 **Medi** → solo trading
        - 🔥 **Forti** → solo trading forte
        """)
    
    # Parametri di default
    with st.container(border=True):
        st.markdown("### ⚙️ Parametri di Default v4.0.0")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            st.markdown("""
            **Risk Management:**
            - SL = 2.0x ATR
            - TP = 4.0x ATR
            - Rischio per trade: 2%
            - Drawdown max: 20%
            """)
        
        with col_p2:
            st.markdown("""
            **Indicatori:**
            - RSI Length: 14
            - ATR Length: 14
            - ADX Length: 14
            - EMA Fast: 20
            - EMA Slow: 50
            - EMA Trend: 200
            """)
        
        with col_p3:
            st.markdown("""
            **Soglie Segnali:**
            - RSI Long Max: 65
            - RSI Short Min: 35
            - ADX Min: 20
            - Score Forte: ≥75
            """)
    
    # Changelog dettagliato
    with st.container(border=True):
        st.markdown("### 📦 Changelog v4.0.0")
        
        st.markdown("""
        **✅ Sistema a 5 Livelli di Confidenza** (23 Febbraio 2026)
        - Implementata gerarchia segnali (L1-L5)
        - Aggiunte note esplicative per ogni livello
        - Filtri ridisegnati per il nuovo sistema
        - Preset rapidi per cambiare visualizzazione
        
        **✅ Radar Yahoo Migliorato**
        - Badge con livello segnale
        - Note contestuali integrate
        - Mai più scan vuoto
        - Colori differenziati per importanza
        
        **✅ UI/UX Potenziata**
        - Tooltip informativi ovunque
        - Feedback visivo immediato
        - Slider interattivo per livelli
        - Checkbox con disabilitazione automatica
        
        **✅ AI Suggeritore v2.1**
        - Integrazione con sistema a livelli
        - Pesi calibrati per accuratezza
        - Analisi contestuale migliorata
        """)
    
    # Disclaimer
    with st.container(border=True):
        st.markdown("### ⚠️ Disclaimer")
        st.markdown("""
        Questo strumento è per **soli scopi educativi e informativi**. 
        
        - I dati forniti non costituiscono consulenza finanziaria
        - Le performance passate non garantiscono risultati futuri
        - I segnali di livello 1-3 sono informativi, non trading
        - Il trading comporta rischi significativi di perdita
        - Si raccomanda di consultare un consulente finanziario professionista
        
        *Golden Eye Pro 2026 ULTIMATE v4.0.0 - Trading Intelligence Platform*
        """)
    
    # Footer con statistiche aggiornate
    st.divider()
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        st.metric("Moduli Attivi", "16+", "v4.0.0")
    with col_f2:
        st.metric("Fonti Dati", "3", "Yahoo, TwelveData, Marketaux")
    with col_f3:
        st.metric("Backtest Anni", "6", "2020-2025")
    with col_f4:
        st.metric("Livelli Segnale", "5", "L1-L5")
