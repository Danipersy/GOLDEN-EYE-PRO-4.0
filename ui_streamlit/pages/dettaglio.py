import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from providers.twelvedata_provider import fetch_td_15m, fetch_td_1h, fetch_td_4h
from providers.marketaux_provider import fetch_marketaux_sentiment
from providers.finnhub_provider import finnhub_provider
from providers.multi_provider import fetch_yf_ohlcv
from indicators.robust_ta import compute_indicators_15m, decide_signal
from ai.asset_analyzer import render_ai_suggestions

def get_combined_news(symbol):
    """Combina news da Marketaux e Finnhub"""
    news_data = {'count': 0, 'sentiment': 0.5, 'label': '⚪ NEUTRO', 'sources': []}
    
    # Marketaux
    try:
        marketaux = fetch_marketaux_sentiment([symbol])
        if marketaux and marketaux.get('count', 0) > 0:
            news_data['count'] += marketaux['count']
            news_data['sentiment'] = (news_data['sentiment'] + marketaux.get('sentiment', 0.5)) / 2
            news_data['sources'].append('Marketaux')
    except:
        pass
    
    # Finnhub
    try:
        finnhub_sent = finnhub_provider.get_news_sentiment(symbol)
        if finnhub_sent and finnhub_sent.get('mentions', 0) > 0:
            news_data['count'] += finnhub_sent['mentions']
            news_data['sentiment'] = (news_data['sentiment'] + finnhub_sent['sentiment']) / 2
            news_data['sources'].append('Finnhub')
    except:
        pass
    
    # Determina label
    if news_data['sentiment'] > 0.6:
        news_data['label'] = '🟢 POSITIVO'
    elif news_data['sentiment'] < 0.4:
        news_data['label'] = '🔴 NEGATIVO'
    else:
        news_data['label'] = '🟡 NEUTRO'
    
    return news_data

def fetch_market_data_triple(symbol):
    """
    Fetch dati di mercato da TRE provider contemporaneamente
    Restituisce un dizionario con tutti i risultati
    """
    results = {
        'twelvedata': {'df_15m': None, 'df_1h': None, 'df_4h': None, 'success': False},
        'yahoo': {'df_15m': None, 'df_1h': None, 'df_4h': None, 'success': False},
        'finnhub': {'df_15m': None, 'df_1h': None, 'df_4h': None, 'success': False}
    }
    
    # TwelveData
    df_15m, src = fetch_td_15m(symbol)
    if df_15m is not None:
        results['twelvedata']['df_15m'] = df_15m
        results['twelvedata']['df_1h'], _ = fetch_td_1h(symbol)
        results['twelvedata']['df_4h'], _ = fetch_td_4h(symbol)
        results['twelvedata']['success'] = True
    
    # Yahoo
    df_15m_y = fetch_yf_ohlcv(symbol, "15m", "5d")
    if df_15m_y is not None:
        results['yahoo']['df_15m'] = df_15m_y
        results['yahoo']['df_1h'] = fetch_yf_ohlcv(symbol, "1h", "1mo")
        results['yahoo']['df_4h'] = fetch_yf_ohlcv(symbol, "4h", "3mo")
        results['yahoo']['success'] = True
    
    # Finnhub (crypto o azioni)
    try:
        if symbol.endswith('USD') and len(symbol) > 4 and symbol not in ['EUR/USD', 'GBP/USD', 'USD/JPY', 'USD/CHF', 'AUD/USD', 'USD/CAD', 'NZD/USD']:
            df_fh, _ = finnhub_provider.get_crypto_historical(symbol, resolution='15', count=500)
        else:
            df_fh, _ = finnhub_provider.get_historical_candles(symbol, resolution='15', count=500)
        
        if df_fh is not None:
            results['finnhub']['df_15m'] = df_fh
            # Finnhub non ha 1h/4h predefiniti, li creiamo resample
            df_fh_1h = df_fh.copy()
            df_fh_1h['datetime'] = pd.to_datetime(df_fh['datetime'])
            df_fh_1h.set_index('datetime', inplace=True)
            df_fh_1h = df_fh_1h.resample('1h').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna().reset_index()
            results['finnhub']['df_1h'] = df_fh_1h
            
            df_fh_4h = df_fh.copy()
            df_fh_4h.set_index('datetime', inplace=True)
            df_fh_4h = df_fh_4h.resample('4h').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            }).dropna().reset_index()
            results['finnhub']['df_4h'] = df_fh_4h
            results['finnhub']['success'] = True
    except:
        pass
    
    return results

