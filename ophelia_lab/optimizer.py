# ophelia_lab/optimizer.py
"""
Optimizador iterativo (10 ciclos) sobre parámetros configurables.
"""
import json
import pandas as pd
from copy import deepcopy
from pathlib import Path


class IterativeOptimizer:
    STAGES = [
        'Baseline', 'Indicadores', 'Filtros entrada', 'Trailing',
        'Break Even', 'Riesgo', 'Temporal', 'Por activo',
        'Por régimen', 'Global', 'Modelo final',
    ]

    def __init__(self, backtest_fn, initial_params: dict, param_grid: dict, n_iterations: int = 10):
        self.backtest_fn = backtest_fn
        self.initial_params = initial_params
        self.param_grid = param_grid
        self.n_iterations = n_iterations
        self.history = []

    def run(self, data: dict) -> pd.DataFrame:
        current = deepcopy(self.initial_params)
        current_m = self.backtest_fn(data, current)
        self.history.append({'iteration': 0, 'stage': 'Baseline', 'params': deepcopy(current), 'metrics': current_m})

        for it in range(1, self.n_iterations + 1):
            stage = self.STAGES[it] if it < len(self.STAGES) else f'Iter {it}'
            best_change = None
            best_m = current_m

            for param, values in self.param_grid.items():
                for v in values:
                    if current.get(param) == v:
                        continue
                    test = deepcopy(current)
                    test[param] = v
                    try:
                        m = self.backtest_fn(data, test)
                    except Exception:
                        continue
                    if self._is_better(m, best_m):
                        best_m = m
                        best_change = (param, v)

            if best_change:
                current[best_change[0]] = best_change[1]
                current_m = best_m

            self.history.append({
                'iteration': it, 'stage': stage,
                'params': deepcopy(current), 'metrics': deepcopy(current_m),
            })

        Path('data/optimization').mkdir(parents=True, exist_ok=True)
        Path('data/optimization/optimization_history.json').write_text(
            json.dumps(self.history, default=str, indent=2)
        )

        return pd.DataFrame([
            {
                'iteration': h['iteration'],
                'stage': h['stage'],
                'win_rate': h['metrics'].get('win_rate'),
                'profit_factor': h['metrics'].get('profit_factor'),
                'sharpe': h['metrics'].get('sharpe'),
                'max_dd': h['metrics'].get('max_drawdown_pct'),
                'n_trades': h['metrics'].get('n_trades'),
            }
            for h in self.history
        ])

    def _is_better(self, new_m, old_m) -> bool:
        if (new_m.get('profit_factor') or 0) < 1.0:
            return False
        return (new_m.get('sharpe') or 0) > (old_m.get('sharpe') or 0)
