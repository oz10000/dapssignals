# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-04T13:54:09.445485+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.4872** (≥0.55 = predictor útil)
- Base rate test: 0.4800
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 50.00% | 2.00 | 2.00 |
| **STANDARD** | 0.450 | 40.00% | 60.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | BTC/USDT | 0.735 | OPHELIA | 02:30 | CONTINUACIÓN | ✅ |
| 2 | BNB/USDT | 0.702 | OPHELIA | 20:25 | CONTINUACIÓN | ❌ |
| 3 | ETC/USDT | 0.688 | OPHELIA | 02:20 | CONTINUACIÓN | ❌ |
| 4 | PEPE/USDT | 0.664 | OPHELIA | 19:55 | CONTINUACIÓN | ❌ |
| 5 | AVAX/USDT | 0.545 | STANDARD | 20:30 | CONTINUACIÓN | ❌ |
| 6 | APT/USDT | 0.544 | STANDARD | 20:30 | CONTINUACIÓN | ❌ |
| 7 | ARB/USDT | 0.534 | STANDARD | 02:10 | CONTINUACIÓN | ✅ |
| 8 | BTC/USDT | 0.528 | STANDARD | 01:10 | CONTINUACIÓN | ❌ |
| 9 | SEI/USDT | 0.526 | STANDARD | 18:20 | CONTINUACIÓN | ❌ |
| 10 | LTC/USDT | 0.520 | STANDARD | 01:10 | CONTINUACIÓN | ❌ |
| 11 | LDO/USDT | 0.517 | STANDARD | 01:00 | CONTINUACIÓN | ❌ |
| 12 | SUI/USDT | 0.513 | STANDARD | 02:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.5153%

## 6. Modelo Temporal

- Trades/día promedio: 6.0
- Intervalo medio: 54.4 min
- Distribución: {'LONG': 12}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 3 |
| 02:00 | 4 |
| 18:00 | 1 |
| 19:00 | 1 |
| 20:00 | 3 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 12 | 16.67% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0002679885379753 |
| median_final | 0.9989085717578153 |
| p5_final | 0.9854691836165183 |
| p95_final | 1.0198476490094917 |
| mean_max_dd | 0.00819523880216407 |
| p95_max_dd | 0.013775103993766954 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 58 < 100
- ❌ Test insuficiente: 25 < 40
- ❌ AUC test bajo: 0.487 < 0.55
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-04 02:30:00 | BTC/USDT | OPHELIA | 0.735 | LONG | 0.299% | 0.000% | 5m | ✅ |
| 2026-11-04 02:20:00 | ETC/USDT | OPHELIA | 0.688 | LONG | 0.000% | -0.171% | 5m | ❌ |
| 2026-11-04 02:10:00 | ARB/USDT | STANDARD | 0.534 | LONG | 1.289% | -0.121% | 25m | ✅ |
| 2026-11-04 02:00:00 | SUI/USDT | STANDARD | 0.513 | LONG | 0.384% | -0.237% | 30m | ❌ |
| 2026-11-04 01:10:00 | BTC/USDT | STANDARD | 0.528 | LONG | 0.043% | -0.307% | 10m | ❌ |
| 2026-11-04 01:10:00 | LTC/USDT | STANDARD | 0.520 | LONG | 0.094% | -0.543% | 10m | ❌ |
| 2026-11-04 01:00:00 | LDO/USDT | STANDARD | 0.517 | LONG | 0.183% | -0.305% | 5m | ❌ |
| 2026-11-03 20:30:00 | AVAX/USDT | STANDARD | 0.545 | LONG | 0.163% | -0.338% | 5m | ❌ |
| 2026-11-03 20:30:00 | APT/USDT | STANDARD | 0.544 | LONG | 0.240% | -0.368% | 5m | ❌ |
| 2026-11-03 20:25:00 | BNB/USDT | OPHELIA | 0.702 | LONG | 0.148% | -0.047% | 10m | ❌ |
| 2026-11-03 19:55:00 | PEPE/USDT | OPHELIA | 0.664 | LONG | 0.124% | -0.492% | 5m | ❌ |
| 2026-11-03 18:20:00 | SEI/USDT | STANDARD | 0.526 | LONG | 0.000% | -0.208% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.