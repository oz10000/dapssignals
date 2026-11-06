# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-06T14:23:15.611367+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5539** (≥0.55 = predictor útil)
- Base rate test: 0.2451
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 27.27% | 35.29% | 0.50 | 1.42 |
| **STANDARD** | 0.550 | 24.10% | 29.03% | 0.94 | 2.58 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | NEAR/USDT | 0.705 | OPHELIA | 21:00 | CONTINUACIÓN | ❌ |
| 2 | OP/USDT | 0.701 | OPHELIA | 22:55 | CONTINUACIÓN | ✅ |
| 3 | ETC/USDT | 0.631 | OPHELIA | 21:50 | CONTINUACIÓN | ❌ |
| 4 | AVAX/USDT | 0.630 | OPHELIA | 22:00 | CONTINUACIÓN | ❌ |
| 5 | WIF/USDT | 0.628 | OPHELIA | 22:00 | CONTINUACIÓN | ❌ |
| 6 | CRV/USDT | 0.625 | OPHELIA | 21:00 | CONTINUACIÓN | ✅ |
| 7 | BTC/USDT | 0.620 | OPHELIA | 02:45 | CONTINUACIÓN | ❌ |
| 8 | BTC/USDT | 0.618 | OPHELIA | 03:55 | CONTINUACIÓN | ✅ |
| 9 | BTC/USDT | 0.614 | OPHELIA | 06:20 | CONTINUACIÓN | ❌ |
| 10 | APT/USDT | 0.613 | OPHELIA | 21:15 | CONTINUACIÓN | ✅ |
| 11 | BTC/USDT | 0.608 | OPHELIA | 22:15 | CONTINUACIÓN | ❌ |
| 12 | UNI/USDT | 0.606 | OPHELIA | 21:00 | CONTINUACIÓN | ❌ |
| 13 | BTC/USDT | 0.606 | OPHELIA | 00:35 | CONTINUACIÓN | ✅ |
| 14 | BTC/USDT | 0.604 | OPHELIA | 19:10 | CONTINUACIÓN | ❌ |
| 15 | SOL/USDT | 0.597 | OPHELIA | 23:00 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3990%

## 6. Modelo Temporal

- Trades/día promedio: 1.69
- Intervalo medio: 20334.0 min
- Distribución: {'LONG': 59}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 02:00 | 6 |
| 05:00 | 5 |
| 21:00 | 8 |
| 22:00 | 5 |
| 23:00 | 6 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 59 | 30.51% |

## 8. Walk-Forward

|   window |   train_wr |   test_wr |   test_tpd |   auc_test |
|---------:|-----------:|----------:|-----------:|-----------:|
|        1 |   0.333333 |  0.5      |   0.666667 |     0.5021 |
|        2 |   0.333333 |  0.3      |   2        |     0.5037 |
|        3 |   0.387097 |  0.214286 |   2        |     0.6223 |
|        4 |   0.333333 |  0.4      |   0.625    |     0.5274 |
|        5 |   0.255814 |  0.352941 |   1.7      |     0.566  |

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.024111627601973 |
| median_final | 1.022892412832961 |
| p5_final | 0.9943761412141581 |
| p95_final | 1.0584618914156885 |
| mean_max_dd | 0.010179377130104333 |
| p95_max_dd | 0.01870170031467728 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ OPHELIA WR test 35.3% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-05 23:05:00 | ETC/USDT | OPHELIA | 0.558 | LONG | 0.430% | 0.000% | 20m | ✅ |
| 2026-11-04 02:30:00 | BTC/USDT | OPHELIA | 0.596 | LONG | 0.290% | 0.000% | 5m | ✅ |
| 2026-11-04 02:20:00 | ETH/USDT | OPHELIA | 0.555 | LONG | 0.018% | -0.130% | 5m | ❌ |
| 2026-11-03 07:00:00 | XRP/USDT | OPHELIA | 0.559 | LONG | 0.064% | -0.048% | 5m | ❌ |
| 2026-11-03 06:20:00 | ETH/USDT | OPHELIA | 0.566 | LONG | 0.224% | -0.033% | 15m | ✅ |
| 2026-11-01 12:00:00 | ETH/USDT | OPHELIA | 0.575 | LONG | 0.048% | -0.085% | 15m | ❌ |
| 2026-11-01 00:40:00 | BTC/USDT | OPHELIA | 0.586 | LONG | 0.000% | -0.081% | 5m | ❌ |
| 2026-10-31 03:20:00 | ATOM/USDT | OPHELIA | 0.554 | LONG | 0.000% | -0.066% | 10m | ❌ |
| 2026-10-30 22:00:00 | AVAX/USDT | OPHELIA | 0.630 | LONG | 0.162% | -0.150% | 5m | ❌ |
| 2026-10-30 21:15:00 | APT/USDT | OPHELIA | 0.613 | LONG | 0.536% | -0.031% | 5m | ✅ |
| 2026-10-29 23:35:00 | ADA/USDT | OPHELIA | 0.557 | LONG | 0.053% | -0.527% | 10m | ❌ |
| 2026-10-28 15:25:00 | BTC/USDT | OPHELIA | 0.562 | LONG | 0.223% | -0.261% | 5m | ❌ |
| 2026-10-28 00:25:00 | ETH/USDT | OPHELIA | 0.565 | LONG | 0.203% | -0.113% | 30m | ❌ |
| 2026-10-27 21:05:00 | ATOM/USDT | OPHELIA | 0.562 | LONG | 0.430% | 0.000% | 5m | ✅ |
| 2026-10-27 09:40:00 | BTC/USDT | OPHELIA | 0.566 | LONG | 0.190% | -0.024% | 10m | ✅ |
| 2026-10-26 12:40:00 | BTC/USDT | OPHELIA | 0.593 | LONG | 0.099% | -0.341% | 10m | ❌ |
| 2026-10-26 02:45:00 | BTC/USDT | OPHELIA | 0.620 | LONG | 0.010% | -0.071% | 5m | ❌ |
| 2026-10-25 09:55:00 | WIF/USDT | OPHELIA | 0.558 | LONG | 0.056% | -0.281% | 5m | ❌ |
| 2026-10-24 21:00:00 | UNI/USDT | OPHELIA | 0.606 | LONG | 0.058% | -0.131% | 5m | ❌ |
| 2026-10-24 15:45:00 | ETH/USDT | OPHELIA | 0.581 | LONG | 0.344% | -0.042% | 10m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.