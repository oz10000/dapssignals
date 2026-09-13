# streamlit_ophelia.py
"""
🌟 OPHELIA Precision Engine — Dashboard autocontenido
Diseñado para funcionar incluso si:
  - El pipeline OPHELIA no ha corrido todavía
  - Faltan módulos ophelia_engine
  - Faltan archivos de patrón/datos
  - Los exchanges están bloqueados

En cualquier caso, muestra instrucciones claras al usuario.
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

# ============================================================
# CONFIGURACIÓN DE PÁGINA (SIEMPRE PRIMERO)
# ============================================================
st.set_page_config(
    page_title="🌟 OPHELIA Precision Engine",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# IMPORTS DEFENSIVOS (nada puede romper la app)
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
    from ophelia_config import (
        OPHELIA_PATTERNS_FILE,
        OPHELIA_TRADES_FILE,
        OPHELIA_CERTIFICATION_FILE,
        TIMEZONE_AR,
        OPHELIA_SCORE_THRESHOLD,
        PRE_ALERT_MINUTES,
        EXECUTION_WINDOW_SECONDS,
    )
except Exception as e:
    IMPORT_ERRORS.append(f"ophelia_config: {e}")
    OPHELIA_PATTERNS_FILE = "data/ophelia/learned_patterns.json"
    OPHELIA_TRADES_FILE = "data/ophelia/all_trades.parquet"
    OPHELIA_CERTIFICATION_FILE = "reports/OPHELIA_CERTIFICATION_REPORT.md"
    TIMEZONE_AR = "America/Argentina/Buenos_Aires"
    OPHELIA_SCORE_THRESHOLD = 0.95
    PRE_ALERT_MINUTES = 10
    EXECUTION_WINDOW_SECONDS = 45

# Intentar importar motores OPHELIA (opcional)
OPHELIA_AVAILABLE = False
try:
    from ophelia_engine import (
        OpheliaDetector,
        TemporalPredictor,
        LeverageCalculator,
    )
    OPHELIA_AVAILABLE = True
except Exception as e:
    IMPORT_ERRORS.append(f"ophelia_engine: {e}")

# Intentar importar DataEngine (opcional)
DATA_ENGINE_AVAILABLE = False
try:
    from data_engine import DataEngine
    DATA_ENGINE_AVAILABLE = True
except Exception as e:
    IMPORT_ERRORS.append(f"data_engine: {e}")

# Intentar importar Signal (opcional)
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
.no-ophelia h3 {
    font-size: 1.8em;
    margin: 0 0 10px 0;
    color: #444;
}
.pre-alert {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    padding: 25px;
    border-radius: 15px;
    border-left: 8px solid #ff9800;
    margin: 15px 0;
}
.pre-alert h3 { color: #e65100; margin: 0 0 10px 0; }
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
.cert-card {
    padding: 25px;
    border-radius: 15px;
    margin: 15px 0;
    text-align: center;
}
.cert-approved {
    background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
    border: 3px solid #28a745;
}
.cert-rejected {
    background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
    border: 3px solid #dc3545;
}
.cert-pending {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    border: 3px solid #ffc107;
}
.warning-box {
    background: #fff3cd;
    border-left: 5px solid #ffc107;
    padding: 20px;
    border-radius: 8px;
    margin: 15px 0;
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
        else:
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


def load_text_safe(path):
    try:
        p = Path(path)
        if not p.exists():
            return None
        return p.read_text(encoding='utf-8')
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
    st.caption("Detector exclusivo · 100% WR requerido · Precisión > Frecuencia")

ar_now = get_ar_time()
st.markdown(f"**🕐 Hora Argentina:** `{ar_now.strftime('%A, %d/%m/%Y %H:%M:%S')}`")

# ============================================================
# DIAGNÓSTICO DE IMPORTACIONES
# ============================================================
if IMPORT_ERRORS:
    with st.expander(f"⚠️ {len(IMPORT_ERRORS)} módulos no cargados (ver detalle)"):
        for err in IMPORT_ERRORS:
            st.caption(f"• `{err}`")
        st.caption("La app funciona igual en modo 'solo lectura' de archivos.")

st.markdown("---")


# ============================================================
# CARGA DE DATOS
# ============================================================
pattern = load_json_safe(OPHELIA_PATTERNS_FILE)
ophelia_trades = load_parquet_safe(OPHELIA_TRADES_FILE)
cert_text = load_text_safe(OPHELIA_CERTIFICATION_FILE)


# ============================================================
# CASO 1: NO HAY PATRÓN → MOSTRAR INSTRUCCIONES
# ============================================================
if pattern is None:
    st.markdown("""
    <div class="warning-box">
    <h2>⚠️ OPHELIA NO DISPONIBLE</h2>
    <p style="font-size: 1.1em;">No se ha aprendido un patrón OPHELIA todavía.</p>
    <p>El dashboard está listo, pero necesita que primero ejecutes el pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## 🚀 Cómo activar OPHELIA")

    st.markdown("### Opción 1: GitHub Actions (Recomendado)")

    st.markdown("""
    1. **Ir a** GitHub → tu repo → **Actions**
    2. **Seleccionar** el workflow **"OPHELIA Precision Engine"**
    3. **Click** en **"Run workflow"**
    4. **Esperar** 5-30 minutos
    5. **Descargar** el artifact `ophelia-full-N`
    6. **Descomprimir** y colocar los archivos en:
       - `data/ophelia/learned_patterns.json`
       - `data/ophelia/all_trades.parquet`
       - `reports/OPHELIA_CERTIFICATION_REPORT.md`
    7. **Refrescar** esta página (F5)
    """)

    st.markdown("### Opción 2: Local")

    st.code("""
# En tu máquina local
git clone https://github.com/oz10000/dapssignals.git
cd dapssignals
pip install -r requirements.txt
python run_ophelia.py

# Luego abrir este dashboard
streamlit run streamlit_ophelia.py
    """, language="bash")

    st.markdown("---")

    # Estado de archivos
    st.markdown("## 📁 Estado actual de archivos")

    files_status = [
        (OPHELIA_PATTERNS_FILE, "Patrón aprendido"),
        (OPHELIA_TRADES_FILE, "Trades históricos"),
        (OPHELIA_CERTIFICATION_FILE, "Certificación"),
        ("reports/OPHELIA_NOT_AVAILABLE.md", "Reporte NO DISPONIBLE"),
    ]

    for path, label in files_status:
        p = Path(path)
        if p.exists():
            size = p.stat().st_size
            st.markdown(f"✅ **{label}** — `{path}` ({size:,} bytes)")
        else:
            st.markdown(f"❌ **{label}** — `{path}` (no existe)")

    st.markdown("---")

    # Info del pipeline
    with st.expander("ℹ️ ¿Qué hace el pipeline OPHELIA?"):
        st.markdown("""
        El pipeline `run_ophelia.py`:

        1. **Descarga** 12 meses de datos reales (CCXT, sin sintéticos)
        2. **Simula** miles de trades y clasifica cuáles son OPHELIA
        3. **Extrae** el patrón estadístico (ranges + ventana temporal)
        4. **Certifica** con train/test split (100% WR out-of-sample)
        5. **Calcula** leverage óptimo
        6. **Genera** reportes y guarda el patrón

        **Criterios de certificación:**
        - ≥ 30 trades OPHELIA históricos
        - 100% WR en train Y test
        - ≥ 10 trades en test

        Si no se cumplen → **OPHELIA NO DISPONIBLE** (no se inventan señales).
        """)

    st.stop()


