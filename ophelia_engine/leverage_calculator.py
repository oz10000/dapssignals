# ophelia_engine/leverage_calculator.py
"""
Calcula el leverage seguro para OPHELIA basado en la MAE histórica máxima.
"""
from typing import Dict
from ophelia_config import (
    LEVERAGE_SAFETY_FACTOR, LEVERAGE_PROFILE, LEVERAGE_PROFILES,
)


class LeverageCalculator:

    def __init__(self, pattern: Dict, profile: str = LEVERAGE_PROFILE):
        self.pattern = pattern
        self.profile = profile
        self.stats = pattern.get('outcome_stats', {})

    def calculate(self) -> Dict:
        """
        Retorna:
          - leverage_max_safe: sin riesgo de liquidación histórica
          - leverage_recommended: perfil moderado
          - leverage_conservative: perfil conservador
        """
        # MAE más negativo histórico (peor caso)
        max_mae = abs(self.stats.get('min_mae', 0.001))

        # Si nunca se movió en contra más de X%, el SL está a X× safety
        # El leverage máximo seguro es tal que NO te liquide antes del SL.
        # Asumiendo liquidación al 90% del margen:
        # leverage_max_safe = 0.9 / (max_mae × safety_factor)
        if max_mae <= 0:
            max_mae = 0.001  # fallback

        raw_max = 0.9 / (max_mae * LEVERAGE_SAFETY_FACTOR)
        max_safe = min(50, max(1, int(raw_max)))  # cap en 50x

        profile_factor = LEVERAGE_PROFILES.get(self.profile, 0.7)
        recommended = max(1, int(max_safe * profile_factor))

        return {
            'leverage_max_safe': max_safe,
            'leverage_recommended': recommended,
            'leverage_conservative': max(1, int(max_safe * 0.4)),
            'leverage_aggressive': min(50, int(max_safe * 1.0)),
            'max_mae_historical': round(-max_mae, 6),
            'safety_factor': LEVERAGE_SAFETY_FACTOR,
            'profile': self.profile,
        }
