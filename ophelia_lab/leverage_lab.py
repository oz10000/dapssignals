# ophelia_lab/leverage_lab.py
"""Research de apalancamiento óptimo por activo."""
import numpy as np
import pandas as pd


class LeverageLab:
    GRID = [1, 2, 3, 4, 5, 7, 10, 15, 20]

    @classmethod
    def analyze(cls, trades_df: pd.DataFrame) -> pd.DataFrame:
        if trades_df is None or trades_df.empty:
            return pd.DataFrame()

        results = []
        for symbol in trades_df['symbol'].unique():
            sub = trades_df[trades_df['symbol'] == symbol]
            if len(sub) < 10:
                continue

            base_returns = sub['net_pnl_pct'].values
            atr_pct = sub['mae'].abs().mean()

            for lev in cls.GRID:
                lev_returns = base_returns * lev
                equity = np.cumprod(1 + lev_returns)
                ruin_prob = float((equity.min() < 0.5).astype(float))
                max_dd = float((np.maximum.accumulate(equity) - equity).max() / np.maximum.accumulate(equity).max())
                sharpe = (lev_returns.mean() / lev_returns.std() * np.sqrt(252)) if lev_returns.std() > 0 else 0

                results.append({
                    'symbol': symbol,
                    'leverage': lev,
                    'atr_pct': float(atr_pct),
                    'ruin_prob': ruin_prob,
                    'max_dd': max_dd,
                    'sharpe': float(sharpe),
                    'mean_return_pct': float(lev_returns.mean() * 100),
                })

        df = pd.DataFrame(results)

        # Resumen por activo: mejor leverage con ruin < 5%
        if not df.empty:
            safe = df[df['ruin_prob'] < 0.05]
            if not safe.empty:
                best = safe.loc[safe.groupby('symbol')['sharpe'].idxmax()]
                best.to_csv('data/optimization/leverage_optimal.csv', index=False)

        return df
