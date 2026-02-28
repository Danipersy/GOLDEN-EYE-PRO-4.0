# test_weak_signals.py

import logging
from datetime import datetime, timedelta
import random
from typing import List

from models.signal import Signal, SignalType, SignalDirection
from models.candle import Candle
from models.trade import Trade, TradeStatus
from patterns.pattern_analyzer import PatternAnalyzer
from patterns.pattern_base import Pattern
from backtesting.backtester import Backtester

# Configura logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Crea un pattern di esempio per test
class SampleWeakPattern(Pattern):
    """Pattern debole di esempio per test"""
    
    def get_name(self) -> str:
        return "Sample Weak Pattern"
    
    def analyze(self, candles: List[Candle]) -> List[Signal]:
        """Genera segnali deboli di esempio"""
        signals = []
        
        if len(candles) < 10:
            return signals
            
        # Genera un segnale ogni 5 candles per test
        for i in range(5, len(candles), 5):
            candle = candles[i]
            
            # Alterna long/short
            direction = SignalDirection.LONG if i % 2 == 0 else SignalDirection.SHORT
            
            signal = Signal(
                symbol="TEST",
                direction=direction,
                entry_price=candle.close,
                timestamp=candle.timestamp,
                signal_type=SignalType.WEAK,  # Segnale debole
                confidence=0.7
            )
            
            signals.append(signal)
            
        return signals

class SampleStrongPattern(Pattern):
    """Pattern forte di esempio per test"""
    
    def get_name(self) -> str:
        return "Sample Strong Pattern"
    
    def analyze(self, candles: List[Candle]) -> List[Signal]:
        """Genera segnali forti con SL/TP predefiniti"""
        signals = []
        
        if len(candles) < 10:
            return signals
            
        # Genera un segnale ogni 8 candles
        for i in range(7, len(candles), 8):
            candle = candles[i]
            
            # Alterna long/short
            if i % 2 == 0:
                signal = Signal(
                    symbol="TEST",
                    direction=SignalDirection.LONG,
                    entry_price=candle.close,
                    timestamp=candle.timestamp,
                    signal_type=SignalType.STRONG,
                    stop_loss=candle.close * 0.98,  # -2%
                    take_profit=candle.close * 1.04,  # +4%
                    confidence=0.9
                )
            else:
                signal = Signal(
                    symbol="TEST",
                    direction=SignalDirection.SHORT,
                    entry_price=candle.close,
                    timestamp=candle.timestamp,
                    signal_type=SignalType.STRONG,
                    stop_loss=candle.close * 1.02,  # +2%
                    take_profit=candle.close * 0.96,  # -4%
                    confidence=0.9
                )
            
            signals.append(signal)
            
        return signals

def generate_test_candles(num_candles: int = 100) -> List[Candle]:
    """Genera dati di test"""
    candles = []
    start_date = datetime(2024, 1, 1)
    price = 50000
    
    for i in range(num_candles):
        timestamp = start_date + timedelta(hours=i)
        
        # Simula movimento prezzo
        change = random.uniform(-0.02, 0.02)
        price = price * (1 + change)
        
        candle = Candle(
            symbol="TEST",
            timestamp=timestamp,
            open=price * (1 + random.uniform(-0.001, 0.001)),
            high=price * (1 + random.uniform(0, 0.005)),
            low=price * (1 - random.uniform(0, 0.005)),
            close=price,
            volume=random.uniform(100, 1000)
        )
        
        candles.append(candle)
        
    return candles

def main():
    print("=== Test Weak Signals with SL/TP ===\n")
    
    # 1. Setup
    analyzer = PatternAnalyzer(atr_period=14)
    backtester = Backtester(initial_capital=10000)
    
    # 2. Registra pattern
    analyzer.register_pattern(SampleWeakPattern())
    analyzer.register_pattern(SampleStrongPattern())
    
    # 3. Genera dati di test
    candles = generate_test_candles(100)
    print(f"Generated {len(candles)} test candles")
    
    # 4. Calcola ATR per riferimento
    atr_series = analyzer.calculate_atr(candles)
    print(f"Current ATR: {atr_series.iloc[-1]:.2f}\n")
    
    # 5. Analizza e genera segnali
    signals = analyzer.analyze(candles)
    
    print("=== Generated Signals ===")
    weak_count = 0
    strong_count = 0
    
    for i, signal in enumerate(signals):
        if signal.signal_type == SignalType.WEAK:
            weak_count += 1
            print(f"\n[{i}] WEAK Signal - {signal.direction.value}")
            print(f"    Entry: {signal.entry_price:.2f}")
            print(f"    SL: {signal.stop_loss:.2f} (calc: {signal.metadata.get('exit_calculation', 'unknown')})")
            print(f"    TP: {signal.take_profit:.2f}")
            print(f"    ATR used: {signal.metadata.get('atr_value', 'N/A')}")
        else:
            strong_count += 1
            print(f"\n[{i}] STRONG Signal - {signal.direction.value}")
            print(f"    Entry: {signal.entry_price:.2f}")
            print(f"    SL: {signal.stop_loss:.2f}")
            print(f"    TP: {signal.take_profit:.2f}")
    
    print(f"\nSummary: {weak_count} weak signals, {strong_count} strong signals")
    
    # 6. Esegui backtest
    print("\n=== Backtest Results ===")
    results = backtester.run(signals, candles)
    
    for key, value in results.items():
        if isinstance(value, float):
            print(f"{key}: {value:.2f}")
        else:
            print(f"{key}: {value}")
    
    # 7. Mostra dettaglio trades
    print("\n=== Trade Details ===")
    for i, trade in enumerate(backtester.trades):
        print(f"\nTrade {i+1}:")
        print(f"  Direction: {trade.direction.value}")
        print(f"  Entry: {trade.entry_price:.2f} @ {trade.entry_time}")
        print(f"  Exit: {trade.exit_price:.2f} @ {trade.exit_time}")
        print(f"  SL: {trade.stop_loss:.2f}, TP: {trade.take_profit:.2f}")
        print(f"  P&L: {trade.pnl:.2f}")

if __name__ == "__main__":
    main()
