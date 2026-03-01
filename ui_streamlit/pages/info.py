import streamlit as st
from datetime import datetime
from config import VERSION

def render():
    st.markdown("""
    <style>
        .info-card {
            background: linear-gradient(135deg, #14181F, #1E242C);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1rem 0;
            border-left: 6px solid #F0B90B;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        }
        .feature-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin: 1.5rem 0;
        }
        .feature-item {
            background: rgba(240, 185, 11, 0.1);
            border: 1px solid rgba(240, 185, 11, 0.3);
            border-radius: 15px;
            padding: 1.2rem;
            text-align: center;
            transition: transform 0.3s;
        }
        .feature-item:hover {
            transform: translateY(-5px);
            border-color: #F0B90B;
            box-shadow: 0 10px 20px rgba(240, 185, 11, 0.2);
        }
        .step-number {
            background: #F0B90B;
            color: #0B0E14;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            margin-right: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

    st.title("ℹ️ Golden Eye Pro 4.0")
    st.caption("Trading Intelligence Platform • Multi-Provider • AI-Powered")

    # Introduzione
    with st.container():
        st.markdown("""
        <div class="info-card">
            <h2 style="color: #F0B90B; margin-top: 0;">🦅 Benvenuto in Golden Eye Pro</h2>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                La piattaforma di trading intelligence più completa, progettata per trader che pretendono il massimo.
                Combina <strong>5 provider di dati</strong>, <strong>AI contestuale</strong> e <strong>strumenti professionali</strong>
                in un'unica interfaccia elegante e potente.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Provider Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Provider Dati", "5", "Yahoo, TwelveData, Finnhub, Alpha Vantage, Polygon")
    with col2:
        st.metric("Provider News", "2", "Marketaux, Finnhub")
    with col3:
        st.metric("Asset Coperti", "10.000+", "Azioni, Crypto, Forex")
    with col4:
        st.metric("Versione", VERSION, "Marzo 2026")

    st.divider()

    # Funzionalità principali
    st.subheader("✨ Funzionalità Principali")
    
    st.markdown("""
    <div class="feature-grid">
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">📡 Radar SCAN</h3>
            <p>Monitoraggio automatico della watchlist con filtri a 5 livelli. Segnali in tempo reale.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">📊 Dettaglio Asset</h3>
            <p>Analisi multi-provider con RSI, ADX, ATR, MTF e confronto tra fonti.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">🤖 AI Suggeritore</h3>
            <p>Sistema a 5 livelli con punteggio, suggerimenti e analisi contestuale.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">📰 News Multi-Provider</h3>
            <p>Sentiment combinato da Marketaux e Finnhub per decisioni informate.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">🔎 Scanner Mercato</h3>
            <p>Top gainers, top losers e most active in tempo reale.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">📈 Backtest & Validazione</h3>
            <p>Test strategie su dati storici, multi-asset e multi-anno.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">⚙️ Ottimizzazione</h3>
            <p>Ricerca automatica parametri ottimali per ogni asset.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">💰 Money Management</h3>
            <p>Calcolo posizione, rischio, drawdown e Sharpe ratio.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">📝 Paper Trading</h3>
            <p>Simula trading con capitale virtuale e dati reali.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">🤖 AutoTrader</h3>
            <p>Bot automatico basato su livelli di confidenza.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">📊 API Dashboard</h3>
            <p>Monitoraggio consumi e limiti di tutti i provider.</p>
        </div>
        <div class="feature-item">
            <h3 style="color: #F0B90B; margin-top: 0;">⚙️ Configurazione</h3>
            <p>Parametri personalizzabili e gestione chiavi API.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Sistema a 5 livelli
    st.subheader("🔥 Sistema a 5 Livelli di Confidenza")
    
    level_data = {
        "L5 - FORTE": {"color": "#00ff88", "desc": "Condizioni ottimali: trend forte, RSI ≤ 55, ADX ≥ 25, allineamento MTF", "action": "✅ Trading attivo"},
        "L4 - MEDIO": {"color": "#f0b90b", "desc": "Trend presente ma condizioni meno stringenti", "action": "🟡 Trading cauto"},
        "L3 - MOMENTUM": {"color": "#3b82f6", "desc": "Pendenza significativa, RSI/ADX non allineati", "action": "📊 Monitorare"},
        "L2 - TENDENZA": {"color": "#8b5cf6", "desc": "Posizione rispetto a EMA200, senza conferma", "action": "ℹ️ Informativo"},
        "L1 - LATERALE": {"color": "#94a3b8", "desc": "Mercato senza direzione chiara", "action": "⚪ Attendere"}
    }
    
    for level, data in level_data.items():
        st.markdown(f"""
        <div style="
            background: {data['color']}10;
            border-left: 6px solid {data['color']};
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
        ">
            <span style="color: {data['color']}; font-weight: 800; font-size: 1.1rem;">{level}</span>
            <p style="margin: 0.3rem 0 0 0; color: #94a3b8;">{data['desc']}</p>
            <p style="margin: 0.2rem 0 0 0; font-weight: 600; color: {data['color']};">{data['action']}</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Guida rapida
    st.subheader("📖 Guida Rapida per Nuovi Utenti")
    
    tabs = st.tabs(["🚀 Primi Passi", "📊 Scan & Dettaglio", "🤖 Trading", "⚙️ Configurazione", "❓ FAQ"])
    
    with tabs[0]:
        st.markdown("""
        ### 🚀 Come iniziare in 5 minuti
        
        1. **Configura le API Keys** (una volta sola)
           - Vai su **Configurazione** → **API Keys**
           - Inserisci le chiavi (TwelveData, Finnhub, Marketaux)
           - Ottieni chiavi gratuite dai link forniti
        
        2. **Personalizza la Watchlist**
           - Vai su **WATCHLIST**
           - Aggiungi i tuoi asset preferiti
           - Usa la ricerca automatica
        
        3. **Avvia il Radar SCAN**
           - Vai su **SCAN**
           - Clicca "AVVIA SCAN"
           - Filtra per livello di confidenza
        
        4. **Analizza un asset**
           - Clicca su un simbolo dai risultati
           - Esplora indicatori, news, AI suggeritore
        
        5. **Prova Paper Trading**
           - Vai su **TRADING** → **Paper Trading**
           - Simula operazioni senza rischi
        """)
    
    with tabs[1]:
        st.markdown("""
        ### 📊 Scan & Dettaglio
        
        **Radar SCAN**
        - Scansiona automaticamente la watchlist
        - Filtri per livello (L1-L5) e score
        - Risultati con badge colorati
        - Clicca su un asset per il dettaglio
        
        **Dettaglio Asset**
        - Scegli il provider (TwelveData/Yahoo/Finnhub)
        - Confronto provider disponibile
        - Grafico interattivo con EMA200
        - RSI, ADX, ATR in tempo reale
        - News multi-provider con sentiment
        - AI Suggeritore con analisi contestuale
        - SL/TP calcolati automaticamente
        """)
    
    with tabs[2]:
        st.markdown("""
        ### 🤖 Trading & Strategia
        
        **Backtest**
        - Testa strategie su dati storici
        - Scegli sorgente (Yahoo/TwelveData)
        - Visualizza trades e statistiche
        
        **Validazione**
        - Test multi-asset e multi-anno
        - Score qualità strategia (A+ a F)
        - Analisi dettagliata per asset
        
        **Ottimizzazione**
        - Ricerca automatica parametri
        - Grid search su SL, TP, ADX, RSI
        - Best parameters con performance
        
        **Money Management**
        - Calcolo posizione ottimale
        - Gestione rischio e drawdown
        - Sharpe ratio e metriche avanzate
        
        **Paper Trading**
        - Simula trading con capitale virtuale
        - Inserisci manualmente o usa dati dettaglio
        
        **AutoTrader**
        - Bot automatico con livelli di confidenza
        - Parametri personalizzabili
        - Statistiche performance
        """)
    
    with tabs[3]:
        st.markdown("""
        ### ⚙️ Configurazione
        
        **Indicatori**
        - RSI Length, ATR Length, ADX Length
        - Soglie personalizzabili
        
        **Risk Management**
        - Multiplicatori SL/TP
        - Abilita/disabilita segnali deboli
        
        **API Keys**
        - TwelveData (800/giorno)
        - Alpha Vantage (25/giorno)
        - Marketaux (100/giorno)
        - Finnhub (60/minuto)
        
        **Avanzate**
        - Watchlist predefinita
        - Reset configurazione
        - Info sistema
        """)
    
    with tabs[4]:
        st.markdown("""
        ### ❓ Domande Frequenti
        
        **Q: Perché alcuni provider non funzionano?**
        A: Verifica le chiavi API in Configurazione. I piani gratuiti hanno limiti giornalieri.
        
        **Q: Come si interpreta il livello L1-L5?**
        A: Vedi la sezione "Sistema a 5 Livelli" sopra. L5 è segnale forte, L1 è laterale.
        
        **Q: Perché i dati di provider diversi differiscono?**
        A: È normale! Ogni provider ha fonti e tempi di aggiornamento diversi. Usa il confronto per avere un quadro completo.
        
        **Q: Posso salvare le mie configurazioni?**
        A: Attualmente i parametri sono per sessione. Presto arriverà il salvataggio permanente!
        
        **Q: Come aggiungo nuovi asset alla watchlist?**
        A: Vai su WATCHLIST, cerca per nome o simbolo, clicca "Aggiungi".
        
        **Q: L'AI Suggeritore è affidabile?**
        A: L'AI è basata su regole e pesi calibrati, non su machine learning. È uno strumento di supporto, non una garanzia.
        """)

    st.divider()

    # Provider dati
    st.subheader("📡 Provider Integrati")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("""
        **📊 Dati di Mercato**
        - TwelveData (800/giorno)
        - Yahoo Finance (illimitato)
        - Finnhub (60/minuto)
        - Alpha Vantage (25/giorno)
        """)
    
    with col_p2:
        st.markdown("""
        **📰 News & Sentiment**
        - Marketaux (100/giorno)
        - Finnhub News (incluse)
        """)
    
    with col_p3:
        st.markdown("""
        **🔧 Utility**
        - Telegram (notifiche)
        - Polygon (dati alternativi)
        """)

    st.divider()

    # Disclaimer
    with st.expander("⚠️ Disclaimer Legale", expanded=False):
        st.markdown("""
        **Golden Eye Pro 4.0** è uno strumento di analisi e simulazione **a scopo puramente educativo e informativo**.
        
        - I dati forniti non costituiscono consulenza finanziaria né raccomandazioni di investimento.
        - Le performance passate non garantiscono risultati futuri.
        - Il trading reale comporta rischi significativi di perdita; si raccomanda di consultare un consulente finanziario professionista.
        - L'uso delle API è soggetto ai termini di servizio dei rispettivi provider.
        - L'autore declina ogni responsabilità per eventuali perdite finanziarie derivanti dall'uso dell'applicazione.
        
        *Investi in modo responsabile.*
        """)

    # Footer
    st.caption(f"📅 Documentazione aggiornata il {datetime.now().strftime('%d/%m/%Y %H:%M')}")
