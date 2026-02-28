# ai/asset_analyzer.py
import streamlit as st
import numpy as np
from datetime import datetime
from typing import Dict, Any, List

class AssetAIAnalyzer:
    """
    AI Suggeritore context-aware per ogni asset - VERSIONE 4.1.0
    Integrato con sistema a 5 livelli di confidenza
    """
    
    def __init__(self):
        self.rules_engine = self._init_rules()
        self.history = {}
        self.calibration_log = []
    
    def _init_rules(self):
        """Inizializza regole di analisi calibrate"""
        return {
            'rsi': {
                'oversold': {'threshold': 30, 'weight': 12},
                'overbought': {'threshold': 70, 'weight': -12},
                'neutral_zone': {'min': 40, 'max': 60, 'weight': 3}
            },
            'adx': {
                'weak': {'threshold': 20, 'weight': -8},
                'strong': {'threshold': 25, 'weight': 8},
                'very_strong': {'threshold': 40, 'weight': 15}
            },
            'volume': {
                'low': {'ratio': 0.8, 'weight': -8},
                'high': {'ratio': 1.5, 'weight': 8}
            },
            'squeeze': {
                'on': {'weight': -10},
                'off': {'weight': 3}
            },
            'mtf_trend': {
                'aligned_bull': {'weight': 15},
                'aligned_bear': {'weight': 15},
                'mixed': {'weight': -5}
            },
            'win_rate': {
                'good': {'threshold': 55, 'weight': 8},
                'excellent': {'threshold': 60, 'weight': 12}
            },
            'news': {
                'positive': {'threshold': 0.6, 'weight': 8},
                'negative': {'threshold': 0.4, 'weight': -8},
                'many': {'threshold': 5, 'weight': 4}
            },
            'signal_alignment': {
                'match': {'weight': 20},
                'mismatch': {'weight': -15}
            },
            'signal_level': {  # NUOVO: pesi per i livelli
                'level_5': {'weight': 20, 'desc': '✅ Segnale di trading forte'},
                'level_4': {'weight': 15, 'desc': '🟡 Segnale di trading medio'},
                'level_3': {'weight': 10, 'desc': '📊 Momentum rilevato'},
                'level_2': {'weight': 5, 'desc': '📈 Tendenza di mercato'},
                'level_1': {'weight': 0, 'desc': '⚪ Mercato laterale'}
            }
        }
    
    def analyze_asset(self, symbol: str, data: Dict[str, Any], news_data: Dict = None) -> Dict:
        """
        Analisi completa dell'asset con sistema a livelli
        """
        score = 50
        signals = []
        warnings = []
        suggestions = []
        calibration_note = []
        
        main_signal = data.get('v', '')
        is_buy_signal = "ACQUISTO" in main_signal
        is_sell_signal = "VENDITA" in main_signal
        
        # ============================================================
        # 1. LIVELLO SEGNALE (NUOVO)
        # ============================================================
        signal_level = data.get('level', 1)
        
        level_weights = {
            5: self.rules_engine['signal_level']['level_5']['weight'],
            4: self.rules_engine['signal_level']['level_4']['weight'],
            3: self.rules_engine['signal_level']['level_3']['weight'],
            2: self.rules_engine['signal_level']['level_2']['weight'],
            1: self.rules_engine['signal_level']['level_1']['weight']
        }
        
        level_descs = {
            5: self.rules_engine['signal_level']['level_5']['desc'],
            4: self.rules_engine['signal_level']['level_4']['desc'],
            3: self.rules_engine['signal_level']['level_3']['desc'],
            2: self.rules_engine['signal_level']['level_2']['desc'],
            1: self.rules_engine['signal_level']['level_1']['desc']
        }
        
        score += level_weights.get(signal_level, 0)
        signals.append(f"{level_descs.get(signal_level, '')} (L{signal_level})")
        
        # Suggerimenti basati sul livello
        if signal_level >= 4:
            suggestions.append("🎯 Segnale di trading attivo - valuta entry con SL/TP standard")
        elif signal_level == 3:
            suggestions.append("⏳ Momentum in atto - aspetta conferma prima di entrare")
        elif signal_level == 2:
            suggestions.append("📊 Tendenza chiara - monitora per possibile entry")
        else:
            suggestions.append("⚪ Mercato laterale - attendi movimento significativo")
        
        # ============================================================
        # 2. RSI Analysis
        # ============================================================
        rsi = data.get('rsi', 50)
        if rsi < self.rules_engine['rsi']['oversold']['threshold']:
            score += self.rules_engine['rsi']['oversold']['weight']
            signals.append(f"🟢 RSI in oversold ({rsi:.0f}) - possibile rimbalzo")
            if is_sell_signal:
                warnings.append("⚠️ RSI oversold ma segnale VENDITA - possibile inversione")
                calibration_note.append("rsi_vs_signal_mismatch")
        elif rsi > self.rules_engine['rsi']['overbought']['threshold']:
            score += self.rules_engine['rsi']['overbought']['weight']
            signals.append(f"🔴 RSI in overbought ({rsi:.0f}) - possibile correzione")
            if is_buy_signal:
                warnings.append("⚠️ RSI overbought ma segnale ACQUISTO - possibile inversione")
                calibration_note.append("rsi_vs_signal_mismatch")
        else:
            score += 3
            signals.append(f"⚪ RSI neutrale ({rsi:.0f})")
        
        # ============================================================
        # 3. ADX Analysis
        # ============================================================
        adx = data.get('adx', 20)
        if adx >= 40:
            score += self.rules_engine['adx']['very_strong']['weight']
            signals.append(f"🔥 Trend fortissimo (ADX: {adx:.0f})")
        elif adx >= 25:
            score += self.rules_engine['adx']['strong']['weight']
            signals.append(f"📈 Trend buono (ADX: {adx:.0f})")
        elif adx < 20:
            score += self.rules_engine['adx']['weak']['weight']
            warnings.append(f"⚠️ Trend debole (ADX: {adx:.0f}) - possibile laterale")
        
        # ============================================================
        # 4. Squeeze Analysis
        # ============================================================
        if data.get('sqz_on', False):
            score += self.rules_engine['squeeze']['on']['weight']
            warnings.append("⚠️ SQUEEZE ON - esplosione imminente (attendere direzione)")
        else:
            score += self.rules_engine['squeeze']['off']['weight']
        
        # ============================================================
        # 5. MTF Alignment
        # ============================================================
        mtf_long = data.get('mtf_long', False)
        mtf_short = data.get('mtf_short', False)
        bias_long = data.get('bias_long', None)
        
        if mtf_long and bias_long is True:
            score += self.rules_engine['mtf_trend']['aligned_bull']['weight']
            signals.append("✅ Allineamento MTF BULLISH (1H+4H)")
        elif mtf_short and bias_long is False:
            score += self.rules_engine['mtf_trend']['aligned_bear']['weight']
            signals.append("✅ Allineamento MTF BEARISH (1H+4H)")
        else:
            score += self.rules_engine['mtf_trend']['mixed']['weight']
            warnings.append("⚠️ Timeframes disallineati - prudenza")
        
        # ============================================================
        # 6. Signal alignment with main signal
        # ============================================================
        ai_direction = "NEUTRALE"
        if score > 65:
            ai_direction = "BULL"
        elif score < 35:
            ai_direction = "BEAR"
        
        if (ai_direction == "BULL" and is_buy_signal) or (ai_direction == "BEAR" and is_sell_signal):
            score += self.rules_engine['signal_alignment']['match']['weight']
            signals.append("✅ AI allineata con segnale principale")
        elif (ai_direction == "BULL" and is_sell_signal) or (ai_direction == "BEAR" and is_buy_signal):
            score += self.rules_engine['signal_alignment']['mismatch']['weight']
            warnings.append("⚠️ AI in disaccordo con segnale principale - massima prudenza")
            calibration_note.append("ai_signal_mismatch")
        
        # ============================================================
        # 7. News Sentiment
        # ============================================================
        if news_data and news_data.get('count', 0) > 0:
            sentiment = news_data.get('sentiment', 0.5)
            news_count = news_data.get('count', 0)
            
            if sentiment > 0.6:
                score += self.rules_engine['news']['positive']['weight']
                signals.append(f"📰 Sentiment POSITIVO ({news_count} news)")
            elif sentiment < 0.4:
                score += self.rules_engine['news']['negative']['weight']
                signals.append(f"📰 Sentiment NEGATIVO ({news_count} news)")
            
            if news_count > 5:
                score += self.rules_engine['news']['many']['weight']
                signals.append(f"🔥 Alta copertura news ({news_count} articoli)")
        else:
            signals.append("📰 Nessuna news recente")
        
        # ============================================================
        # 8. Volatility Analysis
        # ============================================================
        atr = data.get('atr', 0)
        price = data.get('p', 1)
        atr_pct = (atr / price) * 100 if price > 0 else 0
        
        if atr_pct > 3:
            warnings.append(f"⚠️ Volatilità ALTA ({atr_pct:.1f}%) - ridurre size")
            suggestions.append("💰 Rischio consigliato: 1-1.5% del capitale")
        elif atr_pct > 2:
            suggestions.append(f"📊 Volatilità moderata ({atr_pct:.1f}%) - rischio 2%")
        elif atr_pct < 1:
            signals.append(f"📊 Volatilità bassa ({atr_pct:.1f}%) - mercato calmo")
            suggestions.append("💰 Rischio consigliato: 2-2.5% del capitale")
        
        # ============================================================
        # 9. Historical Win Rate
        # ============================================================
        if symbol in self.history:
            hist_win_rate = self.history[symbol].get('win_rate', 50)
            if hist_win_rate > 60:
                score += self.rules_engine['win_rate']['excellent']['weight']
                signals.append(f"📈 Storico eccellente su {symbol} ({hist_win_rate:.0f}% WR)")
            elif hist_win_rate > 55:
                score += self.rules_engine['win_rate']['good']['weight']
                signals.append(f"📈 Storico positivo su {symbol} ({hist_win_rate:.0f}% WR)")
        
        # ============================================================
        # 10. Position Sizing Recommendations
        # ============================================================
        if atr > 0 and price > 0:
            # Adatta SL/TP in base al livello e volatilità
            if signal_level >= 4:
                sl_factor = 2.0
                tp_factor = 4.0
                suggestions.append("📊 Usa SL/TP standard per segnali forti")
            elif signal_level == 3:
                sl_factor = 1.5
                tp_factor = 3.0
                suggestions.append("📊 SL più stretto per momentum (in attesa conferma)")
            else:
                sl_factor = 1.0
                tp_factor = 2.0
                suggestions.append("📊 Dimensioni ridotte in assenza di segnale forte")
            
            # Adatta per volatilità
            if atr_pct > 3:
                sl_factor *= 0.8
                suggestions.append("⚠️ Volatilità alta - SL ridotto")
            
            if "ai_signal_mismatch" in calibration_note:
                sl_factor *= 0.8
                suggestions.append("⚠️ Disallineamento rilevato - prudenza")
            
            suggestions.append(f"🎯 Per LONG: SL {price - atr*sl_factor:.4f} | TP {price + atr*tp_factor:.4f}")
            suggestions.append(f"🎯 Per SHORT: SL {price + atr*sl_factor:.4f} | TP {price - atr*tp_factor:.4f}")
        
        # ============================================================
        # 11. Final Score Normalization
        # ============================================================
        score = max(0, min(100, score))
        
        # Determina azione consigliata (con soglie calibrate)
        if score >= 75:
            action = "🟢 FORTE ACQUISTO"
            confidence = "ALTA"
            action_color = "#00ff88"
        elif score >= 60:
            action = "🟡 ACQUISTO"
            confidence = "MEDIA"
            action_color = "#f0b90b"
        elif score >= 45:
            action = "⚪ NEUTRALE"
            confidence = "BASSA"
            action_color = "#94a3b8"
        elif score >= 30:
            action = "🟠 VENDITA"
            confidence = "MEDIA"
            action_color = "#ff9900"
        else:
            action = "🔴 FORTE VENDITA"
            confidence = "ALTA"
            action_color = "#ff3344"
        
        # Log di calibrazione
        self.calibration_log.append({
            'timestamp': datetime.now(),
            'symbol': symbol,
            'score': score,
            'signal_level': signal_level,
            'main_signal': main_signal,
            'ai_action': action,
            'notes': calibration_note
        })
        
        return {
            'score': score,
            'action': action,
            'action_color': action_color,
            'confidence': confidence,
            'signals': signals[:3],
            'warnings': warnings[:3],
            'suggestions': suggestions[:4],
            'atr_pct': atr_pct,
            'signal_level': signal_level,
            'analysis_timestamp': datetime.now().strftime('%H:%M:%S'),
            'calibration_notes': calibration_note
        }
    
    def update_history(self, symbol: str, trade_result: Dict):
        """Aggiorna storico per apprendimento"""
        if symbol not in self.history:
            self.history[symbol] = {'trades': [], 'win_rate': 50}
        
        self.history[symbol]['trades'].append(trade_result)
        
        # Calcola win rate rolling (ultimi 20 trade)
        recent = self.history[symbol]['trades'][-20:]
        if recent:
            wins = sum(1 for t in recent if t.get('pnl', 0) > 0)
            self.history[symbol]['win_rate'] = (wins / len(recent)) * 100

