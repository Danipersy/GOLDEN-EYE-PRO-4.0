# strategy/auto_trader.py
import streamlit as st
import time
import threading
from datetime import datetime, timedelta
from providers.multi_provider import scan_symbol
from strategy.money_manager import MoneyManager

class AutoTrader:
    """
    Bot automatico per scan e paper trading
    """
    
    def __init__(self):
        self.is_running = False
        self.thread = None
        self.last_scan = None
        self.scan_interval = 300  # 5 minuti
        self.max_trades_per_day = 5
        self.min_signal_level = 4  # Solo L4 e L5
        self.stop_loss_atr = 2.0
        self.take_profit_atr = 4.0
        
    def start(self):
        """Avvia il bot"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_loop)
            self.thread.daemon = True
            self.thread.start()
            return True
        return False
    
    def stop(self):
        """Ferma il bot"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2)
        return True
    
    def _run_loop(self):
        """Loop principale del bot"""
        while self.is_running:
            try:
                # Esegui scan
                self._execute_scan()
                
                # Controlla trade aperti
                self._check_open_trades()
                
                # Aspetta l'intervallo
                for _ in range(self.scan_interval):
                    if not self.is_running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"AutoTrader error: {e}")
                time.sleep(60)
    
    def _execute_scan(self):
        """Esegue scan e apre posizioni"""
        if not st.session_state.get('watchlist'):
            return
        
        self.last_scan = datetime.now()
        
        # Scansiona ogni simbolo
        for symbol in st.session_state.watchlist:
            if not self.is_running:
                break
                
            # Verifica limite giornaliero
            today = datetime.now().date()
            trades_today = [t for t in st.session_state.get('auto_trades', []) 
                          if t.get('time') and t['time'].date() == today]
            
            if len(trades_today) >= self.max_trades_per_day:
                continue
            
            # Scan simbolo
            result = scan_symbol(symbol, "15m", "1mo")
            
            if result and 'error' not in result:
                # Determina livello segnale (simulato per ora)
                level = self._calculate_signal_level(result)
                
                # Apri trade se livello sufficiente
                if level >= self.min_signal_level:
                    self._open_trade(symbol, result, level)
            
            time.sleep(2)  # Pausa tra simboli
    
    def _calculate_signal_level(self, data):
        """Calcola livello segnale (1-5)"""
        # Logica semplificata - da migliorare
        change = abs(data.get('change', 0))
        if change > 2:
            return 5
        elif change > 1:
            return 4
        elif change > 0.5:
            return 3
        elif change > 0.1:
            return 2
        else:
            return 1
    
    def _open_trade(self, symbol, data, level):
        """Apre un trade automatico"""
        
        # Inizializza money manager se non esiste
        if 'auto_money_manager' not in st.session_state:
            st.session_state.auto_money_manager = MoneyManager(initial_capital=10000)
        
        mm = st.session_state.auto_money_manager
        price = data.get('price', 0)
        atr = price * 0.01  # ATR stimato (1% del prezzo)
        
        # Determina direzione in base al cambio
        direction = "LONG" if data.get('change', 0) > 0 else "SHORT"
        
        # Calcola SL/TP
        if direction == "LONG":
            sl = price - (atr * self.stop_loss_atr)
            tp = price + (atr * self.take_profit_atr)
        else:
            sl = price + (atr * self.stop_loss_atr)
            tp = price - (atr * self.take_profit_atr)
        
        # Calcola size (rischio 2%)
        risk_amount = mm.current_capital * 0.02
        stop_distance = abs(price - sl)
        size = risk_amount / stop_distance if stop_distance > 0 else 0
        
        # Registra trade
        trade = {
            'time': datetime.now(),
            'symbol': symbol,
            'direction': direction,
            'entry': price,
            'sl': sl,
            'tp': tp,
            'size': size,
            'level': level,
            'status': 'open'
        }
        
        if 'auto_trades' not in st.session_state:
            st.session_state.auto_trades = []
        
        st.session_state.auto_trades.append(trade)
        print(f"🤖 Auto trade aperto: {symbol} {direction} @ ${price:.2f} (L{level})")
    
    def _check_open_trades(self):
        """Controlla trade aperti e chiudi se SL/TP raggiunti"""
        if 'auto_trades' not in st.session_state:
            return
        
        for trade in st.session_state.auto_trades:
            if trade.get('status') != 'open':
                continue
            
            # Ottieni prezzo attuale
            result = scan_symbol(trade['symbol'], "15m", "1d")
            if not result or 'error' in result:
                continue
            
            current_price = result.get('price', 0)
            if current_price == 0:
                continue
            
            # Verifica SL/TP
            if trade['direction'] == "LONG":
                if current_price <= trade['sl']:
                    trade['status'] = 'closed'
                    trade['exit_price'] = trade['sl']
                    trade['pnl'] = (trade['sl'] - trade['entry']) * trade['size']
                    trade['exit_time'] = datetime.now()
                    trade['exit_reason'] = 'SL'
                    print(f"✅ Trade chiuso per SL: {trade['symbol']} P&L: ${trade['pnl']:.2f}")
                elif current_price >= trade['tp']:
                    trade['status'] = 'closed'
                    trade['exit_price'] = trade['tp']
                    trade['pnl'] = (trade['tp'] - trade['entry']) * trade['size']
                    trade['exit_time'] = datetime.now()
                    trade['exit_reason'] = 'TP'
                    print(f"✅ Trade chiuso per TP: {trade['symbol']} P&L: ${trade['pnl']:.2f}")
            else:  # SHORT
                if current_price >= trade['sl']:
                    trade['status'] = 'closed'
                    trade['exit_price'] = trade['sl']
                    trade['pnl'] = (trade['entry'] - trade['sl']) * trade['size']
                    trade['exit_time'] = datetime.now()
                    trade['exit_reason'] = 'SL'
                    print(f"✅ Trade chiuso per SL: {trade['symbol']} P&L: ${trade['pnl']:.2f}")
                elif current_price <= trade['tp']:
                    trade['status'] = 'closed'
                    trade['exit_price'] = trade['tp']
                    trade['pnl'] = (trade['entry'] - trade['tp']) * trade['size']
                    trade['exit_time'] = datetime.now()
                    trade['exit_reason'] = 'TP'
                    print(f"✅ Trade chiuso per TP: {trade['symbol']} P&L: ${trade['pnl']:.2f}")

