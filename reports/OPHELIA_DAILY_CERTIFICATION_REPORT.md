# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-29T12:25:47.202243+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.3285** (≥0.55 = predictor útil)
- Base rate test: 0.2812
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 100.00% | 0.00% | 2.00 | 2.00 |
| **STANDARD** | 0.450 | 90.00% | 40.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | BTC/USDT | 0.702 | OPHELIA | 16:55 | CONTINUACIÓN | ✅ |
| 2 | AAVE/USDT | 0.701 | OPHELIA | 16:50 | CONTINUACIÓN | ✅ |
| 3 | AVAX/USDT | 0.601 | OPHELIA | 03:00 | CONTINUACIÓN | ❌ |
| 4 | SOL/USDT | 0.565 | OPHELIA | 02:00 | CONTINUACIÓN | ✅ |
| 5 | LINK/USDT | 0.545 | STANDARD | 16:50 | CONTINUACIÓN | ✅ |
| 6 | SEI/USDT | 0.543 | STANDARD | 18:00 | CONTINUACIÓN | ❌ |
| 7 | SUI/USDT | 0.542 | STANDARD | 18:05 | CONTINUACIÓN | ✅ |
| 8 | OP/USDT | 0.542 | STANDARD | 18:00 | CONTINUACIÓN | ❌ |
| 9 | DOT/USDT | 0.541 | STANDARD | 18:15 | CONTINUACIÓN | ❌ |
| 10 | VET/USDT | 0.540 | STANDARD | 05:55 | CONTINUACIÓN | ✅ |
| 11 | BTC/USDT | 0.533 | STANDARD | 01:50 | CONTINUACIÓN | ❌ |
| 12 | LTC/USDT | 0.529 | STANDARD | 06:20 | CONTINUACIÓN | ❌ |
| 13 | AAVE/USDT | 0.527 | STANDARD | 02:05 | CONTINUACIÓN | ✅ |
| 14 | ETC/USDT | 0.524 | STANDARD | 02:00 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3648%

## 6. Modelo Temporal

- Trades/día promedio: 7.0
- Intervalo medio: 81.0 min
- Distribución: {'LONG': 14}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 1 |
| 02:00 | 3 |
| 03:00 | 1 |
| 16:00 | 3 |
| 18:00 | 4 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 14 | 57.14% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0216524565337528 |
| median_final | 1.021637180105401 |
| p5_final | 1.003422513832625 |
| p95_final | 1.040706003286342 |
| mean_max_dd | 0.004612429012737036 |
| p95_max_dd | 0.009074919773221477 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 73 < 100
- ❌ Test insuficiente: 32 < 40
- ❌ AUC test bajo: 0.329 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 100.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-29 06:20:00 | LTC/USDT | STANDARD | 0.529 | LONG | 0.070% | -0.209% | 5m | ❌ |
| 2026-10-29 05:55:00 | VET/USDT | STANDARD | 0.540 | LONG | 0.525% | 0.000% | 10m | ✅ |
| 2026-10-29 03:00:00 | AVAX/USDT | OPHELIA | 0.601 | LONG | 0.183% | -0.217% | 10m | ❌ |
| 2026-10-29 02:05:00 | AAVE/USDT | STANDARD | 0.527 | LONG | 0.594% | -0.053% | 5m | ✅ |
| 2026-10-29 02:00:00 | SOL/USDT | OPHELIA | 0.565 | LONG | 0.359% | 0.000% | 10m | ✅ |
| 2026-10-29 02:00:00 | ETC/USDT | STANDARD | 0.524 | LONG | 0.511% | 0.000% | 10m | ✅ |
| 2026-10-29 01:50:00 | BTC/USDT | STANDARD | 0.533 | LONG | 0.036% | -0.084% | 5m | ❌ |
| 2026-10-28 18:15:00 | DOT/USDT | STANDARD | 0.541 | LONG | 0.126% | -0.389% | 5m | ❌ |
| 2026-10-28 18:05:00 | SUI/USDT | STANDARD | 0.542 | LONG | 0.685% | -0.127% | 10m | ✅ |
| 2026-10-28 18:00:00 | SEI/USDT | STANDARD | 0.543 | LONG | 0.685% | -0.352% | 30m | ❌ |
| 2026-10-28 18:00:00 | OP/USDT | STANDARD | 0.542 | LONG | 0.123% | -0.280% | 5m | ❌ |
| 2026-10-28 16:55:00 | BTC/USDT | OPHELIA | 0.702 | LONG | 0.270% | 0.000% | 5m | ✅ |
| 2026-10-28 16:50:00 | AAVE/USDT | OPHELIA | 0.701 | LONG | 0.631% | -0.029% | 5m | ✅ |
| 2026-10-28 16:50:00 | LINK/USDT | STANDARD | 0.545 | LONG | 1.532% | 0.000% | 10m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.