# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-19T12:21:19.155213+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.4603** (≥0.55 = predictor útil)
- Base rate test: 0.2059
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 100.00% | 0.00% | 2.00 | 2.00 |
| **STANDARD** | 0.450 | 40.00% | 10.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | VET/USDT | 0.845 | OPHELIA | 06:10 | CONTINUACIÓN | ✅ |
| 2 | INJ/USDT | 0.753 | OPHELIA | 03:15 | CONTINUACIÓN | ❌ |
| 3 | ARB/USDT | 0.741 | OPHELIA | 18:50 | CONTINUACIÓN | ✅ |
| 4 | SEI/USDT | 0.728 | OPHELIA | 02:40 | CONTINUACIÓN | ❌ |
| 5 | SOL/USDT | 0.546 | STANDARD | 18:15 | CONTINUACIÓN | ❌ |
| 6 | ADA/USDT | 0.543 | STANDARD | 18:15 | CONTINUACIÓN | ❌ |
| 7 | ATOM/USDT | 0.539 | STANDARD | 19:45 | CONTINUACIÓN | ✅ |
| 8 | ETH/USDT | 0.524 | STANDARD | 19:10 | CONTINUACIÓN | ❌ |
| 9 | ETC/USDT | 0.522 | STANDARD | 22:40 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3851%

## 6. Modelo Temporal

- Trades/día promedio: 4.5
- Intervalo medio: 180.7 min
- Distribución: {'LONG': 9}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 02:00 | 1 |
| 06:00 | 1 |
| 18:00 | 3 |
| 19:00 | 2 |
| 22:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 9 | 33.33% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0043644372575866 |
| median_final | 1.0038950829813975 |
| p5_final | 0.9910430188689453 |
| p95_final | 1.0190820002982919 |
| mean_max_dd | 0.0052529281545211585 |
| p95_max_dd | 0.010156942113081638 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 77 < 100
- ❌ Test insuficiente: 34 < 40
- ❌ AUC test bajo: 0.460 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 100.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-19 03:15:00 | INJ/USDT | OPHELIA | 0.753 | LONG | 0.196% | -0.518% | 5m | ❌ |
| 2026-10-19 02:40:00 | SEI/USDT | OPHELIA | 0.728 | LONG | 0.244% | -0.130% | 10m | ❌ |
| 2026-10-18 22:40:00 | ETC/USDT | STANDARD | 0.522 | LONG | 0.000% | -0.129% | 5m | ❌ |
| 2026-10-18 19:45:00 | ATOM/USDT | STANDARD | 0.539 | LONG | 0.595% | 0.000% | 40m | ✅ |
| 2026-10-18 19:10:00 | ETH/USDT | STANDARD | 0.524 | LONG | 0.131% | -0.173% | 5m | ❌ |
| 2026-10-18 18:50:00 | ARB/USDT | OPHELIA | 0.741 | LONG | 2.412% | -0.056% | 10m | ✅ |
| 2026-10-18 18:15:00 | SOL/USDT | STANDARD | 0.546 | LONG | 0.010% | -0.157% | 5m | ❌ |
| 2026-10-18 18:15:00 | ADA/USDT | STANDARD | 0.543 | LONG | 0.047% | -0.186% | 5m | ❌ |
| 2026-10-18 06:10:00 | VET/USDT | OPHELIA | 0.845 | LONG | 0.604% | -0.044% | 20m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.