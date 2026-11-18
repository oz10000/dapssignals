# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-18T15:15:43.358640+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.4671** (≥0.55 = predictor útil)
- Base rate test: 0.0952
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 0.00% | 0.19 | 1.50 |
| **STANDARD** | 0.550 | 44.44% | 16.67% | 0.29 | 3.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | VET/USDT | 0.592 | OPHELIA | 21:45 | CONTINUACIÓN | ❌ |
| 2 | LTC/USDT | 0.589 | OPHELIA | 19:40 | CONTINUACIÓN | ✅ |
| 3 | AAVE/USDT | 0.588 | OPHELIA | 06:55 | CONTINUACIÓN | ❌ |
| 4 | DOGE/USDT | 0.585 | OPHELIA | 00:30 | CONTINUACIÓN | ❌ |
| 5 | LINK/USDT | 0.580 | OPHELIA | 19:45 | CONTINUACIÓN | ✅ |
| 6 | VET/USDT | 0.572 | OPHELIA | 22:15 | CONTINUACIÓN | ❌ |
| 7 | VET/USDT | 0.557 | OPHELIA | 00:50 | CONTINUACIÓN | ❌ |
| 8 | VET/USDT | 0.555 | OPHELIA | 01:40 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3703%

## 6. Modelo Temporal

- Trades/día promedio: 1.6
- Intervalo medio: 5838.6 min
- Distribución: {'LONG': 8}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 2 |
| 01:00 | 1 |
| 19:00 | 2 |
| 21:00 | 1 |
| 22:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 8 | 37.50% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0064716649843417 |
| median_final | 1.0063275460863716 |
| p5_final | 0.9984148539753169 |
| p95_final | 1.0150216838482384 |
| mean_max_dd | 0.0018944714170307712 |
| p95_max_dd | 0.0037781072941164644 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 96 < 100
- ❌ AUC test bajo: 0.467 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 50.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-18 06:55:00 | AAVE/USDT | OPHELIA | 0.588 | LONG | 0.089% | -0.250% | 5m | ❌ |
| 2026-11-18 00:30:00 | DOGE/USDT | OPHELIA | 0.585 | LONG | 0.050% | -0.185% | 5m | ❌ |
| 2026-11-17 19:45:00 | LINK/USDT | OPHELIA | 0.580 | LONG | 0.487% | -0.011% | 15m | ✅ |
| 2026-11-17 19:40:00 | LTC/USDT | OPHELIA | 0.589 | LONG | 0.800% | -0.089% | 25m | ✅ |
| 2026-11-12 00:50:00 | VET/USDT | OPHELIA | 0.557 | LONG | 0.000% | -0.172% | 5m | ❌ |
| 2026-10-30 22:15:00 | VET/USDT | OPHELIA | 0.572 | LONG | 0.000% | -0.435% | 10m | ❌ |
| 2026-10-30 01:40:00 | VET/USDT | OPHELIA | 0.555 | LONG | 0.615% | -0.034% | 30m | ✅ |
| 2026-10-20 21:45:00 | VET/USDT | OPHELIA | 0.592 | LONG | 0.014% | -0.139% | 15m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.