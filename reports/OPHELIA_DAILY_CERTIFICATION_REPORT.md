# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-20T15:01:03.621614+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5167** (≥0.55 = predictor útil)
- Base rate test: 0.1304
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 25.00% | 0.00% | 2.00 | 2.00 |
| **STANDARD** | 0.450 | 30.00% | 20.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | WIF/USDT | 0.892 | OPHELIA | 05:05 | CONTINUACIÓN | ❌ |
| 2 | ALGO/USDT | 0.883 | OPHELIA | 21:10 | CONTINUACIÓN | ❌ |
| 3 | CRV/USDT | 0.859 | OPHELIA | 02:40 | CONTINUACIÓN | ✅ |
| 4 | LINK/USDT | 0.785 | OPHELIA | 19:45 | CONTINUACIÓN | ❌ |
| 5 | ETH/USDT | 0.529 | STANDARD | 03:40 | CONTINUACIÓN | ✅ |
| 6 | VET/USDT | 0.516 | STANDARD | 02:35 | CONTINUACIÓN | ✅ |
| 7 | AAVE/USDT | 0.514 | STANDARD | 19:25 | CONTINUACIÓN | ✅ |
| 8 | SEI/USDT | 0.507 | STANDARD | 07:35 | CONTINUACIÓN | ❌ |
| 9 | BNB/USDT | 0.502 | STANDARD | 02:50 | CONTINUACIÓN | ❌ |
| 10 | DOT/USDT | 0.489 | STANDARD | 21:20 | CONTINUACIÓN | ❌ |
| 11 | DOGE/USDT | 0.485 | STANDARD | 21:15 | CONTINUACIÓN | ❌ |
| 12 | PEPE/USDT | 0.482 | STANDARD | 22:15 | CONTINUACIÓN | ❌ |
| 13 | ALGO/USDT | 0.474 | STANDARD | 19:35 | CONTINUACIÓN | ❌ |
| 14 | ATOM/USDT | 0.466 | STANDARD | 03:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3731%

## 6. Modelo Temporal

- Trades/día promedio: 7.0
- Intervalo medio: 56.2 min
- Distribución: {'LONG': 14}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 02:00 | 3 |
| 03:00 | 2 |
| 19:00 | 3 |
| 21:00 | 3 |
| 22:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 14 | 28.57% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0016070004438498 |
| median_final | 1.0011883454568156 |
| p5_final | 0.989462901776951 |
| p95_final | 1.015405462111218 |
| mean_max_dd | 0.006442449747843224 |
| p95_max_dd | 0.01180392889648004 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 51 < 100
- ❌ Test insuficiente: 23 < 40
- ❌ AUC test bajo: 0.517 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 25.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-20 07:35:00 | SEI/USDT | STANDARD | 0.507 | LONG | 0.239% | -0.133% | 10m | ❌ |
| 2026-11-20 05:05:00 | WIF/USDT | OPHELIA | 0.892 | LONG | 0.077% | -0.386% | 5m | ❌ |
| 2026-11-20 03:40:00 | ETH/USDT | STANDARD | 0.529 | LONG | 0.384% | 0.000% | 10m | ✅ |
| 2026-11-20 03:00:00 | ATOM/USDT | STANDARD | 0.466 | LONG | 0.079% | -0.237% | 5m | ❌ |
| 2026-11-20 02:50:00 | BNB/USDT | STANDARD | 0.502 | LONG | 0.021% | -0.194% | 5m | ❌ |
| 2026-11-20 02:40:00 | CRV/USDT | OPHELIA | 0.859 | LONG | 0.580% | 0.000% | 5m | ✅ |
| 2026-11-20 02:35:00 | VET/USDT | STANDARD | 0.516 | LONG | 0.642% | 0.000% | 15m | ✅ |
| 2026-11-19 22:15:00 | PEPE/USDT | STANDARD | 0.482 | LONG | 0.000% | -0.303% | 5m | ❌ |
| 2026-11-19 21:20:00 | DOT/USDT | STANDARD | 0.489 | LONG | 0.000% | -0.349% | 5m | ❌ |
| 2026-11-19 21:15:00 | DOGE/USDT | STANDARD | 0.485 | LONG | 0.069% | -0.291% | 10m | ❌ |
| 2026-11-19 21:10:00 | ALGO/USDT | OPHELIA | 0.883 | LONG | 0.000% | -0.338% | 15m | ❌ |
| 2026-11-19 19:45:00 | LINK/USDT | OPHELIA | 0.785 | LONG | 0.000% | -0.366% | 5m | ❌ |
| 2026-11-19 19:35:00 | ALGO/USDT | STANDARD | 0.474 | LONG | 0.000% | -0.130% | 5m | ❌ |
| 2026-11-19 19:25:00 | AAVE/USDT | STANDARD | 0.514 | LONG | 0.592% | -0.115% | 35m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.