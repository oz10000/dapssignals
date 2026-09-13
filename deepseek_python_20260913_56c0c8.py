# ophelia_engine/temporal_predictor.py
"""
Predice CUÁNDO ocurrirá el próximo OPHELIA y CUÁNTO FALTA.
También indica CUÁNTOS MINUTOS ANTES se puede detectar.
"""
from datetime import datetime, timedelta
from typing import Dict, Optional
import pytz
import pandas as pd

from ophelia_config import TIMEZONE_AR, PRE_ALERT_MINUTES


class TemporalPredictor:

    def __init__(self, pattern: Dict):
        self.pattern = pattern
        self.tz = pytz.timezone(TIMEZONE_AR)
        self.temporal_stats = pattern.get('temporal_stats', {})
        self.hour_range = pattern.get('hour_range', {})

    def next_ophelia_prediction(self, last_ophelia_time: Optional[datetime]) -> Dict:
        """
        Retorna:
          - next_window_start: cuándo empieza la próxima ventana OPHELIA
          - next_window_end: cuándo termina
          - minutes_until: minutos hasta el inicio
          - pre_alert_minutes: minutos antes de la ventana para avisar
          - confidence: qué tan segura es la predicción
        """
        now = datetime.now(self.tz)

        mean_interval = self.temporal_stats.get('mean_interval_min', 60)
        std_interval = self.temporal_stats.get('std_interval_min', 30)

        if last_ophelia_time is None:
            # No hay último → usar hora actual + media
            next_start = now + timedelta(minutes=mean_interval - std_interval)
            next_end = now + timedelta(minutes=mean_interval + std_interval)
        else:
            if isinstance(last_ophelia_time, str):
                try:
                    last_ophelia_time = pd.to_datetime(last_ophelia_time).to_pydatetime()
                except Exception:
                    last_ophelia_time = now
            if last_ophelia_time.tzinfo is None:
                last_ophelia_time = self.tz.localize(last_ophelia_time)

            next_start = last_ophelia_time + timedelta(minutes=mean_interval - std_interval)
            next_end = last_ophelia_time + timedelta(minutes=mean_interval + std_interval)

            # Si ya pasó, saltar al siguiente
            if next_end < now:
                offset = (now - next_end).total_seconds() / 60
                cycles = int(offset // mean_interval) + 1
                next_start += timedelta(minutes=mean_interval * cycles)
                next_end += timedelta(minutes=mean_interval * cycles)

        minutes_until = (next_start - now).total_seconds() / 60

        # Confianza: basada en la desviación estándar relativa
        cv = std_interval / mean_interval if mean_interval > 0 else 1.0
        confidence = max(0.0, min(1.0, 1.0 - cv))

        return {
            'next_window_start': next_start.isoformat(),
            'next_window_end': next_end.isoformat(),
            'minutes_until_start': round(max(0, minutes_until), 1),
            'pre_alert_minutes': PRE_ALERT_MINUTES,
            'alert_time': (next_start - timedelta(minutes=PRE_ALERT_MINUTES)).isoformat(),
            'confidence': round(confidence, 3),
            'based_on_n': self.pattern.get('n_train', 0),
        }

    def time_since_last(self, last_ophelia_time: Optional[datetime]) -> Dict:
        """Cuánto tiempo pasó desde el último OPHELIA."""
        if last_ophelia_time is None:
            return {'minutes': None, 'human': 'Sin OPHELIA previo'}

        now = datetime.now(self.tz)
        if isinstance(last_ophelia_time, str):
            try:
                last_ophelia_time = pd.to_datetime(last_ophelia_time).to_pydatetime()
            except Exception:
                return {'minutes': None, 'human': 'Error parseando fecha'}
        if last_ophelia_time.tzinfo is None:
            last_ophelia_time = self.tz.localize(last_ophelia_time)

        delta = now - last_ophelia_time
        minutes = delta.total_seconds() / 60
        hours = int(minutes // 60)
        mins = int(minutes % 60)
        return {
            'minutes': round(minutes, 1),
            'human': f"{hours}h {mins}min",
        }