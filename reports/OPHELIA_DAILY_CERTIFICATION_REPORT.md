# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-08T12:57:20.217522+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.5000** (≥0.55 = predictor útil)
- Base rate test: 0.2143
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 25.00% | 2.00 | 2.00 |
| **STANDARD** | 0.550 | 60.00% | 14.29% | 5.00 | 3.50 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | ATOM/USDT | 0.641 | OPHELIA | 19:40 | CONTINUACIÓN | ✅ |
| 2 | ETH/USDT | 0.635 | OPHELIA | 17:20 | CONTINUACIÓN | ❌ |
| 3 | VET/USDT | 0.577 | OPHELIA | 02:30 | CONTINUACIÓN | ❌ |
| 4 | LINK/USDT | 0.577 | OPHELIA | 02:30 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.1853%

## 6. Modelo Temporal

- Trades/día promedio: 2.0
- Intervalo medio: 275.0 min
- Distribución: {'LONG': 4}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 02:00 | 2 |
| 17:00 | 1 |
| 19:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 4 | 25.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 0.9989248112043708 |
| median_final | 0.9989007704457085 |
| p5_final | 0.995781693955993 |
| p95_final | 1.003645091974201 |
| mean_max_dd | 0.0019109755310330286 |
| p95_max_dd | 0.003345068280464976 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 65 < 100
- ❌ Test insuficiente: 28 < 40
- ❌ AUC test bajo: 0.500 < 0.55
- ❌ OPHELIA WR test 25.0% < 55%
- ❌ Degradación excesiva: 25.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-08 02:30:00 | VET/USDT | OPHELIA | 0.577 | LONG | 0.050% | -0.164% | 5m | ❌ |
| 2026-10-08 02:30:00 | LINK/USDT | OPHELIA | 0.577 | LONG | 0.030% | -0.189% | 5m | ❌ |
| 2026-10-07 19:40:00 | ATOM/USDT | OPHELIA | 0.641 | LONG | 0.468% | 0.000% | 5m | ✅ |
| 2026-10-07 17:20:00 | ETH/USDT | OPHELIA | 0.635 | LONG | 0.074% | -0.090% | 10m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.