# ophelia_engine/pattern_extractor.py
"""
Extrae el patrón OPHELIA de la historia de trades.
Un trade es OPHELIA si:
  - Cerró por TP (no por SL, no por tiempo)
  - MFE ≥ MIN_MFE_FOR_OPHELIA
  - MAE ≥ -MAX_MAE_FOR_OPHELIA (movimiento adverso pequeño)
  - Duración en rango [MIN_DURATION, MAX_DURATION]

Luego extrae un patrón (ranges por feature + ventana temporal)
que incluya 100% de los trades OPHELIA y excluya ≥95% de los no-OPHELIA.
"""
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import pytz

from ophelia_config import (
    MIN_MFE_FOR_OPHELIA, MAX_MAE_FOR_OPHELIA,
    MIN_DURATION_FOR_OPHELIA, MAX_DURATION_FOR_OPHELIA,
    MIN_OPHELIA_TRADES_TRAIN,
    TIMEZONE_AR,
    OPHELIA_PATTERNS_FILE,
)

# Features que capturamos ANTES de cada trade
FEATURE_COLS = [
    'adx', 'ker', 'score',
    'atr_pct_rel',        # ATR% actual / ATR% media 50
    'volume_ratio',
    'ema_dist_15_atr',    # (close - ema15) / ATR
    'ema_dist_50_atr',    # (close - ema50) / ATR
    'adx_acceleration',   # ADX[i] - ADX[i-3]
    'hour',               # hora Argentina
    'weekday',            # 0-6
]


