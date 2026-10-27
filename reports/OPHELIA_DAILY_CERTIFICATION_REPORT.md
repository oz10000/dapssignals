# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-27T11:44:05.803050+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **nan** (≥0.55 = predictor útil)
- Base rate test: 0.0000
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 0.00% | 0.00% | 0.00 | 0.00 |
| **STANDARD** | 0.450 | 60.00% | 0.00% | 5.00 | 1.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | DOGE/USDT | 0.967 | OPHELIA | 20:30 | CONTINUACIÓN | ✅ |
| 2 | ARB/USDT | 0.938 | OPHELIA | 20:45 | CONTINUACIÓN | ✅ |
| 3 | SOL/USDT | 0.590 | OPHELIA | 04:50 | CONTINUACIÓN | ❌ |
| 4 | ETH/USDT | 0.537 | STANDARD | 21:15 | CONTINUACIÓN | ❌ |
| 5 | CRV/USDT | 0.535 | STANDARD | 04:15 | CONTINUACIÓN | ❌ |
| 6 | APT/USDT | 0.489 | STANDARD | 20:50 | CONTINUACIÓN | ✅ |
| 7 | VET/USDT | 0.467 | STANDARD | 21:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.2318%

## 6. Modelo Temporal

- Trades/día promedio: 3.5
- Intervalo medio: 83.3 min
- Distribución: {'LONG': 7}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 04:00 | 2 |
| 20:00 | 3 |
| 21:00 | 2 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 7 | 42.86% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0057376082075495 |
| median_final | 1.0057166665818835 |
| p5_final | 0.9981445981078185 |
| p95_final | 1.0136025742947652 |
| mean_max_dd | 0.0017301065405815115 |
| p95_max_dd | 0.0034978295344849928 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 42 < 100
- ❌ Test insuficiente: 19 < 40
- ❌ OPHELIA WR test 0.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-27 04:50:00 | SOL/USDT | OPHELIA | 0.590 | LONG | 0.000% | -0.219% | 5m | ❌ |
| 2026-10-27 04:15:00 | CRV/USDT | STANDARD | 0.535 | LONG | 0.000% | -0.237% | 10m | ❌ |
| 2026-10-26 21:15:00 | ETH/USDT | STANDARD | 0.537 | LONG | 0.086% | -0.073% | 15m | ❌ |
| 2026-10-26 21:00:00 | VET/USDT | STANDARD | 0.467 | LONG | 0.000% | -0.212% | 5m | ❌ |
| 2026-10-26 20:50:00 | APT/USDT | STANDARD | 0.489 | LONG | 0.330% | -0.043% | 10m | ✅ |
| 2026-10-26 20:45:00 | ARB/USDT | OPHELIA | 0.938 | LONG | 0.636% | -0.077% | 15m | ✅ |
| 2026-10-26 20:30:00 | DOGE/USDT | OPHELIA | 0.967 | LONG | 0.258% | -0.026% | 25m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.