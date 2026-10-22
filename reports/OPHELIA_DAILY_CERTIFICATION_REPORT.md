# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-22T11:17:49.381565+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **1.0000** (≥0.55 = predictor útil)
- Base rate test: 0.0833
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 33.33% | 50.00% | 1.50 | 1.00 |
| **STANDARD** | 0.450 | 25.00% | 50.00% | 2.00 | 1.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | CRV/USDT | 0.883 | OPHELIA | 18:35 | CONTINUACIÓN | ❌ |
| 2 | ARB/USDT | 0.843 | OPHELIA | 22:00 | CONTINUACIÓN | ✅ |
| 3 | VET/USDT | 0.653 | OPHELIA | 23:00 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4429%

## 6. Modelo Temporal

- Trades/día promedio: 1.5
- Intervalo medio: 690.0 min
- Distribución: {'LONG': 3}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 18:00 | 1 |
| 22:00 | 1 |
| 23:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 3 | 33.33% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.003871068076155 |
| median_final | 1.0038556258604474 |
| p5_final | 0.9955498605392493 |
| p95_final | 1.0122306852876517 |
| mean_max_dd | 0.001810588192053502 |
| p95_max_dd | 0.003461764833152726 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 25 < 100
- ❌ Test insuficiente: 12 < 40
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-21 22:00:00 | ARB/USDT | OPHELIA | 0.843 | LONG | 1.240% | 0.000% | 10m | ✅ |
| 2026-10-21 18:35:00 | CRV/USDT | OPHELIA | 0.883 | LONG | 0.025% | -0.351% | 5m | ❌ |
| 2026-10-20 23:00:00 | VET/USDT | OPHELIA | 0.653 | LONG | 0.000% | -0.453% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.