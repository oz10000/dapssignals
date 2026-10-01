# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-01T12:36:08.325502+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.7125** (≥0.55 = predictor útil)
- Base rate test: 0.1667
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 25.00% | 50.00% | 2.00 | 2.00 |
| **STANDARD** | 0.450 | 40.00% | 40.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | BTC/USDT | 0.883 | OPHELIA | 06:20 | CONTINUACIÓN | ✅ |
| 2 | BNB/USDT | 0.858 | OPHELIA | 03:00 | CONTINUACIÓN | ❌ |
| 3 | LTC/USDT | 0.805 | OPHELIA | 20:55 | CONTINUACIÓN | ❌ |
| 4 | ETC/USDT | 0.787 | OPHELIA | 22:05 | CONTINUACIÓN | ❌ |
| 5 | LDO/USDT | 0.548 | STANDARD | 01:45 | CONTINUACIÓN | ✅ |
| 6 | ARB/USDT | 0.547 | STANDARD | 23:55 | CONTINUACIÓN | ❌ |
| 7 | NEAR/USDT | 0.542 | STANDARD | 19:40 | CONTINUACIÓN | ❌ |
| 8 | ADA/USDT | 0.501 | STANDARD | 19:45 | CONTINUACIÓN | ✅ |
| 9 | SEI/USDT | 0.498 | STANDARD | 00:40 | CONTINUACIÓN | ❌ |
| 10 | ALGO/USDT | 0.496 | STANDARD | 21:45 | CONTINUACIÓN | ✅ |
| 11 | VET/USDT | 0.491 | STANDARD | 22:15 | CONTINUACIÓN | ✅ |
| 12 | SOL/USDT | 0.453 | STANDARD | 01:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.5743%

## 6. Modelo Temporal

- Trades/día promedio: 6.0
- Intervalo medio: 58.2 min
- Distribución: {'LONG': 12}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 2 |
| 19:00 | 2 |
| 20:00 | 1 |
| 21:00 | 1 |
| 22:00 | 2 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 12 | 41.67% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.008840886422062 |
| median_final | 1.008458618733244 |
| p5_final | 0.9942433692113477 |
| p95_final | 1.024640713248766 |
| mean_max_dd | 0.004725194130328028 |
| p95_max_dd | 0.009477714986368834 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 53 < 100
- ❌ Test insuficiente: 24 < 40
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-01 06:20:00 | BTC/USDT | OPHELIA | 0.883 | LONG | 0.181% | -0.038% | 10m | ✅ |
| 2026-10-01 03:00:00 | BNB/USDT | OPHELIA | 0.858 | LONG | 0.013% | -0.078% | 5m | ❌ |
| 2026-10-01 01:45:00 | LDO/USDT | STANDARD | 0.548 | LONG | 1.065% | -0.200% | 30m | ✅ |
| 2026-10-01 01:00:00 | SOL/USDT | STANDARD | 0.453 | LONG | 0.008% | -0.160% | 5m | ❌ |
| 2026-10-01 00:40:00 | SEI/USDT | STANDARD | 0.498 | LONG | 0.445% | -0.256% | 25m | ❌ |
| 2026-09-30 23:55:00 | ARB/USDT | STANDARD | 0.547 | LONG | 0.435% | -0.254% | 5m | ❌ |
| 2026-09-30 22:15:00 | VET/USDT | STANDARD | 0.491 | LONG | 0.394% | 0.000% | 10m | ✅ |
| 2026-09-30 22:05:00 | ETC/USDT | OPHELIA | 0.787 | LONG | 0.257% | -0.190% | 10m | ❌ |
| 2026-09-30 21:45:00 | ALGO/USDT | STANDARD | 0.496 | LONG | 0.343% | 0.000% | 5m | ✅ |
| 2026-09-30 20:55:00 | LTC/USDT | OPHELIA | 0.805 | LONG | 0.030% | -0.178% | 5m | ❌ |
| 2026-09-30 19:45:00 | ADA/USDT | STANDARD | 0.501 | LONG | 0.364% | 0.000% | 5m | ✅ |
| 2026-09-30 19:40:00 | NEAR/USDT | STANDARD | 0.542 | LONG | 0.093% | -0.963% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.