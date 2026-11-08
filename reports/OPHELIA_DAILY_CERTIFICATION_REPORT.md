# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-08T12:53:37.858427+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5397** (≥0.55 = predictor útil)
- Base rate test: 0.1250
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 0.00% | 1.00 | 2.00 |
| **STANDARD** | 0.450 | 20.00% | 0.00% | 2.50 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | AVAX/USDT | 0.757 | OPHELIA | 20:30 | CONTINUACIÓN | ✅ |
| 2 | DOGE/USDT | 0.734 | OPHELIA | 20:45 | CONTINUACIÓN | ❌ |
| 3 | SOL/USDT | 0.734 | OPHELIA | 02:25 | CONTINUACIÓN | ❌ |
| 4 | SUI/USDT | 0.725 | OPHELIA | 04:35 | CONTINUACIÓN | ❌ |
| 5 | LDO/USDT | 0.509 | STANDARD | 19:25 | CONTINUACIÓN | ❌ |
| 6 | INJ/USDT | 0.507 | STANDARD | 04:40 | CONTINUACIÓN | ✅ |
| 7 | UNI/USDT | 0.461 | STANDARD | 18:55 | CONTINUACIÓN | ❌ |
| 8 | INJ/USDT | 0.460 | STANDARD | 23:25 | CONTINUACIÓN | ❌ |
| 9 | VET/USDT | 0.458 | STANDARD | 00:15 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3404%

## 6. Modelo Temporal

- Trades/día promedio: 4.5
- Intervalo medio: 73.1 min
- Distribución: {'LONG': 9}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 04:00 | 2 |
| 18:00 | 1 |
| 19:00 | 1 |
| 20:00 | 2 |
| 23:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 9 | 22.22% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 0.9993682523645857 |
| median_final | 0.9991282423145628 |
| p5_final | 0.9940125925316452 |
| p95_final | 1.0057176414335922 |
| mean_max_dd | 0.0031791833155729973 |
| p95_max_dd | 0.005709483677547371 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 53 < 100
- ❌ Test insuficiente: 24 < 40
- ❌ AUC test bajo: 0.540 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 50.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-08 04:40:00 | INJ/USDT | STANDARD | 0.507 | LONG | 0.356% | 0.000% | 5m | ✅ |
| 2026-11-08 04:35:00 | SUI/USDT | OPHELIA | 0.725 | LONG | 0.035% | -0.047% | 5m | ❌ |
| 2026-11-08 02:25:00 | SOL/USDT | OPHELIA | 0.734 | LONG | 0.034% | -0.078% | 5m | ❌ |
| 2026-11-08 00:15:00 | VET/USDT | STANDARD | 0.458 | LONG | 0.000% | -0.284% | 5m | ❌ |
| 2026-11-07 23:25:00 | INJ/USDT | STANDARD | 0.460 | LONG | 0.244% | -0.378% | 5m | ❌ |
| 2026-11-07 20:45:00 | DOGE/USDT | OPHELIA | 0.734 | LONG | 0.070% | -0.070% | 15m | ❌ |
| 2026-11-07 20:30:00 | AVAX/USDT | OPHELIA | 0.757 | LONG | 0.183% | -0.024% | 10m | ✅ |
| 2026-11-07 19:25:00 | LDO/USDT | STANDARD | 0.509 | LONG | 0.185% | -0.092% | 35m | ❌ |
| 2026-11-07 18:55:00 | UNI/USDT | STANDARD | 0.461 | LONG | 0.169% | -0.239% | 15m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.