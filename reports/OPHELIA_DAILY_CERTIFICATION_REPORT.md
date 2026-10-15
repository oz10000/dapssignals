# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-15T10:59:27.843409+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.6190** (≥0.55 = predictor útil)
- Base rate test: 0.1765
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 0.00% | 1.33 | 2.00 |
| **STANDARD** | 0.450 | 28.57% | 0.00% | 2.33 | 3.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | AAVE/USDT | 0.887 | OPHELIA | 01:25 | CONTINUACIÓN | ❌ |
| 2 | VET/USDT | 0.851 | OPHELIA | 05:05 | CONTINUACIÓN | ✅ |
| 3 | BNB/USDT | 0.777 | OPHELIA | 18:45 | CONTINUACIÓN | ❌ |
| 4 | CRV/USDT | 0.732 | OPHELIA | 01:15 | CONTINUACIÓN | ✅ |
| 5 | AAVE/USDT | 0.519 | STANDARD | 20:10 | CONTINUACIÓN | ❌ |
| 6 | APT/USDT | 0.491 | STANDARD | 17:15 | CONTINUACIÓN | ❌ |
| 7 | SUI/USDT | 0.481 | STANDARD | 04:40 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4209%

## 6. Modelo Temporal

- Trades/día promedio: 3.5
- Intervalo medio: 235.8 min
- Distribución: {'LONG': 7}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 2 |
| 05:00 | 1 |
| 17:00 | 1 |
| 18:00 | 1 |
| 20:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 7 | 28.57% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0040741764559569 |
| median_final | 1.0030876492288514 |
| p5_final | 0.9904498041822223 |
| p95_final | 1.0228415607265857 |
| mean_max_dd | 0.004790993979843591 |
| p95_max_dd | 0.008855088439395083 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 38 < 100
- ❌ Test insuficiente: 17 < 40
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 50.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-15 04:40:00 | SUI/USDT | STANDARD | 0.481 | LONG | 0.000% | -0.454% | 5m | ❌ |
| 2026-10-15 01:25:00 | AAVE/USDT | OPHELIA | 0.887 | LONG | 0.593% | -0.244% | 40m | ❌ |
| 2026-10-15 01:15:00 | CRV/USDT | OPHELIA | 0.732 | LONG | 2.594% | -0.183% | 10m | ✅ |
| 2026-10-14 20:10:00 | AAVE/USDT | STANDARD | 0.519 | LONG | 0.000% | -0.233% | 5m | ❌ |
| 2026-10-14 18:45:00 | BNB/USDT | OPHELIA | 0.777 | LONG | 0.000% | -0.096% | 5m | ❌ |
| 2026-10-14 17:15:00 | APT/USDT | STANDARD | 0.491 | LONG | 0.246% | -0.344% | 10m | ❌ |
| 2026-10-14 05:05:00 | VET/USDT | OPHELIA | 0.851 | LONG | 0.164% | 0.000% | 10m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.