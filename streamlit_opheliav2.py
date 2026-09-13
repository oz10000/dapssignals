# streamlit_ophelia.py
"""
🌟 OPHELIA Precision Engine — Dashboard v3
- Escaneo live con OPHELIA Score
- Ranking COMPLETO de TODOS los activos (no solo top 3)
- Clasificación OPHELIA / STANDARD / REJECTED
- Generación de reportes para iteración
- Descarga de TXT + MD + JSON
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
import json
import pytz
import io

# ============================================================
# CONFIGURACIÓN
# ============================================================
st.set_page_config(
    page_title="🌟 OPHELIA Precision Engine",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# IMPORTS DEFENSIVOS
# ============================================================
IMPORT_ERRORS = []

try:
    from config import DEFAULT_PARAMS, SYMBOLS, INITIAL_CAPITAL
except Exception as e:
    IMPORT_ERRORS.append(f"config: {e}")
    DEFAULT_PARAMS = {}
    SYMBOLS = []
    INITIAL_CAPITAL = 10000.0

try:
    from ophelia_v2_config import (
        OPHELIA_V2_MODEL, OPHELIA_V2_METADATA, OPHELIA_V2_TRADES,
        OPHELIA_V2_DAILY, OPHELIA_V2_REPORT, TIMEZONE_AR,
        OPHELIA_SCORE_THRESHOLD, STANDARD_SCORE_THRESHOLD,
        OPHELIA_MAX_PER_DAY, STANDARD_MAX_PER_DAY,
    )
except Exception as e:
    IMPORT_ERRORS.append(f"ophelia_v2_config: {e}")
    OPHELIA_V2_MODEL = 'data/ophelia_v2/model.pkl'
    OPHELIA_V2_METADATA = 'data/ophelia_v2/metadata.json'
    OPHELIA_V2_TRADES = 'data/ophelia_v2/trades.parquet'
    OPHELIA_V2_DAILY = 'data/ophelia_v2/daily_selection.parquet'
    OPHELIA_V2_REPORT = 'reports/OPHELIA_DAILY_CERTIFICATION_REPORT.md'
    TIMEZONE_AR = 'America/Argentina/Buenos_Aires'
    OPHELIA_SCORE_THRESHOLD = 0.75
    STANDARD_SCORE_THRESHOLD = 0.55
    OPHELIA_MAX_PER_DAY = 2
    STANDARD_MAX_PER_DAY = 5

# Intentar importar motores
SCORER_AVAILABLE = False
try:
    from ophelia_engine import (
        OpheliaScorer, TradeCollector, DailySelector,
        LeverageOptimizer, TemporalAnalyzer, Certifier, ReportGenerator,
    )
    SCORER_AVAILABLE = True
except Exception as e:
    IMPORT_ERRORS.append(f"ophelia_engine: {e}")

DATA_AVAILABLE = False
try:
    from data_engine import DataEngine
    DATA_AVAILABLE = True
except Exception as e:
    IMPORT_ERRORS.append(f"data_engine: {e}")

SIGNAL_AVAILABLE = False
try:
    from signal_engine import Signal
    SIGNAL_AVAILABLE = True
except Exception as e:
    IMPORT_ERRORS.append(f"signal_engine: {e}")


# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
.ophelia-badge {
    background: linear-gradient(135deg, #ffd700 0%, #ff8c00 100%);
    color: #000;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 900;
    font-size: 1.1em;
    display: inline-block;
}
.standard-badge {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: #fff;
    padding: 8px 16px;
    border-radius: 20px;
    font-weight: 700;
    display: inline-block;
}
.rejected-badge {
    background: #e8e8e8;
    color: #666;
    padding: 8px 16px;
    border-radius: 20px;
    display: inline-block;
}
.ophelia-alert {
    background: linear-gradient(135deg, #ffd700 0%, #ff8c00 50%, #ff6b00 100%);
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
    color: #000;
    margin: 15px 0;
    border: 3px solid #ff4500;
}
.ophelia-alert h2 {
    font-size: 2.2em;
    margin: 0 0 20px 0;
    text-align: center;
    font-weight: 900;
    letter-spacing: 2px;
}
.ophelia-table {
    width: 100%;
    font-size: 1.1em;
    border-collapse: collapse;
    margin-top: 15px;
}
.ophelia-table td {
    padding: 10px 15px;
    border-bottom: 1px solid rgba(0,0,0,0.15);
}
.ophelia-table td:first-child {
    font-weight: 600;
    width: 45%;
}
.ophelia-table td:last-child {
    font-family: 'Courier New', monospace;
    font-weight: 700;
}
.no-ophelia {
    background: linear-gradient(135deg, #e8e8e8 0%, #d0d0d0 100%);
    padding: 40px;
    border-radius: 15px;
    text-align: center;
    color: #555;
    margin: 20px 0;
    border: 2px dashed #999;
}
.pre-alert {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    padding: 25px;
    border-radius: 15px;
    border-left: 8px solid #ff9800;
    margin: 15px 0;
}
.countdown {
    font-family: 'Courier New', monospace;
    font-size: 3em;
    font-weight: 900;
    text-align: center;
    color: #ff6b00;
    padding: 20px;
    background: #1a1a1a;
    border-radius: 15px;
    margin: 15px 0;
    letter-spacing: 5px;
}
.big-metric {
    text-align: center;
    padding: 20px;
    background: #fff;
    border-radius: 10px;
    border: 1px solid #e0e0e0;
    margin: 5px 0;
}
.big-metric .label {
    font-size: 0.85em;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.big-metric .value {
    font-size: 2em;
    font-weight: 900;
    color: #333;
    margin: 5px 0;
}
.warning-box {
    background: #fff3cd;
    border-left: 5px solid #ffc107;
    padding: 20px;
    border-radius: 8px;
    margin: 15px 0;
}
.info-box {
    background: #d1ecf1;
    border-left: 5px solid #17a2b8;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPERS
# ============================================================
def get_ar_time():
    try:
        return datetime.now(pytz.timezone(TIMEZONE_AR))
    except Exception:
        return datetime.now()


def format_price(value):
    if value is None or value == 0:
        return "N/A"
    try:
        v = float(value)
        if v >= 1000:
            return f"${v:,.2f}"
        elif v >= 1:
            return f"${v:.4f}"
        elif v >= 0.01:
            return f"${v:.6f}"
        return f"${v:.8f}"
    except Exception:
        return str(value)


def format_duration(minutes):
    if minutes is None:
        return "N/A"
    try:
        m = float(minutes)
        if m < 1:
            return "< 1 min"
        if m < 60:
            return f"{int(m)} min"
        return f"{int(m // 60)}h {int(m % 60)}min"
    except Exception:
        return "N/A"


def load_json_safe(path):
    try:
        p = Path(path)
        if not p.exists():
            return None
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception:
        return None


def load_parquet_safe(path):
    try:
        p = Path(path)
        if not p.exists():
            return None
        return pd.read_parquet(p)
    except Exception:
        return None


def load_pickle_safe(path):
    try:
        import pickle
        p = Path(path)
        if not p.exists():
            return None
        with open(p, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None


# ============================================================
# HEADER
# ============================================================
col_logo, col_title = st.columns([1, 8])
with col_logo:
    st.markdown("# 🌟")
with col_title:
    st.markdown("# OPHELIA Precision Engine")
    st.caption("Score como motor principal · 2 niveles · Ranking completo · 100% real")

ar_now = get_ar_time()
st.markdown(f"**🕐 Hora Argentina:** `{ar_now.strftime('%A, %d/%m/%Y %H:%M:%S')}`")

# Diagnóstico
if IMPORT_ERRORS:
    with st.expander(f"⚠️ {len(IMPORT_ERRORS)} módulos no cargados"):
        for err in IMPORT_ERRORS:
            st.caption(f"• `{err}`")

st.markdown("---")


# ============================================================
# CARGA DE DATOS
# ============================================================
scorer_data = load_pickle_safe(OPHELIA_V2_MODEL)
metadata = load_json_safe(OPHELIA_V2_METADATA)
trades_df = load_parquet_safe(OPHELIA_V2_TRADES)
daily_df = load_parquet_safe(OPHELIA_V2_DAILY)
report_text = None
if Path(OPHELIA_V2_REPORT).exists():
    try:
        report_text = Path(OPHELIA_V2_REPORT).read_text(encoding='utf-8')
    except Exception:
        report_text = None


# ============================================================
# CASO 1: NO HAY MODELO ENTRENADO
# ============================================================
if scorer_data is None or metadata is None:
    st.markdown("""
    <div class="warning-box">
    <h2>⚠️ OPHELIA NO DISPONIBLE</h2>
    <p style="font-size: 1.1em;">No se ha entrenado el OPHELIA Score todavía.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 Cómo activar OPHELIA")
    st.markdown("""
    ### Ejecutá el pipeline:
    ```bash
    python run_ophelia_v2.py
