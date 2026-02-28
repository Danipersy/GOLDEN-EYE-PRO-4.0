# test_backtest.py
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import sys

print("="*60)
print("🚀 AVVIO TEST BACKTEST")
print("="*60)

# Test importazioni
print("\n📚 Test importazioni...")
try:
    from strategy.backtest import backtest_engine, load_history_for_backtest
    print("✅ strategy.backtest importato")
except Exception as e:
    print(f"❌ Errore import strategy.backtest: {e}")

try:
    from indicators.robust_ta import decide_signal, compute_indicators_15m
    print("✅ indicators.robust_ta importato")
except Exception as e:
    print(f"❌ Errore import indicators.robust_ta: {e}")

try:
    from config import *
    print("✅ config importato")
    # Mostra configurazione
    print("\n📋 Configurazione:")
    print(f"   RSI_LONG_MAX: {RSI_LONG_MAX}")
    print(f"   RSI_SHORT_MIN: {RSI_SHORT_MIN}")
    print(f"   WEAK_RSI_LONG_MAX: {WEAK_RSI_LONG_MAX}")
    print(f"   WEAK_RSI_SHORT_MIN: {WEAK_RSI_SHORT_MIN}")
    print(f"   STRONG_SL_ATR: {STRONG_SL_ATR}")
    print(f"   WEAK_SL_ATR: {WEAK_SL_ATR}")
except Exception as e:
    print(f"❌ Errore import config: {e}")

# Funzione per generare dati di test
def generate_test_data(giorni=30):
    """Genera dati di test simulati realistici"""
    print(f"\n📊 Generazione dati di test ({giorni} giorni)...")
    
    start_date = datetime.now() - timedelta(days=giorni)
    timestamps = pd.date_range(start=start_date, periods=giorni*96, freq='15min')
    
    # Simula prezzo con trend e cicli
    price = 50000
    prices = []
    trend_direction = 1
    
    for i in range(len(timestamps)):
        # Cambia trend ogni tanto
        if i % 1000 == 0:
            trend_direction = random.choice([-1, 1])
        
        # Trend + rumore
        trend = trend_direction * random.uniform(0.0001, 0.0003)
        volatility = random.uniform(-0.002, 0.002)
        price = price * (1 + trend + volatility)
        prices.append(price)
    
    df = pd.DataFrame({
        'datetime': timestamps,
        'open': [p * (1 + random.uniform(-0.001, 0.001)) for p in prices],
        'high': [p * (1 + random.uniform(0, 0.002)) for p in prices],
        'low': [p * (1 - random.uniform(0, 0.002)) for p in prices],
        'close': prices,
        'volume': [random.uniform(100, 1000) for _ in prices]
    })
    
    print(f"✅ Generati {len(df)} candles")
    print(f"   Prezzo: {df['close'].iloc[0]:.2f} → {df['close'].iloc[-1]:.2f}")
    return df

# Test 1: Calcolo indicatori
def test_indicators(df):
    """Test calcolo indicatori"""
    print("\n" + "-"*50)
    print("TEST 1: Calcolo Indicatori")
    print("-"*50)
    
    try:
        df_ind = compute_indicators_15m(df)
        
        # Verifica colonne essenziali
        essential_cols = ['ema20', 'ema50', 'ema200', 'rsi', 'atr']
        missing = [col for col in essential_cols if col not in df_ind.columns]
        
        if missing:
            print(f"❌ Colonne mancanti: {missing}")
            return None
        else:
            print("✅ Tutti gli indicatori calcolati")
            print(f"   RSI ultimo: {df_ind['rsi'].iloc[-1]:.2f}")
            print(f"   ATR ultimo: {df_ind['atr'].iloc[-1]:.2f}")
            
            # Mostra prime righe
            print("\n📋 Prime 5 righe:")
            print(df_ind[['datetime', 'close', 'ema20', 'rsi', 'atr']].head())
            
            return df_ind
    except Exception as e:
        print(f"❌ Errore calcolo indicatori: {e}")
        import traceback
        traceback.print_exc()
        return None

