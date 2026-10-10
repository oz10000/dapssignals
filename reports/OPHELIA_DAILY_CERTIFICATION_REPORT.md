# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-10T12:02:02.159011+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5263** (≥0.55 = predictor útil)
- Base rate test: 0.3214
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.600 | 0.00% | 33.33% | 1.00 | 1.50 |
| **STANDARD** | 0.500 | 50.00% | 44.44% | 3.00 | 4.50 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | OP/USDT | 0.800 | OPHELIA | 22:40 | CONTINUACIÓN | ❌ |
| 2 | APT/USDT | 0.749 | OPHELIA | 22:40 | CONTINUACIÓN | ✅ |
| 3 | UNI/USDT | 0.642 | OPHELIA | 03:20 | CONTINUACIÓN | ❌ |
| 4 | INJ/USDT | 0.641 | OPHELIA | 01:05 | CONTINUACIÓN | ❌ |
| 5 | DOGE/USDT | 0.599 | STANDARD | 21:15 | CONTINUACIÓN | ✅ |
| 6 | DOGE/USDT | 0.592 | STANDARD | 22:45 | CONTINUACIÓN | ❌ |
| 7 | CRV/USDT | 0.591 | STANDARD | 21:35 | CONTINUACIÓN | ✅ |
| 8 | VET/USDT | 0.588 | STANDARD | 23:50 | CONTINUACIÓN | ❌ |
| 9 | LDO/USDT | 0.576 | STANDARD | 22:35 | CONTINUACIÓN | ✅ |
| 10 | SEI/USDT | 0.573 | STANDARD | 21:05 | CONTINUACIÓN | ✅ |
| 11 | AVAX/USDT | 0.516 | STANDARD | 01:50 | CONTINUACIÓN | ✅ |
| 12 | BTC/USDT | 0.511 | STANDARD | 02:55 | CONTINUACIÓN | ❌ |
| 13 | NEAR/USDT | 0.508 | STANDARD | 01:05 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4539%

## 6. Modelo Temporal

- Trades/día promedio: 4.33
- Intervalo medio: 165.0 min
- Distribución: {'LONG': 13}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 3 |
| 02:00 | 1 |
| 21:00 | 3 |
| 22:00 | 4 |
| 23:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 13 | 53.85% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0172240707310225 |
| median_final | 1.0173665568734211 |
| p5_final | 0.9981125949803028 |
| p95_final | 1.035945258254579 |
| mean_max_dd | 0.005741137690929041 |
| p95_max_dd | 0.012120187448957567 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 65 < 100
- ❌ Test insuficiente: 28 < 40
- ❌ AUC test bajo: 0.526 < 0.55
- ❌ OPHELIA WR test 33.3% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-10 03:20:00 | UNI/USDT | OPHELIA | 0.642 | LONG | 0.053% | -0.240% | 5m | ❌ |
| 2026-10-10 02:55:00 | BTC/USDT | STANDARD | 0.511 | LONG | 0.000% | -0.074% | 5m | ❌ |
| 2026-10-10 01:50:00 | AVAX/USDT | STANDARD | 0.516 | LONG | 0.884% | -0.086% | 20m | ✅ |
| 2026-10-10 01:05:00 | INJ/USDT | OPHELIA | 0.641 | LONG | 0.043% | -0.128% | 5m | ❌ |
| 2026-10-10 01:05:00 | NEAR/USDT | STANDARD | 0.508 | LONG | 0.657% | -0.159% | 5m | ✅ |
| 2026-10-09 22:45:00 | DOGE/USDT | STANDARD | 0.592 | LONG | 0.070% | -0.174% | 15m | ❌ |
| 2026-10-09 22:40:00 | OP/USDT | OPHELIA | 0.800 | LONG | 0.904% | -0.555% | 5m | ❌ |
| 2026-10-09 22:40:00 | APT/USDT | OPHELIA | 0.749 | LONG | 0.965% | -0.145% | 10m | ✅ |
| 2026-10-09 22:35:00 | LDO/USDT | STANDARD | 0.576 | LONG | 1.122% | 0.000% | 20m | ✅ |
| 2026-10-09 21:35:00 | CRV/USDT | STANDARD | 0.591 | LONG | 0.657% | -0.137% | 10m | ✅ |
| 2026-10-09 21:15:00 | DOGE/USDT | STANDARD | 0.599 | LONG | 0.210% | -0.047% | 20m | ✅ |
| 2026-10-09 21:05:00 | SEI/USDT | STANDARD | 0.573 | LONG | 0.513% | 0.000% | 5m | ✅ |
| 2026-10-08 23:50:00 | VET/USDT | STANDARD | 0.588 | LONG | 0.193% | -0.386% | 10m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.