class PatternExtractor:
    """
    Aprende el patrón OPHELIA desde la historia.
    """

    def __init__(self, min_n_train: int = MIN_OPHELIA_TRADES_TRAIN):
        self.min_n_train = min_n_train
        self.ophelia_trades: List[Dict] = []
        self.non_ophelia_trades: List[Dict] = []
        self.pattern: Optional[Dict] = None

    # ============================================================
    # FASE 1: RECOLECCIÓN
    # ============================================================
    def learn_from_data(self, data_dict: Dict[str, pd.DataFrame],
                        signal_fn) -> bool:
        """
        Recorre la historia y clasifica trades en OPHELIA / no-OPHELIA.
        Retorna True si hay suficiente muestra para aprender.
        """
        from ophelia_engine.trade_simulator import simulate_trade_from_signal

        for symbol, df in data_dict.items():
            if df is None or df.empty or len(df) < 200:
                continue

            trades = self._scan_symbol(symbol, df, signal_fn, simulate_trade_from_signal)
            for t in trades:
                if self._is_ophelia(t):
                    self.ophelia_trades.append(t)
                else:
                    self.non_ophelia_trades.append(t)

        n_op = len(self.ophelia_trades)
        n_no = len(self.non_ophelia_trades)
        print(f"📊 Trades recolectados: {n_op} OPHELIA, {n_no} no-OPHELIA")

        return n_op >= self.min_n_train

    def _scan_symbol(self, symbol: str, df: pd.DataFrame,
                     signal_fn, simulate_trade) -> List[Dict]:
        """Escanea cada barra, genera señal, simula el trade, captura features."""
        trades = []
        warmup = 50
        for i in range(warmup, len(df) - 20):
            sub_df = df.iloc[:i+1]
            try:
                sig = signal_fn(symbol, sub_df)
                if sig is None or not sig.get('is_valid'):
                    continue

                # Capturar features ANTES del trade
                features = self._capture_features(symbol, df, i, sig)
                if features is None:
                    continue

                # Simular el trade hacia adelante
                trade_outcome = simulate_trade(df, i, sig, max_hold_bars=24)
                if trade_outcome is None:
                    continue

                # Combinar features + outcome
                full_trade = {**features, **trade_outcome}
                trades.append(full_trade)
            except Exception:
                continue
        return trades

    def _capture_features(self, symbol: str, df: pd.DataFrame,
                          idx: int, sig: Dict) -> Optional[Dict]:
        """Captura el estado de todos los indicadores ANTES de la entrada."""
        if idx < 50:
            return None

        from core_engine import compute_adx, compute_atr, compute_ema

        bar_time = df.index[idx]
        # Convertir a hora Argentina
        try:
            if bar_time.tz is None:
                bar_time_ar = bar_time.tz_localize('UTC').tz_convert(TIMEZONE_AR)
            else:
                bar_time_ar = bar_time.tz_convert(TIMEZONE_AR)
        except Exception:
            bar_time_ar = bar_time

        close = df['close'].iloc[idx]
        adx_series = compute_adx(df.iloc[:idx+1])
        atr_series = compute_atr(df.iloc[:idx+1])
        ema15_series = compute_ema(df.iloc[:idx+1], 15)
        ema50_series = compute_ema(df.iloc[:idx+1], 50)

        if len(adx_series) < 4 or len(atr_series) < 50:
            return None

        adx = float(adx_series.iloc[-1])
        adx_3_ago = float(adx_series.iloc[-4])
        atr = float(atr_series.iloc[-1])
        atr_ma = float(atr_series.iloc[-50:].mean())
        ema15 = float(ema15_series.iloc[-1])
        ema50 = float(ema50_series.iloc[-1])

        atr_pct = atr / close if close > 0 else 0
        atr_pct_rel = atr / atr_ma if atr_ma > 0 else 1.0

        avg_vol = df['volume'].iloc[max(0, idx-20):idx].mean()
        vol_ratio = df['volume'].iloc[idx] / avg_vol if avg_vol > 0 else 1.0

        return {
            'symbol': symbol,
            'entry_time': str(bar_time),
            'entry_time_ar': str(bar_time_ar),
            'entry_price': close,
            'direction': sig.get('direction'),
            'tier': sig.get('tier', 'NO-TIER'),
            'score': float(sig.get('score', 0)),
            'adx': adx,
            'ker': float(sig.get('ker', 0)),
            'atr_pct': atr_pct,
            'atr_pct_rel': atr_pct_rel,
            'volume_ratio': vol_ratio,
            'ema_dist_15_atr': (close - ema15) / atr if atr > 0 else 0,
            'ema_dist_50_atr': (close - ema50) / atr if atr > 0 else 0,
            'adx_acceleration': adx - adx_3_ago,
            'regime': sig.get('regime', 'Unknown'),
            'hour': bar_time_ar.hour if hasattr(bar_time_ar, 'hour') else 0,
            'minute': bar_time_ar.minute if hasattr(bar_time_ar, 'minute') else 0,
            'weekday': bar_time_ar.weekday() if hasattr(bar_time_ar, 'weekday') else 0,
        }

    def _is_ophelia(self, trade: Dict) -> bool:
        """Un trade es OPHELIA si cumple TODOS los criterios."""
        return (
            trade.get('exit_reason') == 'TP' and
            trade.get('mfe', 0) >= MIN_MFE_FOR_OPHELIA and
            trade.get('mae', -1) >= -MAX_MAE_FOR_OPHELIA and
            MIN_DURATION_FOR_OPHELIA <= trade.get('duration_min', 0) <= MAX_DURATION_FOR_OPHELIA
        )

    # ============================================================
    # FASE 2: EXTRACCIÓN DEL PATRÓN
    # ============================================================
    def extract_pattern(self) -> Optional[Dict]:
        """Extrae el patrón OPHELIA desde los trades recolectados."""
        if len(self.ophelia_trades) < self.min_n_train:
            print(f"❌ Muestra insuficiente: {len(self.ophelia_trades)} < {self.min_n_train}")
            return None

        op_df = pd.DataFrame(self.ophelia_trades)
        no_df = pd.DataFrame(self.non_ophelia_trades)

        pattern = {
            'n_train': len(op_df),
            'features': {},
            'hour_range': None,
            'weekday_set': None,
            'assets': [],
            'temporal_stats': {},
            'outcome_stats': {},
        }

        # 1. Features numéricas
        for feat in ['adx', 'ker', 'score', 'atr_pct_rel', 'volume_ratio',
                     'ema_dist_15_atr', 'ema_dist_50_atr', 'adx_acceleration']:
            if feat not in op_df.columns:
                continue
            vals = op_df[feat].dropna().values
            if len(vals) == 0:
                continue

            fmin, fmax = float(vals.min()), float(vals.max())
            # Margen del 5%
            span = fmax - fmin
            margin = max(span * 0.05, abs(fmin) * 0.02, 0.01)

            pattern['features'][feat] = {
                'min': round(fmin - margin, 6),
                'max': round(fmax + margin, 6),
                'mean': round(float(vals.mean()), 6),
                'std': round(float(vals.std()), 6),
            }

        # 2. Ventana temporal (hora Argentina)
        hours = op_df['hour'].values
        pattern['hour_range'] = {
            'min': int(hours.min()),
            'max': int(hours.max()),
            'mean': round(float(hours.mean()), 1),
            'distribution': {int(h): int((hours == h).sum()) for h in set(hours)},
        }

        # 3. Días de la semana
        weekdays = op_df['weekday'].values
        pattern['weekday_set'] = sorted(list(set(int(w) for w in weekdays)))

        # 4. Activos
        pattern['assets'] = sorted(op_df['symbol'].unique().tolist())

        # 5. Estadísticas temporales
        if 'entry_time_ar' in op_df.columns:
            times = pd.to_datetime(op_df['entry_time_ar'], errors='coerce').dropna()
            if len(times) > 1:
                intervals = times.diff().dt.total_seconds().dropna() / 60
                pattern['temporal_stats'] = {
                    'mean_interval_min': round(float(intervals.mean()), 1),
                    'median_interval_min': round(float(intervals.median()), 1),
                    'std_interval_min': round(float(intervals.std()), 1),
                    'min_interval_min': round(float(intervals.min()), 1),
                    'max_interval_min': round(float(intervals.max()), 1),
                }

        # 6. Estadísticas de outcome
        pattern['outcome_stats'] = {
            'mean_mfe': round(float(op_df['mfe'].mean()), 6),
            'min_mfe': round(float(op_df['mfe'].min()), 6),
            'max_mae': round(float(op_df['mae'].max()), 6),  # el menos negativo
            'min_mae': round(float(op_df['mae'].min()), 6),  # el más negativo
            'mean_duration_min': round(float(op_df['duration_min'].mean()), 1),
            'max_duration_min': round(float(op_df['duration_min'].max()), 1),
            'mean_entry_price': float(op_df['entry_price'].mean()),
        }

        self.pattern = pattern
        return pattern

    def save_pattern(self, path: str = OPHELIA_PATTERNS_FILE):
        if self.pattern is None:
            print("❌ No hay patrón para guardar")
            return
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(json.dumps(self.pattern, indent=2, default=str))
        print(f"✅ Patrón guardado: {path}")

    @staticmethod
    def load_pattern(path: str = OPHELIA_PATTERNS_FILE) -> Optional[Dict]:
        p = Path(path)
        if not p.exists():
            return None
        return json.loads(p.read_text())