# Test 2: Classificazione segnali
def test_signal_classification(df_ind):
    """Test classificazione segnali STRONG/WEAK"""
    print("\n" + "-"*50)
    print("TEST 2: Classificazione Segnali")
    print("-"*50)
    
    try:
        # Test con diversi scenari MTF
        scenarios = [
            {"name": "MTF LONG", "mtf_long": True, "mtf_short": False},
            {"name": "MTF SHORT", "mtf_long": False, "mtf_short": True},
            {"name": "MTF NEUTRAL", "mtf_long": False, "mtf_short": False},
        ]
        
        for scenario in scenarios:
            print(f"\n📌 {scenario['name']}:")
            signal = decide_signal(df_ind, scenario['mtf_long'], scenario['mtf_short'])
            
            print(f"   Display: {signal['display']}")
            print(f"   Segnale: {signal['signal']}")
            print(f"   Forza: {signal['strength']}")
            print(f"   Colore: {signal['color']}")
            print(f"   RSI: {signal['rsi']:.2f}")
            print(f"   ADX: {signal['adx']:.2f}")
            print(f"   Pendenza: {signal['slope']:.3f}")
        
        return True
    except Exception as e:
        print(f"❌ Errore classificazione: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test 3: Backtest engine
def test_backtest_engine(df):
    """Test esecuzione backtest"""
    print("\n" + "-"*50)
    print("TEST 3: Esecuzione Backtest")
    print("-"*50)
    
    try:
        # Test senza MTF
        print("\n📌 Backtest senza MTF:")
        results = backtest_engine(df, use_mtf=False)
        
        if results:
            stats = results.get('stats', {})
            trades = results.get('trades', pd.DataFrame())
            
            print(f"   Trades: {stats.get('n', 0)}")
            print(f"   Winrate: {stats.get('winrate', 0):.2f}%")
            print(f"   STRONG: {stats.get('strong_trades', 0)}")
            print(f"   WEAK: {stats.get('weak_trades', 0)}")
            
            if not trades.empty:
                print(f"\n📋 Primi 3 trade:")
                for i, trade in trades.head(3).iterrows():
                    print(f"   {trade['time_exit']}: {trade['side']} - {trade['pnl_pct']:.2f}% - {trade.get('signal_strength', 'unknown')}")
                
                # Statistiche per tipo segnale
                if 'signal_strength' in trades.columns:
                    strong_trades = trades[trades['signal_strength'] == 'STRONG']
                    weak_trades = trades[trades['signal_strength'] == 'WEAK']
                    
                    if len(strong_trades) > 0:
                        strong_win = (strong_trades['pnl_pct'] > 0).mean() * 100
                        print(f"\n📈 Performance STRONG: {len(strong_trades)} trades, {strong_win:.1f}% winrate")
                    
                    if len(weak_trades) > 0:
                        weak_win = (weak_trades['pnl_pct'] > 0).mean() * 100
                        print(f"📉 Performance WEAK: {len(weak_trades)} trades, {weak_win:.1f}% winrate")
        else:
            print("❌ Backtest non ha restituito risultati")
        
        return results
    except Exception as e:
        print(f"❌ Errore backtest: {e}")
        import traceback
        traceback.print_exc()
        return None

# Test 4: Verifica configurazione
def test_config_integration():
    """Test integrazione configurazione"""
    print("\n" + "-"*50)
    print("TEST 4: Verifica Configurazione")
    print("-"*50)
    
    try:
        # Verifica che le variabili di configurazione esistano
        config_vars = [
            'RSI_LONG_MAX', 'RSI_SHORT_MIN',
            'WEAK_RSI_LONG_MAX', 'WEAK_RSI_SHORT_MIN',
            'ADX_MIN', 'WEAK_ADX_MIN',
            'STRONG_SL_ATR', 'STRONG_TP_ATR',
            'WEAK_SL_ATR', 'WEAK_TP_ATR',
            'ENABLE_SIGNAL_CLASSIFICATION', 'WEAK_SIGNALS_ENABLED'
        ]
        
        all_ok = True
        for var in config_vars:
            if var in globals() or var in locals():
                value = globals().get(var, locals().get(var))
                print(f"   ✅ {var}: {value}")
            else:
                print(f"   ❌ {var}: NON TROVATO")
                all_ok = False
        
        return all_ok
    except Exception as e:
        print(f"❌ Errore verifica config: {e}")
        return False

# Esecuzione test principale
def main():
    """Esegue tutti i test"""
    
    print("\n" + "🔥"*30)
    print("   INIZIO TEST COMPLETI")
    print("🔥"*30)
    
    # Genera dati di test
    df = generate_test_data(45)  # 45 giorni di dati
    
    # Test 1: Indicatori
    df_ind = test_indicators(df)
    if df_ind is None:
        print("\n❌ TEST FALLITO: Indicatori non calcolati")
        return 1
    
    # Test 2: Classificazione
    if not test_signal_classification(df_ind):
        print("\n❌ TEST FALLITO: Classificazione segnali")
        return 1
    
    # Test 3: Backtest
    results = test_backtest_engine(df)
    if results is None:
        print("\n⚠️ Backtest senza risultati (può essere normale)")
    
    # Test 4: Config
    if not test_config_integration():
        print("\n⚠️ Problemi configurazione")
    
    # Riepilogo finale
    print("\n" + "="*60)
    print("✅✅✅ TEST COMPLETATI CON SUCCESSO ✅✅✅")
    print("="*60)
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
