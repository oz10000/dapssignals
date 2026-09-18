# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-09-18T10:43:00.614073+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.3283** (≥0.55 = predictor útil)
- Base rate test: 0.3793
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.720 | 50.00% | 33.33% | 1.00 | 1.50 |
| **STANDARD** | 0.450 | 60.00% | 37.50% | 2.50 | 4.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | ARB/USDT | 0.882 | OPHELIA | 22:50 | CONTINUACIÓN | ✅ |
| 2 | SUI/USDT | 0.806 | OPHELIA | 22:00 | CONTINUACIÓN | ✅ |
| 3 | CRV/USDT | 0.770 | OPHELIA | 00:10 | CONTINUACIÓN | ❌ |
| 4 | ADA/USDT | 0.711 | STANDARD | 23:00 | CONTINUACIÓN | ❌ |
| 5 | VET/USDT | 0.698 | STANDARD | 00:20 | CONTINUACIÓN | ❌ |
| 6 | LDO/USDT | 0.692 | STANDARD | 20:25 | CONTINUACIÓN | ❌ |
| 7 | CRV/USDT | 0.683 | STANDARD | 17:15 | CONTINUACIÓN | ✅ |
| 8 | DOGE/USDT | 0.681 | STANDARD | 22:55 | CONTINUACIÓN | ✅ |
| 9 | ETC/USDT | 0.680 | STANDARD | 20:00 | CONTINUACIÓN | ✅ |
| 10 | UNI/USDT | 0.527 | STANDARD | 00:05 | CONTINUACIÓN | ✅ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.2446%

## 6. Modelo Temporal

- Trades/día promedio: 5.0
- Intervalo medio: 47.2 min
- Distribución: {'LONG': 10}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 3 |
| 17:00 | 1 |
| 20:00 | 2 |
| 22:00 | 3 |
| 23:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 10 | 60.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.069974528422052 |
| median_final | 1.0648222695671357 |
| p5_final | 1.0127522590521616 |
| p95_final | 1.1473730049348316 |
| mean_max_dd | 0.0031994073584120223 |
| p95_max_dd | 0.006544255358745132 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 66 < 100
- ❌ Test insuficiente: 29 < 40
- ❌ AUC test bajo: 0.328 < 0.55
- ❌ OPHELIA WR test 33.3% < 55%
- ❌ Degradación excesiva: 16.7%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-09-18 00:20:00 | VET/USDT | STANDARD | 0.698 | LONG | 0.294% | -0.120% | 5m | ❌ |
| 2026-09-18 00:10:00 | CRV/USDT | OPHELIA | 0.770 | LONG | 0.476% | -0.178% | 5m | ❌ |
| 2026-09-18 00:05:00 | UNI/USDT | STANDARD | 0.527 | LONG | 1.556% | -0.149% | 5m | ✅ |
| 2026-09-17 23:00:00 | ADA/USDT | STANDARD | 0.711 | LONG | 0.143% | -0.238% | 5m | ❌ |
| 2026-09-17 22:55:00 | DOGE/USDT | STANDARD | 0.681 | LONG | 0.328% | -0.024% | 5m | ✅ |
| 2026-09-17 22:50:00 | ARB/USDT | OPHELIA | 0.882 | LONG | 4.348% | -0.103% | 40m | ✅ |
| 2026-09-17 22:00:00 | SUI/USDT | OPHELIA | 0.806 | LONG | 0.759% | 0.000% | 40m | ✅ |
| 2026-09-17 20:25:00 | LDO/USDT | STANDARD | 0.692 | LONG | 0.000% | -0.250% | 5m | ❌ |
| 2026-09-17 20:00:00 | ETC/USDT | STANDARD | 0.680 | LONG | 0.294% | -0.067% | 15m | ✅ |
| 2026-09-17 17:15:00 | CRV/USDT | STANDARD | 0.683 | LONG | 0.879% | -0.061% | 5m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.