def compare_providers(results):
    """Confronta i risultati dei vari provider e restituisce il migliore"""
    comparison = []
    
    for provider, data in results.items():
        if data['success']:
            df = data['df_15m']
            comparison.append({
                'provider': provider,
                'candles': len(df),
                'last_price': df['close'].iloc[-1],
                'date_from': df['datetime'].iloc[0],
                'date_to': df['datetime'].iloc[-1]
            })
    
    return pd.DataFrame(comparison)

def show_page(symbol=None):
    if symbol is None:
        symbol = st.session_state.get('selected_asset', 'BTC-USD')
    
    st.subheader(f"📊 Dettaglio {symbol} - Multi-Provider")
    
    # Selezione modalità
    mode = st.radio(
        "Modalità provider",
        ["🔵 TwelveData", "🟢 Yahoo", "🟠 Finnhub", "🔴 Confronto tutti"],
        horizontal=True,
        help="Scegli quale provider usare per i dati storici"
    )
    
    with st.spinner("Caricamento dati da provider multipli..."):
        # Fetch dati da tutti i provider
        all_data = fetch_market_data_triple(symbol)
        
        # Mostra tabella confronto se richiesto
        if mode == "🔴 Confronto tutti":
            st.subheader("📊 Confronto provider")
            comparison_df = compare_providers(all_data)
            if not comparison_df.empty:
                st.dataframe(comparison_df, use_container_width=True)
            else:
                st.warning("Nessun provider disponibile")
        
        # Seleziona il provider attivo
        active_data = None
        source_name = ""
        
        if mode == "🔵 TwelveData" and all_data['twelvedata']['success']:
            active_data = all_data['twelvedata']
            source_name = "TwelveData"
        elif mode == "🟢 Yahoo" and all_data['yahoo']['success']:
            active_data = all_data['yahoo']
            source_name = "Yahoo Finance"
        elif mode == "🟠 Finnhub" and all_data['finnhub']['success']:
            active_data = all_data['finnhub']
            source_name = "Finnhub"
        else:
            # Fallback al primo provider disponibile
            for provider in ['twelvedata', 'yahoo', 'finnhub']:
                if all_data[provider]['success']:
                    active_data = all_data[provider]
                    source_name = provider.capitalize()
                    st.info(f"ℹ️ Provider selezionato non disponibile, usando {source_name} come fallback")
                    break
        
        if active_data is not None and active_data['df_15m'] is not None:
            df_15m = active_data['df_15m']
            df_1h = active_data['df_1h']
            df_4h = active_data['df_4h']
            
            # Arricchisci con Finnhub quote in tempo reale (sempre, se disponibile)
            finnhub_quote = None
            if all_data['finnhub']['success']:
                if symbol.endswith('USD') and len(symbol) > 4:
                    finnhub_quote, _ = finnhub_provider.get_crypto_quote(symbol)
                else:
                    finnhub_quote, _ = finnhub_provider.get_quote(symbol)
            
            df_ind = compute_indicators_15m(df_15m)
            
            # Analisi MTF
            up_1h = True
            up_4h = True
            if df_1h is not None and len(df_1h) > 50:
                up_1h = df_1h['close'].iloc[-1] > df_1h['close'].ewm(50).mean().iloc[-1]
            if df_4h is not None and len(df_4h) > 20:
                up_4h = df_4h['close'].iloc[-1] > df_4h['close'].ewm(20).mean().iloc[-1]
            
            mtf_long = up_1h and up_4h
            mtf_short = (not up_1h) and (not up_4h)
            
            signal = decide_signal(df_ind, mtf_long, mtf_short)
            
            # Prezzo: usa Finnhub se disponibile, altrimenti dati storici
            if finnhub_quote:
                current_price = finnhub_quote.get('price', float(df_15m['close'].iloc[-1]))
                st.info(f"💡 Prezzo in tempo reale da Finnhub: ${current_price:,.2f}")
            else:
                current_price = float(df_15m['close'].iloc[-1])
            
            # Metriche principali
            cols = st.columns(4)
            with cols[0]:
                st.metric("💵 Prezzo", f"${current_price:,.2f}", help=f"Fonte: {source_name}" + (" + Finnhub Real-time" if finnhub_quote else ""))
            with cols[1]:
                st.metric("📊 RSI", f"{signal['rsi']:.1f}")
            with cols[2]:
                st.metric("📈 ADX", f"{signal['adx']:.1f}")
            with cols[3]:
                st.metric("📉 ATR", f"${signal['atr']:.2f}")
            
            # Segnale
            st.markdown(f"""
            <div style="
                background: {signal['color']}20;
                border-left: 8px solid {signal['color']};
                border-radius: 16px;
                padding: 1.5rem;
                margin: 1.5rem 0;
                box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            ">
                <h3 style="color: {signal['color']}; margin: 0;">{signal['display']}</h3>
                <p style="color: #94a3b8; margin-top: 0.5rem;">
                    Forza: {signal['strength']} | MTF Long: {'✅' if mtf_long else '❌'} | MTF Short: {'✅' if mtf_short else '❌'} | Fonte: {source_name}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Grafico
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df_15m['datetime'],
                open=df_15m['open'],
                high=df_15m['high'],
                low=df_15m['low'],
                close=df_15m['close'],
                name='OHLC'
            ))
            fig.add_trace(go.Scatter(
                x=df_15m['datetime'],
                y=df_ind['ema200'],
                line=dict(color='orange', width=2),
                name='EMA 200'
            ))
            
            # Aggiungi prezzo Finnhum come linea orizzontale se disponibile
            if finnhub_quote:
                fig.add_hline(y=current_price, line_dash="dash", line_color="#f0b90b",
                             annotation_text=f"Finnhub: ${current_price:,.2f}", annotation_position="bottom right")
            
            fig.update_layout(
                template='plotly_dark',
                height=500,
                xaxis_rangeslider_visible=False,
                title=f"Andamento {symbol} (dati {source_name})",
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # News multi-provider
            st.subheader("📰 News & Sentiment")
            news = get_combined_news(symbol)
            if news['count'] > 0:
                col_n1, col_n2 = st.columns([1, 1])
                with col_n1:
                    st.info(f"📊 {news['count']} news da {', '.join(news['sources'])}")
                with col_n2:
                    st.metric("Sentiment", news['label'])
                if news['sentiment']:
                    st.progress(news['sentiment'], text=f"Sentiment score: {news['sentiment']:.2f}")
            else:
                st.caption("Nessuna news recente")
            
            # AI Analisi
            st.subheader("🤖 AI Analisi")
            data_for_ai = {
                'p': current_price,
                'rsi': signal['rsi'],
                'adx': signal['adx'],
                'atr': signal['atr'],
                'sqz_on': signal['sqz_on'],
                'v': signal['signal'],
                'level': 5 if signal['strength'] == 'STRONG' else 4 if signal['strength'] == 'WEAK' else 3,
                'mtf_long': mtf_long,
                'mtf_short': mtf_short
            }
            render_ai_suggestions(symbol, data_for_ai, news)
            
            # SL/TP
            st.subheader("💰 Risk Management")
            col_sl, col_tp, col_rr = st.columns(3)
            with col_sl:
                sl = current_price - (signal['atr'] * 2) if signal['is_long'] else current_price + (signal['atr'] * 2)
                st.metric("🛑 Stop Loss", f"${sl:.2f}", delta=f"{((sl-current_price)/current_price*100):.2f}%", border=True)
            with col_tp:
                tp = current_price + (signal['atr'] * 4) if signal['is_long'] else current_price - (signal['atr'] * 4)
                st.metric("🎯 Take Profit", f"${tp:.2f}", delta=f"{((tp-current_price)/current_price*100):.2f}%", border=True)
            with col_rr:
                risk = abs(current_price - sl)
                reward = abs(tp - current_price)
                rr = reward / risk if risk > 0 else 0
                st.metric("📊 Risk/Reward", f"1:{rr:.2f}", border=True)
            
            # Salva i dati in session_state per le altre pagine
            st.session_state.detail_data = {
                'symbol': symbol,
                'p': current_price,
                'atr': signal['atr'],
                'sig': signal['display'],
                'score': signal.get('score', 50),
                'rsi': signal['rsi'],
                'adx': signal['adx'],
                'source': source_name
            }
        else:
            st.session_state.detail_data = None
            st.error(f"❌ Impossibile caricare dati per {symbol} da nessun provider")
