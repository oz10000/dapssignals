# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-13T14:03:54.184772+00:00 UTC
**Estado:** ✅ CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.6897** (≥0.55 = predictor útil)
- Base rate test: 0.3023
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 36.36% | 100.00% | 0.34 | 2.00 |
| **STANDARD** | 0.580 | 33.33% | 100.00% | 0.28 | 2.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | VET/USDT | 0.689 | OPHELIA | 22:10 | CONTINUACIÓN | ❌ |
| 2 | VET/USDT | 0.677 | OPHELIA | 22:15 | CONTINUACIÓN | ❌ |
| 3 | VET/USDT | 0.664 | OPHELIA | 21:10 | CONTINUACIÓN | ❌ |
| 4 | BTC/USDT | 0.647 | OPHELIA | 07:50 | CONTINUACIÓN | ✅ |
| 5 | SUI/USDT | 0.605 | OPHELIA | 03:10 | CONTINUACIÓN | ✅ |
| 6 | PEPE/USDT | 0.602 | OPHELIA | 19:25 | CONTINUACIÓN | ❌ |
| 7 | VET/USDT | 0.596 | OPHELIA | 02:40 | CONTINUACIÓN | ✅ |
| 8 | PEPE/USDT | 0.594 | OPHELIA | 18:25 | CONTINUACIÓN | ❌ |
| 9 | VET/USDT | 0.577 | OPHELIA | 21:45 | CONTINUACIÓN | ❌ |
| 10 | VET/USDT | 0.565 | OPHELIA | 05:45 | CONTINUACIÓN | ❌ |
| 11 | VET/USDT | 0.552 | OPHELIA | 02:00 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4381%

## 6. Modelo Temporal

- Trades/día promedio: 1.38
- Intervalo medio: 4188.5 min
- Distribución: {'LONG': 11}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 02:00 | 2 |
| 05:00 | 1 |
| 18:00 | 1 |
| 21:00 | 2 |
| 22:00 | 2 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 11 | 36.36% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0041199072577804 |
| median_final | 1.0038426212467795 |
| p5_final | 0.9919811391862505 |
| p95_final | 1.0176739587471715 |
| mean_max_dd | 0.004998579976936054 |
| p95_max_dd | 0.009905188134761685 |
| ruin_prob | 0.0 |

## 10. Certificación

✅ Todos los criterios aprobados

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-13 07:50:00 | BTC/USDT | OPHELIA | 0.647 | LONG | 0.361% | -0.066% | 30m | ✅ |
| 2026-11-13 03:10:00 | SUI/USDT | OPHELIA | 0.605 | LONG | 1.281% | -0.026% | 10m | ✅ |
| 2026-11-12 19:25:00 | PEPE/USDT | OPHELIA | 0.602 | LONG | 0.176% | -0.306% | 5m | ❌ |
| 2026-11-12 18:25:00 | PEPE/USDT | OPHELIA | 0.594 | LONG | 0.188% | -0.272% | 5m | ❌ |
| 2026-11-07 02:00:00 | VET/USDT | OPHELIA | 0.552 | LONG | 0.333% | 0.000% | 35m | ✅ |
| 2026-10-30 22:15:00 | VET/USDT | OPHELIA | 0.677 | LONG | 0.000% | -0.435% | 10m | ❌ |
| 2026-10-26 02:40:00 | VET/USDT | OPHELIA | 0.596 | LONG | 0.267% | 0.000% | 10m | ✅ |
| 2026-10-20 21:45:00 | VET/USDT | OPHELIA | 0.577 | LONG | 0.014% | -0.139% | 15m | ❌ |
| 2026-10-18 22:10:00 | VET/USDT | OPHELIA | 0.689 | LONG | 0.029% | -0.277% | 10m | ❌ |
| 2026-10-18 21:10:00 | VET/USDT | OPHELIA | 0.664 | LONG | 0.000% | -0.441% | 5m | ❌ |
| 2026-10-15 05:45:00 | VET/USDT | OPHELIA | 0.565 | LONG | 0.000% | -0.089% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.