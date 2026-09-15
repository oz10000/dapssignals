# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-09-15T11:15:53.595545+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.3765** (≥0.55 = predictor útil)
- Base rate test: 0.2273
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 33.33% | 0.00% | 1.50 | 2.00 |
| **STANDARD** | 0.520 | 33.33% | 25.00% | 3.00 | 4.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | SEI/USDT | 0.825 | OPHELIA | 17:20 | CONTINUACIÓN | ✅ |
| 2 | SUI/USDT | 0.786 | OPHELIA | 05:55 | CONTINUACIÓN | ❌ |
| 3 | PEPE/USDT | 0.778 | OPHELIA | 04:25 | CONTINUACIÓN | ❌ |
| 4 | ADA/USDT | 0.748 | OPHELIA | 17:20 | CONTINUACIÓN | ❌ |
| 5 | VET/USDT | 0.720 | OPHELIA | 23:10 | CONTINUACIÓN | ❌ |
| 6 | LINK/USDT | 0.549 | STANDARD | 03:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3991%

## 6. Modelo Temporal

- Trades/día promedio: 2.0
- Intervalo medio: 461.2 min
- Distribución: {'LONG': 6}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 03:00 | 1 |
| 04:00 | 1 |
| 05:00 | 1 |
| 17:00 | 2 |
| 23:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 6 | 16.67% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 0.9959525705953741 |
| median_final | 0.9958229192340279 |
| p5_final | 0.9910365482884933 |
| p95_final | 1.0035832112104004 |
| mean_max_dd | 0.005054428657812307 |
| p95_max_dd | 0.007629715440563319 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 49 < 100
- ❌ Test insuficiente: 22 < 40
- ❌ AUC test bajo: 0.377 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 33.3%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-09-15 05:55:00 | SUI/USDT | OPHELIA | 0.786 | LONG | 0.014% | -0.141% | 5m | ❌ |
| 2026-09-15 04:25:00 | PEPE/USDT | OPHELIA | 0.778 | LONG | 0.000% | -0.408% | 5m | ❌ |
| 2026-09-15 03:00:00 | LINK/USDT | STANDARD | 0.549 | LONG | 0.000% | -0.243% | 5m | ❌ |
| 2026-09-14 17:20:00 | SEI/USDT | OPHELIA | 0.825 | LONG | 0.309% | -0.022% | 5m | ✅ |
| 2026-09-14 17:20:00 | ADA/USDT | OPHELIA | 0.748 | LONG | 0.046% | -0.371% | 5m | ❌ |
| 2026-09-13 23:10:00 | VET/USDT | OPHELIA | 0.720 | LONG | 0.000% | -0.253% | 10m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.