# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-20T11:02:41.074208+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.3968** (≥0.55 = predictor útil)
- Base rate test: 0.1250
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 66.67% | 33.33% | 1.50 | 1.50 |
| **STANDARD** | 0.550 | 50.00% | 16.67% | 3.00 | 3.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | DOT/USDT | 0.752 | OPHELIA | 20:15 | CONTINUACIÓN | ❌ |
| 2 | VET/USDT | 0.749 | OPHELIA | 23:00 | CONTINUACIÓN | ✅ |
| 3 | BNB/USDT | 0.691 | OPHELIA | 20:15 | CONTINUACIÓN | ✅ |
| 4 | ETH/USDT | 0.664 | OPHELIA | 00:50 | CONTINUACIÓN | ❌ |
| 5 | AAVE/USDT | 0.651 | OPHELIA | 00:45 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3691%

## 6. Modelo Temporal

- Trades/día promedio: 1.67
- Intervalo medio: 516.7 min
- Distribución: {'LONG': 5}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 2 |
| 20:00 | 2 |
| 23:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 5 | 40.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0005163631415268 |
| median_final | 1.0004743016623892 |
| p5_final | 0.9942731978711866 |
| p95_final | 1.0068608014078386 |
| mean_max_dd | 0.0025371313758907037 |
| p95_max_dd | 0.005106675051206861 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 54 < 100
- ❌ Test insuficiente: 24 < 40
- ❌ AUC test bajo: 0.397 < 0.55
- ❌ OPHELIA WR test 33.3% < 55%
- ❌ Degradación excesiva: 33.3%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-20 00:50:00 | ETH/USDT | OPHELIA | 0.664 | LONG | 0.089% | -0.119% | 15m | ❌ |
| 2026-10-20 00:45:00 | AAVE/USDT | OPHELIA | 0.651 | LONG | 0.177% | -0.407% | 20m | ❌ |
| 2026-10-19 20:15:00 | DOT/USDT | OPHELIA | 0.752 | LONG | 0.346% | -0.216% | 35m | ❌ |
| 2026-10-19 20:15:00 | BNB/USDT | OPHELIA | 0.691 | LONG | 0.123% | -0.014% | 15m | ✅ |
| 2026-10-18 23:00:00 | VET/USDT | OPHELIA | 0.749 | LONG | 0.334% | 0.000% | 10m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.