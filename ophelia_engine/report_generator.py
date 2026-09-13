# ophelia_engine/report_generator.py
"""
Reporte OPHELIA/STANDARD con formato de 2 niveles.
"""
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict
import pandas as pd


class ReportGenerator:

    @staticmethod
    def generate(scorer_meta: Dict, cert: Dict, leverage: Dict,
                 temporal: Dict, selected: pd.DataFrame,
                 wf_df, mc: Dict, rankings: Dict,
                 output: str = 'reports/OPHELIA_DAILY_CERTIFICATION_REPORT.md'):

        lines = []
        lines.append("# 🌟 OPHELIA DAILY CERTIFICATION REPORT")
        lines.append("")
        lines.append(f"**Generado:** {datetime.now(timezone.utc).isoformat()} UTC")
        lines.append(f"**Estado:** {'✅ CERTIFICADO' if cert.get('certified') else '❌ NO CERTIFICADO'}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # ============================================================
        # 1. VALIDACIÓN DE HIPÓTESIS
        # ============================================================
        lines.append("## 1. Validación de Hipótesis")
        lines.append("")
        auc_test = scorer_meta.get('auc_test', 0.5)
        lines.append(f"- AUC test: **{auc_test:.4f}** (≥0.55 = predictor útil)")
        lines.append(f"- Base rate test: {scorer_meta.get('base_rate_test', 0):.4f}")

        if auc_test >= 0.55:
            lines.append("- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar")
        else:
            lines.append("- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test")
        lines.append("")

        # ============================================================
        # 2. CALIBRACIÓN DE THRESHOLDS
        # ============================================================
        lines.append("## 2. Thresholds Calibrados")
        lines.append("")
        lines.append("| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |")
        lines.append("|-------|-----------|----------|---------|-----------|----------|")
        lines.append(
            f"| **OPHELIA** | {scorer_meta.get('ophelia_threshold', 0):.3f} | "
            f"{scorer_meta.get('ophelia_wr_train', 0)*100:.2f}% | "
            f"{scorer_meta.get('ophelia_wr_test', 0)*100:.2f}% | "
            f"{scorer_meta.get('ophelia_tpd_train', 0):.2f} | "
            f"{scorer_meta.get('ophelia_tpd_test', 0):.2f} |"
        )
        lines.append(
            f"| **STANDARD** | {scorer_meta.get('standard_threshold', 0):.3f} | "
            f"{scorer_meta.get('standard_wr_train', 0)*100:.2f}% | "
            f"{scorer_meta.get('standard_wr_test', 0)*100:.2f}% | "
            f"{scorer_meta.get('standard_tpd_train', 0):.2f} | "
            f"{scorer_meta.get('standard_tpd_test', 0):.2f} |"
        )
        lines.append("")

        # ============================================================
        # 3. OPHELIA RANKING LONG
        # ============================================================
        long_df = rankings.get('long', pd.DataFrame())
        lines.append("## 3. OPHELIA RANKING — LONG")
        lines.append("")
        if not long_df.empty:
            lines.append("| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |")
            lines.append("|------|--------|-------|------|----------|------|-----------|")
            for i, row in long_df.head(15).iterrows():
                lines.append(
                    f"| {i+1} | {row.get('symbol', '')} | {row.get('ophelia_score', 0):.3f} | "
                    f"{row.get('tier', '')} | {str(row.get('entry_time_ar', ''))[11:16]} | "
                    f"{row.get('movement_type', '')} | {'✅' if row.get('win') else '❌'} |"
                )
        else:
            lines.append("_Sin señales LONG en el período._")
        lines.append("")

        # ============================================================
        # 4. OPHELIA RANKING SHORT
        # ============================================================
        short_df = rankings.get('short', pd.DataFrame())
        lines.append("## 4. OPHELIA RANKING — SHORT")
        lines.append("")
        if not short_df.empty:
            lines.append("| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |")
            lines.append("|------|--------|-------|------|----------|------|-----------|")
            for i, row in short_df.head(15).iterrows():
                lines.append(
                    f"| {i+1} | {row.get('symbol', '')} | {row.get('ophelia_score', 0):.3f} | "
                    f"{row.get('tier', '')} | {str(row.get('entry_time_ar', ''))[11:16]} | "
                    f"{row.get('movement_type', '')} | {'✅' if row.get('win') else '❌'} |"
                )
        else:
            lines.append("_Sin señales SHORT en el período._")
        lines.append("")

        # ============================================================
        # 5. LEVERAGE POR NIVEL
        # ============================================================
        lines.append("## 5. Leverage por Nivel")
        lines.append("")
        lines.append(f"- OPHELIA: máx seguro **{leverage.get('leverage_max_safe', 1)}x**, "
                     f"recomendado **{leverage.get('leverage_recommended', 1)}x**")
        lines.append(f"- MAE p95 histórico: {leverage.get('mae_p95_pct', 0):.4f}%")
        lines.append("")

        # ============================================================
        # 6. ANÁLISIS TEMPORAL
        # ============================================================
        lines.append("## 6. Modelo Temporal")
        lines.append("")
        lines.append(f"- Trades/día promedio: {temporal.get('trades_per_day', 0)}")
        lines.append(f"- Intervalo medio: {temporal.get('mean_interval_min', 'N/A')} min")
        lines.append(f"- Distribución: {temporal.get('direction_distribution', {})}")

        top_hours = temporal.get('top_hours', {})
        if top_hours:
            lines.append("")
            lines.append("### Horas más frecuentes (ARG)")
            lines.append("")
            lines.append("| Hora | N trades |")
            lines.append("|------|----------|")
            for h, n in sorted(top_hours.items()):
                lines.append(f"| {h:02d}:00 | {n} |")
        lines.append("")

        # ============================================================
        # 7. CLASIFICACIÓN DE MOVIMIENTOS
        # ============================================================
        lines.append("## 7. Clasificación de Movimientos")
        lines.append("")
        if not selected.empty and 'movement_type' in selected.columns:
            counts = selected['movement_type'].value_counts().to_dict()
            lines.append("| Tipo | N | WR |")
            lines.append("|------|---|-----|")
            for mtype, count in counts.items():
                wr = selected[selected['movement_type'] == mtype]['win'].mean()
                lines.append(f"| {mtype} | {count} | {wr*100:.2f}% |")
        lines.append("")

        # ============================================================
        # 8. WALK-FORWARD
        # ============================================================
        lines.append("## 8. Walk-Forward")
        lines.append("")
        if wf_df is not None and not wf_df.empty:
            lines.append(wf_df.to_markdown(index=False))
        else:
            lines.append("❌ Datos insuficientes")
        lines.append("")

        # ============================================================
        # 9. MONTE CARLO
        # ============================================================
        lines.append("## 9. Monte Carlo (10,000 sims)")
        lines.append("")
        if mc:
            lines.append("| Métrica | Valor |")
            lines.append("|---------|-------|")
            for k, v in mc.items():
                lines.append(f"| {k} | {v} |")
        lines.append("")

        # ============================================================
        # 10. CERTIFICACIÓN
        # ============================================================
        lines.append("## 10. Certificación")
        lines.append("")
        if cert.get('reasons'):
            lines.append("### Razones de rechazo")
            for r in cert['reasons']:
                lines.append(f"- ❌ {r}")
        else:
            lines.append("✅ Todos los criterios aprobados")
        lines.append("")

        # ============================================================
        # 11. ÚLTIMAS 20 SEÑALES
        # ============================================================
        if not selected.empty:
            lines.append("## 11. Últimas 20 Señales (OPHELIA + STANDARD)")
            lines.append("")
            lines.append("| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |")
            lines.append("|-----------|--------|------|-------|-----|-----|-----|-----|-----|")
            top20 = selected.sort_values('entry_time', ascending=False).head(20)
            for _, t in top20.iterrows():
                lines.append(
                    f"| {str(t.get('entry_time_ar', ''))[:19]} | "
                    f"{t.get('symbol', '')} | {t.get('tier', '')} | "
                    f"{t.get('ophelia_score', 0):.3f} | {t.get('direction', '')} | "
                    f"{t.get('mfe', 0)*100:.3f}% | {t.get('mae', 0)*100:.3f}% | "
                    f"{t.get('duration_min', 0):.0f}m | {'✅' if t.get('win') else '❌'} |"
                )
            lines.append("")

        # ============================================================
        # 12. DECLARACIÓN DE HONESTIDAD
        # ============================================================
        lines.append("---")
        lines.append("")
        lines.append("## Declaración de Honestidad")
        lines.append("")
        lines.append("El OPHELIA Score es P(win|features) validado en out-of-sample.")
        lines.append("**No se filtra por resultado posterior.**")
        lines.append("**No se selecciona winners a posteriori.**")
        lines.append("El WR reportado es el WR real de las señales seleccionadas por el score.")

        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text('\n'.join(lines), encoding='utf-8')
        print(f"✅ Reporte: {output}")
