# ophelia_engine/__init__.py
"""
OPHELIA Precision Engine — detección exclusiva de trades OPHELIA.
"""
__version__ = "1.0.0"

from .pattern_extractor import PatternExtractor
from .ophelia_detector import OpheliaDetector
from .temporal_predictor import TemporalPredictor
from .leverage_calculator import LeverageCalculator
from .certification import OpheliaCertifier
from .report_generator import OpheliaReportGenerator

__all__ = [
    "PatternExtractor",
    "OpheliaDetector",
    "TemporalPredictor",
    "LeverageCalculator",
    "OpheliaCertifier",
    "OpheliaReportGenerator",
]