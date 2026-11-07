# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-07T12:35:09.211422+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5682** (≥0.55 = predictor útil)
- Base rate test: 0.4211
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 50.00% | 2.00 | 2.00 |
| **STANDARD** | 0.600 | 50.00% | 50.00% | 2.00 | 4.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | LDO/USDT | 0.766 | OPHELIA | 01:35 | CONTINUACIÓN | ✅ |
| 2 | WIF/USDT | 0.756 | OPHELIA | 05:40 | CONTINUACIÓN | ❌ |
| 3 | DOGE/USDT | 0.701 | OPHELIA | 18:20 | CONTINUACIÓN | ❌ |
| 4 | ARB/USDT | 0.607 | OPHELIA | 18:15 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3513%

## 6. Modelo Temporal

- Trades/día promedio: 2.0
- Intervalo medio: 228.3 min
- Distribución: {'LONG': 4}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 1 |
| 05:00 | 1 |
| 18:00 | 2 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 4 | 25.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 0.9989071025144 |
| median_final | 0.9989003001509691 |
| p5_final | 0.9959941812539642 |
| p95_final | 1.0019450318149064 |
| mean_max_dd | 0.0016300898732373767 |
| p95_max_dd | 0.0035307379345944777 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 42 < 100
- ❌ Test insuficiente: 19 < 40
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-07 05:40:00 | WIF/USDT | OPHELIA | 0.756 | LONG | 0.062% | -0.369% | 5m | ❌ |
| 2026-11-07 01:35:00 | LDO/USDT | OPHELIA | 0.766 | LONG | 0.123% | 0.000% | 15m | ✅ |
| 2026-11-06 18:20:00 | DOGE/USDT | OPHELIA | 0.701 | LONG | 0.000% | -0.151% | 5m | ❌ |
| 2026-11-06 18:15:00 | ARB/USDT | OPHELIA | 0.607 | LONG | 0.090% | -0.251% | 10m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.