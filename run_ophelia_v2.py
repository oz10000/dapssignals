# run_ophelia_v2.py
"""
Pipeline OPHELIA v3 — Anti-overfitting.
FIX: limit=10000 velas por activo (antes 2000).
"""
import sys
import time
import logging
import json
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
)
logger = logging.getLogger('ophelia')


def main():
    t0 = time.time()

    print("=" * 70)
    print("  OPHELIA PIPELINE v3 — Anti-overfitting")
    print("=" * 70)
    print()

    # ============================================================
    # IMPORTS
    # ============================================================
    try:
        from data_engine import DataEngine
        from signal_engine import Signal
        from config import SYMBOLS, DEFAULT_PARAMS
        from ophelia_v2_config import (
            OPHELIA_V2_MODEL, OPHELIA_V2_METADATA,
            OPHELIA_V2_TRADES, OPHELIA_V2_DAILY, OPHELIA_V2_REPORT,
            BACKTEST_LOOKBACK_VELAS, MIN_AUC_TEST,
        )
        from ophelia_engine import (
            TradeCollector, OpheliaScorer, DailySelector,
            LeverageOptimizer, TemporalAnalyzer, Certifier, ReportGenerator,
        )
    except ImportError as e:
        logger.error(f"❌ Import: {e}")
        sys.exit(1)

    # ============================================================
    # FASE 1: DATOS
    # ============================================================
    print("[FASE 1] Descargando datos...")
    print(f"         Velas por activo: {BACKTEST_LOOKBACK_VELAS}")
    de = DataEngine()
    data_dict = {}

    for i, sym in enumerate(SYMBOLS[:30], 1):
        try:
            df = de.fetch_ohlcv(sym, limit=BACKTEST_LOOKBACK_VELAS)
            if df is not None and not df.empty:
                data_dict[sym] = df
                print(f"  [{i:>2}] ✅ {sym}: {len(df)} velas")
            else:
                print(f"  [{i:>2}] ⚠️ {sym}: sin datos")
        except Exception as e:
            print(f"  [{i:>2}] ❌ {sym}: {e}")

    if len(data_dict) < 5:
        logger.error(f"❌ Solo {len(data_dict)} activos. Abortando.")
        sys.exit(1)

    total_velas = sum(len(df) for df in data_dict.values())
    print(f"\n✅ {len(data_dict)} activos, {total_velas:,} velas totales")

    # ============================================================
    # FASE 2: RECOLECCIÓN
    # ============================================================
    print("\n[FASE 2] Recolectando trades sin bias...")

    def sig_fn(symbol, df):
        try:
            return Signal(symbol, df, DEFAULT_PARAMS).to_dict()
        except Exception:
            return None

    collector = TradeCollector()
    trades_df = collector.collect(data_dict, sig_fn)

    if trades_df.empty:
        logger.error("❌ Sin trades")
        sys.exit(1)

    n_trades = len(trades_df)
    n_long = (trades_df['direction'] == 'LONG').sum()
    n_short = (trades_df['direction'] == 'SHORT').sum()
    wr_base = trades_df['win'].mean()

    print(f"✅ {n_trades} trades recolectados")
    print(f"   WR base: {wr_base*100:.2f}%")
    print(f"   LONG: {n_long} | SHORT: {n_short}")

    trades_df.to_parquet(OPHELIA_V2_TRADES)

    # Validación mínima de muestra
    if n_trades < 200:
        print(f"\n⚠️ ADVERTENCIA: Solo {n_trades} trades.")
        print(f"   Recomendado: ≥500 trades para evitar overfitting.")
        print(f"   El modelo puede fallar en AUC test.")

    # ============================================================
    # FASE 3: ENTRENAMIENTO
    # ============================================================
    print("\n[FASE 3] Entrenando OPHELIA Score...")
    scorer = OpheliaScorer()
    meta = scorer.fit(trades_df)

    if 'error' in meta:
        logger.error(f"❌ {meta['error']}")
        sys.exit(1)

    auc_train = meta.get('auc_train', 0.5)
    auc_test = meta.get('auc_test', 0.5)
    degradation = auc_train - auc_test

    print(f"✅ Modelo entrenado")
    print(f"   N train:       {meta.get('n_train', 0)}")
    print(f"   N test:        {meta.get('n_test', 0)}")
    print(f"   AUC train:     {auc_train:.4f}")
    print(f"   AUC test:      {auc_test:.4f}")
    print(f"   Degradación:   {degradation:.4f}")

    if auc_test < MIN_AUC_TEST:
        print(f"\n🚨 ALERTA: AUC test {auc_test:.4f} < {MIN_AUC_TEST}")
        print(f"   El modelo NO es confiable para operar.")
        print(f"   Causas posibles:")
        print(f"   - Muestra insuficiente (necesitás ~500 trades)")
        print(f"   - Features sin información predictiva")
        print(f"   - Mercado sin edge detectable en este timeframe")

    print(f"   Threshold OPHELIA:  {meta.get('ophelia_threshold', 0):.3f}")
    print(f"   Threshold STANDARD: {meta.get('standard_threshold', 0):.3f}")
    print(f"   OPHELIA WR test:    {meta.get('ophelia_wr_test', 0)*100:.2f}%")
    print(f"   STANDARD WR test:   {meta.get('standard_wr_test', 0)*100:.2f}%")

    scorer.save(OPHELIA_V2_MODEL)
    Path(OPHELIA_V2_METADATA).parent.mkdir(parents=True, exist_ok=True)
    Path(OPHELIA_V2_METADATA).write_text(json.dumps(meta, indent=2, default=str))

    # ============================================================
    # FASE 4: SELECCIÓN
    # ============================================================
    print("\n[FASE 4] Seleccionando OPHELIA + STANDARD...")
    selector = DailySelector(scorer)
    selected = selector.select_from_history(trades_df)

    if not selected.empty:
        ophelia_count = (selected['tier'] == 'OPHELIA').sum()
        standard_count = (selected['tier'] == 'STANDARD').sum()
        wr_global = selected['win'].mean()

        print(f"✅ {len(selected)} trades seleccionados")
        print(f"   OPHELIA:  {ophelia_count}")
        print(f"   STANDARD: {standard_count}")
        print(f"   WR global: {wr_global*100:.2f}%")

    selected.to_parquet(OPHELIA_V2_DAILY)

    # ============================================================
    # FASE 5: RANKINGS
    # ============================================================
    rankings = selector.get_rankings(selected)

    # ============================================================
    # FASE 6: LEVERAGE
    # ============================================================
    print("\n[FASE 6] Calculando leverage...")
    lev = LeverageOptimizer().optimize_portfolio(selected)
    print(f"   Máx seguro:  {lev['leverage_max_safe']}x")
    print(f"   Recomendado: {lev['leverage_recommended']}x")

    # ============================================================
    # FASE 7: TEMPORAL
    # ============================================================
    temporal = TemporalAnalyzer().analyze(selected)
    print(f"\n[FASE 7] Temporal: {temporal.get('trades_per_day', 0):.2f} trades/día")

    # ============================================================
    # FASE 8: CERTIFICACIÓN
    # ============================================================
    print("\n[FASE 8] Certificación...")
    certifier = Certifier()
    cert = certifier.certify(meta, selected)

    status = '✅ CERTIFICADO' if cert['certified'] else '❌ NO CERTIFICADO'
    print(f"   Estado: {status}")

    if cert.get('reasons'):
        for r in cert['reasons']:
            print(f"   - {r}")

    try:
        wf = certifier.walk_forward(scorer, trades_df)
    except Exception as e:
        print(f"   ⚠️ Walk-Forward: {e}")
        wf = pd.DataFrame()

    try:
        mc = certifier.monte_carlo(selected)
    except Exception as e:
        print(f"   ⚠️ Monte Carlo: {e}")
        mc = {}

    # ============================================================
    # FASE 9: REPORTE
    # ============================================================
    print("\n[FASE 9] Generando reporte...")
    try:
        ReportGenerator.generate(
            scorer_meta=meta, cert=cert, leverage=lev,
            temporal=temporal, selected=selected,
            wf_df=wf, mc=mc, rankings=rankings,
            output=OPHELIA_V2_REPORT,
        )
    except Exception as e:
        print(f"   ⚠️ Reporte falló: {e}")

    # ============================================================
    # FIN
    # ============================================================
    elapsed = time.time() - t0
    print()
    print("=" * 70)
    print(f"  ✅ PIPELINE COMPLETADO en {elapsed:.0f}s")
    print("=" * 70)
    print()
    print("Archivos generados:")
    for f in [OPHELIA_V2_MODEL, OPHELIA_V2_METADATA, OPHELIA_V2_TRADES,
              OPHELIA_V2_DAILY, OPHELIA_V2_REPORT]:
        p = Path(f)
        status = "✅" if p.exists() else "❌"
        size = f"{p.stat().st_size:,} bytes" if p.exists() else "no existe"
        print(f"  {status} {f} ({size})")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        print(f"\n❌ ERROR FATAL: {e}")
        traceback.print_exc()
        sys.exit(1)