def render_ai_suggestions(symbol: str, data: Dict, news_data: Dict = None):
    """Renderizza pannello AI suggestions con supporto livelli"""
    
    # Inizializza AI analyzer
    if 'ai_analyzer' not in st.session_state:
        st.session_state.ai_analyzer = AssetAIAnalyzer()
    
    analyzer = st.session_state.ai_analyzer
    
    # Analisi
    analysis = analyzer.analyze_asset(symbol, data, news_data)
    
    # UI Pannello
    st.markdown("### 🤖 AI SUGGERITORE v4.1.0")
    
    # Mostra livello segnale se disponibile
    if analysis.get('signal_level'):
        level = analysis['signal_level']
        level_colors = {5: "#00ff88", 4: "#f0b90b", 3: "#3b82f6", 2: "#8b5cf6", 1: "#94a3b8"}
        level_color = level_colors.get(level, "#94a3b8")
        
        st.markdown(f"""
        <div style='
            background: {level_color}15;
            border: 1px solid {level_color};
            border-radius: 12px;
            padding: 10px;
            margin-bottom: 15px;
            text-align: center;
        '>
            <span style='color:#94a3b8; font-size:0.8rem;'>LIVELLO SEGNALE</span>
            <div style='font-size:1.5rem; font-weight:800; color:{level_color};'>
                L{level}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Layout a 3 colonne
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, {analysis['action_color']}20, {analysis['action_color']}05);
            border: 1px solid {analysis['action_color']};
            border-radius: 16px;
            padding: 16px;
            text-align: center;
        '>
            <div style='color:#94a3b8; font-size:0.8rem;'>SCORE AI</div>
            <div style='font-size:2.5rem; font-weight:900; color:{analysis['action_color']};'>
                {analysis['score']}
            </div>
            <div style='color:#94a3b8; font-size:0.7rem;'>/100</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style='
            background: rgba(255,255,255,0.03);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='color:#94a3b8; font-size:0.8rem;'>AZIONE CONSIGLIATA</div>
            <div style='font-size:1.2rem; font-weight:800; color:{analysis['action_color']};'>
                {analysis['action']}
            </div>
            <div style='color:#94a3b8; font-size:0.7rem;'>Confidenza {analysis['confidence']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style='
            background: rgba(255,255,255,0.03);
            border: 1px solid #30363d;
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            height: 100%;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <div style='color:#94a3b8; font-size:0.8rem;'>VOLATILITÀ</div>
            <div style='font-size:1.4rem; font-weight:800; color:{"#ff3344" if analysis["atr_pct"] > 3 else "#f0b90b" if analysis["atr_pct"] > 2 else "#00ff88"};'>
                {analysis['atr_pct']:.1f}%
            </div>
            <div style='color:#94a3b8; font-size:0.7rem;'>ATR/Prezzo</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Signals e warnings
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        if analysis['signals']:
            with st.container(border=True):
                st.markdown("#### 📶 Segnali Rilevanti")
                for s in analysis['signals']:
                    st.markdown(s)
    
    with col_s2:
        if analysis['warnings']:
            with st.container(border=True):
                st.markdown("#### ⚠️ Attenzioni")
                for w in analysis['warnings']:
                    st.markdown(w)
    
    # Suggerimenti
    if analysis['suggestions']:
        with st.container(border=True):
            st.markdown("#### 💡 Suggerimenti Operativi")
            for s in analysis['suggestions']:
                st.markdown(f"- {s}")
    
    # Note di calibrazione
    if "ai_signal_mismatch" in analysis.get('calibration_notes', []):
        st.warning("⚖️ AI calibrata: peso ridotto per disallineamento")
    
    # Timestamp
    st.caption(f"Analisi AI v4.1.0: {analysis['analysis_timestamp']}")
