# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-09-16T10:58:57.942111+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.0938** (≥0.55 = predictor útil)
- Base rate test: 0.1111
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 33.33% | 0.00% | 1.50 | 2.00 |
| **STANDARD** | 0.450 | 50.00% | 0.00% | 3.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | OP/USDT | 0.863 | OPHELIA | 23:35 | CONTINUACIÓN | ❌ |
| 2 | APT/USDT | 0.825 | OPHELIA | 23:25 | CONTINUACIÓN | ✅ |
| 3 | ARB/USDT | 0.788 | OPHELIA | 01:15 | CONTINUACIÓN | ❌ |
| 4 | SEI/USDT | 0.708 | OPHELIA | 01:20 | CONTINUACIÓN | ❌ |
| 5 | AAVE/USDT | 0.549 | STANDARD | 20:00 | CONTINUACIÓN | ✅ |
| 6 | WIF/USDT | 0.545 | STANDARD | 19:45 | CONTINUACIÓN | ✅ |
| 7 | ALGO/USDT | 0.537 | STANDARD | 23:20 | CONTINUACIÓN | ❌ |
| 8 | VET/USDT | 0.536 | STANDARD | 23:25 | CONTINUACIÓN | ✅ |
| 9 | ETC/USDT | 0.527 | STANDARD | 20:00 | CONTINUACIÓN | ✅ |
| 10 | LDO/USDT | 0.503 | STANDARD | 01:20 | CONTINUACIÓN | ❌ |
| 11 | ALGO/USDT | 0.467 | STANDARD | 01:20 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.3148%

## 6. Modelo Temporal

- Trades/día promedio: 5.5
- Intervalo medio: 55.8 min
- Distribución: {'LONG': 11}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 4 |
| 19:00 | 1 |
| 20:00 | 2 |
| 23:00 | 4 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 11 | 45.45% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0118231161339335 |
| median_final | 1.0116728311424417 |
| p5_final | 0.9956689495930584 |
| p95_final | 1.0284013467564073 |
| mean_max_dd | 0.004958189680500748 |
| p95_max_dd | 0.01007668514254735 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 41 < 100
- ❌ Test insuficiente: 18 < 40
- ❌ AUC test bajo: 0.094 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 33.3%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-09-16 01:20:00 | SEI/USDT | OPHELIA | 0.708 | LONG | 0.024% | -0.071% | 5m | ❌ |
| 2026-09-16 01:20:00 | LDO/USDT | STANDARD | 0.503 | LONG | 0.148% | -0.118% | 5m | ❌ |
| 2026-09-16 01:20:00 | ALGO/USDT | STANDARD | 0.467 | LONG | 0.000% | -0.267% | 5m | ❌ |
| 2026-09-16 01:15:00 | ARB/USDT | OPHELIA | 0.788 | LONG | 0.659% | -0.343% | 5m | ❌ |
| 2026-09-15 23:35:00 | OP/USDT | OPHELIA | 0.863 | LONG | 0.000% | -0.287% | 5m | ❌ |
| 2026-09-15 23:25:00 | APT/USDT | OPHELIA | 0.825 | LONG | 0.623% | 0.000% | 10m | ✅ |
| 2026-09-15 23:25:00 | VET/USDT | STANDARD | 0.536 | LONG | 0.366% | 0.000% | 10m | ✅ |
| 2026-09-15 23:20:00 | ALGO/USDT | STANDARD | 0.537 | LONG | 0.449% | -0.135% | 30m | ❌ |
| 2026-09-15 20:00:00 | AAVE/USDT | STANDARD | 0.549 | LONG | 0.604% | -0.049% | 10m | ✅ |
| 2026-09-15 20:00:00 | ETC/USDT | STANDARD | 0.527 | LONG | 0.429% | -0.041% | 15m | ✅ |
| 2026-09-15 19:45:00 | WIF/USDT | STANDARD | 0.545 | LONG | 0.393% | -0.056% | 20m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.