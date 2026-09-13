# streamlit_opheliav2.py
"""
🌟 OPHELIA Precision Engine — Dashboard v3
- Escaneo live con OPHELIA Score
- Ranking COMPLETO de TODOS los activos
- Clasificación OPHELIA / STANDARD / REJECTED
- TODOS los reportes descargables en formato TXT
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
# CONFIGURACIÓN DE PÁGINA
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
# ESTILOS CSS
# ============================================================
CSS_STYLE = """
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
    font-family: monospace;
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
.success-box {
    background: #d4edda;
    border-left: 5px solid #28a745;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
}
</style>
"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)


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
        with open(path, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None


def df_to_txt_report(df, title="RANKING"):
    """Convierte un DataFrame a texto tabular legible."""
    lines = []
    lines.append("=" * 100)
    lines.append(f"  {title}")
    lines.append("=" * 100)
    lines.append("")
    if df is None or df.empty:
        lines.append("  (sin datos)")
        return '\n'.join(lines)

    # Encabezados
    cols = list(df.columns)
    widths = [max(12, len(str(c))) for c in cols]

    header = "  ".join(str(c).ljust(w) for c, w in zip(cols, widths))
    lines.append(header)
    lines.append("-" * len(header))

    for _, row in df.iterrows():
        line = "  ".join(str(row[c])[:w].ljust(w) for c, w in zip(cols, widths))
        lines.append(line)

    lines.append("")
    return '\n'.join(lines)


# ============================================================
# HEADER
# ============================================================
st.title("🌟 OPHELIA Precision Engine")
st.caption("Score como motor principal · 2 niveles · Ranking completo · 100% real")

ar_now = get_ar_time()
st.markdown(f"**🕐 Hora Argentina:** `{ar_now.strftime('%A, %d/%m/%Y %H:%M:%S')}`")

if IMPORT_ERRORS:
    with st.expander(f"⚠️ {len(IMPORT_ERRORS)} módulos no cargados"):
        for err in IMPORT_ERRORS:
            st.caption(f"• `{err}`")

st.markdown("---")


# ============================================================
# CARGA DE DATOS
# ============================================================
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
# CASO 1: NO HAY MODELO
# ============================================================
if metadata is None:
    st.markdown('<div class="warning-box">', unsafe_allow_html=True)
    st.markdown("## ⚠️ OPHELIA NO DISPONIBLE")
    st.markdown("No se ha entrenado el OPHELIA Score todavía.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 🚀 Cómo activar OPHELIA")
    st.markdown("**Ejecutá el pipeline:**")
    st.code("python run_ophelia_v2.py", language="bash")
    st.markdown("Esto va a descargar datos, entrenar el score, calibrar thresholds y generar reportes.")

    st.markdown("### 📁 Estado actual")
    for path, label in [
        (OPHELIA_V2_MODEL, "Modelo OPHELIA Score"),
        (OPHELIA_V2_METADATA, "Metadata del modelo"),
        (OPHELIA_V2_TRADES, "Trades históricos"),
        (OPHELIA_V2_DAILY, "Selección diaria"),
        (OPHELIA_V2_REPORT, "Reporte de certificación"),
    ]:
        p = Path(path)
        if p.exists():
            st.markdown(f"✅ **{label}** — `{path}` ({p.stat().st_size:,} bytes)")
        else:
            st.markdown(f"❌ **{label}** — `{path}`")

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 📊 OPHELIA Score")
    st.metric("AUC train", f"{metadata.get('auc_train', 0):.4f}")
    st.metric("AUC test", f"{metadata.get('auc_test', 0):.4f}")
    st.metric("N train", metadata.get('n_train', 0))
    st.metric("N test", metadata.get('n_test', 0))

    st.markdown("---")
    st.markdown("### 🎯 Thresholds")
    st.metric("OPHELIA", f"{metadata.get('ophelia_threshold', 0):.3f}")
    st.metric("STANDARD", f"{metadata.get('standard_threshold', 0):.3f}")

    st.markdown("---")
    st.markdown("### 📈 Performance")
    st.metric("OPHELIA WR", f"{metadata.get('ophelia_wr_test', 0)*100:.2f}%")
    st.metric("STANDARD WR", f"{metadata.get('standard_wr_test', 0)*100:.2f}%")
    st.metric("OPHELIA/día", f"{metadata.get('ophelia_tpd_test', 0):.2f}")
    st.metric("STANDARD/día", f"{metadata.get('standard_tpd_test', 0):.2f}")

    st.markdown("---")
    st.caption("v3.0.0 · OPHELIA Precision Engine")


# ============================================================
# PESTAÑAS
# ============================================================
tab_live, tab_ranking, tab_temporal, tab_trades, tab_reports = st.tabs([
    "🌟 Escaneo Live",
    "🏆 Ranking Completo",
    "⏳ Modelo Temporal",
    "📊 Histórico",
    "📄 Reportes TXT",
])


# ============================================================
# TAB 1: ESCANEO LIVE
# ============================================================
with tab_live:
    st.markdown("## 🌟 Escaneo Live — Todos los activos")

    if not SCORER_AVAILABLE or not DATA_AVAILABLE or not SIGNAL_AVAILABLE:
        st.warning("⚠️ Faltan módulos para el escaneo live. Ver Ranking histórico.")
    else:
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            if st.button("🔄 Escanear Ahora", type="primary", use_container_width=True):
                st.session_state.force_scan = True
        with col_info:
            if st.session_state.get('last_scan_time'):
                st.caption(f"Último scan: {st.session_state.last_scan_time}")

        # Ejecutar escaneo
        if st.session_state.get('force_scan', False):
            with st.spinner("🔍 Analizando TODOS los activos..."):
                try:
                    scorer = OpheliaScorer()
                    scorer.load(OPHELIA_V2_MODEL)

                    de = DataEngine()
                    results = []
                    progress = st.progress(0)
                    status_text = st.empty()

                    for i, sym in enumerate(SYMBOLS):
                        status_text.text(f"Analizando {sym} ({i+1}/{len(SYMBOLS)})...")
                        try:
                            df = de.fetch_ohlcv(sym, limit=300)
                            if df is None or df.empty:
                                progress.progress((i+1)/len(SYMBOLS))
                                continue

                            sig = Signal(sym, df, DEFAULT_PARAMS).to_dict()

                            from core_engine import compute_adx, compute_atr, compute_ema

                            close = df['close'].iloc[-1]
                            adx_series = compute_adx(df)
                            atr_series = compute_atr(df)

                            if len(adx_series) < 4 or len(atr_series) < 50:
                                progress.progress((i+1)/len(SYMBOLS))
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
                            vol_ratio = float(df['volume'].iloc[-1] / avg_vol) if avg_vol > 0 else 1.0
                            vol_ratio = max(0.1, vol_ratio)

                            bar_time = df.index[-1]
                            try:
                                if bar_time.tz is None:
                                    bar_time_ar = bar_time.tz_localize('UTC').tz_convert(TIMEZONE_AR)
                                else:
                                    bar_time_ar = bar_time.tz_convert(TIMEZONE_AR)
                            except Exception:
                                bar_time_ar = bar_time

                            hour = bar_time_ar.hour if hasattr(bar_time_ar, 'hour') else 0
                            weekday = bar_time_ar.weekday() if hasattr(bar_time_ar, 'weekday') else 0

                            regime = sig.get('regime', 'Unknown')
                            features = {
                                'symbol': sym,
                                'direction': sig.get('direction', 'LONG'),
                                'entry_price': close,
                                'entry_time_ar': str(bar_time_ar),
                                'hour': hour,
                                'weekday': weekday,
                                'adx': adx,
                                'ker': float(sig.get('ker', 0)),
                                'score': float(sig.get('score', 0)),
                                'atr_pct': atr_pct,
                                'atr_pct_rel': atr_pct_rel,
                                'volume_ratio': vol_ratio,
                                'ema_dist_15_atr': (close - ema15) / atr if atr > 0 else 0,
                                'ema_dist_50_atr': (close - ema50) / atr if atr > 0 else 0,
                                'adx_acceleration': adx - adx_3_ago,
                                'hour_sin': np.sin(2 * np.pi * hour / 24),
                                'hour_cos': np.cos(2 * np.pi * hour / 24),
                                'weekday_sin': np.sin(2 * np.pi * weekday / 7),
                                'weekday_cos': np.cos(2 * np.pi * weekday / 7),
                                'regime_expansion': 1.0 if regime == 'Expansión' else 0.0,
                                'regime_trend': 1.0 if regime in ['Tendencia Fuerte', 'Tendencia Débil'] else 0.0,
                                'regime_chop': 1.0 if regime == 'Chop' else 0.0,
                                'regime': regime,
                                'sl_price': sig.get('sl_price', 0),
                                'tp_price': sig.get('tp_price', 0),
                            }
                            results.append(features)
                        except Exception:
                            pass

                        progress.progress((i+1)/len(SYMBOLS))

                    progress.empty()
                    status_text.empty()

                    if results:
                        results_df = pd.DataFrame(results)
                        results_df['ophelia_score'] = scorer.score(results_df)
                        results_df['tier'] = results_df['ophelia_score'].apply(scorer.classify)
                        results_df['movement_type'] = results_df.apply(
                            lambda r: 'CONTINUACION' if (
                                (r['direction'] == 'LONG' and r['ema_dist_50_atr'] > 0) or
                                (r['direction'] == 'SHORT' and r['ema_dist_50_atr'] < 0)
                            ) else 'REVERSION', axis=1
                        )
                        results_df = results_df.sort_values('ophelia_score', ascending=False).reset_index(drop=True)

                        st.session_state.scan_results = results_df
                        st.session_state.last_scan_time = get_ar_time().strftime('%H:%M:%S')

                    st.session_state.force_scan = False
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.session_state.force_scan = False

        # Mostrar resultados
        scan_results = st.session_state.get('scan_results')

        if scan_results is not None and not scan_results.empty:
            n_ophelia = (scan_results['tier'] == 'OPHELIA').sum()
            n_standard = (scan_results['tier'] == 'STANDARD').sum()
            n_rejected = (scan_results['tier'] == 'REJECTED').sum()

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🌟 OPHELIA", n_ophelia)
            col2.metric("💠 STANDARD", n_standard)
            col3.metric("⚪ Rechazadas", n_rejected)
            col4.metric("📊 Total", len(scan_results))

            st.markdown("---")

            # OPHELIA alerts
            if n_ophelia > 0:
                st.markdown("### 🌟 OPHELIA DETECTADO(S)")
                ophelia_alerts = scan_results[scan_results['tier'] == 'OPHELIA']

                for _, alert in ophelia_alerts.iterrows():
                    try:
                        lev = LeverageOptimizer().optimize_per_signal(alert)
                        lev_rec = lev['leverage_recommended']
                    except Exception:
                        lev_rec = 'N/A'

                    st.markdown('<div class="ophelia-alert">', unsafe_allow_html=True)
                    st.markdown(f"## 🌟 {alert['symbol']} — {alert['direction']}")
                    st.markdown(f"""
- **💵 Precio Entrada:** {format_price(alert['entry_price'])}
- **🕐 Hora ARG:** {str(alert['entry_time_ar'])[:19]}
- **📊 OPHELIA Score:** {alert['ophelia_score']:.4f}
- **📈 Régimen:** {alert['regime']}
- **🎯 Tipo:** {alert['movement_type']}
- **⚙️ Leverage:** {lev_rec}x
- **🛑 SL:** {format_price(alert.get('sl_price'))}
- **🎯 TP:** {format_price(alert.get('tp_price'))}
                    """)
                    st.markdown('</div>', unsafe_allow_html=True)

                    with st.expander(f"📊 Features de {alert['symbol']}"):
                        feat_data = {
                            'ADX': alert['adx'],
                            'KER': alert['ker'],
                            'Score base': alert['score'],
                            'ATR%': alert['atr_pct'],
                            'ATR rel': alert['atr_pct_rel'],
                            'Vol ratio': alert['volume_ratio'],
                            'EMA15 dist': alert['ema_dist_15_atr'],
                            'EMA50 dist': alert['ema_dist_50_atr'],
                            'ADX accel': alert['adx_acceleration'],
                        }
                        st.dataframe(pd.DataFrame([feat_data]).T.rename(columns={0: 'Valor'}))
            else:
                st.markdown('<div class="no-ophelia">', unsafe_allow_html=True)
                st.markdown("### ⚪ NO OPHELIA DETECTADO")
                st.markdown(f"Ninguna de las {len(scan_results)} señales supera el threshold OPHELIA.")
                st.markdown("**Precisión > Frecuencia**")
                st.markdown('</div>', unsafe_allow_html=True)

            # STANDARD
            if n_standard > 0:
                st.markdown("---")
                st.markdown("### 💠 STANDARD (menor edge)")
                standard = scan_results[scan_results['tier'] == 'STANDARD'].head(10)
                st.dataframe(
                    standard[['symbol', 'direction', 'ophelia_score', 'regime',
                              'movement_type', 'entry_price']].rename(columns={
                        'symbol': 'Activo', 'direction': 'Dir',
                        'ophelia_score': 'Score', 'regime': 'Régimen',
                        'movement_type': 'Tipo', 'entry_price': 'Precio',
                    }),
                    use_container_width=True, hide_index=True,
                )
        else:
            st.info("Presioná 'Escanear Ahora' para analizar todos los activos.")


# ============================================================
# TAB 2: RANKING COMPLETO
# ============================================================
with tab_ranking:
    st.markdown("## 🏆 Ranking Completo — TODOS los activos")
    st.caption("Clasificación: 🌟 OPHELIA · 💠 STANDARD · ⚪ REJECTED")

    ranking_df = None
    source = ""

    if 'scan_results' in st.session_state and st.session_state.scan_results is not None:
        ranking_df = st.session_state.scan_results.copy()
        source = "LIVE (último escaneo)"
    elif daily_df is not None and not daily_df.empty:
        ranking_df = daily_df.copy()
        if 'ophelia_score' not in ranking_df.columns and 'score' in ranking_df.columns:
            ranking_df['ophelia_score'] = ranking_df['score']
        source = "HISTORICO (última selección)"

    if ranking_df is None:
        st.warning("⚠️ No hay datos. Presioná 'Escanear Ahora' en la pestaña Live.")
    else:
        st.caption(f"Fuente: {source} · Total: {len(ranking_df)} activos")

        if 'tier' not in ranking_df.columns:
            if SCORER_AVAILABLE:
                try:
                    scorer = OpheliaScorer()
                    scorer.load(OPHELIA_V2_MODEL)
                    ranking_df['ophelia_score'] = scorer.score(ranking_df)
                    ranking_df['tier'] = ranking_df['ophelia_score'].apply(scorer.classify)
                except Exception:
                    ranking_df['tier'] = 'REJECTED'

        # LONG
        st.markdown("### 🟢 Ranking LONG")
        longs = ranking_df[ranking_df['direction'] == 'LONG'].sort_values(
            'ophelia_score', ascending=False
        ).reset_index(drop=True)

        if not longs.empty:
            longs_display = longs[['symbol', 'ophelia_score', 'tier', 'regime',
                                     'movement_type', 'entry_price', 'adx', 'ker']].copy()
            longs_display.columns = ['Activo', 'Score', 'Tier', 'Regimen',
                                      'Tipo', 'Precio', 'ADX', 'KER']
            longs_display.insert(0, 'Rank', range(1, len(longs_display) + 1))
            longs_display['Score'] = longs_display['Score'].apply(lambda x: f"{x:.4f}")
            st.dataframe(longs_display, use_container_width=True, hide_index=True)
        else:
            st.info("Sin señales LONG.")

        st.markdown("---")

        # SHORT
        st.markdown("### 🔴 Ranking SHORT")
        shorts = ranking_df[ranking_df['direction'] == 'SHORT'].sort_values(
            'ophelia_score', ascending=False
        ).reset_index(drop=True)

        if not shorts.empty:
            shorts_display = shorts[['symbol', 'ophelia_score', 'tier', 'regime',
                                       'movement_type', 'entry_price', 'adx', 'ker']].copy()
            shorts_display.columns = ['Activo', 'Score', 'Tier', 'Regimen',
                                        'Tipo', 'Precio', 'ADX', 'KER']
            shorts_display.insert(0, 'Rank', range(1, len(shorts_display) + 1))
            shorts_display['Score'] = shorts_display['Score'].apply(lambda x: f"{x:.4f}")
            st.dataframe(shorts_display, use_container_width=True, hide_index=True)
        else:
            st.info("Sin señales SHORT.")

        st.markdown("---")

        # Distribución
        st.markdown("### 📊 Distribución por Nivel")
        tier_counts = ranking_df['tier'].value_counts()
        fig = px.pie(
            values=tier_counts.values,
            names=tier_counts.index,
            title="Distribución OPHELIA / STANDARD / REJECTED",
            color=tier_counts.index,
            color_discrete_map={
                'OPHELIA': '#ffd700',
                'STANDARD': '#4a90e2',
                'REJECTED': '#e0e0e0',
            }
        )
        st.plotly_chart(fig, use_container_width=True)

        # Descarga TXT
        st.markdown("---")
        st.markdown("### 📥 Descargar Ranking (TXT)")

        txt_content = []
        txt_content.append("=" * 100)
        txt_content.append("  OPHELIA PRECISION ENGINE — RANKING COMPLETO")
        txt_content.append(f"  Generado: {get_ar_time().isoformat()}")
        txt_content.append(f"  Fuente: {source}")
        txt_content.append(f"  Total activos: {len(ranking_df)}")
        txt_content.append("=" * 100)
        txt_content.append("")

        # LONG
        txt_content.append("=" * 100)
        txt_content.append("  RANKING LONG")
        txt_content.append("=" * 100)
        if not longs.empty:
            for i, row in longs.iterrows():
                txt_content.append(
                    f"  #{i+1:<3} {row['symbol']:<15} Score: {row['ophelia_score']:.4f}  "
                    f"Tier: {row['tier']:<12} Tipo: {row.get('movement_type', 'N/A'):<15} "
                    f"Precio: {row['entry_price']:.6f}"
                )
        else:
            txt_content.append("  (sin señales LONG)")
        txt_content.append("")

        # SHORT
        txt_content.append("=" * 100)
        txt_content.append("  RANKING SHORT")
        txt_content.append("=" * 100)
        if not shorts.empty:
            for i, row in shorts.iterrows():
                txt_content.append(
                    f"  #{i+1:<3} {row['symbol']:<15} Score: {row['ophelia_score']:.4f}  "
                    f"Tier: {row['tier']:<12} Tipo: {row.get('movement_type', 'N/A'):<15} "
                    f"Precio: {row['entry_price']:.6f}"
                )
        else:
            txt_content.append("  (sin señales SHORT)")
        txt_content.append("")

        txt_content.append("=" * 100)
        txt_content.append("  FIN DEL RANKING")
        txt_content.append("=" * 100)

        txt_str = '\n'.join(txt_content)

        st.download_button(
            "📥 Descargar ranking_completo.txt",
            data=txt_str,
            file_name=f"ophelia_ranking_{get_ar_time().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# TAB 3: MODELO TEMPORAL
# ============================================================
with tab_temporal:
    st.markdown("## ⏳ Modelo Temporal OPHELIA")

    if trades_df is None or trades_df.empty:
        st.warning("No hay trades históricos.")
    else:
        try:
            temporal = TemporalAnalyzer().analyze(trades_df)

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Trades/día", f"{temporal.get('trades_per_day', 0):.2f}")
            col2.metric("Intervalo medio", f"{temporal.get('mean_interval_min', 'N/A')} min")
            col3.metric("Intervalo mediano", f"{temporal.get('median_interval_min', 'N/A')} min")
            col4.metric("Total trades", temporal.get('n_total', 0))

            st.markdown("---")

            by_hour = temporal.get('by_hour', {})
            if by_hour:
                hours_data = []
                for h, stats in sorted(by_hour.items()):
                    hours_data.append({
                        'Hora': f"{int(h):02d}:00",
                        'Trades': stats.get('n', 0),
                        'WR': stats.get('wr', 0),
                        'MFE': stats.get('mean_mfe', 0),
                    })
                df_hours = pd.DataFrame(hours_data)

                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_hours['Hora'],
                    y=df_hours['Trades'],
                    name='Trades',
                    marker_color='#ff8c00',
                ))
                fig.update_layout(
                    title="Distribución horaria (ARG)",
                    height=400,
                )
                st.plotly_chart(fig, use_container_width=True)

            top_hours = temporal.get('top_hours', {})
            if top_hours:
                st.markdown("### 🕐 Top 5 horas más frecuentes (ARG)")
                for h, n in sorted(top_hours.items(), key=lambda x: -x[1])[:5]:
                    st.markdown(f"- **{int(h):02d}:00** — {n} trades")

            direction_dist = temporal.get('direction_distribution', {})
            if direction_dist:
                st.markdown("### 📊 Distribución direccional")
                for d, n in direction_dist.items():
                    st.markdown(f"- **{d}**: {n}")

            top_assets = temporal.get('top_assets', {})
            if top_assets:
                st.markdown("### 🎯 Top activos")
                for a, n in sorted(top_assets.items(), key=lambda x: -x[1])[:10]:
                    st.markdown(f"- **{a}**: {n} trades")

            # Descarga TXT
            st.markdown("---")
            st.markdown("### 📥 Descargar reporte temporal (TXT)")

            txt = []
            txt.append("=" * 100)
            txt.append("  OPHELIA — ANÁLISIS TEMPORAL")
            txt.append(f"  Generado: {get_ar_time().isoformat()}")
            txt.append("=" * 100)
            txt.append("")
            txt.append(f"  Trades/día: {temporal.get('trades_per_day', 0):.2f}")
            txt.append(f"  Intervalo medio: {temporal.get('mean_interval_min', 'N/A')} min")
            txt.append(f"  Intervalo mediano: {temporal.get('median_interval_min', 'N/A')} min")
            txt.append(f"  Total trades: {temporal.get('n_total', 0)}")
            txt.append("")
            txt.append("  DISTRIBUCIÓN HORARIA (ARG)")
            txt.append("-" * 100)
            for h, stats in sorted(by_hour.items()):
                txt.append(f"  {int(h):02d}:00  Trades: {stats.get('n', 0):<5}  WR: {stats.get('wr', 0)*100:.1f}%  MFE: {stats.get('mean_mfe', 0)*100:.3f}%")
            txt.append("")
            txt.append("  DIRECCIÓN")
            txt.append("-" * 100)
            for d, n in direction_dist.items():
                txt.append(f"  {d}: {n}")
            txt.append("")
            txt.append("  TOP ACTIVOS")
            txt.append("-" * 100)
            for a, n in sorted(top_assets.items(), key=lambda x: -x[1])[:20]:
                txt.append(f"  {a:<20} {n} trades")
            txt.append("")
            txt.append("=" * 100)

            st.download_button(
                "📥 Descargar analisis_temporal.txt",
                data='\n'.join(txt),
                file_name=f"ophelia_temporal_{get_ar_time().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        except Exception as e:
            st.error(f"Error: {e}")


# ============================================================
# TAB 4: HISTÓRICO
# ============================================================
with tab_trades:
    st.markdown("## 📊 Trades Históricos")

    if trades_df is None or trades_df.empty:
        st.warning("No hay trades. Ejecutá `python run_ophelia_v2.py`.")
    else:
        n = len(trades_df)
        wr = trades_df['win'].mean()
        mfe_mean = trades_df['mfe'].mean()
        mae_mean = trades_df['mae'].mean()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total trades", n)
        col2.metric("WR base", f"{wr*100:.2f}%")
        col3.metric("MFE medio", f"{mfe_mean*100:.3f}%")
        col4.metric("MAE medio", f"{mae_mean*100:.3f}%")

        st.markdown("---")

        dir_counts = trades_df['direction'].value_counts()
        col1, col2 = st.columns(2)
        with col1:
            for d, count in dir_counts.items():
                wr_d = trades_df[trades_df['direction'] == d]['win'].mean()
                st.metric(f"{d}", f"{count} trades", delta=f"WR {wr_d*100:.1f}%")

        st.markdown("---")

        col_a, col_b = st.columns(2)
        with col_a:
            symbols_filter = st.multiselect(
                "Filtrar por activo",
                options=sorted(trades_df['symbol'].unique()),
                default=[],
            )
        with col_b:
            show_n = st.slider("Mostrar N", 10, min(500, n), min(50, n))

        df_show = trades_df.copy()
        if symbols_filter:
            df_show = df_show[df_show['symbol'].isin(symbols_filter)]

        if 'entry_time_ar' in df_show.columns:
            df_show = df_show.sort_values('entry_time_ar', ascending=False)

        df_show = df_show.head(show_n)

        display_cols = [c for c in ['entry_time_ar', 'symbol', 'direction',
                                      'entry_price', 'exit_price', 'mfe', 'mae',
                                      'duration_min', 'exit_reason', 'win']
                        if c in df_show.columns]
        df_view = df_show[display_cols].copy()

        if 'mfe' in df_view.columns:
            df_view['mfe'] = df_view['mfe'].apply(lambda x: f"{x*100:.3f}%")
        if 'mae' in df_view.columns:
            df_view['mae'] = df_view['mae'].apply(lambda x: f"{x*100:.3f}%")
        if 'entry_price' in df_view.columns:
            df_view['entry_price'] = df_view['entry_price'].apply(lambda x: f"{x:.6f}")
        if 'exit_price' in df_view.columns:
            df_view['exit_price'] = df_view['exit_price'].apply(lambda x: f"{x:.6f}")
        if 'duration_min' in df_view.columns:
            df_view['duration_min'] = df_view['duration_min'].apply(lambda x: f"{x:.0f}m")
        if 'win' in df_view.columns:
            df_view['win'] = df_view['win'].apply(lambda x: 'WIN' if x else 'LOSS')

        st.dataframe(df_view, use_container_width=True, hide_index=True)

        # Descarga TXT
        txt = []
        txt.append("=" * 140)
        txt.append("  OPHELIA — TRADES HISTÓRICOS")
        txt.append(f"  Generado: {get_ar_time().isoformat()}")
        txt.append(f"  Total: {len(df_show)}")
        txt.append("=" * 140)
        txt.append("")

        header = f"{'Fecha':<22} {'Activo':<14} {'Dir':<7} {'Entrada':<12} {'Salida':<12} {'MFE':<9} {'MAE':<9} {'Dur':<7} {'Win':<5}"
        txt.append(header)
        txt.append("-" * len(header))

        for _, t in df_show.iterrows():
            txt.append(
                f"{str(t.get('entry_time_ar', ''))[:19]:<22} "
                f"{str(t.get('symbol', ''))[:13]:<14} "
                f"{str(t.get('direction', '')):<7} "
                f"{t.get('entry_price', 0):<12.6f} "
                f"{t.get('exit_price', 0):<12.6f} "
                f"{t.get('mfe', 0)*100:<8.3f}% "
                f"{t.get('mae', 0)*100:<8.3f}% "
                f"{t.get('duration_min', 0):<6.0f}m "
                f"{'WIN' if t.get('win') else 'LOSS':<5}"
            )
        txt.append("")
        txt.append("=" * 140)

        st.download_button(
            "📥 Descargar trades_historicos.txt",
            data='\n'.join(txt),
            file_name=f"ophelia_trades_{get_ar_time().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# TAB 5: REPORTES TXT
# ============================================================
with tab_reports:
    st.markdown("## 📄 Reportes en formato TXT")

    # Generar reporte de iteración
    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("🔄 Generar Reporte de Iteración", use_container_width=True):
            with st.spinner("Generando..."):
                try:
                    if trades_df is not None and not trades_df.empty:
                        txt_lines = []
                        txt_lines.append("=" * 100)
                        txt_lines.append("  OPHELIA PRECISION ENGINE — REPORTE DE ITERACIÓN")
                        txt_lines.append(f"  Generado: {get_ar_time().isoformat()}")
                        txt_lines.append("=" * 100)
                        txt_lines.append("")

                        # Metadata
                        txt_lines.append("=" * 100)
                        txt_lines.append("  1. METADATA DEL MODELO")
                        txt_lines.append("=" * 100)
                        txt_lines.append(f"  AUC train:            {metadata.get('auc_train', 0):.4f}")
                        txt_lines.append(f"  AUC test:             {metadata.get('auc_test', 0):.4f}")
                        txt_lines.append(f"  N train:              {metadata.get('n_train', 0)}")
                        txt_lines.append(f"  N test:               {metadata.get('n_test', 0)}")
                        txt_lines.append(f"  Threshold OPHELIA:    {metadata.get('ophelia_threshold', 0):.3f}")
                        txt_lines.append(f"  Threshold STANDARD:   {metadata.get('standard_threshold', 0):.3f}")
                        txt_lines.append(f"  OPHELIA WR test:      {metadata.get('ophelia_wr_test', 0)*100:.2f}%")
                        txt_lines.append(f"  STANDARD WR test:     {metadata.get('standard_wr_test', 0)*100:.2f}%")
                        txt_lines.append("")

                        # Trades
                        txt_lines.append("=" * 100)
                        txt_lines.append("  2. TRADES HISTÓRICOS")
                        txt_lines.append("=" * 100)
                        txt_lines.append(f"  Total:                {len(trades_df)}")
                        txt_lines.append(f"  WR base:              {trades_df['win'].mean()*100:.2f}%")
                        txt_lines.append(f"  LONG:                 {(trades_df['direction']=='LONG').sum()}")
                        txt_lines.append(f"  SHORT:                {(trades_df['direction']=='SHORT').sum()}")
                        txt_lines.append(f"  MFE medio:            {trades_df['mfe'].mean()*100:.4f}%")
                        txt_lines.append(f"  MAE medio:            {trades_df['mae'].mean()*100:.4f}%")
                        txt_lines.append("")

                        # Ranking actual
                        if 'scan_results' in st.session_state and st.session_state.scan_results is not None:
                            df_scan = st.session_state.scan_results
                            txt_lines.append("=" * 100)
                            txt_lines.append("  3. RANKING ACTUAL")
                            txt_lines.append("=" * 100)
                            txt_lines.append("")

                            longs = df_scan[df_scan['direction'] == 'LONG'].sort_values(
                                'ophelia_score', ascending=False
                            )
                            txt_lines.append("  --- LONG ---")
                            for i, (_, row) in enumerate(longs.iterrows(), 1):
                                txt_lines.append(
                                    f"  #{i:<3} {row['symbol']:<15} "
                                    f"Score: {row['ophelia_score']:.4f}  "
                                    f"Tier: {row['tier']:<12} "
                                    f"Precio: {row['entry_price']:.6f}"
                                )
                            txt_lines.append("")

                            shorts = df_scan[df_scan['direction'] == 'SHORT'].sort_values(
                                'ophelia_score', ascending=False
                            )
                            txt_lines.append("  --- SHORT ---")
                            for i, (_, row) in enumerate(shorts.iterrows(), 1):
                                txt_lines.append(
                                    f"  #{i:<3} {row['symbol']:<15} "
                                    f"Score: {row['ophelia_score']:.4f}  "
                                    f"Tier: {row['tier']:<12} "
                                    f"Precio: {row['entry_price']:.6f}"
                                )
                            txt_lines.append("")

                        txt_lines.append("=" * 100)
                        txt_lines.append("  FIN DEL REPORTE")
                        txt_lines.append("=" * 100)

                        full_txt = '\n'.join(txt_lines)
                        Path('reports').mkdir(exist_ok=True)
                        Path('reports/ophelia_iteration_report.txt').write_text(full_txt, encoding='utf-8')
                        st.success("✅ Reporte generado: reports/ophelia_iteration_report.txt")
                    else:
                        st.warning("No hay trades para generar reporte.")
                except Exception as e:
                    st.error(f"Error: {e}")

    with col_b:
        if st.button("📊 Generar Reporte JSON", use_container_width=True):
            with st.spinner("Generando JSON..."):
                try:
                    json_data = {
                        'timestamp': get_ar_time().isoformat(),
                        'model_metadata': metadata,
                        'trades_summary': {
                            'n_total': len(trades_df) if trades_df is not None else 0,
                            'wr_base': float(trades_df['win'].mean()) if trades_df is not None and not trades_df.empty else None,
                        },
                        'ranking': None,
                    }

                    if 'scan_results' in st.session_state and st.session_state.scan_results is not None:
                        json_data['ranking'] = st.session_state.scan_results[
                            ['symbol', 'direction', 'ophelia_score', 'tier', 'entry_price']
                        ].to_dict('records')

                    Path('data/ophelia_v2').mkdir(parents=True, exist_ok=True)
                    Path('data/ophelia_v2/iteration_report.json').write_text(
                        json.dumps(json_data, indent=2, default=str), encoding='utf-8'
                    )
                    st.success("✅ JSON generado: data/ophelia_v2/iteration_report.json")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    # Descargar reporte de iteración
    iter_txt = Path('reports/ophelia_iteration_report.txt')
    if iter_txt.exists():
        st.markdown("### 📄 Reporte de Iteración (TXT)")
        content = iter_txt.read_text(encoding='utf-8')
        st.download_button(
            "📥 Descargar ophelia_iteration_report.txt",
            data=content,
            file_name=f"ophelia_iteration_{get_ar_time().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
        with st.expander("👁️ Vista previa"):
            st.code(content[:5000], language='text')
    else:
        st.info("El reporte de iteración se genera con el botón de arriba.")

    # Descargar certificación
    if report_text:
        st.markdown("### 📋 Reporte de Certificación")
        st.download_button(
            "📥 Descargar ophelia_certification.txt",
            data=report_text,
            file_name=f"ophelia_certification_{get_ar_time().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
        with st.expander("👁️ Ver certificación"):
            st.markdown(report_text)
    else:
        st.warning("No hay certificación. Ejecutá `python run_ophelia_v2.py`.")

    # Estado de archivos
    st.markdown("---")
    st.markdown("### 📁 Estado de archivos")
    for path, label in [
        (OPHELIA_V2_MODEL, "Modelo entrenado"),
        (OPHELIA_V2_METADATA, "Metadata"),
        (OPHELIA_V2_TRADES, "Trades históricos"),
        (OPHELIA_V2_DAILY, "Selección diaria"),
        (OPHELIA_V2_REPORT, "Certificación"),
        ('reports/ophelia_iteration_report.txt', "Reporte iteración TXT"),
        ('data/ophelia_v2/iteration_report.json', "Reporte JSON"),
    ]:
        p = Path(path)
        if p.exists():
            st.markdown(f"✅ **{label}** — `{path}` ({p.stat().st_size:,} bytes)")
        else:
            st.markdown(f"❌ **{label}** — `{path}`")


# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.caption(f"🌟 OPHELIA Precision Engine v3.0.0 · Todos los reportes en TXT · Hora ARG: {get_ar_time().strftime('%Y-%m-%d %H:%M:%S')}")
