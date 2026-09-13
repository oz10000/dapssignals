# ophelia_lab/backtest_engine.py
"""
Motor de backtest realista con comisión, slippage, latencia, TP/SL/trailing.
"""
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, Callable, Optional
from dataclasses import dataclass, asdict
import logging

logger = logging.getLogger(__name__)


@dataclass
class TradeRecord:
    symbol: str
    direction: str
    tier: str
    entry_time: str
    exit_time: str
    entry_price: float
    exit_price: float
    sl_price: float
    tp_price: float
    mfe: float
    mae: float
    duration_minutes: float
    exit_reason: str
    gross_pnl_pct: float
    net_pnl_pct: float
    score: float
    adx: float
    ker: float
    regime: str


class BacktestEngine:
    def __init__(self, commission: float = 0.001, slippage: float = 0.0005,
                 latency_bars: int = 1, initial_capital: float = 10000.0,
                 risk_per_trade: float = 0.01):
        self.commission = commission
        self.slippage = slippage
        self.latency_bars = latency_bars
        self.initial_capital = initial_capital
        self.risk_per_trade = risk_per_trade
        self.trades = []

    def run(self, data_dict: Dict[str, pd.DataFrame],
            signal_fn: Callable, max_hold_bars: int = 12,
            use_trailing: bool = True) -> pd.DataFrame:
        capital = self.initial_capital

        for symbol, df in data_dict.items():
            if df is None or df.empty or len(df) < 100:
                continue

            logger.info(f"Backtest {symbol} ({len(df)} velas)")

            for i in range(50, len(df) - max_hold_bars - self.latency_bars):
                sub_df = df.iloc[:i+1]
                try:
                    sig = signal_fn(symbol, sub_df)
                    if sig is None or not sig.get('is_valid'):
                        continue

                    tr = self._execute(symbol, df, i, sig, max_hold_bars, use_trailing)
                    if tr:
                        self.trades.append(tr)
                        capital *= (1 + tr.net_pnl_pct)
                except Exception:
                    continue

        return self._to_df()

    def _execute(self, symbol, df, entry_idx, sig, max_hold_bars, use_trailing) -> Optional[TradeRecord]:
        actual = entry_idx + self.latency_bars
        if actual >= len(df):
            return None

        bar = df.iloc[actual]
        direction = sig['direction']

        if direction == 'LONG':
            entry = bar['open'] * (1 + self.slippage)
        else:
            entry = bar['open'] * (1 - self.slippage)

        sl = sig['sl_price']
        tp = sig['tp_price']
        trail_act = sig.get('trailing_activation', 0)
        trail_dist = sig.get('trailing_distance', 0)

        exit_price = exit_reason = exit_idx = None
        mfe = mae = 0.0
        current_sl = sl
        trailing_on = False
        trail_extreme = entry

        end = min(actual + max_hold_bars + 1, len(df))

        for j in range(actual + 1, end):
            b = df.iloc[j]
            if direction == 'LONG':
                mfe = max(mfe, (b['high'] - entry) / entry)
                mae = min(mae, (b['low'] - entry) / entry)

                if use_trailing and trail_act > 0:
                    if b['high'] > trail_extreme:
                        trail_extreme = b['high']
                    if not trailing_on and (trail_extreme - entry) / entry >= trail_act:
                        trailing_on = True
                    if trailing_on:
                        new_sl = trail_extreme * (1 - trail_dist)
                        if new_sl > current_sl:
                            current_sl = new_sl

                if b['low'] <= current_sl:
                    exit_price = current_sl * (1 - self.slippage)
                    exit_reason = 'Trailing' if trailing_on else 'SL'
                    exit_idx = j
                    break
                if b['high'] >= tp:
                    exit_price = tp * (1 - self.slippage)
                    exit_reason = 'TP'
                    exit_idx = j
                    break
            else:
                mfe = max(mfe, (entry - b['low']) / entry)
                mae = min(mae, (entry - b['high']) / entry)

                if use_trailing and trail_act > 0:
                    if b['low'] < trail_extreme:
                        trail_extreme = b['low']
                    if not trailing_on and (entry - trail_extreme) / entry >= trail_act:
                        trailing_on = True
                    if trailing_on:
                        new_sl = trail_extreme * (1 + trail_dist)
                        if new_sl < current_sl:
                            current_sl = new_sl

                if b['high'] >= current_sl:
                    exit_price = current_sl * (1 + self.slippage)
                    exit_reason = 'Trailing' if trailing_on else 'SL'
                    exit_idx = j
                    break
                if b['low'] <= tp:
                    exit_price = tp * (1 + self.slippage)
                    exit_reason = 'TP'
                    exit_idx = j
                    break

        if exit_price is None:
            b = df.iloc[end - 1]
            exit_price = b['close']
            exit_reason = 'Time'
            exit_idx = end - 1

        if direction == 'LONG':
            gross = (exit_price - entry) / entry
        else:
            gross = (entry - exit_price) / entry

        net = gross - (2 * self.commission + self.slippage)

        e_time = df.index[actual]
        x_time = df.index[exit_idx]
        dur = (x_time - e_time).total_seconds() / 60

        return TradeRecord(
            symbol=symbol, direction=direction, tier=sig.get('tier', 'NO-TIER'),
            entry_time=str(e_time), exit_time=str(x_time),
            entry_price=entry, exit_price=exit_price,
            sl_price=sl, tp_price=tp, mfe=mfe, mae=mae,
            duration_minutes=dur, exit_reason=exit_reason,
            gross_pnl_pct=gross, net_pnl_pct=net,
            score=sig.get('score', 0), adx=sig.get('adx', 0),
            ker=sig.get('ker', 0), regime=sig.get('regime', 'Unknown'),
        )

    def _to_df(self) -> pd.DataFrame:
        if not self.trades:
            return pd.DataFrame()
        return pd.DataFrame([asdict(t) for t in self.trades])

    def compute_metrics(self) -> dict:
        if not self.trades:
            return {'status': 'PENDING', 'n_trades': 0}

        df = self._to_df()
        wins = df[df['net_pnl_pct'] > 0]
        losses = df[df['net_pnl_pct'] <= 0]

        equity = self.initial_capital * (1 + df['net_pnl_pct']).cumprod()
        peak = equity.cummax()
        dd = (peak - equity) / peak

        gains = wins['net_pnl_pct'].sum() if not wins.empty else 0
        losses_abs = abs(losses['net_pnl_pct'].sum()) if not losses.empty else 1e-9

        returns = df['net_pnl_pct'].values
        sharpe = (returns.mean() / returns.std() * np.sqrt(252)) if returns.std() > 0 else 0

        # Métricas por tier
        by_tier = {}
        for tier in ['OPHELIA', 'S-TIER', 'A-TIER', 'B-TIER', 'NO-TIER']:
            sub = df[df['tier'] == tier]
            if sub.empty:
                continue
            by_tier[tier] = {
                'n': len(sub),
                'wr': (sub['net_pnl_pct'] > 0).mean(),
                'avg_pnl': sub['net_pnl_pct'].mean() * 100,
            }

        return {
            'status': 'VALIDATED',
            'n_trades': len(df),
            'win_rate': float(len(wins) / len(df)),
            'profit_factor': float(gains / losses_abs) if losses_abs > 0 else None,
            'sharpe': float(sharpe),
            'max_drawdown_pct': float(dd.max() * 100),
            'expectancy_pct': float(df['net_pnl_pct'].mean() * 100),
            'avg_win_pct': float(wins['net_pnl_pct'].mean() * 100) if not wins.empty else 0,
            'avg_loss_pct': float(losses['net_pnl_pct'].mean() * 100) if not losses.empty else 0,
            'avg_duration_min': float(df['duration_minutes'].mean()),
            'by_tier': by_tier,
        }