
# streamlit_ophelia.py
"""
🌟 OPHELIA Precision Engine — Dashboard
Detector exclusivo de trades OPHELIA con:
  - Detección en vivo con hora:minuto:segundo
  - Predicción de próxima oportunidad
  - Pre-alerta (X minutos antes)
  - TP/SL/Trailing calculados
  - Leverage recomendado
  - Estadísticas del patrón aprendido
  - Certificación out-of-sample
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime, timedelta
import json
import time
import pytz

# ============================================================
# IMPORTS DEL PROYECTO
# ============================================================
from data_engine import DataEngine
from signal_engine import Signal
from config import DEFAULT_PARAMS, SYMBOLS, INITIAL_CAPITAL

from ophelia_config import (
    OPHELIA_PATTERNS_FILE,
    OPHELIA_TRADES_FILE,
    OPHELIA_CERTIFICATION_FILE,
    OPHELIA_LIVE_ALERTS_FILE,
    TIMEZONE_AR,
    OPHELIA_SCORE_THRESHOLD,
    PRE_ALERT_MINUTES,
    EXECUTION_WINDOW_SECONDS,
    LEVERAGE_PROFILE,
)

# Intentar importar motores OPHELIA
try:
    from ophelia_engine import (
        OpheliaDetector,
        TemporalPredictor,
        LeverageCalculator,
        OpheliaCertifier,
    )
    OPHELIA_AVAILABLE = True
except ImportError as e:
    OPHELIA_AVAILABLE = False
    OPHELIA_IMPORT_ERROR = str(e)


# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="🌟 OPHELIA Precision Engine",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# ESTILOS
# ============================================================
st.markdown("""
<style>
/* Alerta OPHELIA principal */
.ophelia-alert {
    background: linear-gradient(135deg, #ffd700 0%, #ff8c00 50%, #ff6b00 100%);
    padding: 35px;
    border-radius: 20px;
    box-shadow: 0 0 40px rgba(255, 215, 0, 0.6);
    color: #000;
    margin: 15px 0;
    border: 3px solid #ff4500;
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.4); }
    50% { box-shadow: 0 0 50px rgba(255, 215, 0, 0.9); }
    100% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.4); }
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
    font-size: 1.15em;
    border-collapse: collapse;
    margin-top: 15px;
}
.ophelia-table td {
    padding: 10px 15px;
    border-bottom: 1px solid rgba(0,0,0,0.15);
}
.ophelia-table td:first-child {
    font-weight: 600;
    width: 40%;
}
.ophelia-table td:last-child {
    font-family: 'Courier New', monospace;
    font-weight: 700;
    font-size: 1.05em;
}

/* No OPHELIA */
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
.no-ophelia p {
    font-size: 1.1em;
    margin: 5px 0;
}

