# config.py
# Configurazione centralizzata per GOLDEN EYE PRO

# ============================================
# IMPOSTAZIONI GENERALI APP
# ============================================
TITLE = "GOLDEN EYE PRO"
VERSION = "4.0.0"
APP_NAME = "GOLDEN EYE PRO"
APP_ICON = "👁️"
APP_LAYOUT = "wide"
APP_THEME = "dark"

# ============================================
# WATCHLIST - FORMATO COMPATIBILE TWELVEDATA
# ============================================
DEFAULT_WATCHLIST = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD",
    "XRP-USD", "DOGE-USD", "DOT-USD", "LINK-USD", "MATIC-USD",
    "AVAX-USD", "UNI-USD", "ATOM-USD", "ALGO-USD", "VET-USD",
    "XLM-USD", "TRX-USD", "FIL-USD", "ICP-USD", "NEAR-USD",
    "APT-USD", "LTC-USD", "BCH-USD", "ETC-USD", "XMR-USD"
]
WATCHLIST_FILE = "watchlist.json"
MAX_WATCHLIST_SIZE = 50

# ============================================
# IMPOSTAZIONI CACHE
# ============================================
DISK_CACHE_ENABLED = True
DISK_CACHE_DIR = "cache"
CACHE_TTL = 3600
TTL_YF = 300
TTL_TD = 600

# ============================================
# TIMEFRAMES
# ============================================
TIMEFRAMES = {
    "15m": "15m",
    "1h": "1h", 
    "4h": "4h"
}
DEFAULT_TIMEFRAME = "15m"

# ============================================
# PARAMETRI INDICATORI
# ============================================
RSI_LEN = 14
ATR_LEN = 14
ADX_LEN = 14
ST_LEN = 7
ST_MULT = 3.0
SQUEEZE_BB_LEN = 20
SQUEEZE_KC_LEN = 20
EMA_FAST = 20
EMA_SLOW = 50
EMA_VERY_SLOW = 200

# ============================================
# SOGLIE PER SEGNALI
# ============================================
ADX_MIN = 25
RSI_LONG_MAX = 55
RSI_SHORT_MIN = 45
WEAK_RSI_LONG_MAX = 65
WEAK_RSI_SHORT_MIN = 35
WEAK_ADX_MIN = 20
WEAK_SLOPE_MIN = 0.2
SCORE_FORTE_MIN = 70

# ============================================
# COEFFICIENTI SL/TP
# ============================================
SL_ATR = 2.0
TP_ATR = 4.0
BT_SL_ATR = 1.5
BT_TP_ATR = 3.0
STRONG_SL_ATR = 1.2
STRONG_TP_ATR = 2.5
WEAK_SL_ATR = 2.0
WEAK_TP_ATR = 4.0

# ============================================
# CLASSIFICAZIONE
# ============================================
ENABLE_SIGNAL_CLASSIFICATION = True
WEAK_SIGNALS_ENABLED = True
MIN_SIGNAL_CONFIDENCE = 0.6

# ============================================
# MTF (Multi-Timeframe)
# ============================================
MTF_EMA_1H = 50
MTF_EMA_4H = 20
MTF_EMA_FAST = 20
MTF_EMA_SLOW = 50

# ============================================
# PARAMETRI BACKTEST
# ============================================
MIN_DAYS_HISTORY = 30
MAX_DAYS_HISTORY = 365
POSITION_SIZE_PCT = 0.1
MAX_POSITION_SIZE = 0.25

# ============================================
# LIMITI DI MERCATO
# ============================================
MIN_VOLUME = 50000
MIN_PRICE = 0.00001
MAX_PRICE = 1000000

# ============================================
# IMPOSTAZIONI UI
# ============================================
COLOR_STRONG_LONG = "#00ff88"
COLOR_WEAK_LONG = "#88ff88"
COLOR_STRONG_SHORT = "#ff3344"
COLOR_WEAK_SHORT = "#ff8888"
COLOR_NEUTRAL = "#f0b90b"

EMOJI_STRONG_LONG = "💪"
EMOJI_WEAK_LONG = "📈"
EMOJI_STRONG_SHORT = "💪"
EMOJI_WEAK_SHORT = "📉"
EMOJI_NEUTRAL = "⚖️"

CHART_HEIGHT = 600
CHART_WIDTH = 800

# ============================================
# IMPOSTAZIONI PROVIDER DATI
# ============================================
YF_PERIOD = "1mo"
YF_INTERVAL = "15m"
YF_15M_PERIOD = "5d"
YF_15M_INTERVAL = "15m"
YF_MAX_RETRIES = 3

TD_INTERVAL = "15min"
TD_OUTPUTSIZE = 5000
TD_MAX_RETRIES = 3

# ============================================
# IMPOSTAZIONI SCANNER
# ============================================
SCAN_INTERVAL = 300
SCAN_DEFAULT_SYMBOLS = DEFAULT_WATCHLIST
SCAN_MIN_VOLUME = 50000
SCAN_MAX_SYMBOLS = 50
SCAN_TIMEOUT = 30

# ============================================
# PARAMETRI DI VALIDAZIONE
# ============================================
MIN_DATA_POINTS = 50
MIN_CANDLES_FOR_SIGNAL = 30
MAX_DATA_POINTS = 10000
