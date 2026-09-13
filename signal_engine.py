# signal_engine.py
"""
Motor de señales — CORREGIDO.
Fixes:
  - Clasificación OPHELIA / S / A / B basada en score + ADX + KER + régimen
  - Precios SL/TP ajustados por tier
  - Trailing/BE ajustados por tier
"""
import pandas as pd
import numpy as np
from core_engine import (
    compute_adx, compute_ker, compute_atr, compute_ema,
    compute_regime, compute_pidelta_score,
    classify_signal, get_tier_params,
    estimate_mfe, estimate_persistence,
)
from config import DEFAULT_PARAMS, ASSET_PARAMS


class Signal:
    def __init__(self, symbol: str, df: pd.DataFrame, params: dict = None):
        self.symbol = symbol
        self.params = params or DEFAULT_PARAMS
        self.df = df

        # Valores por defecto
        self.score = 0.0
        self.adx = 0.0
        self.ker = 0.0
        self.atr_pct = 0.0
        self.atr_abs = 0.0
        self.regime = 'Chop'
        self.tier = 'NO-TIER'
        self.is_valid = False
        self.reason = "No evaluado"
        self.direction = None
        self.confidence = 0.0
        self.entry_price = 0.0
        self.sl_price = 0.0
        self.tp_price = 0.0
        self.tp_percent = 0.0
        self.sl_percent = 0.0
        self.trailing_activation = 0.0
        self.trailing_distance = 0.0
        self.break_even_trigger = 0.0
        self.break_even_buffer = 0.0
        self.max_hold_minutes = 60
        self.ema15 = 0.0
        self.ema50 = 0.0
        self.volume_ratio = 0.0
        self.mfe_expected = 0.0
        self.max_price_estimate = 0.0
        self.min_price_estimate = 0.0
        self.estimated_time_to_trade = 0
        self.persistence = 0.0

        if not df.empty and len(df) > 30:
            self._compute()

    def _compute(self):
        close = self.df['close'].iloc[-1]
        volume = self.df['volume'].iloc[-1]

        # Params por activo
        ap = ASSET_PARAMS.get(self.symbol, {})
        adx_p = ap.get('adx', 14)
        ker_p = ap.get('ker', 10)
        atr_p = ap.get('atr', 14)

        # Indicadores
        self.score = compute_pidelta_score(self.df, self.symbol)
        self.adx = float(compute_adx(self.df, adx_p).iloc[-1])
        self.ker = float(compute_ker(self.df, ker_p).iloc[-1])

        atr_series = compute_atr(self.df, atr_p)
        self.atr_abs = float(atr_series.iloc[-1])
        self.atr_pct = self.atr_abs / close if close > 0 else 0.0

        self.regime = compute_regime(self.df, self.adx, self.ker, self.atr_pct)

        self.ema15 = float(compute_ema(self.df, 15).iloc[-1])
        self.ema50 = float(compute_ema(self.df, 50).iloc[-1])

        avg_vol = self.df['volume'].rolling(20).mean().iloc[-1]
        self.volume_ratio = float(volume / avg_vol) if avg_vol > 0 else 0.0

        # Dirección
        self.direction = 'LONG' if self.score > 0 else 'SHORT'

        # Clasificación por tier
        self.tier = classify_signal(self.score, self.adx, self.ker, self.regime, self.params)

        # Validación
        if self.tier == 'NO-TIER':
            self.is_valid = False
            self.reason = f"NO-TIER (score {abs(self.score):.2f}, ADX {self.adx:.1f}, KER {self.ker:.2f})"
        elif self.regime == 'Chop':
            self.is_valid = False
            self.reason = "Régimen Chop"
        elif self.direction == 'LONG' and close < self.ema15:
            self.is_valid = False
            self.reason = "Precio < EMA15"
        elif self.direction == 'SHORT' and close > self.ema15:
            self.is_valid = False
            self.reason = "Precio > EMA15"
        else:
            self.is_valid = True
            self.reason = f"OK — {self.tier}"

        # Precios según tier
        tp = get_tier_params(self.tier, self.params)
        sl_mult = tp['sl']
        tpp_mult = tp['tp']

        self.entry_price = close
        if self.direction == 'LONG':
            self.sl_price = close * (1 - sl_mult * self.atr_pct)
            self.tp_price = close * (1 + tpp_mult * self.atr_pct)
        else:
            self.sl_price = close * (1 + sl_mult * self.atr_pct)
            self.tp_price = close * (1 - tpp_mult * self.atr_pct)

        self.tp_percent = (self.tp_price / self.entry_price - 1) * 100
        self.sl_percent = (self.sl_price / self.entry_price - 1) * 100

        self.trailing_activation = tp['trail_act']
        self.trailing_distance = tp['trail_dist']
        self.break_even_trigger = tp['be_trig']
        self.break_even_buffer = self.params.get('be_buffer', 0.0005)
        self.max_hold_minutes = self.params.get('max_hold', 60)

        # Confianza
        self.confidence = (
            30 +
            20 * min(self.adx / 40, 1) +
            20 * min(self.ker / 0.6, 1) +
            15 * min(abs(self.score) / 0.6, 1) +
            15 * min(self.volume_ratio / 1.5, 1)
        )
        self.confidence = float(min(max(self.confidence, 0), 100))

        self.mfe_expected = estimate_mfe(self.df, self.regime, self.atr_pct, self.volume_ratio)
        self.persistence = estimate_persistence(self.score, self.adx, self.ker, self.regime)

        mfe = self.mfe_expected
        if self.direction == 'LONG':
            self.max_price_estimate = close * (1 + mfe * 1.5)
            self.min_price_estimate = close * (1 - mfe * 0.5)
        else:
            self.max_price_estimate = close * (1 + mfe * 0.5)
            self.min_price_estimate = close * (1 - mfe * 1.5)

        self.estimated_time_to_trade = self._estimate_time()

    def _estimate_time(self) -> int:
        if self.is_valid:
            return max(5, int(10 + (100 - self.confidence) / 10))
        if abs(self.score) > 0.5:
            return int(15 + (1 - abs(self.score)) * 30)
        return int(45 + (1 - abs(self.score)) * 60)

    def to_dict(self) -> dict:
        return {
            'symbol': self.symbol,
            'score': self.score,
            'adx': self.adx,
            'ker': self.ker,
            'atr_pct': self.atr_pct,
            'atr_abs': self.atr_abs,
            'regime': self.regime,
            'tier': self.tier,
            'direction': self.direction,
            'is_valid': self.is_valid,
            'reason': self.reason,
            'confidence': self.confidence,
            'entry_price': self.entry_price,
            'sl_price': self.sl_price,
            'tp_price': self.tp_price,
            'tp_percent': self.tp_percent,
            'sl_percent': self.sl_percent,
            'trailing_activation': self.trailing_activation,
            'trailing_distance': self.trailing_distance,
            'break_even_trigger': self.break_even_trigger,
            'break_even_buffer': self.break_even_buffer,
            'max_hold_minutes': self.max_hold_minutes,
            'ema15': self.ema15,
            'ema50': self.ema50,
            'volume_ratio': self.volume_ratio,
            'mfe_expected': self.mfe_expected,
            'max_price_estimate': self.max_price_estimate,
            'min_price_estimate': self.min_price_estimate,
            'estimated_time_to_trade': self.estimated_time_to_trade,
            'persistence': self.persistence,
        }


