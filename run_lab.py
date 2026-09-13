# run_lab.py
"""Orquestador: descarga datos, backtest, labs, certificación."""
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('lab')


def main():
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

    for d in ['data/raw', 'data/trades', 'data/optimization', 'reports']:
        Path(d).mkdir(parents=True, exist_ok=True)

    # 1. Datos
    logger.info("=== Descargando datos reales ===")
    de = DataEngine()
    data_dict = {}
    for sym in SYMBOLS:
        df = de.fetch_ohlcv(sym, limit=500)
        if df is not None and not df.empty:
            data_dict[sym] = df
    logger.info(f"✅ {len(data_dict)} activos descargados")

    if not data_dict:
        logger.error("❌ Sin datos. Abortando.")
        return

    # 2. Backtest
    logger.info("=== Ejecutando backtest ===")
    def sig_fn(symbol, df):
        s = Signal(symbol, df, DEFAULT_PARAMS)
        return s.to_dict()

    bt = BacktestEngine()
    trades_df = bt.run(data_dict, sig_fn)
    bt_metrics = bt.compute_metrics()

    import json
    Path('data/trades').mkdir(exist_ok=True)
    if not trades_df.empty:
        trades_df.to_parquet('data/trades/trades.parquet')
    Path('data/optimization/backtest_metrics.json').write_text(json.dumps(bt_metrics, default=str, indent=2))
    logger.info(f"✅ Backtest: {bt_metrics.get('n_trades', 0)} trades")

    if trades_df.empty:
        logger.warning("Sin trades para análisis adicional")
        Certifier.generate()
        return

    # 3. Labs
    logger.info("=== Labs ===")
    trail = TrailingLab.optimize(trades_df)
    if not trail.empty:
        trail.to_csv('data/optimization/trailing_optimal.csv', index=False)

    be = BreakEvenLab.optimize(trades_df)
    if not be.empty:
        be.to_csv('data/optimization/break_even_optimal.csv', index=False)

    lev = LeverageLab.analyze(trades_df)
    if not lev.empty:
        lev.to_csv('data/optimization/leverage_full.csv', index=False)

    # 4. Walk-Forward
    logger.info("=== Walk-Forward ===")
    def bt_fn(d):
        b = BacktestEngine()
        b.run(d, sig_fn)
        return b.compute_metrics()
    WalkForward().validate(data_dict, bt_fn)

    # 5. Monte Carlo
    logger.info("=== Monte Carlo ===")
    MonteCarlo.run(trades_df)

    # 6. Certificación
    logger.info("=== Certificación ===")
    Certifier.generate()
    logger.info("✅ Pipeline completo. Revisar reports/")


if __name__ == '__main__':
    main()