def render_auto_trader_panel():
    """Renderizza pannello di controllo AutoTrader"""
    
    st.markdown("## 🤖 AutoTrader Bot")
    st.caption("Scan automatico e paper trading")
    
    # Inizializza bot in session state
    if 'auto_trader' not in st.session_state:
        st.session_state.auto_trader = AutoTrader()
    if 'auto_trades' not in st.session_state:
        st.session_state.auto_trades = []
    
    bot = st.session_state.auto_trader
    
    # Parametri configurabili
    with st.expander("⚙️ Parametri Bot", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            bot.scan_interval = st.number_input(
                "Intervallo scan (secondi)",
                min_value=60,
                max_value=3600,
                value=bot.scan_interval,
                step=60,
                key="auto_interval"
            )
        
        with col2:
            bot.max_trades_per_day = st.number_input(
                "Max trades/giorno",
                min_value=1,
                max_value=20,
                value=bot.max_trades_per_day,
                key="auto_max_trades"
            )
        
        with col3:
            bot.min_signal_level = st.select_slider(
                "Livello minimo",
                options=[1, 2, 3, 4, 5],
                value=bot.min_signal_level,
                format_func=lambda x: f"L{x}",
                key="auto_min_level"
            )
        
        col4, col5 = st.columns(2)
        with col4:
            bot.stop_loss_atr = st.slider(
                "Stop Loss (ATR)",
                min_value=1.0,
                max_value=5.0,
                value=bot.stop_loss_atr,
                step=0.5,
                key="auto_sl"
            )
        
        with col5:
            bot.take_profit_atr = st.slider(
                "Take Profit (ATR)",
                min_value=2.0,
                max_value=10.0,
                value=bot.take_profit_atr,
                step=0.5,
                key="auto_tp"
            )
    
    # Controlli
    col_start, col_stop, col_status = st.columns(3)
    
    with col_start:
        if not bot.is_running:
            if st.button("▶️ AVVIA BOT", use_container_width=True, type="primary", key="auto_start"):
                if bot.start():
                    st.success("Bot avviato!")
                    st.rerun()
        else:
            st.info("🤖 Bot in esecuzione...")
    
    with col_stop:
        if bot.is_running:
            if st.button("⏹️ FERMA BOT", use_container_width=True, key="auto_stop"):
                bot.stop()
                st.warning("Bot fermato")
                st.rerun()
    
    with col_status:
        open_trades = len([t for t in st.session_state.auto_trades if t.get('status') == 'open'])
        st.metric("Trades aperti", open_trades)
    
    # Info ultimo scan
    if bot.last_scan:
        st.caption(f"🕒 Ultimo scan: {bot.last_scan.strftime('%H:%M:%S')}")
    
    # Tabella trades automatici
    if st.session_state.auto_trades:
        st.markdown("### 📊 Trades Automatici")
        
        df_trades = []
        for t in st.session_state.auto_trades[-10:]:  # Ultimi 10
            df_trades.append({
                'Ora': t['time'].strftime('%H:%M'),
                'Simbolo': t['symbol'],
                'Direzione': t['direction'],
                'Entry': f"${t['entry']:.2f}",
                'Livello': f"L{t['level']}",
                'P&L': f"${t.get('pnl', 0):+.2f}" if 'pnl' in t else 'aperto',
                'Stato': t['status']
            })
        
        st.dataframe(df_trades, use_container_width=True, hide_index=True)
    
    # Pulsante reset
    if st.button("🔄 Reset Trades", use_container_width=True, key="auto_reset"):
        st.session_state.auto_trades = []
        st.rerun()
