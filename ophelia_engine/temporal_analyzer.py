# ophelia_engine/temporal_analyzer.py
"""
Análisis temporal OPHELIA.
"""
import numpy as np
import pandas as pd
from datetime import datetime
import pytz


class TemporalAnalyzer:

    def __init__(self, tz_name: str = 'America/Argentina/Buenos_Aires'):
        self.tz = pytz.timezone(tz_name)

    def analyze(self, selected_trades: pd.DataFrame) -> dict:
        """Analiza horarios y frecuencias."""
        if selected_trades is None or selected_trades.empty:
            return {}

        df = selected_trades.copy()

        if 'entry_time_ar' not in df.columns:
            return {}

        df['dt'] = pd.to_datetime(df['entry_time_ar'], errors='coerce')
        df = df.dropna(subset=['dt'])

        if df.empty:
            return {}

        # Por hora
        df['hour'] = df['dt'].dt.hour
        by_hour = df.groupby('hour').agg(
            n=('win', 'count'),
            wr=('win', 'mean'),
            mean_mfe=('mfe', 'mean'),
        ).to_dict('index') if 'win' in df.columns and 'mfe' in df.columns else {}

        # Top horas
        top_hours = df['hour'].value_counts().head(5).to_dict()

        # Intervalo entre señales
        times = df.sort_values('dt')['dt']
        diffs = times.diff().dt.total_seconds().dropna() / 60
        diffs = diffs[diffs > 0]

        # Trades por día
        daily = df.groupby(df['dt'].dt.date).size()
        tpd = daily.mean() if len(daily) > 0 else 0

        # Dirección
        direction_counts = df['direction'].value_counts().to_dict() if 'direction' in df.columns else {}

        # Top activos
        top_assets = df['symbol'].value_counts().head(10).to_dict() if 'symbol' in df.columns else {}

        return {
            'trades_per_day': round(float(tpd), 2),
            'by_hour': by_hour,
            'top_hours': top_hours,
            'mean_interval_min': round(float(diffs.mean()), 1) if len(diffs) > 0 else None,
            'median_interval_min': round(float(diffs.median()), 1) if len(diffs) > 0 else None,
            'std_interval_min': round(float(diffs.std()), 1) if len(diffs) > 0 else None,
            'direction_distribution': direction_counts,
            'top_assets': top_assets,
            'n_total': len(df),
        }

    def next_ophelia_prediction(self, selected_trades: pd.DataFrame) -> dict:
        """Predice próxima ventana."""
        if selected_trades is None or selected_trades.empty:
            return {}

        df = selected_trades.copy()
        if 'entry_time_ar' not in df.columns:
            return {}

        df['dt'] = pd.to_datetime(df['entry_time_ar'], errors='coerce')
        df = df.dropna(subset=['dt']).sort_values('dt')

        if len(df) < 3:
            return {}

        times = df['dt']
        diffs = times.diff().dt.total_seconds().dropna() / 60
        diffs = diffs[diffs > 0]

        if diffs.empty:
            return {}

        mean_interval = diffs.mean()
        std_interval = diffs.std()

        last_time = times.iloc[-1]
        now = datetime.now(self.tz)
        elapsed = (now - last_time).total_seconds() / 60

        remaining = max(0, mean_interval - elapsed)

        return {
            'last_time': last_time.isoformat(),
            'elapsed_min': round(elapsed, 1),
            'next_expected_min': round(remaining, 1),
            'mean_interval_min': round(mean_interval, 1),
            'std_interval_min': round(std_interval, 1),
            'confidence': round(max(0, 1 - std_interval / mean_interval), 3) if mean_interval > 0 else 0,
        }
