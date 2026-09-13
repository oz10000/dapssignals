# ophelia_v2_config.py
"""
Configuración OPHELIA v3 — Sistema de 2 niveles.
"""
import os

# ============================================================
# SISTEMA DE 2 NIVELES
# ============================================================
# Nivel 1: OPHELIA (máximo edge, máxima exigencia)
OPHELIA_SCORE_THRESHOLD = 0.75    # ajustable por el optimizer
OPHELIA_MAX_PER_DAY = 2           # máximo de OPHELIA por día

# Nivel 2: STANDARD (menor edge, mayor frecuencia)
STANDARD_SCORE_THRESHOLD = 0.55   # ajustable por el optimizer
STANDARD_MAX_PER_DAY = 5          # máximo de STANDARD por día

# Cooldown entre señales del mismo activo (ambos niveles)
COOLDOWN_MINUTES_PER_SYMBOL = 60
MAX_TRADES_PER_DAY_PER_SYMBOL = 2

# ============================================================
# FEATURES DEL MODELO (mismas que v2)
# ============================================================
MODEL_FEATURES = [
    'adx', 'ker', 'score', 'atr_pct_rel', 'volume_ratio',
    'ema_dist_15_atr', 'ema_dist_50_atr', 'adx_acceleration',
    'hour_sin', 'hour_cos', 'weekday_sin', 'weekday_cos',
    'regime_expansion', 'regime_trend', 'regime_chop',
]

# ============================================================
# OPTIMIZADOR DE THRESHOLD
# ============================================================
# Grid amplio para OPHELIA (alta exigencia)
OPHELIA_THRESHOLD_GRID = [0.65, 0.70, 0.72, 0.75, 0.78, 0.80, 0.82, 0.85]

# Grid para STANDARD (menor exigencia)
STANDARD_THRESHOLD_GRID = [0.45, 0.50, 0.52, 0.55, 0.58, 0.60, 0.62, 0.65]

# Objetivo: maximizar WR sujeto a trades/día ≥ min
MIN_OPHELIA_PER_DAY = 0.3         # al menos 0.3 OPHELIA/día (permite días sin)
MIN_STANDARD_PER_DAY = 1.5

# ============================================================
# MODELO ML
# ============================================================
MODEL_TYPE = 'logistic'
MODEL_RANDOM_STATE = 42
MODEL_TEST_SIZE = 0.30

# ============================================================
# LEVERAGE (per-signal ahora)
# ============================================================
LEVERAGE_SAFETY_FACTOR = 2.5
MAE_PERCENTILE = 95
LIQUIDATION_THRESHOLD = 0.90
LEVERAGE_PROFILE = 'moderate'
LEVERAGE_PROFILES = {
    'conservative': 0.40,
    'moderate': 0.70,
    'aggressive': 1.00,
}

# Leverage máximo por nivel
OPHELIA_MAX_LEVERAGE = 30         # OPHELIA puede usar hasta 30x
STANDARD_MAX_LEVERAGE = 10        # STANDARD limitado a 10x

# ============================================================
# TP / SL / TRAILING
# ============================================================
TP_CAPTURE_RATIO = 0.85
SL_SAFETY_MARGIN = 1.5
TRAILING_ACTIVATION_RATIO = 0.5
TRAILING_DISTANCE_RATIO = 0.30

# ============================================================
# CERTIFICACIÓN
# ============================================================
MIN_TRADES_TRAIN = 60
MIN_TRADES_TEST = 20
MIN_OPHELIA_CERTIFIED_WR = 0.55   # mínimo 55% para OPHELIA
MIN_STANDARD_CERTIFIED_WR = 0.50  # mínimo 50% para STANDARD
MAX_OVERFIT_DEGRADATION = 0.15

# ============================================================
# ANÁLISIS TEMPORAL
# ============================================================
TIMEZONE_AR = 'America/Argentina/Buenos_Aires'
SESSION_SPLIT_HOUR = 14           # 14h ARG divide mañana/tarde

# ============================================================
# BACKTEST
# ============================================================
BACKTEST_DAYS = 90
BACKTEST_TIMEFRAME = '5m'
MAX_HOLD_BARS = 24

# ============================================================
# DIRECTORIOS
# ============================================================
OPHELIA_V2_DIR = 'data/ophelia_v2'
OPHELIA_V2_MODEL = os.path.join(OPHELIA_V2_DIR, 'model.pkl')
OPHELIA_V2_METADATA = os.path.join(OPHELIA_V2_DIR, 'metadata.json')
OPHELIA_V2_TRADES = os.path.join(OPHELIA_V2_DIR, 'trades.parquet')
OPHELIA_V2_DAILY = os.path.join(OPHELIA_V2_DIR, 'daily_selection.parquet')
OPHELIA_V2_REPORT = 'reports/OPHELIA_DAILY_CERTIFICATION_REPORT.md'

os.makedirs(OPHELIA_V2_DIR, exist_ok=True)
os.makedirs('reports', exist_ok=True)
