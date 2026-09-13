# ophelia_engine/ophelia_detector.py
"""
Detector OPHELIA en tiempo real.
Dado un DataFrame actual + el patrón aprendido, decide si ES OPHELIA ahora.
"""
import numpy as np
import pandas as pd
from typing import Optional, Dict
from datetime import datetime
import pytz

from ophelia_config import (
    OPHELIA_SCORE_THRESHOLD, OPHELIA_SCORE_HARD_GATE,
    OPHELIA_SCORE_WEIGHTS, TIMEZONE_AR,
)


class OpheliaDetector:

    def __init__(self, pattern: Dict):
        self.pattern = pattern
        self.asset_list = set(pattern.get('assets', []))

    # ============================================================
    # SCORE
    # ============================================================
    def compute_ophelia_score(self, features: Dict) -> Dict:
        """Calcula el Ophelia Score [0, 1] a partir de las features actuales."""
        scores = {}

        # 1. Similitud de features (distancia al centroide)
        feat_sim = 0.0
        n_feat = 0
        for feat, rng in self.pattern.get('features', {}).items():
            val = features.get(feat)
            if val is None:
                continue
            fmin, fmax = rng['min'], rng['max']
            if fmin <= val <= fmax:
                # Dentro del rango → similitud 1
                feat_sim += 1.0
            else:
                # Penalización proporcional a la distancia fuera del rango
                span = fmax - fmin if fmax > fmin else 1.0
                if val < fmin:
                    dist = (fmin - val) / span
                else:
                    dist = (val - fmax) / span
                sim = max(0.0, 1.0 - dist)
                feat_sim += sim
            n_feat += 1

        scores['feature_similarity'] = feat_sim / n_feat if n_feat > 0 else 0.0

        # 2. Match temporal
        hour_range = self.pattern.get('hour_range', {})
        h_min = hour_range.get('min', 0)
        h_max = hour_range.get('max', 23)
        h = features.get('hour', -1)
        scores['temporal_match'] = 1.0 if h_min <= h <= h_max else 0.0

        # 3. ATR normalizado
        atr_range = self.pattern.get('features', {}).get('atr_pct_rel', {})
        atr_val = features.get('atr_pct_rel', 0)
        if atr_range and atr_range.get('min', 0) <= atr_val <= atr_range.get('max', 0):
            scores['atr_normalized'] = 1.0
        else:
            scores['atr_normalized'] = 0.5  # neutral

        # 4. Confirmación de volumen
        vr = features.get('volume_ratio', 0)
        scores['volume_confirmation'] = min(1.0, vr / 1.5)

        # 5. Match de régimen
        reg = features.get('regime', 'Unknown')
        scores['regime_match'] = 1.0 if reg in ['Expansión', 'Tendencia Fuerte'] else 0.3

        # 6. Match de activo
        sym = features.get('symbol', '')
        scores['asset_match'] = 1.0 if sym in self.asset_list else 0.0

        # Total
        total = sum(scores[k] * OPHELIA_SCORE_WEIGHTS[k] for k in scores)
        total = float(min(max(total, 0.0), 1.0))

        return {
            'ophelia_score': round(total, 4),
            'components': scores,
            'is_ophelia': total >= OPHELIA_SCORE_THRESHOLD,
            'is_candidate': total >= OPHELIA_SCORE_HARD_GATE,
        }

    # ============================================================
    # DETECCIÓN
    # ============================================================
    def detect(self, features: Dict) -> Optional[Dict]:
        """
        Retorna la alerta OPHELIA si las features actuales cumplen el patrón.
        """
        result = self.compute_ophelia_score(features)

        if not result['is_ophelia']:
            return {
                'status': 'NO_OPHELIA',
                'ophelia_score': result['ophelia_score'],
                'components': result['components'],
                'candidate': result['is_candidate'],
            }

        # Calcular TP/SL/Trailing basado en estadísticas históricas
        stats = self.pattern.get('outcome_stats', {})
        entry = features.get('entry_price', 0)

        mean_mfe = stats.get('mean_mfe', 0.0077)
        min_mfe = stats.get('min_mfe', 0.005)
        max_mae = stats.get('max_mae', 0.0008)

        from ophelia_config import (
            TP_CAPTURE_RATIO, SL_SAFETY_MARGIN,
            TRAILING_ACTIVATION_RATIO, TRAILING_DISTANCE_RATIO,
        )

        tp_pct = min_mfe * TP_CAPTURE_RATIO
        sl_pct = max_mae * SL_SAFETY_MARGIN

        direction = features.get('direction', 'LONG')
        if direction == 'LONG':
            tp_price = entry * (1 + tp_pct)
            sl_price = entry * (1 - sl_pct)
        else:
            tp_price = entry * (1 - tp_pct)
            sl_price = entry * (1 + sl_pct)

        trailing_act = entry * (1 + tp_pct * TRAILING_ACTIVATION_RATIO) if direction == 'LONG' else entry * (1 - tp_pct * TRAILING_ACTIVATION_RATIO)
        trailing_dist = entry * (1 + tp_pct * TRAILING_DISTANCE_RATIO) if direction == 'LONG' else entry * (1 - tp_pct * TRAILING_DISTANCE_RATIO)

        return {
            'status': 'OPHELIA',
            'ophelia_score': result['ophelia_score'],
            'components': result['components'],
            'symbol': features.get('symbol'),
            'direction': direction,
            'entry_price': entry,
            'entry_time': features.get('entry_time_ar'),
            'tp_price': round(tp_price, 6),
            'tp_pct': round(tp_pct * 100, 4),
            'sl_price': round(sl_price, 6),
            'sl_pct': round(sl_pct * 100, 4),
            'trailing_activation_price': round(trailing_act, 6),
            'trailing_distance_price': round(trailing_dist, 6),
            'expected_duration_min': stats.get('mean_duration_min', 30),
            'n_historical': self.pattern.get('n_train', 0),
            'historical_wr': 1.0,
            'detected_at': datetime.now(pytz.timezone(TIMEZONE_AR)).isoformat(),
        }