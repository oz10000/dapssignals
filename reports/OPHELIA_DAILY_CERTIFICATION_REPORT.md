# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-01T12:48:04.838193+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.3500** (≥0.55 = predictor útil)
- Base rate test: 0.2381
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 25.00% | 50.00% | 2.00 | 2.00 |
| **STANDARD** | 0.600 | 60.00% | 33.33% | 2.50 | 3.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | VET/USDT | 0.739 | OPHELIA | 05:40 | CONTINUACIÓN | ✅ |
| 2 | OP/USDT | 0.678 | OPHELIA | 01:20 | CONTINUACIÓN | ❌ |
| 3 | AVAX/USDT | 0.663 | OPHELIA | 01:40 | CONTINUACIÓN | ✅ |
| 4 | AAVE/USDT | 0.660 | OPHELIA | 23:35 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4985%

## 6. Modelo Temporal

- Trades/día promedio: 2.0
- Intervalo medio: 400.0 min
- Distribución: {'LONG': 4}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 2 |
| 05:00 | 1 |
| 23:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 4 | 50.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0056761448883955 |
| median_final | 1.0057428239133455 |
| p5_final | 0.9940309741825465 |
| p95_final | 1.0156164779770256 |
| mean_max_dd | 0.002186229227031676 |
| p95_max_dd | 0.004848141959588399 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 47 < 100
- ❌ Test insuficiente: 21 < 40
- ❌ AUC test bajo: 0.350 < 0.55
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-01 01:40:00 | AVAX/USDT | OPHELIA | 0.663 | LONG | 1.555% | -0.011% | 20m | ✅ |
| 2026-11-01 01:20:00 | OP/USDT | OPHELIA | 0.678 | LONG | 0.244% | -0.532% | 10m | ❌ |
| 2026-10-31 23:35:00 | AAVE/USDT | OPHELIA | 0.660 | LONG | 0.037% | -0.308% | 5m | ❌ |
| 2026-10-31 05:40:00 | VET/USDT | OPHELIA | 0.739 | LONG | 0.529% | -0.051% | 10m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.