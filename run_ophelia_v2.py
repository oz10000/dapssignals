# run_ophelia_v2.py
"""
Pipeline OPHELIA v3 — OPHELIA Score como motor principal.
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

    print("╔" + "═" * 68 + "╗")
    print("║" + "  OPHELIA v3 — Score como motor principal".center(68) + "║")
    print("╚" + "═" * 68 + "╝")

    try:
        from data_engine import DataEngine
        from signal_engine import Signal
        from config import SYMBOLS, DEFAULT_PARAMS
        from ophelia_v2_config import (
            OPHELIA_V2_MODEL, OPHELIA_V2_METADATA,
            OPHELIA_V2_TRADES, OPHELIA_V2_DAILY, OPHELIA_V2_REPORT,
        )
        from ophelia_engine import (
            TradeCollector, OpheliaScorer, DailySelector,
            LeverageOptimizer, TemporalAnalyzer, Certifier, ReportGenerator,
        )
    except ImportError as e:
        logger.error(f"❌ Import: {e}")
        sys.exit(1)

    # ============================================================
    # FASE 0: VALIDACIÓN DE HIPÓTESIS
    # ============================================================
    print("\n[FASE 0] Validación de hipótesis del OPHELIA Score...")
    # (implícita: se valida con las métricas del modelo)

    # ============================================================
    # FASE 1: DATOS
    # ============================================================
    print("\n[FASE 1] Descargando datos...")
    de = DataEngine()
    data_dict = {}
    for i, sym in enumerate(SYMBOLS[:30], 1):
        try:
            df = de.fetch_ohlcv(sym, limit=2000)
            if df is not None and not df.empty:
                data_dict[sym] = df
                print(f"  [{i:>2}] ✅ {sym}: {len(df)} velas")
        except Exception as e:
            print(f"  [{i:>2}] ❌ {sym}: {e}")

    if len(data_dict) < 5:
        logger.error("❌ Pocos activos")
        sys.exit(1)

    print(f"\n✅ {len(data_dict)} activos")

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

    print(f"✅ {len(trades_df)} trades")
    print(f"   WR base: {trades_df['win'].mean()*100:.2f}%")
    print(f"   LONG: {(trades_df['direction']=='LONG').sum()}")
    print(f"   SHORT: {(trades_df['direction']=='SHORT').sum()}")

    trades_df.to_parquet(OPHELIA_V2_TRADES)

    # ============================================================
    # FASE 3: ENTRENAMIENTO OPHELIA SCORE
    # ============================================================
    print("\n[FASE 3] Entrenando OPHELIA Score...")
    scorer = OpheliaScorer()
    meta = scorer.fit(trades_df)

    if 'error' in meta:
        logger.error(f"❌ {meta['error']}")
        sys.exit(1)

    print(f"✅ AUC train: {meta['auc_train']:.4f}")
    print(f"✅ AUC test: {meta['auc_test']:.4f}")
    print(f"   Threshold OPHELIA: {meta['ophelia_threshold']:.3f}")
    print(f"   Threshold STANDARD: {meta['standard_threshold']:.3f}")
    print(f"   OPHELIA WR test: {meta['ophelia_wr_test']*100:.2f}%")
    print(f"   STANDARD WR test: {meta['standard_wr_test']*100:.2f}%")

    scorer.save(OPHELIA_V2_MODEL)
    Path(OPHELIA_V2_METADATA).parent.mkdir(parents=True, exist_ok=True)
    Path(OPHELIA_V2_METADATA).write_text(json.dumps(meta, indent=2, default=str))

    # ============================================================
    # FASE 4: SELECCIÓN
    # ============================================================
    print("\n[FASE 4] Seleccionando OPHELIA + STANDARD...")
    selector = DailySelector(scorer)
    selected = selector.select_from_history(trades_df)

    print(f"✅ {len(selected)} trades seleccionados")
    if not selected.empty:
        ophelia_count = (selected['tier'] == 'OPHELIA').sum()
        standard_count = (selected['tier'] == 'STANDARD').sum()
        print(f"   OPHELIA: {ophelia_count}")
        print(f"   STANDARD: {standard_count}")
        print(f"   WR global: {selected['win'].mean()*100:.2f}%")

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
    print(f"   Máx seguro: {lev['leverage_max_safe']}x")
    print(f"   Recomendado: {lev['leverage_recommended']}x")

    # ============================================================
    # FASE 7: TEMPORAL
    # ============================================================
    temporal = TemporalAnalyzer().analyze(selected)
    print(f"\n[FASE 7] Temporal: {temporal.get('trades_per_day', 0)} trades/día")

    # ============================================================
    # FASE 8: CERTIFICACIÓN
    # ============================================================
    print("\n[FASE 8] Certificación...")
    certifier = Certifier()
    cert = certifier.certify(meta, selected)
    print(f"   Estado: {'✅ CERTIFICADO' if cert['certified'] else '❌ NO CERTIFICADO'}")

    wf = certifier.walk_forward(scorer, trades_df)
    mc = certifier.monte_carlo(selected)

    # ============================================================
    # FASE 9: REPORTE
    # ============================================================
    print("\n[FASE 9] Generando reporte...")
    ReportGenerator.generate(
        scorer_meta=meta, cert=cert, leverage=lev,
        temporal=temporal, selected=selected,
        wf_df=wf, mc=mc, rankings=rankings,
        output=OPHELIA_V2_REPORT,
    )

    elapsed = time.time() - t0
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + f"  ✅ COMPLETADO en {elapsed:.0f}s".center(68) + "║")
    print("╚" + "═" * 68 + "╝")


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        import traceback
        print(f"\n❌ ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)
