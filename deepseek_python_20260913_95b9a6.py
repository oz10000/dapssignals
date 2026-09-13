# ophelia_engine/report_generator.py
"""Genera OPHELIA_CERTIFICATION_REPORT.md"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List


class OpheliaReportGenerator:

    @staticmethod
    def generate(pattern: Dict, cert: Dict, leverage: Dict,
                 ophelia_trades: List[Dict],
                 output: str = 'reports/OPHELIA_CERTIFICATION_REPORT.md'):

        lines = []
        lines.append("# 🌟 OPHELIA CERTIFICATION REPORT")
        lines.append("")
        lines.append(f"**Generado:** {datetime.now(timezone.utc).isoformat()} UTC")
        lines.append(f"**Estado:** {'✅ CERTIFICADO' if cert.get('certified') else '❌ NO CERTIFICADO'}")
        lines.append("")

        # 1. Resumen
        lines.append("## 1. Resumen Ejecutivo")
        lines.append("")
        lines.append(f"- Trades OPHELIA históricos: **{pattern.get('n_train', 0)}**")
        lines.append(f"- Win Rate histórico: **{cert.get('train_wr', 0)*100:.1f}%**")
        lines.append(f"- Win Rate out-of-sample: **{cert.get('test_wr', 0)*100:.1f}%**")
        lines.append(f"- Activos OPHELIA: {', '.join(pattern.get('assets', [])[:10])}")
        lines.append(f"- Ventana temporal: {pattern.get('hour_range', {}).get('min', 0)}h - {pattern.get('hour_range', {}).get('max', 0)}h ARG")
        lines.append("")

        # 2. Patrón aprendido
        lines.append("## 2. Patrón Aprendido")
        lines.append("")
        lines.append("| Feature | Min | Max | Mean | Std |")
        lines.append("|---------|-----|-----|------|-----|")
        for feat, rng in pattern.get('features', {}).items():
            lines.append(f"| {feat} | {rng['min']:.4f} | {rng['max']:.4f} | {rng['mean']:.4f} | {rng['std']:.4f} |")
        lines.append("")

        # 3. Estadísticas del patrón
        lines.append("## 3. Estadísticas del Patrón")
        lines.append("")
        stats = pattern.get('outcome_stats', {})
        lines.append(f"- MFE medio: {stats.get('mean_mfe', 0)*100:.4f}%")
        lines.append(f"- MFE mínimo: {stats.get('min_mfe', 0)*100:.4f}%")
        lines.append(f"- MAE máximo: {stats.get('max_mae', 0)*100:.4f}%")
        lines.append(f"- Duración media: {stats.get('mean_duration_min', 0):.1f} min")
        lines.append("")

        # 4. Leverage
        lines.append("## 4. Leverage Recomendado")
        lines.append("")
        lines.append(f"- Máximo seguro: **{leverage.get('leverage_max_safe', 0)}x**")
        lines.append(f"- Recomendado: **{leverage.get('leverage_recommended', 0)}x**")
        lines.append(f"- Conservador: {leverage.get('leverage_conservative', 0)}x")
        lines.append(f"- Basado en MAE histórica: {leverage.get('max_mae_historical', 0)*100:.4f}%")
        lines.append("")

        # 5. Trades OPHELIA (últimos 20)
        lines.append("## 5. Últimos 20 Trades OPHELIA")
        lines.append("")
        lines.append("| Fecha | Activo | Dir | Entry | MFE | MAE | Dur |")
        lines.append("|-------|--------|-----|-------|-----|-----|-----|")
        for t in ophelia_trades[-20:]:
            lines.append(
                f"| {t.get('entry_time_ar', 'N/A')} | {t.get('symbol')} | "
                f"{t.get('direction')} | {t.get('entry_price', 0):.4f} | "
                f"{t.get('mfe', 0)*100:.3f}% | {t.get('mae', 0)*100:.3f}% | "
                f"{t.get('duration_min', 0):.0f}m |"
            )
        lines.append("")

        # 6. Certificación
        lines.append("## 6. Certificación")
        lines.append("")
        lines.append(f"- **{cert.get('reason', 'N/A')}**")
        lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("## Declaración de Honestidad")
        lines.append("")
        lines.append("Este reporte se genera con datos REALES del backtest histórico.")
        lines.append("Un patrón solo se certifica si mantiene 100% WR en out-of-sample.")
        lines.append("Si la muestra es insuficiente, se reporta como NO CERTIFICADO.")

        Path(output).parent.mkdir(parents=True, exist_ok=True)
        Path(output).write_text('\n'.join(lines), encoding='utf-8')
        print(f"✅ Reporte: {output}")