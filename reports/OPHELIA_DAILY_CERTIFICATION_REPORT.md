# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-03T13:45:58.691813+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.2500** (≥0.55 = predictor útil)
- Base rate test: 0.2381
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 0.00% | 0.00% | 1.50 | 2.00 |
| **STANDARD** | 0.450 | 20.00% | 20.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | PEPE/USDT | 0.846 | OPHELIA | 19:50 | CONTINUACIÓN | ❌ |
| 2 | CRV/USDT | 0.768 | OPHELIA | 18:50 | CONTINUACIÓN | ❌ |
| 3 | NEAR/USDT | 0.732 | OPHELIA | 01:45 | CONTINUACIÓN | ❌ |
| 4 | XRP/USDT | 0.730 | OPHELIA | 08:00 | CONTINUACIÓN | ❌ |
| 5 | PEPE/USDT | 0.545 | STANDARD | 22:25 | CONTINUACIÓN | ❌ |
| 6 | ARB/USDT | 0.536 | STANDARD | 01:25 | CONTINUACIÓN | ❌ |
| 7 | OP/USDT | 0.527 | STANDARD | 01:25 | CONTINUACIÓN | ❌ |
| 8 | BNB/USDT | 0.520 | STANDARD | 06:25 | CONTINUACIÓN | ❌ |
| 9 | ATOM/USDT | 0.488 | STANDARD | 02:20 | CONTINUACIÓN | ❌ |
| 10 | CRV/USDT | 0.477 | STANDARD | 06:10 | CONTINUACIÓN | ❌ |
| 11 | SEI/USDT | 0.468 | STANDARD | 18:55 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3866%

## 6. Modelo Temporal

- Trades/día promedio: 5.5
- Intervalo medio: 87.8 min
- Distribución: {'LONG': 11}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 3 |
| 06:00 | 2 |
| 18:00 | 2 |
| 19:00 | 1 |
| 22:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 11 | 0.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 0.9878694217701597 |
| median_final | 0.9879301956342337 |
| p5_final | 0.9850130067110304 |
| p95_final | 0.9905141715297316 |
| mean_max_dd | 0.011040510707354751 |
| p95_max_dd | 0.013801938698414081 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 48 < 100
- ❌ Test insuficiente: 21 < 40
- ❌ AUC test bajo: 0.250 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-03 08:00:00 | XRP/USDT | OPHELIA | 0.730 | LONG | 0.310% | -0.064% | 5m | ❌ |
| 2026-11-03 06:25:00 | BNB/USDT | STANDARD | 0.520 | LONG | 0.073% | -0.099% | 5m | ❌ |
| 2026-11-03 06:10:00 | CRV/USDT | STANDARD | 0.477 | LONG | 0.076% | -0.304% | 25m | ❌ |
| 2026-11-03 02:20:00 | ATOM/USDT | STANDARD | 0.488 | LONG | 0.139% | -0.208% | 5m | ❌ |
| 2026-11-03 01:45:00 | NEAR/USDT | OPHELIA | 0.732 | LONG | 0.026% | -0.234% | 5m | ❌ |
| 2026-11-03 01:25:00 | ARB/USDT | STANDARD | 0.536 | LONG | 0.000% | -0.124% | 5m | ❌ |
| 2026-11-03 01:25:00 | OP/USDT | STANDARD | 0.527 | LONG | 0.110% | -0.312% | 15m | ❌ |
| 2026-11-02 22:25:00 | PEPE/USDT | STANDARD | 0.545 | LONG | 0.054% | -0.455% | 10m | ❌ |
| 2026-11-02 19:50:00 | PEPE/USDT | OPHELIA | 0.846 | LONG | 0.104% | -0.316% | 5m | ❌ |
| 2026-11-02 18:55:00 | SEI/USDT | STANDARD | 0.468 | LONG | 0.021% | -0.318% | 5m | ❌ |
| 2026-11-02 18:50:00 | CRV/USDT | OPHELIA | 0.768 | LONG | 0.225% | -0.150% | 10m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.