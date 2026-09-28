# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-09-28T13:06:42.343823+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.1556** (≥0.55 = predictor útil)
- Base rate test: 0.3571
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 0.00% | 0.00% | 1.00 | 2.00 |
| **STANDARD** | 0.450 | 14.29% | 0.00% | 3.50 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | ALGO/USDT | 0.708 | OPHELIA | 05:25 | CONTINUACIÓN | ❌ |
| 2 | DOGE/USDT | 0.693 | OPHELIA | 18:20 | CONTINUACIÓN | ❌ |
| 3 | DOGE/USDT | 0.666 | OPHELIA | 07:20 | CONTINUACIÓN | ❌ |
| 4 | PEPE/USDT | 0.656 | OPHELIA | 18:20 | CONTINUACIÓN | ❌ |
| 5 | CRV/USDT | 0.540 | STANDARD | 07:30 | CONTINUACIÓN | ✅ |
| 6 | INJ/USDT | 0.527 | STANDARD | 21:20 | CONTINUACIÓN | ❌ |
| 7 | OP/USDT | 0.523 | STANDARD | 18:15 | CONTINUACIÓN | ❌ |
| 8 | LDO/USDT | 0.523 | STANDARD | 18:30 | CONTINUACIÓN | ❌ |
| 9 | LINK/USDT | 0.517 | STANDARD | 07:40 | CONTINUACIÓN | ✅ |
| 10 | VET/USDT | 0.505 | STANDARD | 03:10 | CONTINUACIÓN | ❌ |
| 11 | ATOM/USDT | 0.496 | STANDARD | 20:55 | CONTINUACIÓN | ❌ |
| 12 | AVAX/USDT | 0.495 | STANDARD | 07:45 | CONTINUACIÓN | ✅ |
| 13 | ALGO/USDT | 0.488 | STANDARD | 01:40 | CONTINUACIÓN | ❌ |
| 14 | ETC/USDT | 0.484 | STANDARD | 07:55 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.5905%

## 6. Modelo Temporal

- Trades/día promedio: 7.0
- Intervalo medio: 143.8 min
- Distribución: {'LONG': 14}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 03:00 | 1 |
| 07:00 | 5 |
| 18:00 | 4 |
| 20:00 | 1 |
| 21:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 14 | 28.57% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.005715328906972 |
| median_final | 1.005390132660127 |
| p5_final | 0.9876255031569761 |
| p95_final | 1.025717252914753 |
| mean_max_dd | 0.008067466781600845 |
| p95_max_dd | 0.015174951092971031 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 31 < 100
- ❌ Test insuficiente: 14 < 40
- ❌ AUC test bajo: 0.156 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-09-28 07:55:00 | ETC/USDT | STANDARD | 0.484 | LONG | 0.526% | -0.120% | 40m | ✅ |
| 2026-09-28 07:45:00 | AVAX/USDT | STANDARD | 0.495 | LONG | 0.542% | -0.152% | 20m | ✅ |
| 2026-09-28 07:40:00 | LINK/USDT | STANDARD | 0.517 | LONG | 0.741% | -0.101% | 20m | ✅ |
| 2026-09-28 07:30:00 | CRV/USDT | STANDARD | 0.540 | LONG | 0.939% | 0.000% | 10m | ✅ |
| 2026-09-28 07:20:00 | DOGE/USDT | OPHELIA | 0.666 | LONG | 0.097% | -0.183% | 5m | ❌ |
| 2026-09-28 05:25:00 | ALGO/USDT | OPHELIA | 0.708 | LONG | 0.110% | -0.625% | 5m | ❌ |
| 2026-09-28 01:40:00 | ALGO/USDT | STANDARD | 0.488 | LONG | 0.000% | -0.399% | 5m | ❌ |
| 2026-09-27 21:20:00 | INJ/USDT | STANDARD | 0.527 | LONG | 0.102% | -0.243% | 5m | ❌ |
| 2026-09-27 20:55:00 | ATOM/USDT | STANDARD | 0.496 | LONG | 0.000% | -0.318% | 5m | ❌ |
| 2026-09-27 18:30:00 | LDO/USDT | STANDARD | 0.523 | LONG | 0.000% | -0.572% | 5m | ❌ |
| 2026-09-27 18:20:00 | DOGE/USDT | OPHELIA | 0.693 | LONG | 0.092% | -0.257% | 5m | ❌ |
| 2026-09-27 18:20:00 | PEPE/USDT | OPHELIA | 0.656 | LONG | 0.137% | -0.205% | 5m | ❌ |
| 2026-09-27 18:15:00 | OP/USDT | STANDARD | 0.523 | LONG | 0.211% | -0.218% | 5m | ❌ |
| 2026-09-27 03:10:00 | VET/USDT | STANDARD | 0.505 | LONG | 0.109% | -0.109% | 10m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.