# config.py
# Configurazione centralizzata per GOLDEN EYE PRO
# VERSIONE COMPLETA CON TUTTE LE VARIABILI

# ============================================
# IMPOSTAZIONI GENERALI APP
# ============================================
TITLE = "GOLDEN EYE PRO"
VERSION = "1.0.0"
APP_NAME = "GOLDEN EYE PRO"
APP_ICON = "👁️"
APP_LAYOUT = "wide"
APP_THEME = "dark"

# ============================================
# WATCHLIST
# ============================================
DEFAULT_WATCHLIST = [
    "BTC-USD", "ETH-USD", "BNB-USD", "SOL-USD", "ADA-USD",
    "DOT-USD", "LINK-USD", "MATIC-USD", "AVAX-USD", "UNI-USD"
]
WATCHLIST_FILE = "watchlist.json"
MAX_WATCHLIST_SIZE = 50
WATCHLIST_CACHE_FILE = "watchlist_cache.json"

# ============================================
# IMPOSTAZIONI CACHE
# ============================================
DISK_CACHE_ENABLED = True
DISK_CACHE_DIR = "cache"
CACHE_TTL = 3600  # 1 ora in secondi
CACHE_MAXSIZE = 1000
CACHE_THRESHOLD = 500

# TTL specifici per diversi provider (in secondi)
TTL_YF = 300        # Yahoo Finance: 5 minuti
TTL_TD = 60         # TwelveData: 1 minuto
TTL_MARKETAUX = 600 # MarketAux: 10 minuti
TTL_CACHE = 300     # Cache generica: 5 minuti

# ============================================
# API KEYS
# ============================================
TWELVEDATA_KEY = ""
MARKETAUX_KEY = ""
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
ALPHA_VANTAGE_KEY = "O2MEU23NZEWUYTKY"
FINNHUB_KEY = ""

# ============================================
# IMPOSTAZIONI GENERALI SIMBOLI
# ============================================
DEFAULT_SYMBOLS = DEFAULT_WATCHLIST
SYMBOL_SEPARATOR = "/"
SYMBOL_CASE = "upper"  # upper, lower, asis
SYMBOL_PREFIX = ""
SYMBOL_SUFFIX = ""

# ============================================
# TIMEFRAMES
# ============================================
TIMEFRAMES = {
    "15m": "15m",
    "1h": "1h", 
    "4h": "4h",
    "1d": "1d",
    "1w": "1w"
}
DEFAULT_TIMEFRAME = "15m"
TIMEFRAME_OPTIONS = ["15m", "1h", "4h", "1d", "1w"]

# ============================================
# PARAMETRI INDICATORI BASE
# ============================================
RSI_LEN = 14
RSI_OVERSOLD = 30
RSI_OVERBOUGHT = 70

ATR_LEN = 14
ADX_LEN = 14
ADX_STRONG = 25

# EMA
EMA_FAST = 20
EMA_SLOW = 50
EMA_VERY_SLOW = 200
EMA_CROSSOVER_THRESHOLD = 0.5

# MACD
MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

# Bollinger Bands
BB_LEN = 20
BB_STD = 2.0

# SuperTrend
ST_LEN = 7
ST_MULT = 3.0
ST_FACTOR = 3.0

# Squeeze
SQUEEZE_BB_LEN = 20
SQUEEZE_KC_LEN = 20
SQUEEZE_KC_MULT = 1.5

# ============================================
# SOGLIE PER SEGNALI STRONG
# ============================================
ADX_MIN = 25
RSI_LONG_MAX = 55
RSI_SHORT_MIN = 45
SLOPE_STRONG_THRESHOLD = 1.0

# ============================================
# PARAMETRI PER SEGNALI DEBOLI
# ============================================
WEAK_RSI_LONG_MAX = 65
WEAK_RSI_SHORT_MIN = 35
WEAK_ADX_MIN = 20
WEAK_SLOPE_MIN = 0.2
WEAK_SIGNAL_FACTOR = 0.7

# ============================================
# COEFFICIENTI SL/TP
# ============================================
SL_ATR = 1.5
TP_ATR = 3.0
BT_SL_ATR = 1.5
BT_TP_ATR = 3.0

STRONG_SL_ATR = 1.2
STRONG_TP_ATR = 2.5
WEAK_SL_ATR = 2.0
WEAK_TP_ATR = 4.0

MIN_SL_PERCENT = 0.5
MAX_SL_PERCENT = 5.0
MIN_TP_PERCENT = 1.0
MAX_TP_PERCENT = 10.0

# ============================================
# PARAMETRI PER CLASSIFICAZIONE
# ============================================
ENABLE_SIGNAL_CLASSIFICATION = True
WEAK_SIGNALS_ENABLED = True
MIN_SIGNAL_CONFIDENCE = 0.6
SIGNAL_CONFIDENCE_STRONG = 0.8
SIGNAL_CONFIDENCE_WEAK = 0.5

# ============================================
# PARAMETRI MTF (Multi-Timeframe)
# ============================================
MTF_EMA_1H = 50
MTF_EMA_4H = 20
MTF_ENABLED = True
MTF_WEIGHT_15M = 0.3
MTF_WEIGHT_1H = 0.3
MTF_WEIGHT_4H = 0.4

