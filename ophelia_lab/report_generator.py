# ophelia_lab/report_generator.py
"""
Generador de reportes en TXT y MD.
Crea:
  - reports/full_report.txt          (para descargar desde Streamlit)
  - reports/CERTIFICATION_REPORT.md  (certificación)
"""
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Optional


class ReportGenerator:

    @staticmethod
    def _load_json(path: str) -> Optional[dict]:
        p = Path(path)
        return json.loads(p.read_text()) if p.exists() else None

    @staticmethod
    def _load_df(path: str) -> Optional[pd.DataFrame]:
        p = Path(path)
        if not p.exists():
            return None
        try:
            if p.suffix == '.csv':
                return pd.read_csv(p)
            elif p.suffix == '.json':
                return pd.read_json(p)
            elif p.suffix == '.parquet':
                return pd.read_parquet(p)
        except Exception:
            return None
        return None

    @classmethod
    def generate_txt(cls, output: str = 'reports/full_report.txt') -> str:
        """
        Genera un reporte completo en TXT con TODAS las métricas disponibles.
        Este archivo es el que descarga Streamlit.
        """
        lines = []
        lines.append("=" * 70)
        lines.append("  DAPS Ω × OPHELIA RESEARCH LAB — FULL REPORT")
        lines.append(f"  Generado: {datetime.utcnow().isoformat()} UTC")
        lines.append("=" * 70)
        lines.append("")

        # 1. Backtest
        bt = cls._load_json('data/optimization/backtest_metrics.json')
        lines.append("─" * 70)
        lines.append(" 1. BACKTEST METRICS")
        lines.append("─" * 70)
        if bt and bt.get('status') == 'VALIDATED':
            lines.append(f"  N° trades          : {bt.get('n_trades', 'N/A')}")
            lines.append(f"  Win rate           : {bt.get('win_rate', 0):.2%}")
            lines.append(f"  Profit factor      : {bt.get('profit_factor', 0):.3f}")
            lines.append(f"  Sharpe             : {bt.get('sharpe', 0):.3f}")
            lines.append(f"  Max drawdown       : {bt.get('max_drawdown_pct', 0):.2f}%")
            lines.append(f"  Expectancy         : {bt.get('expectancy_pct', 0):.4f}%")
            lines.append(f"  Avg win            : {bt.get('avg_win_pct', 0):.4f}%")
            lines.append(f"  Avg loss           : {bt.get('avg_loss_pct', 0):.4f}%")
            lines.append(f"  Avg duration       : {bt.get('avg_duration_min', 0):.2f} min")
            lines.append("")

            if 'by_tier' in bt and bt['by_tier']:
                lines.append("  ── Desglose por Tier ──")
                lines.append(f"  {'Tier':<12} {'N':>6} {'WR':>8} {'AvgPnL':>10}")
                for tier, m in bt['by_tier'].items():
                    lines.append(f"  {tier:<12} {m['n']:>6} {m['wr']:>7.2%} {m['avg_pnl']:>9.4f}%")
        else:
            lines.append("  ❌ NO VALIDADO — ejecutar 'python run_lab.py' primero")
        lines.append("")

        # 2. Walk-Forward
        wf = cls._load_df('data/optimization/walk_forward.json')
        lines.append("─" * 70)
        lines.append(" 2. WALK-FORWARD VALIDATION")
        lines.append("─" * 70)
        if wf is not None and not wf.empty:
            lines.append(wf.to_string(index=False))
        else:
            lines.append("  ❌ NO VALIDADO")
        lines.append("")

        # 3. Monte Carlo
        mc = cls._load_json('data/optimization/monte_carlo.json')
        lines.append("─" * 70)
        lines.append(" 3. MONTE CARLO (10,000 simulaciones)")
        lines.append("─" * 70)
        if mc and mc.get('status') == 'VALIDATED':
            for k, v in mc.items():
                if k == 'status':
                    continue
                lines.append(f"  {k:<25}: {v}")
        else:
            lines.append("  ❌ NO VALIDADO")
        lines.append("")

        # 4. Trailing óptimo
        trail = cls._load_df('data/optimization/trailing_optimal.csv')
        lines.append("─" * 70)
        lines.append(" 4. TRAILING ÓPTIMO POR ACTIVO")
        lines.append("─" * 70)
        if trail is not None and not trail.empty:
            lines.append(trail.to_string(index=False))
        else:
            lines.append("  ❌ NO VALIDADO")
        lines.append("")

        # 5. Break Even óptimo
        be = cls._load_df('data/optimization/break_even_optimal.csv')
        lines.append("─" * 70)
        lines.append(" 5. BREAK EVEN ÓPTIMO POR ACTIVO")
        lines.append("─" * 70)
        if be is not None and not be.empty:
            lines.append(be.to_string(index=False))
        else:
            lines.append("  ❌ NO VALIDADO")
        lines.append("")

        # 6. Leverage óptimo
        lev = cls._load_df('data/optimization/leverage_optimal.csv')
        lines.append("─" * 70)
        lines.append(" 6. LEVERAGE ÓPTIMO POR ACTIVO")
        lines.append("─" * 70)
        if lev is not None and not lev.empty:
            lines.append(lev.to_string(index=False))
        else:
            lines.append("  ❌ NO VALIDADO")
        lines.append("")

        # 7. Optimization history
        opt = cls._load_json('data/optimization/optimization_history.json')
        lines.append("─" * 70)
        lines.append(" 7. HISTORIAL DE OPTIMIZACIÓN")
        lines.append("─" * 70)
        if opt:
            for h in opt:
                m = h.get('metrics', {})
                lines.append(
                    f"  Iter {h.get('iteration')} [{h.get('stage', '')}]: "
                    f"WR={m.get('win_rate', 0):.3f} PF={m.get('profit_factor', 0):.3f} "
                    f"Sharpe={m.get('sharpe', 0):.3f}"
                )
        else:
            lines.append("  ❌ NO VALIDADO")
        lines.append("")

        lines.append("=" * 70)
        lines.append("  FIN DEL REPORTE")
        lines.append("=" * 70)

        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text('\n'.join(lines), encoding='utf-8')
        return output

    @classmethod
    def generate_all(cls):
        """Genera todos los reportes disponibles."""
        cls.generate_txt('reports/full_report.txt')
        # El resto los genera Certifier
