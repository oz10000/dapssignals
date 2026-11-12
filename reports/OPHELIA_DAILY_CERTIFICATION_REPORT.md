# 🌟 OPHELIA DAILY CERTIFICATION REPORT

**Generado:** 2026-11-12T14:45:58.945702+00:00 UTC
**Estado:** ❌ NO CERTIFICADO

---

## 1. Validación de Hipótesis

- AUC test: **nan** (≥0.55 = predictor útil)
- Base rate test: 0.0000
- ❌ **HIPÓTESIS RECHAZADA**: El OPHELIA Score no supera al azar en test

## 2. Thresholds Calibrados

| Nivel | Threshold | WR Train | WR Test | TPD Train | TPD Test |
|-------|-----------|----------|---------|-----------|----------|
| **OPHELIA** | 0.550 | 25.00% | 0.00% | 2.00 | 2.00 |
| **STANDARD** | 0.450 | 10.00% | 0.00% | 5.00 | 5.00 |

## 3. OPHELIA RANKING — LONG

| Rank | Activo | Score | Tier | Hora ARG | Tipo | Resultado |
|------|--------|-------|------|----------|------|-----------|
| 1 | DOGE/USDT | 0.894 | OPHELIA | 19:15 | CONTINUACIÓN | ❌ |
| 2 | VET/USDT | 0.819 | OPHELIA | 07:30 | CONTINUACIÓN | ✅ |
| 3 | LDO/USDT | 0.801 | OPHELIA | 07:00 | CONTINUACIÓN | ❌ |
| 4 | WIF/USDT | 0.732 | OPHELIA | 03:25 | CONTINUACIÓN | ❌ |
| 5 | CRV/USDT | 0.547 | STANDARD | 01:55 | CONTINUACIÓN | ❌ |
| 6 | PEPE/USDT | 0.468 | STANDARD | 08:45 | CONTINUACIÓN | ❌ |
| 7 | ALGO/USDT | 0.463 | STANDARD | 23:15 | CONTINUACIÓN | ❌ |
| 8 | WIF/USDT | 0.462 | STANDARD | 23:15 | CONTINUACIÓN | ❌ |
| 9 | ARB/USDT | 0.454 | STANDARD | 02:05 | CONTINUACIÓN | ❌ |

## 4. OPHELIA RANKING — SHORT

_Sin señales SHORT en el período._

## 5. Leverage por Nivel

- OPHELIA: máx seguro **30x**, recomendado **21x**
- MAE p95 histórico: 0.4722%

## 6. Modelo Temporal

- Trades/día promedio: 4.5
- Intervalo medio: 216.4 min
- Distribución: {'LONG': 9}

### Horas más frecuentes (ARG)

| Hora | N trades |
|------|----------|
| 01:00 | 1 |
| 02:00 | 1 |
| 07:00 | 2 |
| 19:00 | 1 |
| 23:00 | 2 |

## 7. Clasificación de Movimientos

| Tipo | N | WR |
|------|---|-----|
| CONTINUACIÓN | 9 | 11.11% |

## 8. Walk-Forward

❌ Datos insuficientes

## 9. Monte Carlo (10,000 sims)

| Métrica | Valor |
|---------|-------|
| mean_final | 0.9933106192823856 |
| median_final | 0.9930848312357532 |
| p5_final | 0.9886330649303712 |
| p95_final | 0.9985863373324777 |
| mean_max_dd | 0.006663643549842231 |
| p95_max_dd | 0.010455034779020113 |
| ruin_prob | 0.0 |

## 10. Certificación

### Razones de rechazo
- ❌ Train insuficiente: 26 < 100
- ❌ Test insuficiente: 12 < 40
- ❌ OPHELIA WR test 0.0% < 55%
- ❌ Degradación excesiva: 25.0%

## 11. Últimas 20 Señales (OPHELIA + STANDARD)

| Fecha ARG | Activo | Tier | Score | Dir | MFE | MAE | Dur | Win |
|-----------|--------|------|-------|-----|-----|-----|-----|-----|
| 2026-11-12 08:45:00 | PEPE/USDT | STANDARD | 0.468 | LONG | 0.254% | -0.251% | 5m | ❌ |
| 2026-11-12 07:00:00 | LDO/USDT | OPHELIA | 0.801 | LONG | 0.000% | -0.352% | 5m | ❌ |
| 2026-11-12 03:25:00 | WIF/USDT | OPHELIA | 0.732 | LONG | 0.000% | -0.259% | 5m | ❌ |
| 2026-11-12 02:05:00 | ARB/USDT | STANDARD | 0.454 | LONG | 0.106% | -0.409% | 5m | ❌ |
| 2026-11-12 01:55:00 | CRV/USDT | STANDARD | 0.547 | LONG | 0.000% | -0.373% | 5m | ❌ |
| 2026-11-11 23:15:00 | ALGO/USDT | STANDARD | 0.463 | LONG | 0.112% | -0.279% | 5m | ❌ |
| 2026-11-11 23:15:00 | WIF/USDT | STANDARD | 0.462 | LONG | 0.064% | -0.514% | 5m | ❌ |
| 2026-11-11 19:15:00 | DOGE/USDT | OPHELIA | 0.894 | LONG | 0.000% | -0.204% | 5m | ❌ |
| 2026-11-11 07:30:00 | VET/USDT | OPHELIA | 0.819 | LONG | 0.270% | 0.000% | 5m | ✅ |

---

## Declaración de Honestidad

El OPHELIA Score es P(win|features) validado en out-of-sample.
**No se filtra por resultado posterior.**
**No se selecciona winners a posteriori.**
El WR reportado es el WR real de las señales seleccionadas por el score.