/* Pre-alerta */
.pre-alert {
    background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
    padding: 25px;
    border-radius: 15px;
    border-left: 8px solid #ff9800;
    margin: 15px 0;
}
.pre-alert h3 { color: #e65100; margin: 0 0 10px 0; }

/* Countdown */
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

/* Métricas grandes */
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
.big-metric .subvalue {
    font-size: 0.9em;
    color: #888;
}

/* Cards de certificación */
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
.cert-card h2 { margin: 0 0 10px 0; font-size: 2em; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
}
.stTabs [data-baseweb="tab"] {
    padding: 12px 24px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def get_ar_time():
    """Retorna el datetime actual en zona horaria Argentina."""
    return datetime.now(pytz.timezone(TIMEZONE_AR))


def format_price(value, decimals=6):
    """Formatea precio con decimales apropiados."""
    if value is None or value == 0:
        return "N/A"
    if value >= 1000:
        return f"${value:,.2f}"
    elif value >= 1:
        return f"${value:.4f}"
    elif value >= 0.01:
        return f"${value:.6f}"
    else:
        return f"${value:.8f}"


def format_duration(minutes):
    """Formatea minutos como Xh Ym."""
    if minutes is None:
        return "N/A"
    if minutes < 1:
        return "< 1 min"
    if minutes < 60:
        return f"{int(minutes)} min"
    h = int(minutes // 60)
    m = int(minutes % 60)
    return f"{h}h {m}min"


def load_pattern():
    """Carga el patrón OPHELIA si existe."""
    p = Path(OPHELIA_PATTERNS_FILE)
    if not p.exists():
        return None
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


def load_ophelia_trades():
    """Carga los trades OPHELIA históricos."""
    p = Path(OPHELIA_TRADES_FILE)
    if not p.exists():
        return None
    try:
        return pd.read_parquet(p)
    except Exception:
        return None


def load_certification():
    """Carga el reporte de certificación (texto)."""
    p = Path(OPHELIA_CERTIFICATION_FILE)
    if not p.exists():
        return None
    try:
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
    st.caption(f"Detector exclusivo · 100% WR requerido · Precisión > Frecuencia")

ar_now = get_ar_time()
st.markdown(f"**🕐 Hora Argentina:** `{ar_now.strftime('%A, %d/%m/%Y %H:%M:%S')}`")
st.markdown("---")


# ============================================================
# ESTADO INICIAL
# ============================================================
if 'data_engine' not in st.session_state:
    with st.spinner("Inicializando DataEngine..."):
        try:
            st.session_state.data_engine = DataEngine()
        except Exception as e:
            st.error(f"❌ Error inicializando DataEngine: {e}")
            st.stop()

if 'live_alerts' not in st.session_state:
    st.session_state.live_alerts = []

if 'last_scan_time' not in st.session_state:
    st.session_state.last_scan_time = None

if 'force_scan' not in st.session_state:
    st.session_state.force_scan = True

if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = False


# ============================================================
# VERIFICACIÓN DE OPHELIA DISPONIBLE
# ============================================================
if not OPHELIA_AVAILABLE:
    st.error("❌ **Módulos OPHELIA no disponibles**")
    st.code(f"Error: {OPHELIA_IMPORT_ERROR}")
    st.info("""
    **Solución:**
    Asegurate de tener los módulos en `ophelia_engine/`:
    - `__init__.py`
    - `pattern_extractor.py`
    - `trade_simulator.py`
    - `ophelia_detector.py`
    - `temporal_predictor.py`
    - `leverage_calculator.py`
    - `certification.py`
    - `report_generator.py`
    """)
    st.stop()


pattern = load_pattern()

if pattern is None:
    st.warning("⚠️ **OPHELIA NO DISPONIBLE** — No se ha aprendido un patrón todavía.")
    st.markdown("""
    ### ¿Qué hacer?

    Para activar el detector OPHELIA, ejecutá primero el pipeline de aprendizaje:

    ```bash
    python run_ophelia.py
    ```

    Este comando:
    1. Descarga **12 meses** de datos históricos reales (CCXT, sin sintéticos)
    2. Simula **miles de trades** y clasifica cuáles son OPHELIA
    3. Extrae el **patrón estadístico** (ranges por feature + ventana temporal)
    4. Certifica con **train/test split** (100% WR en ambos = certificado)
    5. Genera reportes y guarda el patrón

    **Duración:** 5-30 minutos según cantidad de activos.

    ---

    ### Requisitos mínimos para certificar

    | Requisito | Valor |
    |-----------|-------|
    | Trades OPHELIA históricos | ≥ 30 |
    | Win Rate train | 100% |
    | Win Rate test | 100% |
    | N test | ≥ 10 |

    **Si no se cumplen → OPHELIA NO DISPONIBLE** (no se inventan señales).
    """)

    # Botón de diagnóstico
    with st.expander("🔧 Diagnóstico rápido"):
        st.markdown("**Estado de archivos:**")
        for f in [OPHELIA_PATTERNS_FILE, OPHELIA_TRADES_FILE, OPHELIA_CERTIFICATION_FILE]:
            p = Path(f)
            status = "✅" if p.exists() else "❌"
            st.caption(f"{status} `{f}`")

    st.stop()


# ============================================================
# PATRÓN CARGADO — MOSTRAR DASHBOARD COMPLETO
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

    st.metric("Ventana ARG", f"{hr.get('min', 0)}h → {hr.get('max', 0)}h")

    st.markdown("---")

    # Estadísticas del patrón
    stats = pattern.get('outcome_stats', {})
    st.markdown("### 📈 Estadísticas históricas")
    st.metric("MFE medio", f"{stats.get('mean_mfe', 0)*100:.4f}%")
    st.metric("MFE mínimo", f"{stats.get('min_mfe', 0)*100:.4f}%")
    st.metric("MAE máximo", f"{stats.get('max_mae', 0)*100:.4f}%")
    st.metric("Duración media", f"{stats.get('mean_duration_min', 0):.0f} min")

    st.markdown("---")

    # Controles
    st.markdown("### ⚙️ Control")

    if st.button("🔄 Escanear Ahora", type="primary", use_container_width=True):
        st.session_state.force_scan = True
        st.rerun()

    auto = st.checkbox("⚡ Auto-refresh (30s)", value=st.session_state.auto_refresh)
    if auto != st.session_state.auto_refresh:
        st.session_state.auto_refresh = auto
        st.rerun()

    if st.session_state.last_scan_time:
        st.caption(f"Último scan: {st.session_state.last_scan_time}")

    st.markdown("---")

    # Leverage rápido
    try:
        lev = LeverageCalculator(pattern).calculate()
        st.markdown("### ⚙️ Leverage")
        st.metric("Recomendado", f"{lev['leverage_recommended']}x")
        st.metric("Máximo seguro", f"{lev['leverage_max_safe']}x")
    except Exception:
        pass

    st.markdown("---")
    st.caption(f"v1.0.0 · OPHELIA Precision Engine")


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
    st.caption(f"Escaner de {len(pattern.get('assets', []))} activos buscando el patrón certificado")

    # Ejecutar scan
    if st.session_state.force_scan or st.session_state.last_scan_time is None:
        with st.spinner("🔍 Buscando OPHELIA en el mercado actual..."):
            try:
                de = st.session_state.data_engine
                detector = OpheliaDetector(pattern)

                alerts = []
                scanned = []
                progress = st.progress(0)
                status = st.empty()

                assets = pattern.get('assets', [])[:30]

                for i, sym in enumerate(assets):
                    status.text(f"Analizando {sym} ({i+1}/{len(assets)})...")
                    try:
                        df = de.fetch_ohlcv(sym, limit=300)
                        if df is None or df.empty:
                            progress.progress((i+1)/len(assets))
                            continue

                        # Generar señal actual
                        sig = Signal(sym, df, DEFAULT_PARAMS).to_dict()

                        # Capturar features (mismo formato que el extractor)
                        from core_engine import (
                            compute_adx, compute_atr, compute_ema
                        )

                        close = df['close'].iloc[-1]
                        adx_series = compute_adx(df)
                        atr_series = compute_atr(df)

                        if len(adx_series) < 4 or len(atr_series) < 50:
                            progress.progress((i+1)/len(assets))
                            continue

                        adx = float(adx_series.iloc[-1])
                        adx_3_ago = float(adx_series.iloc[-4])
                        atr = float(atr_series.iloc[-1])
                        atr_ma = float(atr_series.iloc[-50:].mean())
                        ema15 = float(compute_ema(df, 15).iloc[-1])
                        ema50 = float(compute_ema(df, 50).iloc[-1])

                        atr_pct = atr / close if close > 0 else 0
                        atr_pct_rel = atr / atr_ma if atr_ma > 0 else 1.0
                        avg_vol = df['volume'].iloc[-20:].mean()
                        vol_ratio = df['volume'].iloc[-1] / avg_vol if avg_vol > 0 else 1.0

                        # Hora Argentina
                        bar_time = df.index[-1]
                        try:
                            if bar_time.tz is None:
                                bar_time_ar = bar_time.tz_localize('UTC').tz_convert(TIMEZONE_AR)
                            else:
                                bar_time_ar = bar_time.tz_convert(TIMEZONE_AR)
                        except Exception:
                            bar_time_ar = bar_time

                        features = {
                            'symbol': sym,
                            'direction': sig.get('direction', 'LONG'),
                            'entry_price': close,
                            'entry_time_ar': bar_time_ar.strftime('%Y-%m-%d %H:%M:%S'),
                            'score': float(sig.get('score', 0)),
                            'adx': adx,
                            'ker': float(sig.get('ker', 0)),
                            'atr_pct': atr_pct,
                            'atr_pct_rel': atr_pct_rel,
                            'volume_ratio': vol_ratio,
                            'ema_dist_15_atr': (close - ema15) / atr if atr > 0 else 0,
                            'ema_dist_50_atr': (close - ema50) / atr if atr > 0 else 0,
                            'adx_acceleration': adx - adx_3_ago,
                            'regime': sig.get('regime', 'Unknown'),
                            'hour': bar_time_ar.hour,
                            'weekday': bar_time_ar.weekday(),
                        }

                        result = detector.detect(features)
                        scanned.append({
                            'symbol': sym,
                            'score': result.get('ophelia_score', 0),
                            'status': result.get('status', 'NO_OPHELIA'),
                        })

                        if result.get('status') == 'OPHELIA':
                            result['sl_pct'] = result.get('sl_pct', 0.0)
                            result['tp_pct'] = result.get('tp_pct', 0.0)
                            alerts.append(result)

                    except Exception as e:
                        pass

                    progress.progress((i+1)/len(assets))

                progress.empty()
                status.empty()

                st.session_state.live_alerts = alerts
                st.session_state.last_scan_time = get_ar_time().strftime('%H:%M:%S')
                st.session_state.scanned = scanned
                st.session_state.force_scan = False

            except Exception as e:
                st.error(f"❌ Error en escaneo: {e}")

    # Mostrar alertas
    alerts = st.session_state.get('live_alerts', [])

    if alerts:
        st.markdown(f"### 🎯 {len(alerts)} OPHELIA DETECTADO(S)")

        for alert in alerts:
            entry_time = alert.get('entry_time', '')
            detected = alert.get('detected_at', '')

            st.markdown(f"""
            <div class="ophelia-alert">
                <h2>🌟 {alert['symbol']} — {alert['direction']}</h2>
                <table class="ophelia-table">
                    <tr>
                        <td>💵 Precio de Entrada</td>
                        <td>{format_price(alert['entry_price'])}</td>
                    </tr>
                    <tr>
                        <td>🕐 Hora Exacta</td>
                        <td>{entry_time}</td>
                    </tr>
                    <tr>
                        <td>⏱️ Detectado a las</td>
                        <td>{detected[:19]}</td>
                    </tr>
                    <tr>
                        <td>🎯 Take Profit</td>
                        <td>{format_price(alert['tp_price'])} (+{alert['tp_pct']:.4f}%)</td>
                    </tr>
                    <tr>
                        <td>🛑 Stop Loss</td>
                        <td>{format_price(alert['sl_price'])} (-{alert['sl_pct']:.4f}%)</td>
                    </tr>
                    <tr>
                        <td>📈 Trailing Activación</td>
                        <td>{format_price(alert['trailing_activation_price'])}</td>
                    </tr>
                    <tr>
                        <td>📉 Trailing Distancia</td>
                        <td>{format_price(alert['trailing_distance_price'])}</td>
                    </tr>
                    <tr>
                        <td>⏳ Duración esperada</td>
                        <td>{format_duration(alert['expected_duration_min'])}</td>
                    </tr>
                    <tr>
                        <td>🎯 OPHELIA Score</td>
                        <td>{alert['ophelia_score']:.4f} / 1.0000</td>
                    </tr>
                    <tr>
                        <td>🏆 WR Histórico</td>
                        <td>{alert['historical_wr']*100:.0f}% (N={alert['n_historical']})</td>
                    </tr>
                    <tr>
                        <td>⚙️ Leverage Recomendado</td>
                        <td>{LeverageCalculator(pattern).calculate()['leverage_recommended']}x</td>
                    </tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

            # Componentes del score
            with st.expander(f"📊 Componentes del score para {alert['symbol']}"):
                comps = alert.get('components', {})
                df_c = pd.DataFrame([
                    {'Componente': k, 'Valor': v}
                    for k, v in comps.items()
                ])
                st.dataframe(df_c, use_container_width=True, hide_index=True)

            st.markdown("---")

    else:
        # NO OPHELIA
        st.markdown("""
        <div class="no-ophelia">
            <h3>⚪ NO OPHELIA DETECTADO</h3>
            <p>Ninguna de las condiciones históricas certificadas se cumple ahora.</p>
            <p style="margin-top: 20px;"><b>Precisión > Frecuencia</b></p>
            <p style="font-size: 0.9em; color: #888;">
                El sistema NO inventa señales. Prefiere esperar
                a la próxima oportunidad real.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Mostrar top candidatos
        scanned = st.session_state.get('scanned', [])
        if scanned:
            st.markdown("### 📊 Top candidatos (no alcanzan el umbral)")
            df_scan = pd.DataFrame(scanned).sort_values('score', ascending=False).head(10)

            # Formatear
            df_scan['score_fmt'] = df_scan['score'].apply(lambda x: f"{x:.4f}")
            df_scan['estado'] = df_scan['status'].apply(
                lambda x: '🌟 OPHELIA' if x == 'OPHELIA' else ('🟡 Candidato' if x == 'CANDIDATE' else '⚪ No')
            )

            st.dataframe(
                df_scan[['symbol', 'score_fmt', 'estado']].rename(columns={
                    'symbol': 'Activo',
                    'score_fmt': 'OPHELIA Score',
                    'estado': 'Estado',
                }),
                use_container_width=True,
                hide_index=True,
            )

            st.caption(f"Umbral OPHELIA: {OPHELIA_SCORE_THRESHOLD:.2f} · Escaneados: {len(scanned)} activos")


# ============================================================
# TAB 2: PRÓXIMA OPORTUNIDAD
# ============================================================
with tab2:
    st.markdown("## ⏳ Predicción Temporal OPHELIA")
    st.caption("Estimación de cuándo aparecerá el próximo trade certificado")

    try:
        temporal = TemporalPredictor(pattern)

        # Último OPHELIA
        ophelia_df = load_ophelia_trades()
        last_time = None
        if ophelia_df is not None and not ophelia_df.empty:
            last_row = ophelia_df.iloc[-1]
            last_time = last_row.get('entry_time_ar') or last_row.get('entry_time')

        # Tiempo desde último
        since = temporal.time_since_last(last_time)

        # Predicción
        pred = temporal.next_ophelia_prediction(last_time)

        # Layout principal
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("### 🕐 Último OPHELIA")
            if since['minutes'] is not None:
                st.markdown(f"""
                <div class="big-metric">
                    <div class="label">Tiempo desde último</div>
                    <div class="value">{since['human']}</div>
                    <div class="subvalue">{since['minutes']:.0f} minutos</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Sin OPHELIA previo registrado")

        with col2:
            st.markdown("### ⏳ Próximo OPHELIA")
            minutes_until = pred['minutes_until_start']

            st.markdown(f"""
            <div class="countdown">
                {int(minutes_until):02d}:{int((minutes_until % 1) * 60):02d}
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
            <div class="big-metric">
                <div class="label">Ventana estimada</div>
                <div class="value" style="font-size: 1.2em;">
                    {pred['next_window_start'][11:16]} → {pred['next_window_end'][11:16]}
                </div>
                <div class="subvalue">{pred['next_window_start'][:10]}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("### 🔔 Pre-alerta")
            alert_time = pred['alert_time'][11:16]
            st.markdown(f"""
            <div class="pre-alert">
                <h3>🔔 ALERTA A LAS {alert_time}</h3>
                <p style="font-size: 1.1em;">{pred['pre_alert_minutes']} minutos antes de la ventana</p>
                <p style="font-size: 1.05em; margin-top: 10px;">
                    <b>Confianza:</b> {pred['confidence']*100:.1f}%
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

        # Detalle de la predicción
        st.markdown("### 📊 Detalles de la Predicción")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**Estadísticas temporales**")
            tstats = pattern.get('temporal_stats', {})
            st.markdown(f"""
            | Métrica | Valor |
            |---------|-------|
            | Intervalo medio | {tstats.get('mean_interval_min', 0):.0f} min |
            | Intervalo mediano | {tstats.get('median_interval_min', 0):.0f} min |
            | Desviación estándar | {tstats.get('std_interval_min', 0):.0f} min |
            | Intervalo mínimo | {tstats.get('min_interval_min', 0):.0f} min |
            | Intervalo máximo | {tstats.get('max_interval_min', 0):.0f} min |
            """)

        with col_b:
            st.markdown("**Ventana horaria OPHELIA (Argentina)**")
            hr = pattern.get('hour_range', {})
            st.markdown(f"""
            | Métrica | Valor |
            |---------|-------|
            | Hora mínima | {hr.get('min', 0):02d}:00 |
            | Hora máxima | {hr.get('max', 0):02d}:00 |
            | Hora media | {hr.get('mean', 0):.1f}h |
            | Días activos | {', '.join(['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'][d] for d in pattern.get('weekday_set', []))} |
            """)

        st.markdown("---")

        # Histograma de intervalos
        if ophelia_df is not None and not ophelia_df.empty and len(ophelia_df) > 1:
            st.markdown("### 📊 Distribución de intervalos entre OPHELIAs")

            times = pd.to_datetime(ophelia_df['entry_time_ar'], errors='coerce').dropna()
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

        # Info importante
        st.info(f"""
        **⚠️ Importante:** La predicción temporal es una **estimación estadística**
        basada en {pattern.get('n_train', 0)} trades históricos. La confianza de
        {pred['confidence']*100:.1f}% indica la consistencia histórica del patrón.

        El sistema **avisa {pred['pre_alert_minutes']} minutos antes** para que puedas posicionarte.
        Una vez dentro de la ventana, la ejecución debe ser rápida
        (ventana de {EXECUTION_WINDOW_SECONDS} segundos por trade).
        """)

    except Exception as e:
        st.error(f"❌ Error en predicción temporal: {e}")
        st.exception(e)


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
    col3.metric("Features capturadas", len(pattern.get('features', {})))
    col4.metric("Duración media", f"{pattern.get('outcome_stats', {}).get('mean_duration_min', 0):.0f} min")

    st.markdown("---")

    # Tabla de features
    st.markdown("### 🔬 Features del Patrón")
    st.caption("Un trade es OPHELIA si TODAS sus features caen en estos rangos")

    features = pattern.get('features', {})
    if features:
        rows = []
        for feat, rng in features.items():
            rows.append({
                'Feature': feat,
                'Min': f"{rng['min']:.6f}",
                'Max': f"{rng['max']:.6f}",
                'Media': f"{rng['mean']:.6f}",
                'Std': f"{rng['std']:.6f}",
                'Rango': f"{rng['max'] - rng['min']:.6f}",
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Activos
    st.markdown("### 🎯 Activos OPHELIA")
    assets = pattern.get('assets', [])
    if assets:
        cols = st.columns(min(6, len(assets)))
        for i, a in enumerate(assets):
            with cols[i % 6]:
                st.markdown(f"**{a}**")

    st.markdown("---")

    # Ventana horaria
    st.markdown("### 🕐 Ventana Horaria (Argentina)")
    hr = pattern.get('hour_range', {})
    dist = hr.get('distribution', {})

    if dist:
        hours = sorted([int(h) for h in dist.keys()])
        counts = [dist[str(h)] if str(h) in dist else dist.get(h, 0) for h in hours]

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

    # Estadísticas de outcome
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
    st.markdown("---")
    st.markdown("### ⚙️ Leverage Calculado")

    try:
        lev = LeverageCalculator(pattern).calculate()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Conservador", f"{lev['leverage_conservative']}x")
        col2.metric("Recomendado", f"{lev['leverage_recommended']}x", delta="+0 base")
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
    st.caption("Todos los trades que cumplieron el patrón en el período analizado")

    ophelia_df = load_ophelia_trades()

    if ophelia_df is None or ophelia_df.empty:
        st.warning("No hay trades OPHELIA guardados. Ejecutá `python run_ophelia.py`.")
    else:
        # Métricas rápidas
        n = len(ophelia_df)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total trades", n)
        col2.metric("WR", "100%")
        col3.metric("MFE medio", f"{ophelia_df['mfe'].mean()*100:.4f}%")
        col4.metric("Duración media", f"{ophelia_df['duration_min'].mean():.0f} min")

        st.markdown("---")

        # Filtros
        col_a, col_b = st.columns(2)
        with col_a:
            symbols_filter = st.multiselect(
                "Filtrar por activo",
                options=sorted(ophelia_df['symbol'].unique()),
                default=[]
            )
        with col_b:
            show_n = st.slider("Mostrar últimos N", 10, min(500, n), min(50, n))

        df_show = ophelia_df.copy()
        if symbols_filter:
            df_show = df_show[df_show['symbol'].isin(symbols_filter)]

        df_show = df_show.sort_values('entry_time', ascending=False).head(show_n)

        # Preparar columnas
        display_cols = []
        rename_map = {}

        if 'entry_time_ar' in df_show.columns:
            display_cols.append('entry_time_ar')
            rename_map['entry_time_ar'] = 'Fecha ARG'

        for col, label in [
            ('symbol', 'Activo'),
            ('direction', 'Dir'),
            ('entry_price', 'Entrada'),
            ('exit_price', 'Salida'),
            ('mfe', 'MFE'),
            ('mae', 'MAE'),
            ('duration_min', 'Dur'),
            ('exit_reason', 'Cierre'),
        ]:
            if col in df_show.columns:
                display_cols.append(col)
                rename_map[col] = label

        df_view = df_show[display_cols].rename(columns=rename_map)

        # Formatear
        if 'MFE' in df_view.columns:
            df_view['MFE'] = df_view['MFE'].apply(lambda x: f"{x*100:.4f}%")
        if 'MAE' in df_view.columns:
            df_view['MAE'] = df_view['MAE'].apply(lambda x: f"{x*100:.4f}%")
        if 'Dur' in df_view.columns:
            df_view['Dur'] = df_view['Dur'].apply(lambda x: f"{x:.0f}m")
        if 'Entrada' in df_view.columns:
            df_view['Entrada'] = df_view['Entrada'].apply(lambda x: f"{x:.6f}")
        if 'Salida' in df_view.columns:
            df_view['Salida'] = df_view['Salida'].apply(lambda x: f"{x:.6f}")

        st.dataframe(df_view, use_container_width=True, hide_index=True)

        # Descarga
        csv = df_show.to_csv(index=False)
        st.download_button(
            "📥 Descargar CSV",
            data=csv,
            file_name=f"ophelia_trades_{get_ar_time().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

        st.markdown("---")

        # Distribución por activo
        st.markdown("### 📊 Distribución por Activo")
        by_asset = ophelia_df.groupby('symbol').agg({
            'mfe': 'mean',
            'duration_min': 'mean',
        }).round(4)
        by_asset['n_trades'] = ophelia_df.groupby('symbol').size()
        by_asset = by_asset.sort_values('n_trades', ascending=False)

        fig = px.bar(
            x=by_asset.index,
            y=by_asset['n_trades'],
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

    cert_text = load_certification()

    if cert_text is None:
        st.warning("No hay reporte de certificación. Ejecutá `python run_ophelia.py`.")

        # Mostrar estado inferido del patrón
        if pattern:
            st.markdown("### Estado inferido")

            n_train = pattern.get('n_train', 0)

            if n_train >= 30:
                st.markdown("""
                <div class="cert-card cert-pending">
                    <h2>⚠️ PENDIENTE DE CERTIFICACIÓN</h2>
                    <p>El patrón tiene suficientes muestras pero falta el reporte formal.</p>
                    <p><b>Ejecutá:</b> <code>python run_ophelia.py</code></p>
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
        # Parsear el reporte para mostrar resumen visual
        st.markdown("### Resumen Visual")

        # Intentar extraer info clave del reporte
        lines = cert_text.split('\n')
        is_certified = 'CERTIFICADO' in cert_text and 'NO CERTIFICADO' not in cert_text.split('\n')[3] if len(lines) > 3 else False

        if '✅ CERTIFICADO' in cert_text[:500]:
            st.markdown("""
            <div class="cert-card cert-approved">
                <h2>✅ CERTIFICADO</h2>
                <p>El patrón OPHELIA mantiene 100% WR en train y test out-of-sample.</p>
                <p><b>El detector está operativo.</b></p>
            </div>
            """, unsafe_allow_html=True)
        elif '❌ NO CERTIFICADO' in cert_text[:500]:
            st.markdown("""
            <div class="cert-card cert-rejected">
                <h2>❌ NO CERTIFICADO</h2>
                <p>El patrón no cumple los criterios mínimos.</p>
                <p>Ver detalles abajo.</p>
            </div>
            """, unsafe_allow_html=True)

        # Mostrar reporte completo
        st.markdown("---")
        st.markdown("### 📋 Reporte Completo")

        with st.expander("Ver reporte completo", expanded=True):
            st.markdown(cert_text)

        # Descarga
        st.download_button(
            "📥 Descargar OPHELIA_CERTIFICATION_REPORT.md",
            data=cert_text,
            file_name=f"ophelia_cert_{get_ar_time().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
        )


# ============================================================
# AUTO-REFRESH
# ============================================================
if st.session_state.get('auto_refresh', False):
    time.sleep(30)
    st.session_state.force_scan = True
    st.rerun()


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
