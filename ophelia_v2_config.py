# ophelia_v2_config.py
"""
Configuración OPHELIA v3 — Sistema de 2 niveles con anti-overfitting.
FIX: features reducidos de 15 → 3 para evitar overfitting.
"""
import os

# ============================================================
# SISTEMA DE 2 NIVELES
# ============================================================
OPHELIA_SCORE_THRESHOLD = 0.65
OPHELIA_MAX_PER_DAY = 2

STANDARD_SCORE_THRESHOLD = 0.50
STANDARD_MAX_PER_DAY = 5

# ============================================================
# COOLDOWN
# ============================================================
COOLDOWN_MINUTES_PER_SYMBOL = 60
MAX_TRADES_PER_DAY_PER_SYMBOL = 2

# ============================================================
# FEATURES DEL MODELO — REDUCIDO A 3
# ============================================================
# FIX CRÍTICO: reducir de 15 a 3 features.
# Regla: mínimo 10 trades por feature.
# Con 3 features → mínimo 30 trades en test.
MODEL_FEATURES = [
    'adx',
    'ker',
    'score',
]

# ============================================================
# OPTIMIZADOR DE THRESHOLD
# ============================================================
OPHELIA_THRESHOLD_GRID = [0.55, 0.60, 0.62, 0.65, 0.68, 0.70, 0.72]
STANDARD_THRESHOLD_GRID = [0.45, 0.48, 0.50, 0.52, 0.55, 0.58, 0.60]

MIN_OPHELIA_PER_DAY = 0.3
MIN_STANDARD_PER_DAY = 1.5

# ============================================================
# MODELO ML
# ============================================================
MODEL_TYPE = 'logistic'
MODEL_RANDOM_STATE = 42
MODEL_TEST_SIZE = 0.30

# ============================================================
# LEVERAGE
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

OPHELIA_MAX_LEVERAGE = 30
STANDARD_MAX_LEVERAGE = 10

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
MIN_TRADES_TRAIN = 100
MIN_TRADES_TEST = 40
MIN_OPHELIA_CERTIFIED_WR = 0.55
MIN_STANDARD_CERTIFIED_WR = 0.50
MAX_OVERFIT_DEGRADATION = 0.15

# AUC mínimo para que el modelo se considere válido
MIN_AUC_TEST = 0.55

# ============================================================
# ANÁLISIS TEMPORAL
# ============================================================
TIMEZONE_AR = 'America/Argentina/Buenos_Aires'
SESSION_SPLIT_HOUR = 14

# ============================================================
# BACKTEST — AUMENTADO PARA MÁS DATOS
# ============================================================
BACKTEST_DAYS = 90
BACKTEST_TIMEFRAME = '5m'
BACKTEST_LOOKBACK_VELAS = 10000   # ← 10,000 velas (~35 días en 5m)
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
