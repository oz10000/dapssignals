# ophelia_lab/walk_forward.py
"""Walk-Forward Validation con 5 ventanas."""
import numpy as np
import pandas as pd
from pathlib import Path


class WalkForward:
    def __init__(self, n_windows: int = 5, train_ratio: float = 0.7):
        self.n_windows = n_windows
        self.train_ratio = train_ratio

    def validate(self, data_dict: dict, backtest_fn) -> pd.DataFrame:
        results = []
        for w in range(self.n_windows):
            train, test = {}, {}
            for sym, df in data_dict.items():
                if df is None or df.empty:
                    continue
                n = len(df)
                offset = int(n * 0.08 * w)
                split = int((n - offset) * self.train_ratio)
                train[sym] = df.iloc[offset:offset+split]
                test[sym] = df.iloc[offset+split:]

            try:
                tr_m = backtest_fn(train)
                te_m = backtest_fn(test)
                overfit = (te_m.get('profit_factor') or 0) / max(tr_m.get('profit_factor') or 1, 1e-9)
                results.append({
                    'window': w + 1,
                    'train_wr': tr_m.get('win_rate'),
                    'test_wr': te_m.get('win_rate'),
                    'train_pf': tr_m.get('profit_factor'),
                    'test_pf': te_m.get('profit_factor'),
                    'test_sharpe': te_m.get('sharpe'),
                    'test_dd': te_m.get('max_drawdown_pct'),
                    'overfit_ratio': overfit,
                })
            except Exception as e:
                results.append({'window': w + 1, 'error': str(e)})

        df = pd.DataFrame(results)
        Path('data/optimization').mkdir(parents=True, exist_ok=True)
        df.to_json('data/optimization/walk_forward.json', orient='records', indent=2)
        return df