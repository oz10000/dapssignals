# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-21T14:20:27.245043+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5792** (≥0.55 = predictor útil)
- Base rate test: 0.4333
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 25.00% | 0.00% | 2.00 | 2.00 |
| **STANDARD** | 0.450 | 40.00% | 40.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | ARB/USDT | 0.904 | OPHELIA | 03:45 | CONTINUACIÓN | ❌ |
| 2 | WIF/USDT | 0.887 | OPHELIA | 03:40 | CONTINUACIÓN | ❌ |
| 3 | CRV/USDT | 0.636 | OPHELIA | 18:40 | CONTINUACIÓN | ❌ |
| 4 | DOGE/USDT | 0.603 | OPHELIA | 18:40 | CONTINUACIÓN | ❌ |
| 5 | WIF/USDT | 0.547 | STANDARD | 18:40 | CONTINUACIÓN | ❌ |
| 6 | AAVE/USDT | 0.535 | STANDARD | 18:40 | CONTINUACIÓN | ❌ |
| 7 | ARB/USDT | 0.531 | STANDARD | 20:25 | CONTINUACIÓN | ❌ |
| 8 | XRP/USDT | 0.528 | STANDARD | 19:40 | CONTINUACIÓN | ❌ |
| 9 | NEAR/USDT | 0.524 | STANDARD | 04:40 | CONTINUACIÓN | ❌ |
| 10 | NEAR/USDT | 0.523 | STANDARD | 19:40 | CONTINUACIÓN | ❌ |
| 11 | ADA/USDT | 0.513 | STANDARD | 03:40 | CONTINUACIÓN | ✅ |
| 12 | ALGO/USDT | 0.500 | STANDARD | 03:40 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.7569%

## 6. Modelo Temporal

- Trades/día promedio: 6.0
- Intervalo medio: 120.0 min
- Distribución: {'LONG': 12}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 03:00 | 4 |
| 04:00 | 1 |
| 18:00 | 4 |
| 19:00 | 2 |
| 20:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 12 | 16.67% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 0.9851839204525485 |
| median_final | 0.9844979862144263 |
| p5_final | 0.9646695619639729 |
| p95_final | 1.0086111056133564 |
| mean_max_dd | 0.020635579816288715 |
| p95_max_dd | 0.03322213372530025 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 67 < 100
- ❌ Test insuficiente: 30 < 40
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 25.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-21 04:40:00 | NEAR/USDT | STANDARD | 0.524 | LONG | 0.075% | -0.671% | 5m | ❌ |
| 2026-11-21 03:45:00 | ARB/USDT | OPHELIA | 0.904 | LONG | 0.622% | -0.485% | 15m | ❌ |
| 2026-11-21 03:40:00 | WIF/USDT | OPHELIA | 0.887 | LONG | 1.723% | -0.861% | 65m | ❌ |
| 2026-11-21 03:40:00 | ADA/USDT | STANDARD | 0.513 | LONG | 1.440% | -0.216% | 5m | ✅ |
| 2026-11-21 03:40:00 | ALGO/USDT | STANDARD | 0.500 | LONG | 1.635% | 0.000% | 5m | ✅ |
| 2026-11-20 20:25:00 | ARB/USDT | STANDARD | 0.531 | LONG | 0.156% | -0.278% | 15m | ❌ |
| 2026-11-20 19:40:00 | XRP/USDT | STANDARD | 0.528 | LONG | 0.011% | -0.590% | 5m | ❌ |
| 2026-11-20 19:40:00 | NEAR/USDT | STANDARD | 0.523 | LONG | 0.000% | -0.417% | 5m | ❌ |
| 2026-11-20 18:40:00 | CRV/USDT | OPHELIA | 0.636 | LONG | 0.000% | -0.393% | 5m | ❌ |
| 2026-11-20 18:40:00 | DOGE/USDT | OPHELIA | 0.603 | LONG | 0.037% | -0.536% | 5m | ❌ |
| 2026-11-20 18:40:00 | WIF/USDT | STANDARD | 0.547 | LONG | 0.000% | -0.576% | 5m | ❌ |
| 2026-11-20 18:40:00 | AAVE/USDT | STANDARD | 0.535 | LONG | 0.000% | -0.573% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.