# ============================================
# PARAMETRI BACKTEST
# ============================================
MIN_DAYS_HISTORY = 15
MAX_DAYS_HISTORY = 365
POSITION_SIZE_PCT = 0.1
MAX_POSITION_SIZE = 0.25
MAX_TRADES_PER_DAY = 10
BACKTEST_COMMISSION = 0.001  # 0.1%
BACKTEST_SLIPPAGE = 0.001    # 0.1%

# ============================================
# LIMITI DI MERCATO
# ============================================
MIN_VOLUME = 50000
MIN_PRICE = 0.00001
MAX_PRICE = 1000000
MIN_MARKET_CAP = 1000000
MAX_SPREAD_PERCENT = 0.5

# ============================================
# IMPOSTAZIONI UI
# ============================================
COLOR_STRONG_LONG = "#00ff88"
COLOR_WEAK_LONG = "#88ff88"
COLOR_STRONG_SHORT = "#ff3344"
COLOR_WEAK_SHORT = "#ff8888"
COLOR_NEUTRAL = "#f0b90b"
COLOR_BACKGROUND = "#0E1117"
COLOR_TEXT = "#FAFAFA"

EMOJI_STRONG_LONG = "💪"
EMOJI_WEAK_LONG = "📈"
EMOJI_STRONG_SHORT = "💪"
EMOJI_WEAK_SHORT = "📉"
EMOJI_NEUTRAL = "⚖️"
EMOJI_LOADING = "🔄"
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_WARNING = "⚠️"

CHART_HEIGHT = 600
CHART_WIDTH = 800
CHART_TEMPLATE = "plotly_dark"

# ============================================
# IMPOSTAZIONI PROVIDER DATI - MODIFICATE!
# ============================================
YF_PERIOD = "3mo"           # Aumentato da 1mo
YF_INTERVAL = "15m"
YF_MAX_RETRIES = 3
YF_TIMEOUT = 10

TD_INTERVAL = "15min"
TD_OUTPUTSIZE = 5000
TD_MAX_RETRIES = 3
TD_TIMEOUT = 10

# ============================================
# IMPOSTAZIONI SCANNER
# ============================================
SCAN_INTERVAL = 300
SCAN_DEFAULT_SYMBOLS = DEFAULT_WATCHLIST
SCAN_MIN_VOLUME = 50000
SCAN_MAX_SYMBOLS = 50
SCAN_THREADS = 5
SCAN_TIMEOUT = 30

# ============================================
# IMPOSTAZIONI PAPER TRADING
# ============================================
PAPER_TRADING_CAPITAL = 10000
PAPER_TRADING_FILE = "paper_trading.json"
PAPER_TRADING_MAX_POSITIONS = 10
PAPER_TRADING_MAX_DAILY_LOSS = 0.05  # 5%

# ============================================
# LOGGING
# ============================================
LOG_LEVEL = "INFO"
LOG_FILE = "app.log"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_MAX_BYTES = 10485760  # 10MB
LOG_BACKUP_COUNT = 5

# ============================================
# FEATURE FLAGS
# ============================================
ENABLE_PAPER_TRADING = True
ENABLE_BACKTEST = True
ENABLE_SCANNER = True
ENABLE_MTF = True
ENABLE_TELEGRAM = False
ENABLE_CACHE = True
ENABLE_LOGGING = True
ENABLE_METRICS = True
ENABLE_ALERTS = True
ENABLE_NOTIFICATIONS = False

# ============================================
# PARAMETRI DI SISTEMA
# ============================================
DEBUG_MODE = False
TEST_MODE = False
PRODUCTION_MODE = True
MAX_WORKERS = 4
REQUEST_TIMEOUT = 30
RETRY_ATTEMPTS = 3
RETRY_DELAY = 1

# ============================================
# PARAMETRI DI PERFORMANCE
# ============================================
BATCH_SIZE = 100
CHUNK_SIZE = 1000
PREFETCH_SIZE = 10
POOL_SIZE = 4

# ============================================
# PARAMETRI DI SICUREZZA
# ============================================
ENABLE_RATE_LIMITING = True
MAX_REQUESTS_PER_MINUTE = 60
MAX_REQUESTS_PER_HOUR = 1000
RATE_LIMIT_WINDOW = 60  # secondi

# ============================================
# PARAMETRI DI VALIDAZIONE - MODIFICATI!
# ============================================
MIN_DATA_POINTS = 50        # Ridotto da 100
MIN_CANDLES_FOR_SIGNAL = 30
MAX_DATA_POINTS = 10000
MIN_DATE_RANGE = "2020-01-01"
MAX_DATE_RANGE = "2026-12-31"

# ============================================
# PARAMETRI DI EXPORT
# ============================================
EXPORT_FORMATS = ["csv", "json", "excel"]
EXPORT_DIR = "exports"
EXPORT_FILENAME_PREFIX = "export"
EXPORT_INCLUDE_TIMESTAMP = True

#Defeatbeta settings (nessuna chiave necessaria!)
DEFEATBETA_ENABLED = True

# Fallback a dati fake se tutto fallisce
USE_FAKE_DATA_FALLBACK = True