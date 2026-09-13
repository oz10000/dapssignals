# ophelia_config.py
"""
Configuración EXCLUSIVA para el detector OPHELIA.
No hay tiers A/B/S. Solo OPHELIA o nada.
"""

# ============================================================
# REQUISITOS MÍNIMOS DE CERTIFICACIÓN
# ============================================================
MIN_OPHELIA_TRADES_TRAIN = 30   # mínimo en training para aprender patrón
MIN_OPHELIA_TRADES_TEST = 10    # mínimo en test para certificar
REQUIRED_WIN_RATE = 1.0         # 100% — sin excepciones
MAX_OVERFIT_RATIO = 1.15        # test_WR / train_WR no debe superar esto

# ============================================================
# FILTROS DE OPHELIA (aprendidos, no hard-coded)
# ============================================================
# Estos son los umbrales LOOSE para el escaneo inicial.
# El patrón real OPHELIA se APRENDE de los trades TP-hitters.
MIN_MFE_FOR_OPHELIA = 0.0050    # 0.50% mínimo favorable
MAX_MAE_FOR_OPHELIA = 0.0030    # 0.30% máximo adverso
MIN_DURATION_FOR_OPHELIA = 3    # minutos
MAX_DURATION_FOR_OPHELIA = 120  # minutos

# ============================================================
# OPHELIA SCORE
# ============================================================
OPHELIA_SCORE_THRESHOLD = 0.95   # ≥ este valor → OPHELIA
OPHELIA_SCORE_HARD_GATE = 0.85   # < esto → descartar sin análisis

# Pesos del score (deben sumar 1.0)
OPHELIA_SCORE_WEIGHTS = {
    'feature_similarity': 0.40,   # distancia al centroide OPHELIA
    'temporal_match': 0.20,       # ¿está en ventana temporal?
    'atr_normalized': 0.15,       # ATR% en rango correcto
    'volume_confirmation': 0.10,  # volumen > 1.2× media
    'regime_match': 0.10,         # régimen coincide
    'asset_match': 0.05,          # activo está en lista OPHELIA
}

# ============================================================
# VENTANA TEMPORAL
# ============================================================
TIMEZONE_AR = 'America/Argentina/Buenos_Aires'
TEMPORAL_WINDOW_HOURS_BEFORE = 1   # ventana de ±1h para detectar
TEMPORAL_WINDOW_HOURS_AFTER = 1

# ============================================================
# LEVERAGE
# ============================================================
LEVERAGE_SAFETY_FACTOR = 3.0    # max_MAE × 3 = margen de seguridad
LEVERAGE_PROFILE = 'moderate'   # conservative, moderate, aggressive
LEVERAGE_PROFILES = {
    'conservative': 0.4,
    'moderate': 0.7,
    'aggressive': 1.0,
}

# ============================================================
# TP/SL/TRAILING
# ============================================================
# Con 100% WR, TP y SL son SIMÉTRICOS (misma magnitud).
# El TP se calcula como (min_MFE histórica × 0.85).
# El SL se calcula como (max_MAE histórica × 1.5) pero con signo opuesto.
TP_CAPTURE_RATIO = 0.85         # capturar 85% del MFE mínimo histórico
SL_SAFETY_MARGIN = 1.5          # SL = max_MAE × 1.5 (nunca se toca)
TRAILING_ACTIVATION_RATIO = 0.5 # activar trailing al 50% del TP
TRAILING_DISTANCE_RATIO = 0.3   # distancia = 30% del TP

# ============================================================
# PRE-ALERTA
# ============================================================
PRE_ALERT_MINUTES = 10          # avisar 10 min antes
EXECUTION_WINDOW_SECONDS = 45   # ventana para ejecutar

# ============================================================
# BACKTEST
# ============================================================
BACKTEST_DAYS = 365             # 1 año mínimo
BACKTEST_ASSETS = None          # None = todos los SYMBOLS
BACKTEST_TIMEFRAME = '5m'

# ============================================================
# DIRECTORIOS
# ============================================================
import os
OPHELIA_DIR = 'data/ophelia'
OPHELIA_TRADES_FILE = os.path.join(OPHELIA_DIR, 'all_trades.parquet')
OPHELIA_PATTERNS_FILE = os.path.join(OPHELIA_DIR, 'learned_patterns.json')
OPHELIA_CERTIFICATION_FILE = 'reports/OPHELIA_CERTIFICATION_REPORT.md'
OPHELIA_LIVE_ALERTS_FILE = os.path.join(OPHELIA_DIR, 'live_alerts.json')

os.makedirs(OPHELIA_DIR, exist_ok=True)
os.makedirs('reports', exist_ok=True)
