# ophelia_lab/trailing_lab.py
"""Laboratorio de optimización del Trailing Stop por activo."""
import numpy as np
import pandas as pd
from itertools import product


class TrailingLab:
    ACTIVATIONS = [0.002, 0.004, 0.006, 0.008, 0.010, 0.015, 0.020]
    DISTANCES = [0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.010]

    @classmethod
    def optimize(cls, trades_df: pd.DataFrame) -> pd.DataFrame:
        """
        Para cada activo, busca la mejor combinación (activation, distance)
        maximizando el Sharpe de la serie de PnLs simulados.
        """
        if trades_df is None or trades_df.empty:
            return pd.DataFrame()

        results = []
        for symbol in trades_df['symbol'].unique():
            sub = trades_df[trades_df['symbol'] == symbol]
            if len(sub) < 10:
                continue

            best = None
            best_sharpe = -np.inf

            for act, dist in product(cls.ACTIVATIONS, cls.DISTANCES):
                if dist >= act:
                    continue
                pnls = cls._simulate(sub, act, dist)
                if len(pnls) < 5:
                    continue
                sharpe = cls._sharpe(pnls)
                if sharpe > best_sharpe:
                    best_sharpe = sharpe
                    best = {
                        'symbol': symbol,
                        'activation': act,
                        'distance': dist,
                        'sharpe': sharpe,
                        'win_rate': float((pnls > 0).mean()),
                        'profit_factor': cls._pf(pnls),
                        'expectancy_pct': float(pnls.mean() * 100),
                        'n_trades': len(pnls),
                    }
            if best:
                results.append(best)

        return pd.DataFrame(results)

    @staticmethod
    def _simulate(trades: pd.DataFrame, act: float, dist: float) -> np.ndarray:
        """Simula trailing con activación/retroceso sobre el MFE/MAE registrado."""
        pnls = []
        for _, t in trades.iterrows():
            mfe = t['mfe']
            original = t['net_pnl_pct']
            if mfe >= act:
                # Mejora sobre el original si el retroceso desde el máximo es menor
                trailed = mfe - dist
                final = max(trailed, original) if trailed > 0 else original
            else:
                final = original
            pnls.append(final)
        return np.array(pnls)

    @staticmethod
    def _sharpe(pnls: np.ndarray) -> float:
        if len(pnls) < 2 or pnls.std() == 0:
            return -np.inf
        return float(pnls.mean() / pnls.std() * np.sqrt(252))

    @staticmethod
    def _pf(pnls: np.ndarray) -> float:
        gains = pnls[pnls > 0].sum()
        losses = abs(pnls[pnls < 0].sum())
        return float(gains / losses) if losses > 0 else float('inf')
