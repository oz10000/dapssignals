# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-18T10:33:42.050744+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.6282** (≥0.55 = predictor útil)
- Base rate test: 0.2041
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 25.00% | 50.00% | 0.12 | 2.00 |
| **STANDARD** | 0.550 | 20.00% | 60.00% | 0.16 | 2.50 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | WIF/USDT | 0.566 | OPHELIA | 21:05 | CONTINUACIÓN | ✅ |
| 2 | ALGO/USDT | 0.564 | OPHELIA | 00:30 | CONTINUACIÓN | ❌ |
| 3 | VET/USDT | 0.559 | OPHELIA | 01:20 | CONTINUACIÓN | ❌ |
| 4 | VET/USDT | 0.559 | OPHELIA | 05:45 | CONTINUACIÓN | ❌ |
| 5 | ALGO/USDT | 0.556 | OPHELIA | 16:40 | CONTINUACIÓN | ✅ |
| 6 | LTC/USDT | 0.553 | OPHELIA | 04:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.2356%

## 6. Modelo Temporal

- Trades/día promedio: 1.5
- Intervalo medio: 3488.0 min
- Distribución: {'LONG': 6}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 1 |
| 01:00 | 1 |
| 05:00 | 1 |
| 16:00 | 1 |
| 21:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 6 | 33.33% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0008666726173665 |
| median_final | 1.000791904954212 |
| p5_final | 0.9962268655189092 |
| p95_final | 1.0059072092588057 |
| mean_max_dd | 0.0017964402792069315 |
| p95_max_dd | 0.0033968512714126747 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-18 04:00:00 | LTC/USDT | OPHELIA | 0.553 | LONG | 0.068% | -0.220% | 15m | ❌ |
| 2026-10-18 00:30:00 | ALGO/USDT | OPHELIA | 0.564 | LONG | 0.000% | -0.161% | 5m | ❌ |
| 2026-10-17 21:05:00 | WIF/USDT | OPHELIA | 0.566 | LONG | 0.252% | 0.000% | 10m | ✅ |
| 2026-10-17 16:40:00 | ALGO/USDT | OPHELIA | 0.556 | LONG | 0.277% | 0.000% | 10m | ✅ |
| 2026-10-07 05:45:00 | VET/USDT | OPHELIA | 0.559 | LONG | 0.000% | -0.241% | 5m | ❌ |
| 2026-10-06 01:20:00 | VET/USDT | OPHELIA | 0.559 | LONG | 0.920% | -0.138% | 15m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.