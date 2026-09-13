# ophelia_lab/monte_carlo.py
"""Monte Carlo con 10,000 simulaciones reproducibles."""
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Optional


class MonteCarlo:
    @staticmethod
    def run(trades_df: pd.DataFrame, n_sims: int = 10000,
            initial_capital: float = 10000.0, seed: int = 42) -> dict:
        if trades_df is None or trades_df.empty:
            return {'status': 'PENDING', 'reason': 'no trades'}

        rng = np.random.default_rng(seed=seed)
        returns = trades_df['net_pnl_pct'].values
        n = len(returns)

        finals = np.zeros(n_sims)
        max_dds = np.zeros(n_sims)
        ruin = 0

        for i in range(n_sims):
            sampled = rng.choice(returns, size=n, replace=True)
            sampled = rng.permutation(sampled)
            equity = initial_capital * np.cumprod(1 + sampled)
            finals[i] = equity[-1]
            peak = np.maximum.accumulate(equity)
            dd = (peak - equity) / peak
            max_dds[i] = dd.max()
            if equity.min() < initial_capital * 0.5:
                ruin += 1

        result = {
            'status': 'VALIDATED',
            'n_sims': n_sims,
            'seed': seed,
            'mean_final': float(finals.mean()),
            'median_final': float(np.median(finals)),
            'p5_final': float(np.percentile(finals, 5)),
            'p95_final': float(np.percentile(finals, 95)),
            'mean_max_dd_pct': float(max_dds.mean() * 100),
            'p95_max_dd_pct': float(np.percentile(max_dds, 95) * 100),
            'ruin_probability': float(ruin / n_sims),
        }

        Path('data/optimization').mkdir(parents=True, exist_ok=True)
        Path('data/optimization/monte_carlo.json').write_text(
            json.dumps(result, indent=2)
        )

        md = ["# MONTE CARLO REPORT\n"]
        md.append(f"**Simulaciones:** {n_sims} | **Seed:** {seed}\n")
        md.append("| Métrica | Valor |")
        md.append("|---------|-------|")
        for k, v in result.items():
            if k == 'status': continue
            md.append(f"| {k} | {v} |")
        Path('reports').mkdir(exist_ok=True)
        Path('reports/MONTE_CARLO_REPORT.md').write_text('\n'.join(md))

        return result