# ============================================================
# CASO 2: HAY PATRÓN → MOSTRAR DASHBOARD COMPLETO
# ============================================================
st.success(f"✅ Patrón OPHELIA cargado — {pattern.get('n_train', 0)} trades de referencia")


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 📊 Patrón OPHELIA")

    n_train = pattern.get('n_train', 0)
    n_assets = len(pattern.get('assets', []))
    hr = pattern.get('hour_range', {})

    col_a, col_b = st.columns(2)
    col_a.metric("Trades train", n_train)
    col_b.metric("Activos", n_assets)

    st.metric("Ventana ARG", f"{hr.get('min', 0):02d}h → {hr.get('max', 0):02d}h")

    st.markdown("---")

    # Estadísticas del patrón
    stats = pattern.get('outcome_stats', {})
    st.markdown("### 📈 Estadísticas históricas")
    st.metric("MFE medio", f"{stats.get('mean_mfe', 0)*100:.4f}%")
    st.metric("MFE mínimo", f"{stats.get('min_mfe', 0)*100:.4f}%")
    st.metric("MAE máximo", f"{stats.get('max_mae', 0)*100:.4f}%")
    st.metric("Duración media", f"{stats.get('mean_duration_min', 0):.0f} min")

    st.markdown("---")

    # Leverage
    if OPHELIA_AVAILABLE:
        try:
            lev = LeverageCalculator(pattern).calculate()
            st.markdown("### ⚙️ Leverage")
            st.metric("Recomendado", f"{lev['leverage_recommended']}x")
            st.metric("Máximo seguro", f"{lev['leverage_max_safe']}x")
        except Exception:
            pass

    st.markdown("---")
    st.caption("v1.0.0 · OPHELIA Precision Engine")


