# ophelia_lab/__init__.py
"""
Ophelia Research Lab — módulos de backtesting, validación, optimización y reportes.
"""
__version__ = "3.0.0"

from .backtest_engine import BacktestEngine, TradeRecord
from .monte_carlo import MonteCarlo
from .walk_forward import WalkForward
from .trailing_lab import TrailingLab
from .break_even_lab import BreakEvenLab
from .leverage_lab import LeverageLab
from .optimizer import IterativeOptimizer
from .certification import Certifier
from .report_generator import ReportGenerator
from .operational_report import OperationalReport

__all__ = [
    "BacktestEngine",
    "TradeRecord",
    "MonteCarlo",
    "WalkForward",
    "TrailingLab",
    "BreakEvenLab",
    "LeverageLab",
    "IterativeOptimizer",
    "Certifier",
    "ReportGenerator",
    "OperationalReport",
]
