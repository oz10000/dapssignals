# ophelia_engine/leverage_optimizer.py
"""
Leverage por señal individual (no conjunto).
"""
import numpy as np
import pandas as pd
from typing import Dict

from ophelia_v2_config import (
    LEVERAGE_SAFETY_FACTOR, MAE_PERCENTILE,
    LIQUIDATION_THRESHOLD, LEVERAGE_PROFILE, LEVERAGE_PROFILES,
    OPHELIA_MAX_LEVERAGE, STANDARD_MAX_LEVERAGE,
)


class LeverageOptimizer:

    def __init__(self, profile: str = LEVERAGE_PROFILE):
        self.profile = profile

    def optimize_portfolio(self, selected: pd.DataFrame) -> Dict:
        """Resumen de leverage para todo el conjunto."""
        if selected.empty or 'mae' not in selected.columns:
            return {'leverage_max_safe': 1, 'leverage_recommended': 1}

        mae_p95 = abs(float(selected['mae'].quantile(1 - MAE_PERCENTILE / 100)))
        if mae_p95 <= 0:
            mae_p95 = 0.005

        raw_max = LIQUIDATION_THRESHOLD / (mae_p95 * LEVERAGE_SAFETY_FACTOR)
        max_safe = int(min(OPHELIA_MAX_LEVERAGE, max(1, raw_max)))

        return {
            'leverage_max_safe': max_safe,
            'leverage_recommended': max(1, int(max_safe * LEVERAGE_PROFILES.get(self.profile, 0.7))),
            'leverage_conservative': max(1, int(max_safe * 0.4)),
            'mae_p95_pct': round(mae_p95 * 100, 4),
            'safety_factor': LEVERAGE_SAFETY_FACTOR,
            'profile': self.profile,
        }

    def optimize_per_signal(self, row) -> Dict:
        """
        Calcula leverage individual para una señal.
        Usa MAE histórico del nivel (OPHELIA o STANDARD).
        """
        tier = row.get('tier', 'STANDARD')
        ophelia_score = row.get('ophelia_score', 0.5)
        atr_pct = abs(row.get('atr_pct', 0.01))
        mae = abs(row.get('mae', 0.005))

        # Usar el peor de atr_pct o mae para el cálculo
        risk_metric = max(mae, atr_pct * 0.5)

        if risk_metric <= 0:
            risk_metric = 0.005

        # Raw max
        raw_max = LIQUIDATION_THRESHOLD / (risk_metric * LEVERAGE_SAFETY_FACTOR)

        # Cap por tier
        cap = OPHELIA_MAX_LEVERAGE if tier == 'OPHELIA' else STANDARD_MAX_LEVERAGE
        max_safe = int(min(cap, max(1, raw_max)))

        # Ajuste por score (score alto → más leverage permitido)
        score_factor = 0.5 + 0.5 * ophelia_score
        recommended = max(1, int(max_safe * LEVERAGE_PROFILES.get(self.profile, 0.7) * score_factor))

        return {
            'leverage_max_safe': max_safe,
            'leverage_recommended': min(cap, recommended),
            'risk_metric_pct': round(risk_metric * 100, 4),
        }
