# run_ophelia.py — VERSIÓN CORREGIDA
"""
Pipeline OPHELIA — con logging visible y manejo de errores.
"""
import sys
import logging
import traceback
import time
from pathlib import Path
from datetime import datetime, timezone

# ============================================================
# LOGGING PRIMERO
# ============================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    handlers=[
        logging.StreamHandler(sys.stdout),
    ]
)
logger = logging.getLogger('ophelia')


def main():
    t0 = time.time()

    print("=" * 70, flush=True)
    print("  OPHELIA PRECISION ENGINE — PIPELINE", flush=True)
    print(f"  Inicio: {datetime.now(timezone.utc).isoformat()}", flush=True)
    print("=" * 70, flush=True)

    # ============================================================
    # IMPORTS — con try/except individual para ver cuál falla
    # ============================================================
    print("\n[IMPORTS] Cargando módulos...", flush=True)

    try:
        from config import SYMBOLS, DEFAULT_PARAMS
        print(f"  ✅ config ({len(SYMBOLS)} symbols)", flush=True)
    except Exception as e:
        print(f"  ❌ config: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    try:
        from data_engine import DataEngine
        print(f"  ✅ data_engine", flush=True)
    except Exception as e:
        print(f"  ❌ data_engine: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    try:
        from signal_engine import Signal
        print(f"  ✅ signal_engine", flush=True)
    except Exception as e:
        print(f"  ❌ signal_engine: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    try:
        from ophelia_config import (
            OPHELIA_PATTERNS_FILE, OPHELIA_TRADES_FILE,
            OPHELIA_CERTIFICATION_FILE, BACKTEST_ASSETS,
        )
        print(f"  ✅ ophelia_config", flush=True)
    except Exception as e:
        print(f"  ❌ ophelia_config: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    try:
        from ophelia_engine import (
            PatternExtractor, OpheliaDetector, TemporalPredictor,
            LeverageCalculator, OpheliaCertifier, OpheliaReportGenerator,
        )
        from ophelia_engine.trade_simulator import simulate_trade_from_signal
        print(f"  ✅ ophelia_engine", flush=True)
    except Exception as e:
        print(f"  ❌ ophelia_engine: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    print("  ✅ Todos los imports OK\n", flush=True)

    # ============================================================
    # FASE 1 — DATA
    # ============================================================
    print("[FASE 1] Inicializando DataEngine...", flush=True)
    try:
        de = DataEngine()
        print(f"  ✅ Conectado a: {list(de.exchanges.keys())}", flush=True)
    except Exception as e:
        print(f"  ❌ DataEngine falló: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)

    symbols = BACKTEST_ASSETS if BACKTEST_ASSETS else SYMBOLS
    # Limitar para test rápido (configurable)
    import os
    limit_assets = int(os.getenv('OPHELIA_ASSETS_LIMIT', '0'))
    if limit_assets > 0:
        symbols = symbols[:limit_assets]
        print(f"  ⚠️ Limitado a {limit_assets} activos (por env OPHELIA_ASSETS_LIMIT)", flush=True)

    print(f"\n[FASE 1] Descargando {len(symbols)} activos...", flush=True)

    data_dict = {}
    for i, sym in enumerate(symbols, 1):
        try:
            df = de.fetch_ohlcv(sym, limit=2000)  # 2000 velas = ~7 días en 5m
            if df is not None and not df.empty:
                data_dict[sym] = df
                print(f"  [{i:>2}/{len(symbols)}] ✅ {sym}: {len(df)} velas", flush=True)
            else:
                print(f"  [{i:>2}/{len(symbols)}] ⚠️ {sym}: sin datos", flush=True)
        except Exception as e:
            print(f"  [{i:>2}/{len(symbols)}] ❌ {sym}: {e}", flush=True)

    if len(data_dict) < 3:
        print(f"\n❌ Solo {len(data_dict)} activos con datos. Abortando.", flush=True)
        sys.exit(1)

    print(f"\n✅ {len(data_dict)} activos descargados\n", flush=True)

    # ============================================================
    # FASE 2 — APRENDER PATRÓN
    # ============================================================
    print("[FASE 2] Extrayendo patrón OPHELIA...", flush=True)

    def sig_fn(symbol, df):
        try:
            return Signal(symbol, df, DEFAULT_PARAMS).to_dict()
        except Exception as e:
            return None

    extractor = PatternExtractor()
    print("  Ejecutando learn_from_data()...", flush=True)
    has_enough = extractor.learn_from_data(data_dict, sig_fn)

    n_op = len(extractor.ophelia_trades)
    n_no = len(extractor.non_ophelia_trades)
    print(f"\n  Trades recolectados: {n_op} OPHELIA, {n_no} no-OPHELIA", flush=True)

    if not has_enough:
        print(f"\n❌ OPHELIA NO DISPONIBLE", flush=True)
        print(f"   Trades OPHELIA: {n_op} < mínimo {extractor.min_n_train}", flush=True)

        # Generar reporte de NO DISPONIBLE
        Path('reports').mkdir(exist_ok=True)
        Path('reports/OPHELIA_NOT_AVAILABLE.md').write_text(
            f"# 🌟 OPHELIA NO DISPONIBLE\n\n"
            f"**Trades OPHELIA encontrados:** {n_op}\n"
            f"**Mínimo requerido:** {extractor.min_n_train}\n\n"
            f"**Sugerencias:**\n"
            f"- Ampliar período histórico\n"
            f"- Añadir más activos\n"
            f"- Revisar umbrales en `ophelia_config.py`\n"
        )
        print("  ✅ Reporte OPHELIA_NOT_AVAILABLE.md generado", flush=True)
        sys.exit(0)  # salida limpia (no error)

    # Extraer patrón
    print("\n[FASE 2] Extrayendo patrón estadístico...", flush=True)
    pattern = extractor.extract_pattern()

    if pattern is None:
        print("❌ No se pudo extraer patrón", flush=True)
        sys.exit(1)

    print(f"✅ Patrón extraído:", flush=True)
    print(f"   Trades OPHELIA: {pattern['n_train']}", flush=True)
    print(f"   Activos: {len(pattern['assets'])}", flush=True)
    print(f"   Ventana: {pattern['hour_range']['min']}h-{pattern['hour_range']['max']}h ARG", flush=True)

    # Guardar
    Path(OPHELIA_PATTERNS_FILE).parent.mkdir(parents=True, exist_ok=True)
    extractor.save_pattern(OPHELIA_PATTERNS_FILE)
    print(f"  ✅ Patrón guardado: {OPHELIA_PATTERNS_FILE}", flush=True)

    # Guardar trades
    import pandas as pd
    pd.DataFrame(extractor.ophelia_trades).to_parquet(OPHELIA_TRADES_FILE)
    print(f"  ✅ Trades guardados: {OPHELIA_TRADES_FILE}", flush=True)

    # ============================================================
    # FASE 3 — CERTIFICACIÓN
    # ============================================================
    print("\n[FASE 3] Certificación train/test...", flush=True)

    train, test = OpheliaCertifier.split_train_test(
        extractor.ophelia_trades, test_size=0.3
    )
    certifier = OpheliaCertifier(pattern, train, test)
    cert = certifier.certify()

    print(f"  Train: N={len(train)}, WR={cert.get('train_wr', 0)*100:.1f}%", flush=True)
    print(f"  Test:  N={len(test)}, WR={cert.get('test_wr', 0)*100:.1f}%", flush=True)
    print(f"  Resultado: {'✅ CERTIFICADO' if cert['certified'] else '❌ NO CERTIFICADO'}", flush=True)
    print(f"  Razón: {cert['reason']}", flush=True)

    # ============================================================
    # FASE 4 — LEVERAGE
    # ============================================================
    print("\n[FASE 4] Calculando leverage...", flush=True)
    lev_calc = LeverageCalculator(pattern)
    leverage = lev_calc.calculate()
    print(f"  Máximo seguro: {leverage['leverage_max_safe']}x", flush=True)
    print(f"  Recomendado: {leverage['leverage_recommended']}x", flush=True)

    # ============================================================
    # FASE 5 — REPORTES
    # ============================================================
    print("\n[FASE 5] Generando reportes...", flush=True)
    OpheliaReportGenerator.generate(
        pattern=pattern,
        cert=cert,
        leverage=leverage,
        ophelia_trades=extractor.ophelia_trades,
        output=OPHELIA_CERTIFICATION_FILE,
    )
    print(f"  ✅ {OPHELIA_CERTIFICATION_FILE}", flush=True)

    # ============================================================
    # FIN
    # ============================================================
    elapsed = time.time() - t0
    print()
    print("=" * 70, flush=True)
    print(f"  ✅ PIPELINE COMPLETO en {elapsed:.0f}s", flush=True)
    print("=" * 70, flush=True)

    # Resumen de archivos
    print("\nArchivos generados:", flush=True)
    for f in [OPHELIA_PATTERNS_FILE, OPHELIA_TRADES_FILE, OPHELIA_CERTIFICATION_FILE]:
        p = Path(f)
        if p.exists():
            print(f"  ✅ {f} ({p.stat().st_size} bytes)", flush=True)
        else:
            print(f"  ❌ {f}", flush=True)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR FATAL: {e}", flush=True)
        traceback.print_exc()
        sys.exit(1)
