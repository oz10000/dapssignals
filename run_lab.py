# run_lab.py
"""
Orquestador completo: datos → backtest → labs → validación → certificación → reporte operativo.
"""
import logging
import json
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('lab')


def ensure_dirs():
    for d in ['data/raw', 'data/trades', 'data/optimization',
              'data/certifications', 'reports']:
        Path(d).mkdir(parents=True, exist_ok=True)


def phase(n: int, name: str):
    logger.info("")
    logger.info("=" * 60)
    logger.info(f"  FASE {n}: {name}")
    logger.info("=" * 60)


def main():
    ensure_dirs()

    # Importaciones controladas
    try:
        from data_engine import DataEngine
        from signal_engine import Signal
        from config import SYMBOLS, DEFAULT_PARAMS
        from ophelia_lab.backtest_engine import BacktestEngine
        from ophelia_lab.walk_forward import WalkForward
        from ophelia_lab.monte_carlo import MonteCarlo
        from ophelia_lab.trailing_lab import TrailingLab
        from ophelia_lab.break_even_lab import BreakEvenLab
        from ophelia_lab.leverage_lab import LeverageLab
        from ophelia_lab.certification import Certifier
        from ophelia_lab.report_generator import ReportGenerator
        from ophelia_lab.operational_report import OperationalReport
    except ImportError as e:
        logger.error(f"❌ Error importando: {e}")
        sys.exit(1)

    # ============================================================
    # FASE 1: Descarga de datos
    # ============================================================
    phase(1, "Descarga de datos reales")
    try:
        de = DataEngine()
    except Exception as e:
        logger.error(f"❌ DataEngine falló: {e}")
        sys.exit(1)

    data_dict = {}
    for sym in SYMBOLS:
        try:
            df = de.fetch_ohlcv(sym, limit=500)
            if df is not None and not df.empty:
                data_dict[sym] = df
        except Exception as e:
            logger.warning(f"⚠️ Error con {sym}: {e}")
    logger.info(f"✅ {len(data_dict)}/{len(SYMBOLS)} activos descargados")

    if len(data_dict) < 5:
        logger.error("❌ Muy pocos activos. Abortando.")
        sys.exit(1)

    # ============================================================
    # FASE 2: Backtest realista
    # ============================================================
    phase(2, "Backtest realista")

    def sig_fn(symbol, df):
        s = Signal(symbol, df, DEFAULT_PARAMS)
        return s.to_dict()

    bt = BacktestEngine()
    trades_df = bt.run(data_dict, sig_fn)
    bt_metrics = bt.compute_metrics()

    if not trades_df.empty:
        trades_df.to_parquet('data/trades/trades.parquet')
    Path('data/optimization/backtest_metrics.json').write_text(
        json.dumps(bt_metrics, default=str, indent=2),
        encoding='utf-8'
    )
    logger.info(f"✅ {bt_metrics.get('n_trades', 0)} trades ejecutados")
    logger.info(f"   Win Rate: {bt_metrics.get('win_rate', 0)}")
    logger.info(f"   PF: {bt_metrics.get('profit_factor', 0)}")
    logger.info(f"   Sharpe: {bt_metrics.get('sharpe', 0)}")

    if trades_df.empty:
        logger.warning("⚠️ Sin trades. Se genera certificación con estado PENDING.")
        Certifier.generate()
        ReportGenerator.generate_all()
        OperationalReport().generate()
        return

    # ============================================================
    # FASE 3: Labs
    # ============================================================
    phase(3, "Labs de optimización")

    try:
        trail = TrailingLab.optimize(trades_df)
        if not trail.empty:
            trail.to_csv('data/optimization/trailing_optimal.csv', index=False)
            logger.info(f"✅ Trailing óptimo: {len(trail)} activos")
    except Exception as e:
        logger.warning(f"⚠️ Trailing Lab falló: {e}")

    try:
        be = BreakEvenLab.optimize(trades_df)
        if not be.empty:
            be.to_csv('data/optimization/break_even_optimal.csv', index=False)
            logger.info(f"✅ Break Even óptimo: {len(be)} activos")
    except Exception as e:
        logger.warning(f"⚠️ Break Even Lab falló: {e}")

    try:
        lev = LeverageLab.analyze(trades_df)
        if not lev.empty:
            lev.to_csv('data/optimization/leverage_full.csv', index=False)
            logger.info(f"✅ Leverage analizado: {len(lev)} filas")
    except Exception as e:
        logger.warning(f"⚠️ Leverage Lab falló: {e}")

    # ============================================================
    # FASE 4: Walk-Forward
    # ============================================================
    phase(4, "Walk-Forward Validation")

    def bt_fn(d):
        b = BacktestEngine()
        b.run(d, sig_fn)
        return b.compute_metrics()

    try:
        wf_df = WalkForward(n_windows=5).validate(data_dict, bt_fn)
        logger.info(f"✅ Walk-Forward: {len(wf_df)} ventanas")
    except Exception as e:
        logger.warning(f"⚠️ Walk-Forward falló: {e}")

    # ============================================================
    # FASE 5: Monte Carlo
    # ============================================================
    phase(5, "Monte Carlo (10k simulaciones)")
    try:
        mc = MonteCarlo.run(trades_df, n_sims=10000)
        logger.info(f"✅ MC: ruin_prob={mc.get('ruin_probability', 0)}")
    except Exception as e:
        logger.warning(f"⚠️ Monte Carlo falló: {e}")

    # ============================================================
    # FASE 6: Certificación + Reportes
    # ============================================================
    phase(6, "Certificación y Reportes")
    try:
        Certifier.generate()
        ReportGenerator.generate_all()
        OperationalReport().generate()
        logger.info("✅ Reportes generados:")
        logger.info("   - reports/full_report.txt")
        logger.info("   - reports/CERTIFICATION_REPORT.md")
        logger.info("   - reports/MONTE_CARLO_REPORT.md")
        logger.info("   - reports/OPHELIA_OPERATIONAL_REPORT.md")
    except Exception as e:
        logger.error(f"❌ Certificación falló: {e}")

    logger.info("")
    logger.info("=" * 60)
    logger.info("  ✅ PIPELINE COMPLETO")
    logger.info("=" * 60)


if __name__ == '__main__':
    main()