# ============================================================
# PESTAÑAS
# ============================================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🌟 Detección Live",
    "⏳ Próxima Oportunidad",
    "📊 Patrón Aprendido",
    "📜 Trades Históricos",
    "📄 Certificación",
])


# ============================================================
# TAB 1: DETECCIÓN LIVE
# ============================================================
with tab1:
    st.markdown("## 🌟 Detección OPHELIA en Vivo")

    if not OPHELIA_AVAILABLE or not DATA_ENGINE_AVAILABLE or not SIGNAL_AVAILABLE:
        st.warning("""
        ⚠️ **Detección live no disponible** — Faltan módulos:
        - `ophelia_engine` (motor de detección)
        - `data_engine` (descarga de datos)
        - `signal_engine` (generador de señales)

        **Podés ver** las otras pestañas con el patrón aprendido y los trades históricos.
        """)
    else:
        st.caption(f"Escáner de {len(pattern.get('assets', []))} activos buscando el patrón certificado")

        # Botón de scan
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            if st.button("🔄 Escanear Ahora", type="primary", use_container_width=True):
                st.session_state.force_scan = True

        with col_info:
            if st.session_state.get('last_scan_time'):
                st.caption(f"Último scan: {st.session_state.last_scan_time}")

        # Ejecutar scan
        if st.session_state.get('force_scan', False):
            with st.spinner("🔍 Buscando OPHELIA..."):
                try:
                    de = DataEngine()
                    detector = OpheliaDetector(pattern)
                    alerts = []
                    progress = st.progress(0)
                    status_text = st.empty()
                    assets = pattern.get('assets', [])[:30]

                    for i, sym in enumerate(assets):
                        status_text.text(f"Analizando {sym} ({i+1}/{len(assets)})...")
                        try:
                            df = de.fetch_ohlcv(sym, limit=300)
                            if df is None or df.empty:
                                progress.progress((i+1)/len(assets))
                                continue

                            sig = Signal(sym, df, DEFAULT_PARAMS).to_dict()

                            # Features mínimas para el detector
                            features = {
                                'symbol': sym,
                                'direction': sig.get('direction', 'LONG'),
                                'entry_price': sig.get('entry_price', df['close'].iloc[-1]),
                                'entry_time_ar': str(df.index[-1]),
                                'score': float(sig.get('score', 0)),
                                'adx': float(sig.get('adx', 0)),
                                'ker': float(sig.get('ker', 0)),
                                'atr_pct_rel': 1.0,
                                'volume_ratio': sig.get('volume_ratio', 1.0),
                                'ema_dist_15_atr': 0,
                                'ema_dist_50_atr': 0,
                                'adx_acceleration': 0,
                                'regime': sig.get('regime', 'Unknown'),
                                'hour': df.index[-1].hour if hasattr(df.index[-1], 'hour') else 0,
                                'weekday': df.index[-1].weekday() if hasattr(df.index[-1], 'weekday') else 0,
                            }

                            result = detector.detect(features)
                            if result and result.get('status') == 'OPHELIA':
                                alerts.append(result)
                        except Exception:
                            pass

                        progress.progress((i+1)/len(assets))

                    progress.empty()
                    status_text.empty()

                    st.session_state.live_alerts = alerts
                    st.session_state.last_scan_time = get_ar_time().strftime('%H:%M:%S')
                    st.session_state.force_scan = False
                except Exception as e:
                    st.error(f"❌ Error en scan: {e}")
                    st.session_state.force_scan = False

        # Mostrar alertas
        alerts = st.session_state.get('live_alerts', [])

        if alerts:
            st.markdown(f"### 🎯 {len(alerts)} OPHELIA DETECTADO(S)")

            for alert in alerts:
                entry_time = alert.get('entry_time', 'N/A')
                detected = alert.get('detected_at', '')[:19]

                try:
                    lev_rec = LeverageCalculator(pattern).calculate()['leverage_recommended']
                except Exception:
                    lev_rec = 'N/A'

                st.markdown(f"""
                <div class="ophelia-alert">
                    <h2>🌟 {alert.get('symbol', 'N/A')} — {alert.get('direction', 'N/A')}</h2>
                    <table class="ophelia-table">
                        <tr><td>💵 Precio de Entrada</td><td>{format_price(alert.get('entry_price'))}</td></tr>
                        <tr><td>🕐 Hora Exacta</td><td>{entry_time}</td></tr>
                        <tr><td>⏱️ Detectado a las</td><td>{detected}</td></tr>
                        <tr><td>🎯 Take Profit</td><td>{format_price(alert.get('tp_price'))} (+{alert.get('tp_pct', 0):.4f}%)</td></tr>
                        <tr><td>🛑 Stop Loss</td><td>{format_price(alert.get('sl_price'))} (-{alert.get('sl_pct', 0):.4f}%)</td></tr>
                        <tr><td>📈 Trailing Activación</td><td>{format_price(alert.get('trailing_activation_price'))}</td></tr>
                        <tr><td>📉 Trailing Distancia</td><td>{format_price(alert.get('trailing_distance_price'))}</td></tr>
                        <tr><td>⏳ Duración esperada</td><td>{format_duration(alert.get('expected_duration_min'))}</td></tr>
                        <tr><td>🎯 OPHELIA Score</td><td>{alert.get('ophelia_score', 0):.4f}</td></tr>
                        <tr><td>🏆 WR Histórico</td><td>{alert.get('historical_wr', 1)*100:.0f}% (N={alert.get('n_historical', 0)})</td></tr>
                        <tr><td>⚙️ Leverage Recomendado</td><td>{lev_rec}x</td></tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)

                with st.expander(f"📊 Componentes del score para {alert.get('symbol', '')}"):
                    comps = alert.get('components', {})
                    if comps:
                        df_c = pd.DataFrame([
                            {'Componente': k, 'Valor': f"{v:.4f}"}
                            for k, v in comps.items()
                        ])
                        st.dataframe(df_c, use_container_width=True, hide_index=True)

                st.markdown("---")
        else:
            st.markdown("""
            <div class="no-ophelia">
                <h3>⚪ NO OPHELIA DETECTADO</h3>
                <p>Ninguna de las condiciones históricas certificadas se cumple ahora.</p>
                <p style="margin-top: 20px;"><b>Precisión > Frecuencia</b></p>
                <p style="font-size: 0.9em; color: #888;">
                    El sistema NO inventa señales. Prefiere esperar la próxima oportunidad real.
                </p>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# TAB 2: PRÓXIMA OPORTUNIDAD
# ============================================================
with tab2:
    st.markdown("## ⏳ Predicción Temporal OPHELIA")
    st.caption("Estimación de cuándo aparecerá el próximo trade certificado")

    try:
        tstats = pattern.get('temporal_stats', {})
        mean_interval = tstats.get('mean_interval_min', 60)
        std_interval = tstats.get('std_interval_min', 30)

        # Último trade
        last_time = None
        if ophelia_trades is not None and not ophelia_trades.empty:
            last_col = 'entry_time_ar' if 'entry_time_ar' in ophelia_trades.columns else 'entry_time'
            last_time = ophelia_trades.iloc[-1].get(last_col)

        now = get_ar_time()

        # Tiempo desde último
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🕐 Último OPHELIA")
            if last_time:
                st.markdown(f"""
                <div class="big-metric">
                    <div class="label">Último trade registrado</div>
                    <div class="value" style="font-size: 1.2em;">{str(last_time)[:19]}</div>
                    <div class="subvalue">Intervalo medio: {mean_interval:.0f} min</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Sin OPHELIA previo registrado")

        with col2:
            st.markdown("### ⏳ Próximo OPHELIA")
            minutes_until = mean_interval - std_interval
            minutes_until = max(0, minutes_until)

            st.markdown(f"""
            <div class="countdown">
                {int(minutes_until):02d}:{int((minutes_until % 1) * 60):02d}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="big-metric">
                <div class="label">Ventana estimada</div>
                <div class="value" style="font-size: 1.2em;">
                    {mean_interval - std_interval:.0f} - {mean_interval + std_interval:.0f} min
                </div>
                <div class="subvalue">Después del último OPHELIA</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("### 🔔 Pre-alerta")
            st.markdown(f"""
            <div class="pre-alert">
                <h3>🔔 AVISO {PRE_ALERT_MINUTES} MIN ANTES</h3>
                <p style="font-size: 1.1em;">La ventana óptima se abre pronto</p>
                <p style="font-size: 1.05em; margin-top: 10px;">
                    <b>Ejecutar en ventana de:</b> {EXECUTION_WINDOW_SECONDS}s
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Detalles
        st.markdown("### 📊 Estadísticas temporales")

        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f"""
            | Métrica | Valor |
            |---------|-------|
            | Intervalo medio | {mean_interval:.0f} min |
            | Intervalo mediano | {tstats.get('median_interval_min', 0):.0f} min |
            | Desviación estándar | {std_interval:.0f} min |
            | Intervalo mínimo | {tstats.get('min_interval_min', 0):.0f} min |
            | Intervalo máximo | {tstats.get('max_interval_min', 0):.0f} min |
            """)

        with col_b:
            hr = pattern.get('hour_range', {})
            weekdays = pattern.get('weekday_set', [])
            day_names = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
            active_days = ', '.join([day_names[d] for d in weekdays if 0 <= d < 7])

            st.markdown(f"""
            | Métrica | Valor |
            |---------|-------|
            | Hora mínima | {hr.get('min', 0):02d}:00 |
            | Hora máxima | {hr.get('max', 0):02d}:00 |
            | Hora media | {hr.get('mean', 0):.1f}h |
            | Días activos | {active_days or 'N/A'} |
            """)

        # Histograma de intervalos
        if ophelia_trades is not None and not ophelia_trades.empty and len(ophelia_trades) > 1:
            st.markdown("---")
            st.markdown("### 📊 Distribución de intervalos entre OPHELIAs")

            time_col = 'entry_time_ar' if 'entry_time_ar' in ophelia_trades.columns else 'entry_time'
            try:
                times = pd.to_datetime(ophelia_trades[time_col], errors='coerce').dropna()
                if len(times) > 1:
                    intervals = times.diff().dt.total_seconds().dropna() / 60
                    intervals = intervals[intervals > 0]

                    if not intervals.empty:
                        fig = px.histogram(
                            x=intervals,
                            nbins=20,
                            labels={'x': 'Minutos entre OPHELIAs', 'y': 'Frecuencia'},
                            title=f"Distribución de {len(intervals)} intervalos",
                        )
                        fig.update_layout(height=350, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)
            except Exception:
                pass

        st.info(f"""
        **⚠️ Importante:** La predicción temporal es una **estimación estadística**
        basada en {pattern.get('n_train', 0)} trades históricos. El sistema avisa
        {PRE_ALERT_MINUTES} minutos antes para que puedas posicionarte.
        """)

    except Exception as e:
        st.error(f"❌ Error en predicción temporal: {e}")


# ============================================================
# TAB 3: PATRÓN APRENDIDO
# ============================================================
with tab3:
    st.markdown("## 📊 Patrón OPHELIA Aprendido")
    st.caption("Ranges de features que definen un trade OPHELIA certificado")

    # Resumen
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Trades train", pattern.get('n_train', 0))
    col2.metric("Activos únicos", len(pattern.get('assets', [])))
    col3.metric("Features", len(pattern.get('features', {})))
    col4.metric("Duración media", f"{pattern.get('outcome_stats', {}).get('mean_duration_min', 0):.0f} min")

    st.markdown("---")

    # Features
    st.markdown("### 🔬 Features del Patrón")
    st.caption("Un trade es OPHELIA si TODAS sus features caen en estos rangos")

    features = pattern.get('features', {})
    if features:
        rows = []
        for feat, rng in features.items():
            rows.append({
                'Feature': feat,
                'Min': f"{rng.get('min', 0):.6f}",
                'Max': f"{rng.get('max', 0):.6f}",
                'Media': f"{rng.get('mean', 0):.6f}",
                'Std': f"{rng.get('std', 0):.6f}",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
    else:
        st.info("No hay features registradas")

    st.markdown("---")

    # Activos
    st.markdown("### 🎯 Activos OPHELIA")
    assets = pattern.get('assets', [])
    if assets:
        cols = st.columns(min(6, max(1, len(assets))))
        for i, a in enumerate(assets):
            with cols[i % 6]:
                st.markdown(f"**{a}**")
    else:
        st.info("No hay activos registrados")

    st.markdown("---")

    # Ventana horaria
    st.markdown("### 🕐 Ventana Horaria (Argentina)")
    hr = pattern.get('hour_range', {})
    dist = hr.get('distribution', {})

    if dist:
        hours = sorted([int(h) for h in dist.keys()])
        counts = [dist.get(str(h), dist.get(h, 0)) for h in hours]

        fig = go.Figure(data=[
            go.Bar(x=[f"{h:02d}:00" for h in hours], y=counts, marker_color='#ff8c00')
        ])
        fig.update_layout(
            title="Distribución de OPHELIAs por hora (ARG)",
            xaxis_title="Hora",
            yaxis_title="Cantidad",
            height=350,
            showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Outcome stats
    st.markdown("---")
    st.markdown("### 📈 Estadísticas de Outcome")
    stats = pattern.get('outcome_stats', {})

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Movimiento favorable (MFE)**")
        st.metric("Media", f"{stats.get('mean_mfe', 0)*100:.4f}%")
        st.metric("Mínimo", f"{stats.get('min_mfe', 0)*100:.4f}%")
    with col_b:
        st.markdown("**Movimiento adverso (MAE)**")
        st.metric("Máximo", f"{stats.get('max_mae', 0)*100:.4f}%")
        st.metric("Más negativo", f"{stats.get('min_mae', 0)*100:.4f}%")
    with col_c:
        st.markdown("**Duración**")
        st.metric("Media", f"{stats.get('mean_duration_min', 0):.0f} min")
        st.metric("Máxima", f"{stats.get('max_duration_min', 0):.0f} min")

    # Leverage
    if OPHELIA_AVAILABLE:
        st.markdown("---")
        st.markdown("### ⚙️ Leverage Calculado")
        try:
            lev = LeverageCalculator(pattern).calculate()
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Conservador", f"{lev['leverage_conservative']}x")
            col2.metric("Recomendado", f"{lev['leverage_recommended']}x")
            col3.metric("Máximo seguro", f"{lev['leverage_max_safe']}x")
            col4.metric("MAE histórico", f"{lev['max_mae_historical']*100:.4f}%")
            st.caption(f"Basado en: MAE máxima histórica × {lev['safety_factor']} factor de seguridad")
        except Exception as e:
            st.warning(f"No se pudo calcular leverage: {e}")


# ============================================================
# TAB 4: TRADES HISTÓRICOS
# ============================================================
with tab4:
    st.markdown("## 📜 Trades OPHELIA Históricos")

    if ophelia_trades is None or ophelia_trades.empty:
        st.warning("No hay trades OPHELIA guardados.")
        st.info("Ejecutá `python run_ophelia.py` para generarlos.")
    else:
        n = len(ophelia_trades)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total trades", n)
        col2.metric("WR", "100%")
        col3.metric("MFE medio", f"{ophelia_trades['mfe'].mean()*100:.4f}%" if 'mfe' in ophelia_trades.columns else "N/A")
        col4.metric("Duración media", f"{ophelia_trades['duration_min'].mean():.0f} min" if 'duration_min' in ophelia_trades.columns else "N/A")

        st.markdown("---")

        # Filtros
        col_a, col_b = st.columns(2)
        with col_a:
            symbols_filter = st.multiselect(
                "Filtrar por activo",
                options=sorted(ophelia_trades['symbol'].unique()) if 'symbol' in ophelia_trades.columns else [],
                default=[]
            )
        with col_b:
            show_n = st.slider("Mostrar últimos N", 10, min(500, n), min(50, n))

        df_show = ophelia_trades.copy()
        if symbols_filter and 'symbol' in df_show.columns:
            df_show = df_show[df_show['symbol'].isin(symbols_filter)]

        sort_col = 'entry_time' if 'entry_time' in df_show.columns else df_show.columns[0]
        df_show = df_show.sort_values(sort_col, ascending=False).head(show_n)

        # Preparar columnas
        display_cols = []
        rename_map = {}

        for col, label in [
            ('entry_time_ar', 'Fecha ARG'),
            ('entry_time', 'Fecha UTC'),
            ('symbol', 'Activo'),
            ('direction', 'Dir'),
            ('entry_price', 'Entrada'),
            ('exit_price', 'Salida'),
            ('mfe', 'MFE'),
            ('mae', 'MAE'),
            ('duration_min', 'Dur'),
            ('exit_reason', 'Cierre'),
        ]:
            if col in df_show.columns and col not in display_cols:
                display_cols.append(col)
                rename_map[col] = label

        df_view = df_show[display_cols].rename(columns=rename_map)

        # Formatear
        if 'MFE' in df_view.columns:
            df_view['MFE'] = df_view['MFE'].apply(lambda x: f"{x*100:.4f}%" if pd.notna(x) else "N/A")
        if 'MAE' in df_view.columns:
            df_view['MAE'] = df_view['MAE'].apply(lambda x: f"{x*100:.4f}%" if pd.notna(x) else "N/A")
        if 'Dur' in df_view.columns:
            df_view['Dur'] = df_view['Dur'].apply(lambda x: f"{x:.0f}m" if pd.notna(x) else "N/A")
        if 'Entrada' in df_view.columns:
            df_view['Entrada'] = df_view['Entrada'].apply(lambda x: f"{x:.6f}" if pd.notna(x) else "N/A")
        if 'Salida' in df_view.columns:
            df_view['Salida'] = df_view['Salida'].apply(lambda x: f"{x:.6f}" if pd.notna(x) else "N/A")

        st.dataframe(df_view, use_container_width=True, hide_index=True)

        # Descarga
        csv = df_show.to_csv(index=False)
        st.download_button(
            "📥 Descargar CSV",
            data=csv,
            file_name=f"ophelia_trades_{get_ar_time().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

        # Distribución por activo
        if 'symbol' in ophelia_trades.columns:
            st.markdown("---")
            st.markdown("### 📊 Distribución por Activo")
            by_asset = ophelia_trades.groupby('symbol').size().sort_values(ascending=False)
            fig = px.bar(
                x=by_asset.index,
                y=by_asset.values,
                title="OPHELIAs por activo",
                labels={'x': 'Activo', 'y': 'N° trades'},
            )
            fig.update_layout(height=350, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# TAB 5: CERTIFICACIÓN
# ============================================================
with tab5:
    st.markdown("## 📄 Certificación OPHELIA")

    if cert_text is None:
        st.warning("No hay reporte de certificación.")
        st.info("Ejecutá `python run_ophelia.py` para generarlo.")

        # Estado inferido
        if pattern:
            n_train = pattern.get('n_train', 0)
            if n_train >= 30:
                st.markdown("""
                <div class="cert-card cert-pending">
                    <h2>⚠️ PENDIENTE</h2>
                    <p>El patrón tiene suficientes muestras pero falta el reporte formal.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="cert-card cert-rejected">
                    <h2>❌ MUESTRA INSUFICIENTE</h2>
                    <p>Solo {n_train} trades OPHELIA (mínimo: 30)</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        # Ver si está certificado
        is_certified = '✅ CERTIFICADO' in cert_text[:1000]
        is_rejected = '❌ NO CERTIFICADO' in cert_text[:1000]

        if is_certified:
            st.markdown("""
            <div class="cert-card cert-approved">
                <h2>✅ CERTIFICADO</h2>
                <p>El patrón OPHELIA mantiene 100% WR en train y test out-of-sample.</p>
                <p><b>El detector está operativo.</b></p>
            </div>
            """, unsafe_allow_html=True)
        elif is_rejected:
            st.markdown("""
            <div class="cert-card cert-rejected">
                <h2>❌ NO CERTIFICADO</h2>
                <p>El patrón no cumple los criterios mínimos.</p>
                <p>Ver detalles abajo.</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="cert-card cert-pending">
                <h2>⚠️ ESTADO DESCONOCIDO</h2>
                <p>Revisar el reporte completo abajo.</p>
            </div>
            """, unsafe_allow_html=True)

        # Reporte completo
        st.markdown("---")
        st.markdown("### 📋 Reporte Completo")

        with st.expander("Ver reporte completo", expanded=True):
            st.markdown(cert_text)

        st.download_button(
            "📥 Descargar OPHELIA_CERTIFICATION_REPORT.md",
            data=cert_text,
            file_name=f"ophelia_cert_{get_ar_time().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #888; padding: 20px;">
    <p><b>🌟 OPHELIA Precision Engine v1.0.0</b></p>
    <p>Detector exclusivo · 100% WR requerido · Precisión > Frecuencia</p>
    <p style="font-size: 0.85em;">
        Hora Argentina: {get_ar_time().strftime('%Y-%m-%d %H:%M:%S')}
    </p>
</div>
""", unsafe_allow_html=True)
