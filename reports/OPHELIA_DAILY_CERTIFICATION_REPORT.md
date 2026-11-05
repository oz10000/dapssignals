# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-05T14:09:41.223924+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.3566** (≥0.55 = predictor útil)
- Base rate test: 0.1905
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 36.84% | 0.00% | 0.63 | 2.00 |
| **STANDARD** | 0.450 | 33.33% | 0.00% | 1.60 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | APT/USDT | 0.667 | OPHELIA | 03:50 | CONTINUACIÓN | ❌ |
| 2 | VET/USDT | 0.663 | OPHELIA | 05:45 | CONTINUACIÓN | ❌ |
| 3 | VET/USDT | 0.661 | OPHELIA | 21:45 | CONTINUACIÓN | ❌ |
| 4 | VET/USDT | 0.653 | OPHELIA | 01:20 | CONTINUACIÓN | ❌ |
| 5 | ADA/USDT | 0.639 | OPHELIA | 19:05 | CONTINUACIÓN | ✅ |
| 6 | APT/USDT | 0.635 | OPHELIA | 18:30 | CONTINUACIÓN | ✅ |
| 7 | VET/USDT | 0.621 | OPHELIA | 01:50 | CONTINUACIÓN | ❌ |
| 8 | ALGO/USDT | 0.609 | OPHELIA | 02:35 | CONTINUACIÓN | ❌ |
| 9 | VET/USDT | 0.608 | OPHELIA | 22:20 | CONTINUACIÓN | ✅ |
| 10 | VET/USDT | 0.607 | OPHELIA | 21:00 | CONTINUACIÓN | ❌ |
| 11 | VET/USDT | 0.605 | OPHELIA | 22:05 | CONTINUACIÓN | ✅ |
| 12 | VET/USDT | 0.590 | OPHELIA | 08:35 | CONTINUACIÓN | ✅ |
| 13 | VET/USDT | 0.590 | OPHELIA | 02:30 | CONTINUACIÓN | ❌ |
| 14 | VET/USDT | 0.585 | OPHELIA | 05:45 | CONTINUACIÓN | ❌ |
| 15 | VET/USDT | 0.581 | OPHELIA | 22:40 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.5858%

## 6. Modelo Temporal

- Trades/día promedio: 2.04
- Intervalo medio: 877.8 min
- Distribución: {'LONG': 57}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 8 |
| 02:00 | 6 |
| 05:00 | 5 |
| 21:00 | 10 |
| 22:00 | 8 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 57 | 31.58% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0055694947830947 |
| median_final | 1.0053507635437184 |
| p5_final | 0.9870279263649177 |
| p95_final | 1.025098236562188 |
| mean_max_dd | 0.010190571385441067 |
| p95_max_dd | 0.01884590928361277 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 96 < 100
- ❌ AUC test bajo: 0.357 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 36.8%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-05 05:45:00 | DOT/USDT | STANDARD | 0.538 | LONG | 0.292% | -0.167% | 25m | ❌ |
| 2026-11-05 03:55:00 | INJ/USDT | STANDARD | 0.526 | LONG | 0.184% | -0.590% | 5m | ❌ |
| 2026-11-05 03:50:00 | APT/USDT | OPHELIA | 0.667 | LONG | 0.016% | -0.234% | 5m | ❌ |
| 2026-11-05 02:35:00 | ALGO/USDT | OPHELIA | 0.609 | LONG | 0.000% | -0.327% | 5m | ❌ |
| 2026-11-05 01:30:00 | DOGE/USDT | STANDARD | 0.530 | LONG | 0.052% | -0.233% | 5m | ❌ |
| 2026-11-05 00:35:00 | OP/USDT | STANDARD | 0.548 | LONG | 0.000% | -0.313% | 5m | ❌ |
| 2026-11-05 00:15:00 | ADA/USDT | STANDARD | 0.532 | LONG | 0.050% | -0.151% | 5m | ❌ |
| 2026-11-04 22:50:00 | ADA/USDT | STANDARD | 0.545 | LONG | 0.000% | -0.404% | 5m | ❌ |
| 2026-11-04 21:30:00 | UNI/USDT | STANDARD | 0.542 | LONG | 0.000% | -0.684% | 5m | ❌ |
| 2026-11-04 19:25:00 | ETC/USDT | STANDARD | 0.542 | LONG | 0.311% | -0.041% | 15m | ✅ |
| 2026-11-04 19:20:00 | ATOM/USDT | STANDARD | 0.544 | LONG | 0.477% | 0.000% | 10m | ✅ |
| 2026-11-04 19:10:00 | DOGE/USDT | STANDARD | 0.548 | LONG | 0.298% | -0.013% | 20m | ✅ |
| 2026-11-04 19:05:00 | ADA/USDT | OPHELIA | 0.639 | LONG | 0.558% | 0.000% | 10m | ✅ |
| 2026-11-04 18:30:00 | APT/USDT | OPHELIA | 0.635 | LONG | 0.519% | -0.031% | 20m | ✅ |
| 2026-11-03 01:25:00 | VET/USDT | STANDARD | 0.516 | LONG | 0.000% | -0.125% | 5m | ❌ |
| 2026-11-02 21:15:00 | VET/USDT | STANDARD | 0.492 | LONG | 0.071% | -0.408% | 25m | ❌ |
| 2026-10-31 21:05:00 | VET/USDT | STANDARD | 0.546 | LONG | 0.136% | -0.034% | 5m | ❌ |
| 2026-10-30 22:15:00 | VET/USDT | STANDARD | 0.533 | LONG | 0.000% | -0.435% | 10m | ❌ |
| 2026-10-30 01:40:00 | VET/USDT | OPHELIA | 0.573 | LONG | 0.615% | -0.034% | 30m | ✅ |
| 2026-10-30 00:35:00 | VET/USDT | STANDARD | 0.506 | LONG | 0.103% | -0.447% | 30m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.