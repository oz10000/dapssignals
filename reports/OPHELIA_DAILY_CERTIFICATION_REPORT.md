# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-02T14:56:18.205100+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **0.4318** (≥0.55 = predictor útil)
- Base rate test: 0.0833
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 0.00% | 0.00% | 0.00 | 0.00 |
| **STANDARD** | 0.450 | 60.00% | 0.00% | 5.00 | 4.50 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | ARB/USDT | 0.551 | OPHELIA | 19:55 | CONTINUACIÓN | ❌ |
| 2 | SEI/USDT | 0.548 | STANDARD | 20:00 | CONTINUACIÓN | ✅ |
| 3 | VET/USDT | 0.546 | STANDARD | 03:05 | CONTINUACIÓN | ❌ |
| 4 | UNI/USDT | 0.542 | STANDARD | 20:00 | CONTINUACIÓN | ✅ |
| 5 | LDO/USDT | 0.541 | STANDARD | 00:30 | CONTINUACIÓN | ❌ |
| 6 | BTC/USDT | 0.541 | STANDARD | 22:40 | CONTINUACIÓN | ❌ |
| 7 | BNB/USDT | 0.535 | STANDARD | 00:40 | CONTINUACIÓN | ❌ |
| 8 | ETH/USDT | 0.534 | STANDARD | 00:20 | CONTINUACIÓN | ❌ |
| 9 | BTC/USDT | 0.531 | STANDARD | 20:25 | CONTINUACIÓN | ✅ |
| 10 | SEI/USDT | 0.530 | STANDARD | 00:30 | CONTINUACIÓN | ❌ |
| 11 | SOL/USDT | 0.527 | STANDARD | 00:20 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.2861%

## 6. Modelo Temporal

- Trades/día promedio: 5.5
- Intervalo medio: 185.0 min
- Distribución: {'LONG': 11}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 00:00 | 5 |
| 03:00 | 1 |
| 19:00 | 1 |
| 20:00 | 3 |
| 22:00 | 1 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 11 | 27.27% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 1.001475984258118 |
| median_final | 1.001005342497645 |
| p5_final | 0.9925234134458677 |
| p95_final | 1.011803123678231 |
| mean_max_dd | 0.004196995653593522 |
| p95_max_dd | 0.0077628981024184295 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 56 < 100
- ❌ Test insuficiente: 24 < 40
- ❌ AUC test bajo: 0.432 < 0.55
- ❌ OPHELIA WR test 0.0% < 55%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-02 00:40:00 | BNB/USDT | STANDARD | 0.535 | LONG | 0.105% | -0.138% | 10m | ❌ |
| 2026-11-02 00:30:00 | LDO/USDT | STANDARD | 0.541 | LONG | 0.029% | -0.319% | 15m | ❌ |
| 2026-11-02 00:30:00 | SEI/USDT | STANDARD | 0.530 | LONG | 0.123% | -0.225% | 10m | ❌ |
| 2026-11-02 00:20:00 | ETH/USDT | STANDARD | 0.534 | LONG | 0.249% | -0.253% | 5m | ❌ |
| 2026-11-02 00:20:00 | SOL/USDT | STANDARD | 0.527 | LONG | 0.209% | -0.189% | 5m | ❌ |
| 2026-11-01 22:40:00 | BTC/USDT | STANDARD | 0.541 | LONG | 0.001% | -0.081% | 5m | ❌ |
| 2026-11-01 20:25:00 | BTC/USDT | STANDARD | 0.531 | LONG | 0.130% | -0.015% | 5m | ✅ |
| 2026-11-01 20:00:00 | SEI/USDT | STANDARD | 0.548 | LONG | 0.603% | 0.000% | 10m | ✅ |
| 2026-11-01 20:00:00 | UNI/USDT | STANDARD | 0.542 | LONG | 0.376% | -0.042% | 5m | ✅ |
| 2026-11-01 19:55:00 | ARB/USDT | OPHELIA | 0.551 | LONG | 0.226% | -0.153% | 5m | ❌ |
| 2026-11-01 03:05:00 | VET/USDT | STANDARD | 0.546 | LONG | 0.000% | -0.118% | 5m | ❌ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.