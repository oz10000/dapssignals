# ophelia_engine/certification.py
"""
Certifica si el patrón OPHELIA es real o overfitting.
Divide la historia en train (70%) / test (30%).
Solo certifica si test WR = 100% con N_test ≥ MIN.
"""
import json
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd
from pathlib import Path

from ophelia_config import (
    MIN_OPHELIA_TRADES_TEST,
    REQUIRED_WIN_RATE,
    MAX_OVERFIT_RATIO,
    OPHELIA_CERTIFICATION_FILE,
)


class OpheliaCertifier:

    def __init__(self, pattern: Dict, train_trades: List[Dict],
                 test_trades: List[Dict]):
        self.pattern = pattern
        self.train = train_trades
        self.test = test_trades

    def certify(self) -> Dict:
        """Certifica o rechaza el patrón."""
        result = {
            'certified': False,
            'n_train': len(self.train),
            'n_test': len(self.test),
            'train_wr': None,
            'test_wr': None,
            'overfit_ratio': None,
            'reason': None,
        }

        if len(self.train) < 20:
            result['reason'] = f"Muestra train insuficiente ({len(self.train)} < 20)"
            return result

        if len(self.test) < MIN_OPHELIA_TRADES_TEST:
            result['reason'] = f"Muestra test insuficiente ({len(self.test)} < {MIN_OPHELIA_TRADES_TEST})"
            return result

        # WR de train y test
        train_wr = sum(1 for t in self.train if t.get('exit_reason') == 'TP') / len(self.train)
        test_wr = sum(1 for t in self.test if t.get('exit_reason') == 'TP') / len(self.test)

        result['train_wr'] = round(train_wr, 4)
        result['test_wr'] = round(test_wr, 4)
        result['overfit_ratio'] = round(test_wr / train_wr, 4) if train_wr > 0 else 0

        # Criterios de certificación
        if train_wr < REQUIRED_WIN_RATE:
            result['reason'] = f"Train WR {train_wr*100:.1f}% < 100%"
            return result

        if test_wr < REQUIRED_WIN_RATE:
            result['reason'] = f"Test WR {test_wr*100:.1f}% < 100%"
            return result

        if result['overfit_ratio'] < (1.0 / MAX_OVERFIT_RATIO):
            result['reason'] = f"Overfit ratio {result['overfit_ratio']:.3f} muy bajo"
            return result

        result['certified'] = True
        result['reason'] = "Patrón validado: 100% WR en train y test"
        return result

    @staticmethod
    def split_train_test(trades: List[Dict], test_size: float = 0.3
                         ) -> Tuple[List[Dict], List[Dict]]:
        """Split por tiempo: primeros 70% = train, últimos 30% = test."""
        if not trades:
            return [], []
        sorted_trades = sorted(trades, key=lambda t: t.get('entry_time', ''))
        split_idx = int(len(sorted_trades) * (1 - test_size))
        return sorted_trades[:split_idx], sorted_trades[split_idx:]