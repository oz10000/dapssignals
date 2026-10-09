# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-09T12:42:40.731357+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.7153** (≥0.55 = predictor útil)
- Base rate test: 0.2000
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 50.00% | 25.00% | 2.00 | 2.00 |
| **STANDARD** | 0.580 | 40.00% | 50.00% | 5.00 | 3.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | UNI/USDT | 0.608 | OPHELIA | 00:45 | CONTINUACIÓN | ❌ |
| 2 | APT/USDT | 0.607 | OPHELIA | 19:05 | CONTINUACIÓN | ✅ |
| 3 | SUI/USDT | 0.605 | OPHELIA | 22:30 | CONTINUACIÓN | ❌ |
| 4 | LINK/USDT | 0.600 | OPHELIA | 02:15 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3704%

## 6. Modelo Temporal

- Trades/día promedio: 2.0
- Intervalo medio: 143.3 min
- Distribución: {'LONG': 4}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 1 |
| 02:00 | 1 |
| 19:00 | 1 |
| 22:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 4 | 25.00% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0010169036718326 |
| median_final | 1.0010146061071685 |
| p5_final | 0.9949235268241015 |
| p95_final | 1.0119126842398343 |
| mean_max_dd | 0.002409657396178792 |
| p95_max_dd | 0.004015028791630685 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 69 < 100
- ❌ Test insuficiente: 30 < 40
- ❌ OPHELIA WR test 25.0% < 55%
- ❌ Degradación excesiva: 25.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-09 02:15:00 | LINK/USDT | OPHELIA | 0.600 | LONG | 0.031% | -0.372% | 5m | ❌ |
| 2026-10-09 00:45:00 | UNI/USDT | OPHELIA | 0.608 | LONG | 0.095% | -0.312% | 5m | ❌ |
| 2026-10-08 22:30:00 | SUI/USDT | OPHELIA | 0.605 | LONG | 0.009% | -0.360% | 5m | ❌ |
| 2026-10-08 19:05:00 | APT/USDT | OPHELIA | 0.607 | LONG | 0.511% | 0.000% | 25m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.