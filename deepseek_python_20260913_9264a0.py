# streamlit_ophelia.py
"""
Dashboard OPHELIA — solo muestra trades OPHELIA certificados.
"""
import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import pytz

from data_engine import DataEngine
from signal_engine import Signal
from config import DEFAULT_PARAMS, SYMBOLS
from ophelia_config import OPHELIA_PATTERNS_FILE, OPHELIA_TRADES_FILE, TIMEZONE_AR
from ophelia_engine import OpheliaDetector, TemporalPredictor, LeverageCalculator

st.set_page_config(page_title="🌟 OPHELIA Precision Engine", layout="wide", page_icon="🌟")

st.markdown("""
<style>
.ophelia-alert {
    background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
    color: #000;
    font-size: 1.1em;
}
.no-ophelia {
    background: #f0f0f0;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    color: #666;
}
.metric-big { font-size: 2em; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🌟 OPHELIA Precision Engine")
st.caption("Detector exclusivo de trades OPHELIA — 100% WR certificado")

# ============================================================
# CARGAR PATRÓN
# ============================================================
pattern_path = Path(OPHELIA_PATTERNS_FILE)
if not pattern_path.exists():
    st.error("❌ **OPHELIA NO DISPONIBLE**")
    st.warning("""
    No se ha aprendido un patrón OPHELIA todavía.
    
    **Ejecutá primero:**
    ```bash
    python run_ophelia.py