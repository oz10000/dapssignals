# ophelia_engine/certifier.py
"""
Certificador — Walk-Forward + Monte Carlo.
"""
import numpy as np
import pandas as pd

from ophelia_v2_config import (
    MIN_TRADES_TRAIN,
    MIN_TRADES_TEST,
    MIN_OPHELIA_CERTIFIED_WR,
    MAX_OVERFIT_DEGRADATION,
)


class Certifier:

    def certify(self, optimizer_metadata: dict,
                selected_trades: pd.DataFrame) -> dict:
        result = {
            'certified': False,
            'reasons': [],
            'metrics': {},
        }

        n_train = optimizer_metadata.get('n_train', 0)
        n_test = optimizer_metadata.get('n_test', 0)

        if n_train < MIN_TRADES_TRAIN:
            result['reasons'].append(
                f'Train insuficiente: {n_train} < {MIN_TRADES_TRAIN}'
            )
        if n_test < MIN_TRADES_TEST:
            result['reasons'].append(
                f'Test insuficiente: {n_test} < {MIN_TRADES_TEST}'
            )

        auc_test = optimizer_metadata.get('auc_test', 0.5)
        if auc_test < 0.55:
            result['reasons'].append(
                f'AUC test bajo: {auc_test:.3f} < 0.55'
            )

        test_wr = optimizer_metadata.get('ophelia_wr_test', 0)
        train_wr = optimizer_metadata.get('ophelia_wr_train', 0)

        if test_wr < MIN_OPHELIA_CERTIFIED_WR:
            result['reasons'].append(
                f'OPHELIA WR test {test_wr*100:.1f}% < '
                f'{MIN_OPHELIA_CERTIFIED_WR*100:.0f}%'
            )

        if train_wr > 0:
            degradation = train_wr - test_wr
            if degradation > MAX_OVERFIT_DEGRADATION:
                result['reasons'].append(
                    f'Degradación excesiva: {degradation*100:.1f}%'
                )

        if selected_trades is not None and not selected_trades.empty:
            result['metrics'] = {
                'n_selected': len(selected_trades),
                'wr_overall': float(selected_trades['win'].mean())
                    if 'win' in selected_trades.columns else 0,
                'mean_mfe': float(selected_trades['mfe'].mean())
                    if 'mfe' in selected_trades.columns else 0,
                'mean_mae': float(selected_trades['mae'].mean())
                    if 'mae' in selected_trades.columns else 0,
                'mean_duration': float(selected_trades['duration_min'].mean())
                    if 'duration_min' in selected_trades.columns else 0,
            }

        result['certified'] = len(result['reasons']) == 0
        return result

    def walk_forward(self, optimizer, trades_df: pd.DataFrame,
                     n_windows: int = 5) -> pd.DataFrame:
        if trades_df is None or trades_df.empty:
            return pd.DataFrame()

        df = trades_df.sort_values('entry_time').reset_index(drop=True)
        window_size = len(df) // (n_windows + 1)

        results = []
        for w in range(n_windows):
            train_end = window_size * (w + 1)
            test_end = min(window_size * (w + 2), len(df))

            train = df.iloc[:train_end]
            test = df.iloc[train_end:test_end]

            if len(train) < MIN_TRADES_TRAIN or len(test) < MIN_TRADES_TEST:
                continue

            try:
                from ophelia_engine.ophelia_scorer import OpheliaScorer
                opt = OpheliaScorer()
                meta = opt.fit(train)

                if 'error' in meta:
                    continue

                results.append({
                    'window': w + 1,
                    'train_wr': meta.get('ophelia_wr_train', 0),
                    'test_wr': meta.get('ophelia_wr_test', 0),
                    'test_tpd': meta.get('ophelia_tpd_test', 0),
                    'auc_test': meta.get('auc_test', 0),
                })
            except Exception:
                continue

        return pd.DataFrame(results)

    def monte_carlo(self, selected_trades: pd.DataFrame,
                    n_sims: int = 10000, seed: int = 42) -> dict:
        if selected_trades is None or selected_trades.empty:
            return {}
        if 'pnl_pct' not in selected_trades.columns:
            return {}

        rng = np.random.default_rng(seed=seed)
        returns = selected_trades['pnl_pct'].values
        n = len(returns)

        final_capitals = []
        max_dds = []

        for _ in range(n_sims):
            sampled = rng.choice(returns, size=n, replace=True)
            sampled = rng.permutation(sampled)
            equity = np.cumprod(1 + sampled)
            final_capitals.append(equity[-1])
            peak = np.maximum.accumulate(equity)
            dd = ((peak - equity) / peak).max()
            max_dds.append(dd)

        final_capitals = np.array(final_capitals)
        max_dds = np.array(max_dds)

        return {
            'mean_final': float(final_capitals.mean()),
            'median_final': float(np.median(final_capitals)),
            'p5_final': float(np.percentile(final_capitals, 5)),
            'p95_final': float(np.percentile(final_capitals, 95)),
            'mean_max_dd': float(max_dds.mean()),
            'p95_max_dd': float(np.percentile(max_dds, 95)),
            'ruin_prob': float((final_capitals < 0.5).mean()),
        }
