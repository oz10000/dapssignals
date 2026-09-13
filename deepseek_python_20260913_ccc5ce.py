# ophelia_lab/break_even_lab.py
"""Optimización del Break Even por activo."""
import numpy as np
import pandas as pd


class BreakEvenLab:
    THRESHOLDS = [0.001, 0.002, 0.003, 0.005, 0.008, 0.012, 0.020]
    COMMISSION = 0.001
    SLIPPAGE = 0.0005
    BE_BUFFER = 0.0005

    @classmethod
    def optimize(cls, trades_df: pd.DataFrame) -> pd.DataFrame:
        if trades_df is None or trades_df.empty:
            return pd.DataFrame()

        results = []
        for symbol in trades_df['symbol'].unique():
            sub = trades_df[trades_df['symbol'] == symbol]
            if len(sub) < 10:
                continue

            best = None
            best_exp = -np.inf

            for thr in cls.THRESHOLDS:
                pnls = cls._simulate(sub, thr)
                exp = pnls.mean()
                if exp > best_exp:
                    best_exp = exp
                    best = {
                        'symbol': symbol,
                        'be_threshold': thr,
                        'expectancy_pct': float(exp * 100),
                        'win_rate': float((pnls > 0).mean()),
                        'profit_factor': cls._pf(pnls),
                    }
            if best:
                results.append(best)

        return pd.DataFrame(results)

    @classmethod
    def _simulate(cls, trades: pd.DataFrame, threshold: float) -> np.ndarray:
        be_real = 2 * cls.COMMISSION + cls.SLIPPAGE + cls.BE_BUFFER
        pnls = []
        for _, t in trades.iterrows():
            mfe = t['mfe']
            original = t['net_pnl_pct']
            if mfe >= threshold:
                if original < be_real:
                    final = be_real  # protegido por BE
                else:
                    final = original
            else:
                final = original
            pnls.append(final)
        return np.array(pnls)

    @staticmethod
    def _pf(pnls: np.ndarray) -> float:
        gains = pnls[pnls > 0].sum()
        losses = abs(pnls[pnls < 0].sum())
        return float(gains / losses) if losses > 0 else float('inf')