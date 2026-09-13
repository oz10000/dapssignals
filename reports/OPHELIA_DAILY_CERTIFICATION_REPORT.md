# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-09-13T18:57:36.258975+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.4318** (≥0.55 = predictor útil)
- Base rate test: 0.4211
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.650 | 0.00% | 0.00% | 0.00 | 0.00 |
| **STANDARD** | 0.450 | 58.33% | 0.00% | 2.40 | 3.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | ATOM/USDT | 0.924 | OPHELIA | 02:25 | CONTINUACIÓN | ✅ |
| 2 | VET/USDT | 0.882 | OPHELIA | 02:55 | CONTINUACIÓN | ❌ |
| 3 | LTC/USDT | 0.823 | OPHELIA | 01:40 | CONTINUACIÓN | ✅ |
| 4 | VET/USDT | 0.784 | OPHELIA | 23:10 | CONTINUACIÓN | ✅ |
| 5 | AVAX/USDT | 0.707 | OPHELIA | 23:40 | CONTINUACIÓN | ✅ |
| 6 | VET/USDT | 0.706 | OPHELIA | 22:35 | CONTINUACIÓN | ✅ |
| 7 | APT/USDT | 0.644 | STANDARD | 02:45 | CONTINUACIÓN | ❌ |
| 8 | SEI/USDT | 0.638 | STANDARD | 00:10 | CONTINUACIÓN | ❌ |
| 9 | VET/USDT | 0.621 | STANDARD | 21:35 | CONTINUACIÓN | ✅ |
| 10 | WIF/USDT | 0.607 | STANDARD | 02:25 | CONTINUACIÓN | ✅ |
| 11 | OP/USDT | 0.575 | STANDARD | 04:30 | CONTINUACIÓN | ❌ |
| 12 | XRP/USDT | 0.570 | STANDARD | 11:05 | CONTINUACIÓN | ❌ |
| 13 | DOGE/USDT | 0.560 | STANDARD | 23:40 | CONTINUACIÓN | ❌ |
| 14 | ATOM/USDT | 0.535 | STANDARD | 23:20 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4255%

## 6. Modelo Temporal

- Trades/día promedio: 3.5
- Intervalo medio: 457.7 min
- Distribución: {'LONG': 14}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 1 |
| 02:00 | 4 |
| 21:00 | 1 |
| 22:00 | 1 |
| 23:00 | 4 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 14 | 50.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0178602384457571 |
| median_final | 1.0168855383606354 |
| p5_final | 1.002011442205228 |
| p95_final | 1.0373335208984238 |
| mean_max_dd | 0.002537375202546438 |
| p95_max_dd | 0.004866094305924436 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 44 < 60
- ❌ Test insuficiente: 19 < 20
- ❌ AUC test bajo: 0.432 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-09-13 11:05:00 | XRP/USDT | STANDARD | 0.570 | LONG | 0.030% | -0.067% | 5m | ❌ |
| 2026-09-13 04:30:00 | OP/USDT | STANDARD | 0.575 | LONG | 0.270% | -0.467% | 15m | ❌ |
| 2026-09-13 02:45:00 | APT/USDT | STANDARD | 0.644 | LONG | 0.218% | -0.117% | 10m | ❌ |
| 2026-09-13 02:25:00 | ATOM/USDT | OPHELIA | 0.924 | LONG | 0.249% | 0.000% | 20m | ✅ |
| 2026-09-13 02:25:00 | WIF/USDT | STANDARD | 0.607 | LONG | 0.263% | -0.053% | 20m | ✅ |
| 2026-09-13 01:40:00 | LTC/USDT | OPHELIA | 0.823 | LONG | 0.298% | 0.000% | 5m | ✅ |
| 2026-09-13 00:10:00 | SEI/USDT | STANDARD | 0.638 | LONG | 0.000% | -0.403% | 5m | ❌ |
| 2026-09-12 23:40:00 | AVAX/USDT | OPHELIA | 0.707 | LONG | 0.175% | -0.027% | 10m | ✅ |
| 2026-09-12 23:40:00 | DOGE/USDT | STANDARD | 0.560 | LONG | 0.070% | -0.094% | 10m | ❌ |
| 2026-09-12 23:20:00 | ATOM/USDT | STANDARD | 0.535 | LONG | 0.000% | -0.062% | 5m | ❌ |
| 2026-09-12 22:35:00 | VET/USDT | OPHELIA | 0.706 | LONG | 0.342% | 0.000% | 15m | ✅ |
| 2026-09-11 21:35:00 | VET/USDT | STANDARD | 0.621 | LONG | 0.434% | 0.000% | 15m | ✅ |
| 2026-09-11 02:55:00 | VET/USDT | OPHELIA | 0.882 | LONG | 0.000% | -0.212% | 5m | ❌ |
| 2026-09-09 23:10:00 | VET/USDT | OPHELIA | 0.784 | LONG | 1.613% | -0.302% | 25m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.