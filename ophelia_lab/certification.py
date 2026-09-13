# ophelia_lab/certification.py
"""Genera certificación final con estado PENDING/validado."""
import json
import pandas as pd
from pathlib import Path
from datetime import datetime


class Certifier:
    @classmethod
    def generate(cls, output: str = 'reports/CERTIFICATION_REPORT.md'):
        bt = cls._load('data/optimization/backtest_metrics.json')
        mc = cls._load('data/optimization/monte_carlo.json')
        opt = cls._load('data/optimization/optimization_history.json')
        wf = cls._load_df('data/optimization/walk_forward.json')
        trail = cls._load_df('data/optimization/trailing_optimal.csv')
        be = cls._load_df('data/optimization/break_even_optimal.csv')
        lev = cls._load_df('data/optimization/leverage_optimal.csv')

        lines = [f"# CERTIFICATION REPORT — DAPS Ω × Ophelia\n"]
        lines.append(f"**Fecha:** {datetime.utcnow().isoformat()}")

        lines.append("\n## 1. Backtest\n")
        if bt and bt.get('status') == 'VALIDATED':
            lines.append("| Métrica | Valor |")
            lines.append("|---------|-------|")
            for k, v in bt.items():
                if k == 'status' or k == 'by_tier':
                    continue
                lines.append(f"| {k} | {v} |")
            if 'by_tier' in bt:
                lines.append("\n### Por Tier\n")
                lines.append("| Tier | N | Win Rate | Avg PnL |")
                lines.append("|------|---|----------|---------|")
                for tier, m in bt['by_tier'].items():
                    lines.append(f"| {tier} | {m['n']} | {m['wr']:.2%} | {m['avg_pnl']:.3f}% |")
        else:
            lines.append("❌ **NO VALIDADO** — ejecutar backtest")

        lines.append("\n## 2. Walk-Forward\n")
        if wf is not None and not wf.empty:
            lines.append(wf.to_markdown(index=False))
        else:
            lines.append("❌ NO VALIDADO")

        lines.append("\n## 3. Monte Carlo\n")
        if mc and mc.get('status') == 'VALIDATED':
            lines.append("| Métrica | Valor |")
            lines.append("|---------|-------|")
            for k, v in mc.items():
                if k == 'status': continue
                lines.append(f"| {k} | {v} |")
        else:
            lines.append("❌ NO VALIDADO")

        lines.append("\n## 4. Trailing Óptimo por Activo\n")
        if trail is not None and not trail.empty:
            lines.append(trail.to_markdown(index=False))
        else:
            lines.append("❌ NO VALIDADO")

        lines.append("\n## 5. Break Even Óptimo por Activo\n")
        if be is not None and not be.empty:
            lines.append(be.to_markdown(index=False))
        else:
            lines.append("❌ NO VALIDADO")

        lines.append("\n## 6. Leverage Óptimo por Activo\n")
        if lev is not None and not lev.empty:
            lines.append(lev.to_markdown(index=False))
        else:
            lines.append("❌ NO VALIDADO")

        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text('\n'.join(lines))
        print(f"✅ Reporte: {output}")

    @staticmethod
    def _load(path):
        p = Path(path)
        return json.loads(p.read_text()) if p.exists() else None

    @staticmethod
    def _load_df(path):
        p = Path(path)
        return pd.read_csv(p) if p.exists() and p.suffix == '.csv' else (pd.read_json(p) if p.exists() else None)
