# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-11T13:42:17.219748+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.4902** (≥0.55 = predictor útil)
- Base rate test: 0.2609
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 50.00% | 2.00 | 2.00 |
| **STANDARD** | 0.550 | 60.00% | 40.00% | 5.00 | 2.50 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | PEPE/USDT | 0.784 | OPHELIA | 21:00 | CONTINUACIÓN | ❌ |
| 2 | VET/USDT | 0.672 | OPHELIA | 01:25 | CONTINUACIÓN | ✅ |
| 3 | UNI/USDT | 0.564 | OPHELIA | 07:20 | CONTINUACIÓN | ✅ |
| 4 | ALGO/USDT | 0.561 | OPHELIA | 04:20 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4550%

## 6. Modelo Temporal

- Trades/día promedio: 2.0
- Intervalo medio: 598.3 min
- Distribución: {'LONG': 4}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 1 |
| 04:00 | 1 |
| 07:00 | 1 |
| 21:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 4 | 50.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0024053030654938 |
| median_final | 1.002472183046386 |
| p5_final | 0.9927254840037336 |
| p95_final | 1.0130580964686513 |
| mean_max_dd | 0.003117211617888194 |
| p95_max_dd | 0.00750462911388806 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 53 < 100
- ❌ Test insuficiente: 23 < 40
- ❌ AUC test bajo: 0.490 < 0.55
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-11 07:20:00 | UNI/USDT | OPHELIA | 0.564 | LONG | 0.558% | 0.000% | 5m | ✅ |
| 2026-11-11 04:20:00 | ALGO/USDT | OPHELIA | 0.561 | LONG | 0.033% | -0.177% | 5m | ❌ |
| 2026-11-10 21:00:00 | PEPE/USDT | OPHELIA | 0.784 | LONG | 0.567% | -0.504% | 15m | ❌ |
| 2026-11-10 01:25:00 | VET/USDT | OPHELIA | 0.672 | LONG | 0.363% | 0.000% | 5m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.