# ============================================================
# RANKING Y CLASIFICACIÓN
# ============================================================
TIER_ORDER = {'OPHELIA': 0, 'S-TIER': 1, 'A-TIER': 2, 'B-TIER': 3, 'NO-TIER': 4}


def rank_signals(signals: list) -> list:
    """
    Ordena por tier (OPHELIA primero) y dentro de cada tier por |score|.
    """
    ranked = sorted(
        signals,
        key=lambda s: (TIER_ORDER.get(s.get('tier', 'NO-TIER'), 99), -abs(s.get('score', 0)))
    )
    for i, s in enumerate(ranked, 1):
        s['rank'] = i
        s['rank_label'] = f"#{i} {s['tier']}"
    return ranked


def classify_by_tier(signals: list) -> dict:
    """Agrupa señales por tier y dirección."""
    result = {
        'ophelia': [], 's': [], 'a': [], 'b': [], 'no_tier': [],
        'long_valid': [], 'short_valid': [],
        'all': signals,
    }
    for s in signals:
        tier = s.get('tier', 'NO-TIER')
        if tier == 'OPHELIA':
            result['ophelia'].append(s)
        elif tier == 'S-TIER':
            result['s'].append(s)
        elif tier == 'A-TIER':
            result['a'].append(s)
        elif tier == 'B-TIER':
            result['b'].append(s)
        else:
            result['no_tier'].append(s)

        if s.get('is_valid'):
            if s.get('direction') == 'LONG':
                result['long_valid'].append(s)
            else:
                result['short_valid'].append(s)

    return result
