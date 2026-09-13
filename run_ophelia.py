# run_ophelia.py
"""
Pipeline OPHELIA completo:
  1. Descarga 12 meses de datos reales
  2. Simula todos los trades
  3. Extrae patrón OPHELIA
  4. Certifica train/test
  5. Calcula leverage
  6. Genera reportes
  7. Guarda el patrón para uso live
"""
import json
import logging
import sys
import time
from pathlib import Path
from datetime import datetime

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('ophelia')


def main():
    t0 = time.time()

    print("╔" + "═" * 68 + "╗")
    print("║" + "  OPHELIA PRECISION ENGINE".center(68) + "║")
    print("║" + "  Detector exclusivo de trades OPHELIA".center(68) + "║")
    print("╚" + "═" * 68 + "╝")

    # ============================================================
    # IMPORTS
    # ============================================================
    try:
        from data_engine import DataEngine
        from signal_engine import Signal
        from config import SYMBOLS, DEFAULT_PARAMS
        from ophelia_config import (
            BACKTEST_DAYS, BACKTEST_ASSETS, OPHELIA_TRADES_FILE,
            OPHELIA_PATTERNS_FILE, OPHELIA_CERTIFICATION_FILE,
        )
        from ophelia_engine import (
            PatternExtractor, OpheliaDetector, TemporalPredictor,
            LeverageCalculator, OpheliaCertifier, OpheliaReportGenerator,
        )
        from ophelia_engine.certification import OpheliaCertifier as Certifier
    except ImportError as e:
        logger.error(f"❌ Error importando: {e}")
        sys.exit(1)

    # ============================================================
    # FASE 1: DESCARGA DE DATOS
    # ============================================================
    print("\n" + "=" * 70)
    print("  FASE 1: Descarga de datos reales")
    print("=" * 70)

    de = DataEngine()
    symbols = BACKTEST_ASSETS if BACKTEST_ASSETS else SYMBOLS

    data_dict = {}
    for i, sym in enumerate(symbols, 1):
        try:
            # 12 meses en 5m ≈ 105,120 velas
            df = de.fetch_ohlcv(sym, limit=10000)  # límite práctico
            if df is not None and not df.empty:
                data_dict[sym] = df
                print(f"  [{i:>2}/{len(symbols)}] ✅ {sym}: {len(df)} velas")
            else:
                print(f"  [{i:>2}/{len(symbols)}] ⚠️ {sym}: sin datos")
        except Exception as e:
            print(f"  [{i:>2}/{len(symbols)}] ❌ {sym}: {e}")

    if len(data_dict) < 3:
        logger.error("❌ Muy pocos activos con datos. Abortando.")
        sys.exit(1)

    print(f"\n✅ {len(data_dict)} activos descargados")

    # ============================================================
    # FASE 2: APRENDER PATRÓN OPHELIA
    # ============================================================
    print("\n" + "=" * 70)
    print("  FASE 2: Extrayendo patrón OPHELIA de la historia")
    print("=" * 70)

    def sig_fn(symbol, df):
        try:
            return Signal(symbol, df, DEFAULT_PARAMS).to_dict()
        except Exception:
            return None

    extractor = PatternExtractor()
    has_enough = extractor.learn_from_data(data_dict, sig_fn)

    if not has_enough:
        print(f"\n❌ OPHELIA NO DISPONIBLE")
        print(f"   Trades OPHELIA encontrados: {len(extractor.ophelia_trades)}")
        print(f"   Mínimo requerido: {extractor.min_n_train}")
        print(f"   → Ampliá el período histórico o relajá los filtros.")
        # Generar reporte de NO DISPONIBLE
        report = {
            'status': 'OPHELIA_NO_DISPONIBLE',
            'reason': f'Solo {len(extractor.ophelia_trades)} trades OPHELIA (< {extractor.min_n_train})',
            'ophelia_trades_found': len(extractor.ophelia_trades),
        }
        Path('reports').mkdir(exist_ok=True)
        Path('reports/OPHELIA_NOT_AVAILABLE.md').write_text(
            f"# 🌟 OPHELIA NO DISPONIBLE\n\n"
            f"**Razón:** {report['reason']}\n\n"
            f"Se encontraron {len(extractor.ophelia_trades)} trades que cumplen los criterios OPHELIA.\n"
            f"Se requieren al menos {extractor.min_n_train} para aprender un patrón robusto.\n\n"
            f"**Sugerencias:**\n"
            f"- Ampliar el período histórico (más meses)\n"
            f"- Añadir más activos\n"
            f"- Revisar los umbrales de OPHELIA en ophelia_config.py\n"
        )
        sys.exit(1)

    # Extraer patrón
    pattern = extractor.extract_pattern()
    if pattern is None:
        print("❌ No se pudo extraer patrón")
        sys.exit(1)

    print(f"\n✅ Patrón extraído:")
    print(f"   Trades OPHELIA: {pattern['n_train']}")
    print(f"   Activos: {len(pattern['assets'])}")
    print(f"   Ventana: {pattern['hour_range']['min']}h-{pattern['hour_range']['max']}h ARG")

    extractor.save_pattern(OPHELIA_PATTERNS_FILE)

    # Guardar trades OPHELIA
    Path(OPHELIA_TRADES_FILE).parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(extractor.ophelia_trades).to_parquet(OPHELIA_TRADES_FILE)

    # ============================================================
    # FASE 3: CERTIFICACIÓN (TRAIN/TEST SPLIT)
    # ============================================================
    print("\n" + "=" * 70)
    print("  FASE 3: Certificación out-of-sample")
    print("=" * 70)

    train, test = Certifier.split_train_test(extractor.ophelia_trades, test_size=0.3)
    certifier = Certifier(pattern, train, test)
    cert = certifier.certify()

    print(f"\n📊 Certificación:")
    print(f"   Train: N={len(train)}, WR={cert.get('train_wr', 0)*100:.1f}%")
    print(f"   Test:  N={len(test)}, WR={cert.get('test_wr', 0)*100:.1f}%")
    print(f"   Resultado: {'✅ CERTIFICADO' if cert['certified'] else '❌ NO CERTIFICADO'}")
    print(f"   Razón: {cert['reason']}")

    if not cert['certified']:
        print("\n⚠️ El patrón NO fue certificado. Los reportes se generarán marcando esto.")

    # ============================================================
    # FASE 4: LEVERAGE
    # ============================================================
    print("\n" + "=" * 70)
    print("  FASE 4: Cálculo de leverage")
    print("=" * 70)

    lev_calc = LeverageCalculator(pattern)
    leverage = lev_calc.calculate()
    print(f"   Máximo seguro: {leverage['leverage_max_safe']}x")
    print(f"   Recomendado:   {leverage['leverage_recommended']}x")

    # ============================================================
    # FASE 5: PREDICCIÓN TEMPORAL
    # ============================================================
    print("\n" + "=" * 70)
    print("  FASE 5: Predicción temporal")
    print("=" * 70)

    temporal = TemporalPredictor(pattern)
    last_trade_time = None
    if extractor.ophelia_trades:
        last_trade_time = extractor.ophelia_trades[-1].get('entry_time_ar')
    prediction = temporal.next_ophelia_prediction(last_trade_time)
    print(f"   Próxima ventana: {prediction['next_window_start']} → {prediction['next_window_end']}")
    print(f"   Minutos hasta:   {prediction['minutes_until_start']}")
    print(f"   Confianza:       {prediction['confidence']*100:.1f}%")

    # ============================================================
    # FASE 6: REPORTES
    # ============================================================
    print("\n" + "=" * 70)
    print("  FASE 6: Generando reportes")
    print("=" * 70)

    OpheliaReportGenerator.generate(
        pattern=pattern,
        cert=cert,
        leverage=leverage,
        ophelia_trades=extractor.ophelia_trades,
        output=OPHELIA_CERTIFICATION_FILE,
    )

    # ============================================================
    # RESUMEN
    # ============================================================
    elapsed = time.time() - t0
    print()
    print("╔" + "═" * 68 + "╗")
    print("║" + f"  ✅ PIPELINE OPHELIA COMPLETADO en {elapsed:.0f}s".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print("📁 Archivos generados:")
    for f in [OPHELIA_PATTERNS_FILE, OPHELIA_TRADES_FILE, OPHELIA_CERTIFICATION_FILE]:
        p = Path(f)
        status = "✅" if p.exists() else "❌"
        print(f"   {status} {f}")
    print()
    print("🚀 Dashboard: streamlit run streamlit_ophelia.py")


if __name__ == '__main__':
    main()
