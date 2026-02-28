# strategy/money_manager.py
import streamlit as st
import pandas as pd
import numpy as np

class MoneyManager:
    """
    Gestione del capitale e risk management
    """
    
    def __init__(self, initial_capital=10000):
        self.initial_capital = initial_capital
        self.current_capital = initial_capital
        self.peak_capital = initial_capital
        self.trades_history = []
        self.max_risk_per_trade = 0.02  # 2%
        self.max_risk_total = 0.06      # 6%
        self.max_drawdown_limit = 0.20  # 20%
        
    def calculate_position_size(self, price, stop_distance, risk_percent=None):
        """
        Calcola dimensione posizione ottimale
        """
        if risk_percent is None:
            risk_percent = self.max_risk_per_trade
        
        risk_amount = self.current_capital * risk_percent
        position_size = risk_amount / stop_distance
        
        # Limita a max 25% del capitale in una posizione
        max_size_by_capital = self.current_capital * 0.25 / price
        position_size = min(position_size, max_size_by_capital)
        
        return {
            'size': round(position_size, 4),
            'risk_amount': round(risk_amount, 2),
            'risk_percent': risk_percent * 100,
            'capital_used': round(position_size * price, 2)
        }
    
    def update_after_trade(self, pnl):
        """
        Aggiorna capitale dopo trade
        """
        self.current_capital += pnl
        if self.current_capital > self.peak_capital:
            self.peak_capital = self.current_capital
        
        drawdown = (self.peak_capital - self.current_capital) / self.peak_capital
        
        self.trades_history.append({
            'pnl': pnl,
            'capital': self.current_capital,
            'drawdown': drawdown
        })
        
        return {
            'new_capital': self.current_capital,
            'drawdown': drawdown,
            'stop_trading': drawdown > self.max_drawdown_limit
        }
    
    def get_metrics(self):
        """
        Calcola metriche di performance
        """
        if not self.trades_history:
            return {
                'total_pnl': 0,
                'total_pnl_pct': 0,
                'current_drawdown': 0,
                'max_drawdown': 0,
                'sharpe': 0,
                'trades': 0,
                'current_capital': self.current_capital
            }
        
        df = pd.DataFrame(self.trades_history)
        
        total_pnl = df['pnl'].sum()
        total_pnl_pct = (total_pnl / self.initial_capital) * 100
        current_drawdown = df['drawdown'].iloc[-1]
        max_drawdown = df['drawdown'].max()
        
        # Sharpe ratio approssimato
        returns = df['pnl'] / self.initial_capital
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0
        
        return {
            'total_pnl': round(total_pnl, 2),
            'total_pnl_pct': round(total_pnl_pct, 2),
            'current_drawdown': round(current_drawdown * 100, 2),
            'max_drawdown': round(max_drawdown * 100, 2),
            'sharpe': round(sharpe, 2),
            'trades': len(self.trades_history),
            'current_capital': round(self.current_capital, 2)
        }
    
    def get_position_recommendation(self, atr, price, signal_strength):
        """
        Raccomandazione dimensionamento basata su condizioni di mercato
        """
        base_risk = self.max_risk_per_trade
        
        # Riduci rischio se ATR alto (volatilità)
        atr_pct = (atr / price) * 100
        if atr_pct > 3:
            base_risk *= 0.7
        elif atr_pct > 2:
            base_risk *= 0.85
        
        # Aumenta rischio se segnale forte (score alto)
        if signal_strength > 80:
            base_risk *= 1.2
        elif signal_strength < 50:
            base_risk *= 0.5
        
        # Limiti
        base_risk = max(0.01, min(0.03, base_risk))
        
        stop_distance = atr * 2
        pos_size = self.calculate_position_size(price, stop_distance, base_risk)
        
        return {
            'recommended_risk': round(base_risk * 100, 1),
            'position_size': pos_size['size'],
            'capital_needed': pos_size['capital_used'],
            'risk_amount': pos_size['risk_amount'],
            'stop_distance': round(stop_distance, 4)
        }

def render_money_manager_panel(current_price, atr, signal_score):
    """Renderizza pannello money management"""
    
    st.markdown("## 💰 Money Management")
    st.caption("Gestione del capitale e calcolo dimensioni posizioni")
    
    # Inizializza money manager in session state
    if 'money_manager' not in st.session_state:
        st.session_state.money_manager = MoneyManager(initial_capital=10000)
    
    mm = st.session_state.money_manager
    
    with st.expander("📊 Gestione Capitale", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            metrics = mm.get_metrics()
            st.metric("Capitale Iniziale", f"${mm.initial_capital:,.0f}")
            st.metric("Capitale Attuale", f"${mm.current_capital:,.2f}", 
                     delta=f"{metrics['total_pnl_pct']:+.2f}%")
        
        with col2:
            st.metric("Drawdown Attuale", f"{metrics['current_drawdown']:.1f}%")
            st.metric("Max Drawdown", f"{metrics['max_drawdown']:.1f}%")
        
        with col3:
            st.metric("Trades Eseguiti", metrics['trades'])
            st.metric("Sharpe Ratio", metrics['sharpe'])
        
        # Raccomandazione posizione
        if atr > 0 and current_price > 0:
            rec = mm.get_position_recommendation(atr, current_price, signal_score)
            
            st.markdown("### 🎯 Raccomandazione per questo trade")
            
            col_r1, col_r2, col_r3, col_r4 = st.columns(4)
            col_r1.metric("Rischio Consigliato", f"{rec['recommended_risk']}%")
            col_r2.metric("Dimensione", rec['position_size'])
            col_r3.metric("Capitale Richiesto", f"${rec['capital_needed']:,.2f}")
            col_r4.metric("Importo Rischio", f"${rec['risk_amount']:,.2f}")
            
            if rec['recommended_risk'] < 1.5:
                st.warning("⚠️ Rischio ridotto - volatilità alta o segnale debole")
            elif rec['recommended_risk'] > 2.5:
                st.success("✅ Rischio aumentato - ottima opportunità!")
    
    # Bottone per resettare (nuovo capitale)
    if st.button("🔄 Reset Money Management", use_container_width=True):
        st.session_state.money_manager = MoneyManager(initial_capital=10000)
        st.rerun()
