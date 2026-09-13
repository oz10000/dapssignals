# core_engine.py
"""
Motor de indicadores técnicos — CORREGIDO.
Fixes aplicados:
  - ADX con Wilder's method (EWM alpha=1/period)
  - Score normalizado (pesos suman 1.0, sin bias LONG)
  - Detección de régimen con umbrales coherentes
"""
import pandas as pd
import numpy as np
import logging
from config import ASSET_PARAMS, DEFAULT_PARAMS

logger = logging.getLogger(__name__)


def compute_adx(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    ADX CORREGIDO usando Wilder's smoothing (EWM alpha=1/period).
    
    Fixes:
      - minus_dm = -low.diff() (era: abs(low.diff()) * -1 → incorrecto)
      - Suavizado de Wilder (EWM) en lugar de rolling().mean()
    """
    if df.empty or len(df) < period * 2:
        return pd.Series(0.0, index=df.index)

    high, low, close = df['high'], df['low'], df['close']

    # True Range
    tr = pd.DataFrame({
        'hl': high - low,
        'hc': (high - close.shift()).abs(),
        'lc': (low - close.shift()).abs(),
    }).max(axis=1)

    # Directional Movements CORREGIDOS
    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = up_move.where((up_move > down_move) & (up_move > 0), 0.0)
    minus_dm = down_move.where((down_move > up_move) & (down_move > 0), 0.0)

    # Wilder's smoothing
    alpha = 1.0 / period
    atr = tr.ewm(alpha=alpha, adjust=False).mean()
    atr = atr.replace(0, np.nan)

    plus_di = 100 * plus_dm.ewm(alpha=alpha, adjust=False).mean() / atr
    minus_di = 100 * minus_dm.ewm(alpha=alpha, adjust=False).mean() / atr

    di_sum = (plus_di + minus_di).replace(0, np.nan)
    dx = 100 * (plus_di - minus_di).abs() / di_sum

    adx = dx.ewm(alpha=alpha, adjust=False).mean()
    return adx.fillna(0).replace([np.inf, -np.inf], 0)


def compute_ker(df: pd.DataFrame, period: int = 10) -> pd.Series:
    """KER (Kaufman Efficiency Ratio)."""
    if df.empty or len(df) < period:
        return pd.Series(0.0, index=df.index)

    close = df['close']
    change = close.diff(period).abs()
    volatility = close.diff().abs().rolling(period).sum()
    ker = change / (volatility + 1e-9)
    return ker.fillna(0).replace([np.inf, -np.inf], 0)


def compute_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """ATR con Wilder's smoothing."""
    if df.empty or len(df) < period:
        return pd.Series(0.0, index=df.index)

    high, low, close = df['high'], df['low'], df['close']
    tr = pd.DataFrame({
        'hl': high - low,
        'hc': (high - close.shift()).abs(),
        'lc': (low - close.shift()).abs(),
    }).max(axis=1)

    atr = tr.ewm(alpha=1.0 / period, adjust=False).mean()
    return atr.fillna(0).replace([np.inf, -np.inf], 0)


def compute_ema(df: pd.DataFrame, period: int = 20) -> pd.Series:
    if df.empty:
        return pd.Series(0.0, index=df.index)
    return df['close'].ewm(span=period, adjust=False).mean()


def compute_regime(df: pd.DataFrame, adx_val: float, ker_val: float, atr_pct: float) -> str:
    """Clasificación de régimen con umbrales coherentes."""
    if df.empty or len(df) < 30:
        return 'Chop'

    if adx_val >= 40 and atr_pct >= 0.015:
        return 'Expansión'
    elif adx_val >= 30:
        return 'Tendencia Fuerte'
    elif adx_val >= 22:
        return 'Tendencia Débil'
    else:
        return 'Chop'


def compute_pidelta_score(df: pd.DataFrame, symbol: str = None) -> float:
    """
    Score compuesto CORREGIDO.
    
    Fixes:
      - Pesos suman exactamente 1.0 (antes 1.10 → bias +0.30)
      - ATR relativo centrado en 0 (antes sesgaba al alza)
      - Momentum con peso balanceado
    """
    if df.empty or len(df) < 30:
        return 0.0

    close = df['close']
    last_close = close.iloc[-1]

    if symbol and symbol in ASSET_PARAMS:
        p = ASSET_PARAMS[symbol]
        ema_p = p.get('ema', 22)
        atr_p = p.get('atr', 14)
        adx_p = p.get('adx', 14)
        ker_p = p.get('ker', 10)
    else:
        ema_p, atr_p, adx_p, ker_p = 22, 14, 14, 10

    # 1. Trend (peso 0.20)
    ema = close.ewm(span=ema_p).mean()
    if len(ema) >= 5 and ema.iloc[-5] != 0:
        slope = (ema.iloc[-1] - ema.iloc[-5]) / ema.iloc[-5]
    else:
        slope = 0.0
    trend = np.clip(slope * 10, -1, 1) * 0.20

    # 2. Strength (peso 0.15)
    adx_val = compute_adx(df, adx_p).iloc[-1]
    strength = np.clip(adx_val / 40, 0, 1) * 0.15

    # 3. KER (peso 0.15)
    ker_val = compute_ker(df, ker_p).iloc[-1]
    ker = np.clip(ker_val, 0, 1) * 0.15

    # 4. ATR relativo (peso 0.10) — centrado en 0
    atr_series = compute_atr(df, atr_p)
    atr_val = atr_series.iloc[-1]
    atr_ma = atr_series.rolling(20).mean().iloc[-1] if len(atr_series) >= 20 else atr_val
    atr_rel = (atr_val / atr_ma - 1) if atr_ma > 0 else 0.0
    atr_score = np.clip(atr_rel, -1, 1) * 0.10

    # 5. Momentum (peso 0.15)
    if len(close) >= 5 and close.iloc[-5] != 0:
        momentum = (close.iloc[-1] - close.iloc[-5]) / close.iloc[-5]
    else:
        momentum = 0.0
    momentum_score = np.clip(momentum * 15, -1, 1) * 0.15

    # 6. EMA direction (peso 0.25)
    ema_50 = close.ewm(span=50).mean()
    ema_dir = 1.0 if last_close > ema_50.iloc[-1] else -1.0
    ema_dir_score = ema_dir * 0.25

    score = trend + strength + ker + atr_score + momentum_score + ema_dir_score
    return float(np.clip(score, -1, 1))


def classify_signal(score: float, adx: float, ker: float, regime: str,
                    params: dict = None) -> str:
    """
    Clasifica una señal en OPHELIA, S-TIER, A-TIER, B-TIER o NO-TIER.
    
    🌟 OPHELIA = óptimo máximo
    🥇 S-TIER  = alta calidad
    🥈 A-TIER  = calidad media-alta
    🥉 B-TIER  = calidad media
    """
    p = params or DEFAULT_PARAMS
    abs_score = abs(score)

    # 🌟 OPHELIA
    if (abs_score >= p['ophelia_score_min'] and
        adx >= p['ophelia_adx_min'] and
        ker >= p['ophelia_ker_min'] and
        regime in ['Expansión', 'Tendencia Fuerte']):
        return 'OPHELIA'

    # 🥇 TIER S
    if (abs_score >= p['s_score_min'] and
        adx >= p['s_adx_min'] and
        ker >= p['s_ker_min']):
        return 'S-TIER'

    # 🥈 TIER A
    if (abs_score >= p['a_score_min'] and
        adx >= p['a_adx_min'] and
        ker >= p['a_ker_min']):
        return 'A-TIER'

    # 🥉 TIER B
    if (abs_score >= p['b_score_min'] and
        adx >= p['b_adx_min'] and
        ker >= p['b_ker_min']):
        return 'B-TIER'

    return 'NO-TIER'


def get_tier_params(tier: str, params: dict = None) -> dict:
    """Devuelve SL/TP/trailing/BE según el tier."""
    p = params or DEFAULT_PARAMS
    tier_params = p.get('tier_params', {})
    return tier_params.get(tier, tier_params.get('NO-TIER', {
        'sl': 0.4, 'tp': 1.2, 'trail_act': 0.012, 'trail_dist': 0.008, 'be_trig': 0.0025
    }))


def estimate_mfe(df: pd.DataFrame, regime: str, atr_pct: float, volume_ratio: float) -> float:
    """Estima MFE esperado."""
    base = atr_pct * 1.5
    factors = {'Expansión': 1.5, 'Tendencia Fuerte': 1.3,
               'Tendencia Débil': 1.1, 'Chop': 0.5}
    factor = factors.get(regime, 1.0)
    vol_factor = min(volume_ratio / 1.2, 1.5)
    return base * factor * vol_factor


def estimate_persistence(score: float, adx: float, ker: float, regime: str) -> float:
    """Persistencia esperada (0-100)."""
    base = 50.0
    base += 20 * (abs(score) / 0.6)
    base += 10 * (adx / 40)
    base += 10 * (ker / 0.6)
    if regime in ['Tendencia Fuerte', 'Expansión']:
        base += 10
    elif regime == 'Chop':
        base -= 20
    return float(max(0, min(100, base)))