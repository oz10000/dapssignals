# ophelia_lab/operational_report.py
"""
Generador de OPHELIA_OPERATIONAL_REPORT.md
Basado EXCLUSIVAMENTE en datos reales generados por run_lab.py.
Si una métrica no existe, se marca como ❌ NO VALIDADO.
"""
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Dict, List


class OperationalReport:
    """
    Genera el reporte operativo completo con datos reales del laboratorio.
    """

    MIN_SIGNALS_FOR_VALIDATION = 30        # mínimo para considerar un activo válido
    MIN_SIGNALS_PER_TIER = 10              # mínimo por tier
    MAX_DRAWDOWN_OK = 20.0                 # % máximo aceptable
    MIN_PROFIT_FACTOR_OK = 1.2             # PF mínimo
    MIN_SHARPE_OK = 0.8                    # Sharpe mínimo

    def __init__(self, output_path: str = 'reports/OPHELIA_OPERATIONAL_REPORT.md'):
        self.output_path = output_path
        self.data = self._load_all_data()

    # ============================================================
    # CARGA DE DATOS
    # ============================================================
    def _load_all_data(self) -> Dict:
        return {
            'backtest':     self._load_json('data/optimization/backtest_metrics.json'),
            'monte_carlo':  self._load_json('data/optimization/monte_carlo.json'),
            'walk_forward': self._load_df('data/optimization/walk_forward.json'),
            'optimization': self._load_json('data/optimization/optimization_history.json'),
            'trailing':     self._load_df('data/optimization/trailing_optimal.csv'),
            'break_even':   self._load_df('data/optimization/break_even_optimal.csv'),
            'leverage':     self._load_df('data/optimization/leverage_optimal.csv'),
            'trades':       self._load_df('data/trades/trades.parquet'),
        }

    @staticmethod
    def _load_json(path: str) -> Optional[dict]:
        p = Path(path)
        if not p.exists():
            return None
        try:
            return json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            return None

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

    @staticmethod
    def _fmt(value, fmt='.4f', suffix='') -> str:
        if value is None:
            return "❌ NO VALIDADO"
        if isinstance(value, float) and (np.isnan(value) or np.isinf(value)):
            return "❌ NO VALIDADO"
        try:
            return f"{value:{fmt}}{suffix}"
        except Exception:
            return str(value)

    @staticmethod
    def _safe_to_datetime(series: pd.Series) -> pd.Series:
        """
        Convierte una serie a datetime sin importar si es string, int,
        o datetime ya parseado. Y sin importar el timezone.
        """
        try:
            dt = pd.to_datetime(series, errors='coerce', utc=True)
            # Quitar tz para cálculos uniformes
            return dt.dt.tz_convert(None)
        except Exception:
            return pd.to_datetime(series, errors='coerce')

    # ============================================================
    # GENERADOR PRINCIPAL
    # ============================================================
    def generate(self) -> str:
        lines = []
        lines += self._section_header()
        lines += self._section_executive_summary()
        lines += self._section_architecture()
        lines += self._section_assets()
        lines += self._section_global_stats()
        lines += self._section_per_tier()
        lines += self._section_per_asset()
        lines += self._section_winning_vs_losing()
        lines += self._section_next_opportunities()
        lines += self._section_calendar()
        lines += self._section_simulation()
        lines += self._section_operational_ranking()
        lines += self._section_alerts()
        lines += self._section_certification()
        lines += self._section_footer()

        Path(self.output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(self.output_path).write_text('\n'.join(lines), encoding='utf-8')
        print(f"✅ Reporte operativo: {self.output_path}")
        return self.output_path

    # ============================================================
    # SECCIONES
    # ============================================================
    def _section_header(self) -> List[str]:
        bt = self.data['backtest']
        status = "✅ VALIDADO" if (bt and bt.get('status') == 'VALIDATED') else "❌ NO VALIDADO"
        return [
            "# 🔬 OPHELIA OPERATIONAL REPORT",
            "",
            f"**Generado:** {datetime.now(timezone.utc).isoformat()} UTC",
            f"**Fuente:** Ejecución real de `run_lab.py`",
            f"**Estado global:** {status}",
            "",
            "> Este reporte se genera EXCLUSIVAMENTE con datos reales.",
            "> Las métricas marcadas con `❌ NO VALIDADO` requieren ejecutar el pipeline.",
            "",
            "---",
            "",
        ]

    def _section_executive_summary(self) -> List[str]:
        lines = ["## 1. Resumen Ejecutivo", ""]
        bt = self.data['backtest']

        if bt and bt.get('status') == 'VALIDATED':
            lines.append(f"**Trades ejecutados:** {bt.get('n_trades', 0)}")
            lines.append(f"**Win Rate:** {self._fmt(bt.get('win_rate'), '.4f')}")
            lines.append(f"**Profit Factor:** {self._fmt(bt.get('profit_factor'), '.4f')}")
            lines.append(f"**Sharpe:** {self._fmt(bt.get('sharpe'), '.4f')}")
            lines.append(f"**Max Drawdown:** {self._fmt(bt.get('max_drawdown_pct'), '.4f', '%')}")
            lines.append("")
        else:
            lines.append("❌ **NO VALIDADO** — Ejecutá `python run_lab.py` primero.")
            lines.append("")

        lines.append("**Propósito del laboratorio:**")
        lines.append("- Determinar calidad estadística de cada señal")
        lines.append("- Certificar qué activos son operables")
        lines.append("- Detectar sobreoptimización")
        lines.append("- Estimar próxima oportunidad")
        lines.append("- Clasificar en OPHELIA / S / A / B")
        lines.append("")
        return lines

    def _section_architecture(self) -> List[str]:
        return [
            "## 2. Arquitectura Operativa",
            "",
            "```",
            "Datos de mercado (CCXT, sin sintéticos)",
            "        ↓",
            "Indicadores (ADX Wilder, KER, ATR, EMA, Score)",
            "        ↓",
            "Filtros (régimen ≠ Chop, EMA15 alineada)",
            "        ↓",
            "Clasificación (OPHELIA / S / A / B / NO-TIER)",
            "        ↓",
            "Backtest realista (comisión + slippage + latencia)",
            "        ↓",
            "Walk-Forward (5 ventanas)",
            "        ↓",
            "Monte Carlo (10,000 simulaciones, seed=42)",
            "        ↓",
            "Certificación (auto-generada)",
            "        ↓",
            "Decisión operativa",
            "```",
            "",
        ]

    def _section_assets(self) -> List[str]:
        lines = ["## 3. Activos Analizados", ""]
        trades = self.data['trades']

        if trades is None or trades.empty:
            lines.append("❌ **NO VALIDADO** — No hay trades ejecutados.")
            lines.append("")
            return lines

        lines.append("| Activo | Trades | Período | Estado |")
        lines.append("|--------|--------|---------|--------|")

        for sym in sorted(trades['symbol'].unique()):
            sub = trades[trades['symbol'] == sym]
            n = len(sub)
            first = sub['entry_time'].min()
            last = sub['exit_time'].max()

            if n >= self.MIN_SIGNALS_FOR_VALIDATION:
                status = "🟢 Operable"
            elif n >= 10:
                status = "🟡 Bajo observación"
            else:
                status = "🔴 No recomendado"

            lines.append(f"| {sym} | {n} | {first} → {last} | {status} |")

        lines.append("")
        return lines

    def _section_global_stats(self) -> List[str]:
        lines = ["## 4. Estadísticas Globales", ""]
        bt = self.data['backtest']

        if bt and bt.get('status') == 'VALIDATED':
            lines.append("| Métrica | Valor |")
            lines.append("|---------|-------|")
            for k in ['n_trades', 'win_rate', 'profit_factor', 'sharpe',
                      'max_drawdown_pct', 'expectancy_pct', 'avg_win_pct',
                      'avg_loss_pct', 'avg_duration_min']:
                lines.append(f"| {k} | {self._fmt(bt.get(k))} |")
        else:
            lines.append("❌ **NO VALIDADO**")

        lines.append("")
        return lines

    def _section_per_tier(self) -> List[str]:
        lines = ["## 5. Estadísticas por Tier (OPHELIA / S / A / B)", ""]
        bt = self.data['backtest']

        if not bt or 'by_tier' not in bt or not bt['by_tier']:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        lines.append("| Tier | N | Win Rate | Avg PnL | Estado |")
        lines.append("|------|---|----------|---------|--------|")

        for tier in ['OPHELIA', 'S-TIER', 'A-TIER', 'B-TIER', 'NO-TIER']:
            if tier in bt['by_tier']:
                m = bt['by_tier'][tier]
                status = "✅" if m['n'] >= self.MIN_SIGNALS_PER_TIER else "⚠️ muestra insuficiente"
                lines.append(
                    f"| {tier} | {m['n']} | {m['wr']:.4f} | {m['avg_pnl']:.4f}% | {status} |"
                )

        lines.append("")
        return lines

    def _section_per_asset(self) -> List[str]:
        lines = ["## 6. Métricas por Activo", ""]
        trades = self.data['trades']

        if trades is None or trades.empty:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        lines.append("| Activo | Trades | Win Rate | PF | Avg PnL | Duración | Estado |")
        lines.append("|--------|--------|----------|-----|---------|----------|--------|")

        for sym in sorted(trades['symbol'].unique()):
            sub = trades[trades['symbol'] == sym]
            if len(sub) < 5:
                continue

            wins = sub[sub['net_pnl_pct'] > 0]
            losses = sub[sub['net_pnl_pct'] <= 0]
            wr = len(wins) / len(sub)
            gains = wins['net_pnl_pct'].sum() if not wins.empty else 0
            losses_abs = abs(losses['net_pnl_pct'].sum()) if not losses.empty else 1e-9
            pf = gains / losses_abs if losses_abs > 0 else None
            avg_pnl = sub['net_pnl_pct'].mean()
            dur = sub['duration_minutes'].mean()

            if wr > 0.5 and (pf or 0) > 1.2:
                status = "🟢"
            elif wr > 0.4:
                status = "🟡"
            else:
                status = "🔴"

            lines.append(
                f"| {sym} | {len(sub)} | {wr:.4f} | "
                f"{self._fmt(pf, '.4f')} | {avg_pnl*100:.4f}% | "
                f"{dur:.1f} min | {status} |"
            )

        lines.append("")
        return lines

    def _section_winning_vs_losing(self) -> List[str]:
        lines = ["## 7. Señales Ganadoras vs Perdedoras", ""]
        trades = self.data['trades']

        if trades is None or trades.empty:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        wins = trades[trades['net_pnl_pct'] > 0]
        losses = trades[trades['net_pnl_pct'] <= 0]

        if wins.empty or losses.empty:
            lines.append("⚠️ Se necesitan ambas categorías para comparar.")
            lines.append("")
            return lines

        lines.append("| Métrica | Ganadoras | Perdedoras | Diferencia |")
        lines.append("|---------|-----------|------------|------------|")

        for col in ['adx', 'ker', 'score']:
            if col in trades.columns:
                w = wins[col].mean()
                l = losses[col].mean()
                lines.append(f"| {col.upper()} | {w:.4f} | {l:.4f} | {w - l:+.4f} |")

        if 'regime' in trades.columns:
            w_mode = wins['regime'].mode()
            l_mode = losses['regime'].mode()
            w_regime = w_mode.iloc[0] if not w_mode.empty else 'N/A'
            l_regime = l_mode.iloc[0] if not l_mode.empty else 'N/A'
            lines.append(f"| Régimen dominante | {w_regime} | {l_regime} | — |")

        lines.append("")
        return lines

    def _section_next_opportunities(self) -> List[str]:
        lines = ["## 8. Próximas Oportunidades Estimadas", ""]
        trades = self.data['trades']

        if trades is None or trades.empty:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        lines.append("| Tier | Tiempo desde última señal | Promedio entre señales | Próxima esperada |")
        lines.append("|------|----------------------------|------------------------|------------------|")

        now = pd.Timestamp.now(tz=None)

        for tier in ['OPHELIA', 'S-TIER', 'A-TIER', 'B-TIER']:
            sub = trades[trades['tier'] == tier]
            if len(sub) < 2:
                lines.append(
                    f"| {tier} | ❌ datos insuficientes | ❌ datos insuficientes | ❌ datos insuficientes |"
                )
                continue

            try:
                sub = sub.sort_values('entry_time')
                times = self._safe_to_datetime(sub['entry_time'])
                intervals = times.diff().dt.total_seconds().dropna() / 60
                avg_interval = intervals.mean()
                last = times.iloc[-1]
                elapsed = (now - last).total_seconds() / 60
                remaining = max(0, avg_interval - elapsed)

                lines.append(
                    f"| {tier} | {elapsed:.0f} min | {avg_interval:.0f} min | {remaining:.0f} min |"
                )
            except Exception:
                lines.append(f"| {tier} | ❌ error de cálculo | ❌ error de cálculo | ❌ error de cálculo |")

        lines.append("")
        return lines

    def _section_calendar(self) -> List[str]:
        lines = ["## 9. Calendario de Oportunidades", ""]
        trades = self.data['trades']

        if trades is None or trades.empty:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        try:
            trades = trades.copy()
            trades['entry_dt'] = self._safe_to_datetime(trades['entry_time'])
            trades['hour'] = trades['entry_dt'].dt.hour
            trades['weekday'] = trades['entry_dt'].dt.day_name()
        except Exception:
            lines.append("❌ Error procesando timestamps.")
            lines.append("")
            return lines

        lines.append("### Por Hora (UTC)")
        lines.append("| Hora | Trades | Win Rate | Avg PnL |")
        lines.append("|------|--------|----------|---------|")

        for hour, sub in trades.groupby('hour'):
            wr = (sub['net_pnl_pct'] > 0).mean()
            avg = sub['net_pnl_pct'].mean()
            lines.append(f"| {hour:02d}:00 | {len(sub)} | {wr:.4f} | {avg*100:.4f}% |")

        lines.append("")
        lines.append("### Por Día de la Semana")
        lines.append("| Día | Trades | Win Rate | Avg PnL |")
        lines.append("|-----|--------|----------|---------|")

        for day, sub in trades.groupby('weekday'):
            wr = (sub['net_pnl_pct'] > 0).mean()
            avg = sub['net_pnl_pct'].mean()
            lines.append(f"| {day} | {len(sub)} | {wr:.4f} | {avg*100:.4f}% |")

        lines.append("")
        return lines

    def _section_simulation(self) -> List[str]:
        lines = ["## 10. Simulación Operativa (basada en histórico)", ""]
        trades = self.data['trades']

        if trades is None or trades.empty:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        for capital in [100, 1000]:
            lines.append(f"### Capital inicial: {capital} USDT")
            lines.append("| Tier | N trades | Retorno total | DD esperado | Prob. pérdida |")
            lines.append("|------|----------|---------------|-------------|---------------|")

            for tier in ['OPHELIA', 'S-TIER', 'A-TIER', 'B-TIER']:
                sub = trades[trades['tier'] == tier]
                if sub.empty:
                    lines.append(f"| {tier} | 0 | ❌ | ❌ | ❌ |")
                    continue

                returns = sub['net_pnl_pct'].values
                equity = capital * np.cumprod(1 + returns)
                total_return = (equity[-1] / capital - 1) * 100
                peak = np.maximum.accumulate(equity)
                dd = ((peak - equity) / peak).max() * 100
                prob_loss = (returns < 0).mean()

                lines.append(
                    f"| {tier} | {len(sub)} | {total_return:.4f}% | "
                    f"{dd:.4f}% | {prob_loss:.4f} |"
                )

            lines.append("")
        return lines

    def _section_operational_ranking(self) -> List[str]:
        lines = ["## 11. Ranking Operativo Final", ""]
        trades = self.data['trades']

        if trades is None or trades.empty:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        lines.append("| Activo | Mejor Tier | Operar | Motivo |")
        lines.append("|--------|------------|--------|--------|")

        for sym in sorted(trades['symbol'].unique()):
            sub = trades[trades['symbol'] == sym]
            if len(sub) < 5:
                lines.append(f"| {sym} | — | ❌ No | Muestra insuficiente ({len(sub)}) |")
                continue

            best_tier = None
            best_wr = -1
            for tier in ['OPHELIA', 'S-TIER', 'A-TIER', 'B-TIER']:
                ts = sub[sub['tier'] == tier]
                if len(ts) >= 3:
                    wr = (ts['net_pnl_pct'] > 0).mean()
                    if wr > best_wr:
                        best_wr = wr
                        best_tier = tier

            wr_global = (sub['net_pnl_pct'] > 0).mean()
            if wr_global > 0.55 and len(sub) >= 20:
                op = "✅ Sí"
                motivo = f"WR {wr_global:.4f}, N={len(sub)}"
            elif wr_global > 0.45 and len(sub) >= 10:
                op = "⚠️ Observación"
                motivo = f"WR {wr_global:.4f}, N={len(sub)}"
            else:
                op = "❌ No"
                motivo = f"WR {wr_global:.4f} bajo o N insuficiente"

            lines.append(f"| {sym} | {best_tier or '—'} | {op} | {motivo} |")

        lines.append("")
        return lines

    def _section_alerts(self) -> List[str]:
        lines = ["## 12. Alertas del Laboratorio", ""]
        bt = self.data['backtest']
        trades = self.data['trades']
        alerts = []

        if bt is None or trades is None:
            lines.append("❌ **NO VALIDADO**")
            lines.append("")
            return lines

        # Sobreoptimización
        opt = self.data['optimization']
        if opt and len(opt) > 0:
            first = opt[0].get('metrics', {}) or {}
            last = opt[-1].get('metrics', {}) or {}
            delta_wr = (last.get('win_rate', 0) or 0) - (first.get('win_rate', 0) or 0)
            if delta_wr > 0.30:
                alerts.append(
                    f"⚠️ **Sobreoptimización:** mejora de WR {delta_wr:.4f} entre baseline y final."
                )

        # Muestras insuficientes
        if bt.get('n_trades', 0) < 100:
            alerts.append(
                f"⚠️ **Muestra baja:** solo {bt.get('n_trades', 0)} trades. Mínimo recomendado: 100."
            )

        # Drawdown excesivo
        dd = bt.get('max_drawdown_pct', 0) or 0
        if dd > self.MAX_DRAWDOWN_OK:
            alerts.append(f"⚠️ **Drawdown elevado:** {dd:.4f}% > {self.MAX_DRAWDOWN_OK}%.")

        # Profit factor bajo
        pf = bt.get('profit_factor', 0) or 0
        if pf < self.MIN_PROFIT_FACTOR_OK:
            alerts.append(f"⚠️ **Profit Factor bajo:** {pf:.4f} < {self.MIN_PROFIT_FACTOR_OK}.")

        # Sharpe bajo
        sh = bt.get('sharpe', 0) or 0
        if sh < self.MIN_SHARPE_OK:
            alerts.append(f"⚠️ **Sharpe bajo:** {sh:.4f} < {self.MIN_SHARPE_OK}.")

        # Activos inestables
        for sym in trades['symbol'].unique():
            sub = trades[trades['symbol'] == sym]
            if len(sub) < 10:
                continue
            wr = (sub['net_pnl_pct'] > 0).mean()
            if wr < 0.30 and len(sub) >= 20:
                alerts.append(f"⚠️ **{sym}:** WR muy bajo ({wr:.4f}) con N={len(sub)}.")

        if not alerts:
            lines.append("✅ **No se detectaron alertas críticas.**")
        else:
            for a in alerts:
                lines.append(f"- {a}")

        lines.append("")
        return lines

    def _section_certification(self) -> List[str]:
        lines = ["## 13. Certificación Final", ""]
        bt = self.data['backtest']

        if not bt or bt.get('status') != 'VALIDATED':
            lines.append("❌ **NO CERTIFICADO** — Sin datos de backtest válidos.")
            lines.append("")
            return lines

        n = bt.get('n_trades', 0)
        wr = bt.get('win_rate', 0) or 0
        pf = bt.get('profit_factor', 0) or 0
        dd = bt.get('max_drawdown_pct', 0) or 0
        sh = bt.get('sharpe', 0) or 0

        checks = {
            'Mínimo 100 trades': n >= 100,
            'Win Rate > 45%': wr > 0.45,
            'Profit Factor > 1.2': pf > 1.2,
            'Max Drawdown < 20%': dd < 20,
            'Sharpe > 0.8': sh > 0.8,
        }

        lines.append("| Criterio | Estado |")
        lines.append("|----------|--------|")
        for k, v in checks.items():
            lines.append(f"| {k} | {'✅' if v else '❌'} |")

        passed = sum(checks.values())
        total = len(checks)

        if passed == total:
            status = "✅ **CERTIFICADO**"
        elif passed >= total - 2:
            status = "⚠️ **EN OBSERVACIÓN**"
        else:
            status = "❌ **NO CERTIFICADO**"

        lines.append("")
        lines.append(f"### {status}")
        lines.append(f"**Checks aprobados:** {passed}/{total}")
        lines.append("")
        return lines

    def _section_footer(self) -> List[str]:
        return [
            "---",
            "",
            "## Declaración de Honestidad",
            "",
            "Este reporte se genera automáticamente con datos reales del laboratorio.",
            "**Ninguna métrica es estimada ni inventada.**",
            "Las secciones marcadas como `❌ NO VALIDADO` requieren ejecutar el pipeline completo.",
            "",
            "**Para regenerar este reporte:**",
            "```bash",
            "python run_lab.py",
            "python -c 'from ophelia_lab.operational_report import OperationalReport; OperationalReport().generate()'",
            "```",
            "",
            f"**Generado:** {datetime.now(timezone.utc).isoformat()} UTC",
        ]


if __name__ == '__main__':
    OperationalReport().generate()
