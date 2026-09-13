# ophelia_engine/trade_collector.py
"""
Trade Collector — Recolecta TODOS los trades históricos sin bias.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import pytz

from ophelia_v2_config import (
    MODEL_FEATURES, MAX_HOLD_BARS, COOLDOWN_MINUTES_PER_SYMBOL,
    MAX_TRADES_PER_DAY_PER_SYMBOL, BACKTEST_TIMEFRAME,
)


class TradeCollector:

    def __init__(self, tz_name: str = 'America/Argentina/Buenos_Aires'):
        self.tz = pytz.timezone(tz_name)
        self.trades: List[Dict] = []

    def collect(self, data_dict: Dict[str, pd.DataFrame], signal_fn) -> pd.DataFrame:
        for symbol, df in data_dict.items():
            if df is None or df.empty or len(df) < 200:
                continue
            self._scan_symbol(symbol, df, signal_fn)
        return pd.DataFrame(self.trades)

    def _scan_symbol(self, symbol: str, df: pd.DataFrame, signal_fn):
        last_trade_idx = None
        daily_count = {}

        for i in range(100, len(df) - MAX_HOLD_BARS - 1):
            current_time = df.index[i]
            current_date = current_time.date()

            if last_trade_idx is not None:
                bars_since = i - last_trade_idx
                minutes_since = bars_since * self._tf_to_minutes(BACKTEST_TIMEFRAME)
                if minutes_since < COOLDOWN_MINUTES_PER_SYMBOL:
                    continue

            if daily_count.get(current_date, 0) >= MAX_TRADES_PER_DAY_PER_SYMBOL:
                continue

            try:
                sig = signal_fn(symbol, df.iloc[:i+1])
            except Exception:
                continue
            if sig is None or not sig.get('is_valid'):
                continue

            features = self._capture_features(symbol, df, i, sig)
            if features is None:
                continue

            outcome = self._simulate_outcome(df, i, sig)
            if outcome is None:
                continue

            trade = {**features, **outcome}
            self.trades.append(trade)

            last_trade_idx = i
            daily_count[current_date] = daily_count.get(current_date, 0) + 1

    def _capture_features(self, symbol: str, df: pd.DataFrame,
                          idx: int, sig: Dict) -> Optional[Dict]:
        from core_engine import compute_adx, compute_atr, compute_ema

        if idx < 50:
            return None

        close = df['close'].iloc[idx]
        adx_series = compute_adx(df.iloc[:idx+1])
        atr_series = compute_atr(df.iloc[:idx+1])

        if len(adx_series) < 4 or len(atr_series) < 50:
            return None

        adx = float(adx_series.iloc[-1])
        adx_3_ago = float(adx_series.iloc[-4])
        atr = float(atr_series.iloc[-1])
        atr_ma = float(atr_series.iloc[-50:].mean())
        ema15 = float(compute_ema(df.iloc[:idx+1], 15).iloc[-1])
        ema50 = float(compute_ema(df.iloc[:idx+1], 50).iloc[-1])

        if atr <= 0:
            return None

        atr_pct = atr / close if close > 0 else 0
        atr_pct_rel = atr / atr_ma if atr_ma > 0 else 1.0

        avg_vol = df['volume'].iloc[max(0, idx-20):idx].mean()
        vol_ratio = float(df['volume'].iloc[idx] / avg_vol) if avg_vol > 0 else 1.0
        vol_ratio = max(0.1, vol_ratio)

        bar_time = df.index[idx]
        try:
            if bar_time.tz is None:
                bar_time_ar = bar_time.tz_localize('UTC').tz_convert(self.tz)
            else:
                bar_time_ar = bar_time.tz_convert(self.tz)
        except Exception:
            bar_time_ar = bar_time

        hour = bar_time_ar.hour if hasattr(bar_time_ar, 'hour') else 0
        weekday = bar_time_ar.weekday() if hasattr(bar_time_ar, 'weekday') else 0

        regime = sig.get('regime', 'Unknown')

        return {
            'symbol': symbol,
            'entry_time': str(bar_time),
            'entry_time_ar': str(bar_time_ar),
            'date_ar': bar_time_ar.date() if hasattr(bar_time_ar, 'date') else None,
            'direction': sig.get('direction', 'LONG'),
            'entry_price': close,
            'adx': adx,
            'ker': float(sig.get('ker', 0)),
            'score': float(sig.get('score', 0)),
            'atr_pct': atr_pct,
            'atr_pct_rel': atr_pct_rel,
            'volume_ratio': vol_ratio,
            'ema_dist_15_atr': (close - ema15) / atr,
            'ema_dist_50_atr': (close - ema50) / atr,
            'adx_acceleration': adx - adx_3_ago,
            'hour': hour,
            'weekday': weekday,
            'hour_sin': np.sin(2 * np.pi * hour / 24),
            'hour_cos': np.cos(2 * np.pi * hour / 24),
            'weekday_sin': np.sin(2 * np.pi * weekday / 7),
            'weekday_cos': np.cos(2 * np.pi * weekday / 7),
            'regime_expansion': 1.0 if regime == 'Expansión' else 0.0,
            'regime_trend': 1.0 if regime in ['Tendencia Fuerte', 'Tendencia Débil'] else 0.0,
            'regime_chop': 1.0 if regime == 'Chop' else 0.0,
            'regime': regime,
        }

    def _simulate_outcome(self, df: pd.DataFrame, idx: int, sig: Dict) -> Optional[Dict]:
        entry = sig.get('entry_price', df['close'].iloc[idx])
        sl = sig.get('sl_price')
        tp = sig.get('tp_price')
        direction = sig.get('direction')

        if sl is None or tp is None or direction is None:
            return None

        mfe = 0.0
        mae = 0.0
        exit_price = None
        exit_reason = None
        exit_idx = None

        end = min(idx + MAX_HOLD_BARS + 1, len(df))

        for j in range(idx + 1, end):
            bar = df.iloc[j]
            if direction == 'LONG':
                mfe = max(mfe, (bar['high'] - entry) / entry)
                mae = min(mae, (bar['low'] - entry) / entry)
                if bar['low'] <= sl:
                    exit_price, exit_reason, exit_idx = sl, 'SL', j
                    break
                if bar['high'] >= tp:
                    exit_price, exit_reason, exit_idx = tp, 'TP', j
                    break
            else:
                mfe = max(mfe, (entry - bar['low']) / entry)
                mae = min(mae, (entry - bar['high']) / entry)
                if bar['high'] >= sl:
                    exit_price, exit_reason, exit_idx = sl, 'SL', j
                    break
                if bar['low'] <= tp:
                    exit_price, exit_reason, exit_idx = tp, 'TP', j
                    break

        if exit_price is None:
            last = df.iloc[end - 1]
            exit_price = last['close']
            exit_reason = 'Time'
            exit_idx = end - 1

        if direction == 'LONG':
            pnl = (exit_price - entry) / entry
        else:
            pnl = (entry - exit_price) / entry

        duration_min = (df.index[exit_idx] - df.index[idx]).total_seconds() / 60

        return {
            'exit_time': str(df.index[exit_idx]),
            'exit_price': float(exit_price),
            'exit_reason': exit_reason,
            'mfe': float(mfe),
            'mae': float(mae),
            'duration_min': float(duration_min),
            'pnl_pct': float(pnl),
            'win': 1 if pnl > 0 else 0,
        }

    @staticmethod
    def _tf_to_minutes(tf: str) -> int:
        return {'1m': 1, '3m': 3, '5m': 5, '15m': 15, '30m': 30, '1h': 60}.get(tf, 5)
