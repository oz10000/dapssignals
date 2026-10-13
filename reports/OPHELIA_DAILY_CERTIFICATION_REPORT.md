# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-10-13T13:44:19.845283+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.6122** (≥0.55 = predictor útil)
- Base rate test: 0.3158
- ✅ **HIPÓTESIS VALIDADA**: El OPHELIA Score es un predictor superior al azar

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.680 | 75.00% | 50.00% | 0.13 | 1.00 |
| **STANDARD** | 0.600 | 75.00% | 42.86% | 0.26 | 3.50 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | VET/USDT | 0.804 | OPHELIA | 22:00 | CONTINUACIÓN | ❌ |
| 2 | SOL/USDT | 0.783 | OPHELIA | 23:00 | CONTINUACIÓN | ✅ |
| 3 | DOGE/USDT | 0.767 | OPHELIA | 22:50 | CONTINUACIÓN | ✅ |
| 4 | VET/USDT | 0.719 | OPHELIA | 22:35 | CONTINUACIÓN | ✅ |
| 5 | ADA/USDT | 0.680 | STANDARD | 23:10 | CONTINUACIÓN | ✅ |
| 6 | OP/USDT | 0.676 | STANDARD | 22:45 | CONTINUACIÓN | ✅ |
| 7 | XRP/USDT | 0.662 | STANDARD | 23:15 | CONTINUACIÓN | ✅ |
| 8 | AVAX/USDT | 0.662 | STANDARD | 22:45 | CONTINUACIÓN | ✅ |
| 9 | LTC/USDT | 0.660 | STANDARD | 22:55 | CONTINUACIÓN | ✅ |
| 10 | LTC/USDT | 0.651 | STANDARD | 02:05 | CONTINUACIÓN | ❌ |
| 11 | DOT/USDT | 0.641 | STANDARD | 01:30 | CONTINUACIÓN | ❌ |
| 12 | VET/USDT | 0.622 | STANDARD | 21:45 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.2508%

## 6. Modelo Temporal

- Trades/día promedio: 2.4
- Intervalo medio: 4341.0 min
- Distribución: {'LONG': 12}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 1 |
| 02:00 | 1 |
| 21:00 | 1 |
| 22:00 | 6 |
| 23:00 | 3 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 12 | 66.67% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.0593665746818113 |
| median_final | 1.0593100541867884 |
| p5_final | 1.032557921310975 |
| p95_final | 1.0862997150835352 |
| mean_max_dd | 0.0018203083695811039 |
| p95_max_dd | 0.003803565624456378 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 87 < 100
- ❌ Test insuficiente: 38 < 40
- ❌ OPHELIA WR test 50.0% < 55%
- ❌ Degradación excesiva: 25.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-10-13 02:05:00 | LTC/USDT | STANDARD | 0.651 | LONG | 0.081% | -0.097% | 5m | ❌ |
| 2026-10-13 01:30:00 | DOT/USDT | STANDARD | 0.641 | LONG | 0.186% | -0.279% | 5m | ❌ |
| 2026-10-12 23:15:00 | XRP/USDT | STANDARD | 0.662 | LONG | 0.721% | -0.059% | 40m | ✅ |
| 2026-10-12 23:10:00 | ADA/USDT | STANDARD | 0.680 | LONG | 0.897% | -0.214% | 55m | ✅ |
| 2026-10-12 23:00:00 | SOL/USDT | OPHELIA | 0.783 | LONG | 1.223% | -0.047% | 20m | ✅ |
| 2026-10-12 22:55:00 | LTC/USDT | STANDARD | 0.660 | LONG | 0.751% | -0.098% | 70m | ✅ |
| 2026-10-12 22:50:00 | DOGE/USDT | OPHELIA | 0.767 | LONG | 0.918% | -0.036% | 30m | ✅ |
| 2026-10-12 22:45:00 | OP/USDT | STANDARD | 0.676 | LONG | 1.365% | -0.046% | 30m | ✅ |
| 2026-10-12 22:45:00 | AVAX/USDT | STANDARD | 0.662 | LONG | 1.130% | -0.049% | 25m | ✅ |
| 2026-09-18 21:45:00 | VET/USDT | STANDARD | 0.622 | LONG | 0.000% | -0.228% | 5m | ❌ |
| 2026-09-16 22:00:00 | VET/USDT | OPHELIA | 0.804 | LONG | 0.000% | -0.195% | 5m | ❌ |
| 2026-09-12 22:35:00 | VET/USDT | OPHELIA | 0.719 | LONG | 0.342% | 0.000% | 15m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.