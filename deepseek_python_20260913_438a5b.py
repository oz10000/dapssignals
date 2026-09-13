# config.py
import os

# ============================================================
# PROYECTO
# ============================================================
PROJECT_NAME = "DAPS Ω × Ophelia Research Lab"
VERSION = "3.0.0"

# ============================================================
# ZONA HORARIA
# ============================================================
TIMEZONE = 'America/Argentina/Buenos_Aires'

# ============================================================
# CONSTANTES PRINCIPALES
# ============================================================
TIMEFRAME = '5m'
INITIAL_CAPITAL = 10000.0
MAX_HOLD = 60
RISK_PER_TRADE = 0.01
LEVERAGE = 3                    # ← FIX: era 1 (subutilizaba capital)

# ============================================================
# DIRECTORIOS
# ============================================================
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(ROOT_DIR, 'cache')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOGS_DIR = os.path.join(ROOT_DIR, 'logs')

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'raw'), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'trades'), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'optimization'), exist_ok=True)
os.makedirs(os.path.join(DATA_DIR, 'certifications'), exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# ============================================================
# ACTIVOS — Solo cripto con datos reales en exchanges
# ============================================================
SYMBOLS = [
    # Majors
    'BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'XRP/USDT', 'ADA/USDT',
    'DOT/USDT', 'LINK/USDT', 'AVAX/USDT', 'UNI/USDT', 'ATOM/USDT',
    'BNB/USDT', 'LTC/USDT', 'ETC/USDT',
    # Layer 1/2
    'MATIC/USDT', 'NEAR/USDT', 'APT/USDT', 'ARB/USDT', 'OP/USDT',
    'INJ/USDT', 'SEI/USDT', 'SUI/USDT',
    # DeFi
    'AAVE/USDT', 'MKR/USDT', 'CRV/USDT', 'LDO/USDT',
    # Memes con liquidez
    'DOGE/USDT', 'PEPE/USDT', 'WIF/USDT',
    # Otros
    'VET/USDT', 'ALGO/USDT', 'FTM/USDT', 'FIL/USDT', 'ICP/USDT',
    'SAND/USDT', 'MANA/USDT', 'GALA/USDT', 'AXS/USDT',
]

# ============================================================
# EXCHANGES (orden de prioridad para failover)
# ============================================================
EXCHANGE_PRIORITY = ['binance', 'okx', 'kucoin', 'mexc', 'kraken', 'bybit', 'gateio']

# ============================================================
# UMBRALES DE CLASIFICACIÓN — REESCRITOS
# ============================================================
# 🌟 OPHELIA (óptimo máximo)
OPHELIA_SCORE_MIN = 0.75
OPHELIA_ADX_MIN = 40
OPHELIA_KER_MIN = 0.70
OPHELIA_REGIMES = ['Expansión', 'Tendencia Fuerte']

# 🥇 TIER S
S_SCORE_MIN = 0.60
S_ADX_MIN = 35
S_KER_MIN = 0.60

# 🥈 TIER A
A_SCORE_MIN = 0.45
A_ADX_MIN = 28
A_KER_MIN = 0.50

# 🥉 TIER B
B_SCORE_MIN = 0.35
B_ADX_MIN = 22
B_KER_MIN = 0.42

# ============================================================
# PARÁMETROS DE GESTIÓN POR TIER
# ============================================================
# Formato: (sl_mult × ATR, tp_mult × ATR, trailing_activation, trailing_distance, be_trigger)
TIER_PARAMS = {
    'OPHELIA': {'sl': 0.6, 'tp': 3.0, 'trail_act': 0.006, 'trail_dist': 0.004, 'be_trig': 0.0010},
    'S-TIER':  {'sl': 0.6, 'tp': 2.5, 'trail_act': 0.008, 'trail_dist': 0.005, 'be_trig': 0.0015},
    'A-TIER':  {'sl': 0.5, 'tp': 1.8, 'trail_act': 0.010, 'trail_dist': 0.006, 'be_trig': 0.0020},
    'B-TIER':  {'sl': 0.4, 'tp': 1.2, 'trail_act': 0.012, 'trail_dist': 0.008, 'be_trig': 0.0025},
    'NO-TIER': {'sl': 0.4, 'tp': 1.2, 'trail_act': 0.012, 'trail_dist': 0.008, 'be_trig': 0.0025},
}

BE_BUFFER = 0.0005

# ============================================================
# PARÁMETROS POR ACTIVO
# ============================================================
ASSET_PARAMS = {
    'BTC/USDT': {'adx': 21, 'ker': 14, 'ema': 34, 'atr': 16},
    'ETH/USDT': {'adx': 16, 'ker': 12, 'ema': 21, 'atr': 14},
    'SOL/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'XRP/USDT': {'adx': 14, 'ker': 10, 'ema': 21, 'atr': 14},
    'ADA/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 14},
    'BNB/USDT': {'adx': 14, 'ker': 10, 'ema': 21, 'atr': 14},
    'DOT/USDT': {'adx': 14, 'ker': 10, 'ema': 21, 'atr': 14},
    'LINK/USDT': {'adx': 14, 'ker': 10, 'ema': 21, 'atr': 14},
    'AVAX/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 12},
    'UNI/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 12},
    'ATOM/USDT': {'adx': 14, 'ker': 10, 'ema': 21, 'atr': 14},
    'MATIC/USDT': {'adx': 10, 'ker': 8, 'ema': 13, 'atr': 10},
    'LTC/USDT': {'adx': 14, 'ker': 10, 'ema': 21, 'atr': 14},
    'ETC/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 12},
    'VET/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'ALGO/USDT': {'adx': 10, 'ker': 8, 'ema': 13, 'atr': 10},
    'FTM/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'NEAR/USDT': {'adx': 12, 'ker': 9, 'ema': 17, 'atr': 12},
    'APT/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'ARB/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'OP/USDT': {'adx': 10, 'ker': 8,   'ema': 13, 'atr': 10},
    'INJ/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 12},
    'SEI/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'SUI/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'DOGE/USDT': {'adx': 8, 'ker': 6,  'ema': 10, 'atr': 8},
    'PEPE/USDT': {'adx': 8, 'ker': 6,  'ema': 10, 'atr': 8},
    'WIF/USDT': {'adx': 8, 'ker': 6,   'ema': 10, 'atr': 8},
    'AAVE/USDT': {'adx': 12, 'ker': 9, 'ema': 17, 'atr': 12},
    'MKR/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 12},
    'CRV/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'LDO/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'SAND/USDT': {'adx': 10, 'ker': 8, 'ema': 13, 'atr': 10},
    'MANA/USDT': {'adx': 10, 'ker': 8, 'ema': 13, 'atr': 10},
    'GALA/USDT': {'adx': 10, 'ker': 8, 'ema': 13, 'atr': 10},
    'AXS/USDT': {'adx': 10, 'ker': 8,  'ema': 13, 'atr': 10},
    'FIL/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 12},
    'ICP/USDT': {'adx': 12, 'ker': 9,  'ema': 17, 'atr': 12},
}

# ============================================================
# PARÁMETROS POR DEFECTO
# ============================================================
DEFAULT_PARAMS = {
    'ophelia_score_min': OPHELIA_SCORE_MIN,
    'ophelia_adx_min': OPHELIA_ADX_MIN,
    'ophelia_ker_min': OPHELIA_KER_MIN,
    's_score_min': S_SCORE_MIN,
    's_adx_min': S_ADX_MIN,
    's_ker_min': S_KER_MIN,
    'a_score_min': A_SCORE_MIN,
    'a_adx_min': A_ADX_MIN,
    'a_ker_min': A_KER_MIN,
    'b_score_min': B_SCORE_MIN,
    'b_adx_min': B_ADX_MIN,
    'b_ker_min': B_KER_MIN,
    'tier_params': TIER_PARAMS,
    'be_buffer': BE_BUFFER,
    'max_hold': MAX_HOLD,
    'risk_per_trade': RISK_PER_TRADE,
    'leverage': LEVERAGE,
}