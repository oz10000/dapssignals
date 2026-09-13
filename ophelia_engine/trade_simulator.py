# ophelia_engine/trade_simulator.py
"""
Simula un trade hacia adelante y devuelve su outcome.
Este es el simulador "puro" — sin comisiones (para clasificar patrón).
Las comisiones se aplican luego en el detector live.
"""
from typing import Optional, Dict
import pandas as pd


def simulate_trade_from_signal(df: pd.DataFrame, entry_idx: int,
                                sig: Dict, max_hold_bars: int = 24) -> Optional[Dict]:
    """
    Simula un trade desde entry_idx hacia adelante.
    Retorna outcome: {exit_reason, exit_price, mfe, mae, duration_min, gross_pnl_pct}
    """
    if entry_idx >= len(df) - 2:
        return None

    entry_price = sig.get('entry_price', df['close'].iloc[entry_idx])
    sl_price = sig.get('sl_price')
    tp_price = sig.get('tp_price')
    direction = sig.get('direction')

    if sl_price is None or tp_price is None:
        return None

    mfe = 0.0
    mae = 0.0
    exit_price = None
    exit_reason = None
    exit_idx = None

    end = min(entry_idx + max_hold_bars + 1, len(df))

    for j in range(entry_idx + 1, end):
        bar = df.iloc[j]
        if direction == 'LONG':
            mfe = max(mfe, (bar['high'] - entry_price) / entry_price)
            mae = min(mae, (bar['low'] - entry_price) / entry_price)
            if bar['low'] <= sl_price:
                exit_price, exit_reason, exit_idx = sl_price, 'SL', j
                break
            if bar['high'] >= tp_price:
                exit_price, exit_reason, exit_idx = tp_price, 'TP', j
                break
        else:
            mfe = max(mfe, (entry_price - bar['low']) / entry_price)
            mae = min(mae, (entry_price - bar['high']) / entry_price)
            if bar['high'] >= sl_price:
                exit_price, exit_reason, exit_idx = sl_price, 'SL', j
                break
            if bar['low'] <= tp_price:
                exit_price, exit_reason, exit_idx = tp_price, 'TP', j
                break

    if exit_price is None:
        last = df.iloc[end - 1]
        exit_price = last['close']
        exit_reason = 'Time'
        exit_idx = end - 1

    if direction == 'LONG':
        gross = (exit_price - entry_price) / entry_price
    else:
        gross = (entry_price - exit_price) / entry_price

    e_time = df.index[entry_idx]
    x_time = df.index[exit_idx]
    duration_min = (x_time - e_time).total_seconds() / 60

    return {
        'exit_reason': exit_reason,
        'exit_price': exit_price,
        'mfe': mfe,
        'mae': mae,
        'duration_min': duration_min,
        'gross_pnl_pct': gross,
    }
