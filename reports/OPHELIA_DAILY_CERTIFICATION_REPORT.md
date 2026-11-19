# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-19T15:22:35.368907+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5000** (≥0.55 = predictor útil)
- Base rate test: 0.4000
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 100.00% | 100.00% | 2.00 | 2.00 |
| **STANDARD** | 0.580 | 90.00% | 100.00% | 5.00 | 3.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | PEPE/USDT | 0.853 | OPHELIA | 20:15 | CONTINUACIÓN | ✅ |
| 2 | LDO/USDT | 0.851 | OPHELIA | 20:25 | CONTINUACIÓN | ✅ |
| 3 | SOL/USDT | 0.736 | OPHELIA | 00:35 | CONTINUACIÓN | ✅ |
| 4 | DOGE/USDT | 0.693 | OPHELIA | 00:35 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.0490%

## 6. Modelo Temporal

- Trades/día promedio: 2.0
- Intervalo medio: 130.0 min
- Distribución: {'LONG': 4}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 2 |
| 20:00 | 2 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 4 | 100.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.019620548974894 |
| median_final | 1.019603217627935 |
| p5_final | 1.0136260325559416 |
| p95_final | 1.0289078447616544 |
| mean_max_dd | 0.0 |
| p95_max_dd | 0.0 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 57 < 100
- ❌ Test insuficiente: 25 < 40
- ❌ AUC test bajo: 0.500 < 0.55

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-19 00:35:00 | SOL/USDT | OPHELIA | 0.736 | LONG | 0.787% | 0.000% | 10m | ✅ |
| 2026-11-19 00:35:00 | DOGE/USDT | OPHELIA | 0.693 | LONG | 0.580% | -0.051% | 10m | ✅ |
| 2026-11-18 20:25:00 | LDO/USDT | OPHELIA | 0.851 | LONG | 0.668% | -0.037% | 15m | ✅ |
| 2026-11-18 20:15:00 | PEPE/USDT | OPHELIA | 0.853 | LONG | 1.173% | -0.011% | 25m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.