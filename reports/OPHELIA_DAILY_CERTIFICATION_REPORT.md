# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-17T10:16:40.279312+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.3810** (≥0.55 = predictor útil)
- Base rate test: 0.0870
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 75.00% | 0.00% | 1.33 | 2.00 |
| **STANDARD** | 0.450 | 50.00% | 0.00% | 2.67 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | LTC/USDT | 0.840 | OPHELIA | 00:25 | CONTINUACIÓN | ✅ |
| 2 | ETH/USDT | 0.790 | OPHELIA | 04:00 | CONTINUACIÓN | ❌ |
| 3 | LTC/USDT | 0.777 | OPHELIA | 16:55 | REVERSIÓN | ❌ |
| 4 | SEI/USDT | 0.754 | OPHELIA | 20:30 | CONTINUACIÓN | ✅ |
| 5 | OP/USDT | 0.497 | STANDARD | 00:35 | CONTINUACIÓN | ❌ |
| 6 | AAVE/USDT | 0.490 | STANDARD | 00:30 | CONTINUACIÓN | ✅ |
| 7 | NEAR/USDT | 0.482 | STANDARD | 19:30 | CONTINUACIÓN | ✅ |
| 8 | DOT/USDT | 0.480 | STANDARD | 20:15 | CONTINUACIÓN | ❌ |
| 9 | ETC/USDT | 0.468 | STANDARD | 00:35 | CONTINUACIÓN | ❌ |
| 10 | APT/USDT | 0.464 | STANDARD | 20:20 | CONTINUACIÓN | ❌ |
| 11 | UNI/USDT | 0.458 | STANDARD | 16:10 | CONTINUACIÓN | ❌ |
| 12 | WIF/USDT | 0.458 | STANDARD | 21:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4362%

## 6. Modelo Temporal

- Trades/día promedio: 6.0
- Intervalo medio: 71.0 min
- Distribución: {'LONG': 12}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 4 |
| 16:00 | 2 |
| 19:00 | 1 |
| 20:00 | 3 |
| 21:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 11 | 36.36% |
| REVERSIÓN | 1 | 0.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0028671934621154 |
| median_final | 1.0023983256455735 |
| p5_final | 0.989903341795078 |
| p95_final | 1.0174312709757924 |
| mean_max_dd | 0.006153551466857381 |
| p95_max_dd | 0.011896360674459885 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 51 < 100
- ❌ Test insuficiente: 23 < 40
- ❌ AUC test bajo: 0.381 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 75.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-17 04:00:00 | ETH/USDT | OPHELIA | 0.790 | LONG | 0.016% | -0.047% | 5m | ❌ |
| 2026-10-17 00:35:00 | OP/USDT | STANDARD | 0.497 | LONG | 0.472% | -0.279% | 10m | ❌ |
| 2026-10-17 00:35:00 | ETC/USDT | STANDARD | 0.468 | LONG | 0.063% | -0.125% | 10m | ❌ |
| 2026-10-17 00:30:00 | AAVE/USDT | STANDARD | 0.490 | LONG | 0.244% | -0.051% | 10m | ✅ |
| 2026-10-17 00:25:00 | LTC/USDT | OPHELIA | 0.840 | LONG | 0.217% | 0.000% | 5m | ✅ |
| 2026-10-16 21:00:00 | WIF/USDT | STANDARD | 0.458 | LONG | 0.196% | -0.098% | 15m | ❌ |
| 2026-10-16 20:30:00 | SEI/USDT | OPHELIA | 0.754 | LONG | 0.368% | 0.000% | 15m | ✅ |
| 2026-10-16 20:20:00 | APT/USDT | STANDARD | 0.464 | LONG | 0.000% | -0.178% | 5m | ❌ |
| 2026-10-16 20:15:00 | DOT/USDT | STANDARD | 0.480 | LONG | 0.051% | -0.273% | 5m | ❌ |
| 2026-10-16 19:30:00 | NEAR/USDT | STANDARD | 0.482 | LONG | 1.144% | -0.099% | 30m | ✅ |
| 2026-10-16 16:55:00 | LTC/USDT | OPHELIA | 0.777 | LONG | 0.067% | -0.151% | 5m | ❌ |
| 2026-10-16 16:10:00 | UNI/USDT | STANDARD | 0.458 | LONG | 0.205% | -0.629% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.