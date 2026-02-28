# ui_streamlit/components/paper_trading.py
import streamlit as st
import pandas as pd
from datetime import datetime
from strategy.money_manager import MoneyManager

def render_paper_trading_panel(focus, current_price, atr, signal_score, signal_label):
    """Renderizza pannello paper trading"""
    
    st.markdown("## 📝 Paper Trading")
    st.caption("Simula trading con capitale virtuale")
    
    # Inizializza
    if 'paper_manager' not in st.session_state:
        st.session_state.paper_manager = MoneyManager(initial_capital=10000)
    if 'paper_trades' not in st.session_state:
        st.session_state.paper_trades = []
    
    mm = st.session_state.paper_manager
    
    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💼 Apri Trade", "📋 Storico"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        metrics = mm.get_metrics()
        
        col1.metric("Capitale", f"${mm.current_capital:,.2f}", 
                   delta=f"{metrics['total_pnl_pct']:+.2f}%")
        col2.metric("Drawdown", f"{metrics['current_drawdown']:.1f}%")
        col3.metric("Trades", metrics['trades'])
        col4.metric("Sharpe", metrics['sharpe'])
        
        # Curva equity
        if st.session_state.paper_trades:
            df = pd.DataFrame(st.session_state.paper_trades)
            df['cum_pnl'] = df['pnl'].cumsum() + 10000
            
            st.line_chart(df.set_index('time')['cum_pnl'], height=200)
    
    with tab2:
        st.markdown(f"### 📈 Segnale: {signal_label}")
        
        if atr > 0 and current_price > 0:
            rec = mm.get_position_recommendation(atr, current_price, signal_score)
            
            st.info(f"💡 Dimensione consigliata: {rec['position_size']} (rischio {rec['recommended_risk']}%)")
            
            col_a1, col_a2 = st.columns(2)
            
            with col_a1:
                direzione = st.selectbox("Direzione", ["Long", "Short"], key="paper_direction")
                entry = st.number_input("Entry", value=current_price, format="%.4f", key="paper_entry")
                size = st.number_input("Size", value=rec['position_size'], format="%.4f", key="paper_size")
            
            with col_a2:
                sl = st.number_input(
                    "Stop Loss", 
                    value=current_price - atr*2 if direzione=="Long" else current_price + atr*2, 
                    format="%.4f",
                    key="paper_sl"
                )
                tp = st.number_input(
                    "Take Profit", 
                    value=current_price + atr*4 if direzione=="Long" else current_price - atr*4, 
                    format="%.4f",
                    key="paper_tp"
                )
            
            if st.button("✅ Apri Trade (Paper)", use_container_width=True, type="primary"):
                # Simula trade
                if direzione == "Long":
                    pnl = (current_price - entry) * size
                else:
                    pnl = (entry - current_price) * size
                
                # Aggiorna capitale
                result = mm.update_after_trade(pnl)
                
                # Salva trade
                st.session_state.paper_trades.append({
                    'time': datetime.now(),
                    'asset': focus,
                    'direzione': direzione,
                    'entry': entry,
                    'exit': current_price,
                    'size': size,
                    'pnl': pnl,
                    'pnl_pct': (pnl / (entry * size)) * 100 if entry * size != 0 else 0
                })
                
                if result['stop_trading']:
                    st.error("🛑 STOP TRADING - Drawdown massimo raggiunto!")
                else:
                    st.success(f"✅ Trade chiuso! PnL: ${pnl:+.2f}")
                st.rerun()
    
    with tab3:
        if st.session_state.paper_trades:
            df = pd.DataFrame(st.session_state.paper_trades)
            df['time'] = pd.to_datetime(df['time']).dt.strftime('%d/%m %H:%M')
            
            def color_pnl(val):
                if val > 0:
                    return 'color: #00ff88'
                elif val < 0:
                    return 'color: #ff3344'
                return ''
            
            styled = df.style.map(color_pnl, subset=['pnl', 'pnl_pct'])
            st.dataframe(styled, use_container_width=True, hide_index=True)
            
            # Statistiche
            col_s1, col_s2, col_s3 = st.columns(3)
            col_s1.metric("Trades Vincenti", len(df[df['pnl'] > 0]))
            col_s2.metric("Trades Perdenti", len(df[df['pnl'] < 0]))
            col_s3.metric("Win Rate", f"{len(df[df['pnl'] > 0])/len(df)*100:.1f}%" if len(df) > 0 else "0%")
        else:
            st.info("Nessun trade eseguito")
    
    # Reset
    if st.button("🔄 Reset Paper Trading", use_container_width=True):
        st.session_state.paper_manager = MoneyManager(initial_capital=10000)
        st.session_state.paper_trades = []
        st.rerun()
