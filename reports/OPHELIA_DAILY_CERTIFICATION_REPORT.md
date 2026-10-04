# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-04T11:54:11.676946+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.7250** (≥0.55 = predictor útil)
- Base rate test: 0.2308
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 25.00% | 50.00% | 1.33 | 2.00 |
| **STANDARD** | 0.450 | 30.00% | 60.00% | 3.33 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | LTC/USDT | 0.795 | OPHELIA | 17:30 | CONTINUACIÓN | ❌ |
| 2 | DOT/USDT | 0.785 | OPHELIA | 03:00 | CONTINUACIÓN | ❌ |
| 3 | AAVE/USDT | 0.784 | OPHELIA | 17:25 | CONTINUACIÓN | ✅ |
| 4 | AVAX/USDT | 0.756 | OPHELIA | 02:25 | CONTINUACIÓN | ✅ |
| 5 | INJ/USDT | 0.548 | STANDARD | 21:20 | CONTINUACIÓN | ✅ |
| 6 | ETC/USDT | 0.545 | STANDARD | 04:10 | CONTINUACIÓN | ❌ |
| 7 | APT/USDT | 0.545 | STANDARD | 01:15 | CONTINUACIÓN | ❌ |
| 8 | SEI/USDT | 0.537 | STANDARD | 18:05 | CONTINUACIÓN | ✅ |
| 9 | BNB/USDT | 0.529 | STANDARD | 00:40 | CONTINUACIÓN | ✅ |
| 10 | SUI/USDT | 0.511 | STANDARD | 17:05 | CONTINUACIÓN | ❌ |
| 11 | ARB/USDT | 0.506 | STANDARD | 00:30 | CONTINUACIÓN | ❌ |
| 12 | APT/USDT | 0.503 | STANDARD | 02:45 | CONTINUACIÓN | ❌ |
| 13 | PEPE/USDT | 0.486 | STANDARD | 17:35 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.2219%

## 6. Modelo Temporal

- Trades/día promedio: 6.5
- Intervalo medio: 55.4 min
- Distribución: {'LONG': 13}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 2 |
| 02:00 | 2 |
| 17:00 | 4 |
| 18:00 | 1 |
| 21:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 13 | 38.46% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0026481873057989 |
| median_final | 1.0024708449833037 |
| p5_final | 0.9952417283070565 |
| p95_final | 1.0102871907530775 |
| mean_max_dd | 0.0032206368623779397 |
| p95_max_dd | 0.006166268441173282 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 58 < 100
- ❌ Test insuficiente: 26 < 40
- ❌ OPHELIA WR test 50.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-04 04:10:00 | ETC/USDT | STANDARD | 0.545 | LONG | 0.011% | -0.124% | 5m | ❌ |
| 2026-10-04 03:00:00 | DOT/USDT | OPHELIA | 0.785 | LONG | 0.202% | -0.218% | 20m | ❌ |
| 2026-10-04 02:45:00 | APT/USDT | STANDARD | 0.503 | LONG | 0.000% | -0.087% | 5m | ❌ |
| 2026-10-04 02:25:00 | AVAX/USDT | OPHELIA | 0.756 | LONG | 0.262% | -0.009% | 10m | ✅ |
| 2026-10-04 01:15:00 | APT/USDT | STANDARD | 0.545 | LONG | 0.000% | -0.212% | 5m | ❌ |
| 2026-10-04 00:40:00 | BNB/USDT | STANDARD | 0.529 | LONG | 0.115% | -0.013% | 5m | ✅ |
| 2026-10-04 00:30:00 | ARB/USDT | STANDARD | 0.506 | LONG | 0.040% | -0.227% | 5m | ❌ |
| 2026-10-03 21:20:00 | INJ/USDT | STANDARD | 0.548 | LONG | 0.702% | 0.000% | 5m | ✅ |
| 2026-10-03 18:05:00 | SEI/USDT | STANDARD | 0.537 | LONG | 0.338% | 0.000% | 5m | ✅ |
| 2026-10-03 17:35:00 | PEPE/USDT | STANDARD | 0.486 | LONG | 0.000% | -0.092% | 5m | ❌ |
| 2026-10-03 17:30:00 | LTC/USDT | OPHELIA | 0.795 | LONG | 0.087% | -0.116% | 10m | ❌ |
| 2026-10-03 17:25:00 | AAVE/USDT | OPHELIA | 0.784 | LONG | 0.483% | -0.022% | 15m | ✅ |
| 2026-10-03 17:05:00 | SUI/USDT | STANDARD | 0.511 | LONG | 0.042% | -0.119% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.