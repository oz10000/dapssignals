# streamlit_ophelia.py
"""
🌟 OPHELIA Precision Engine — Dashboard v3
FIX: AUC gate que bloquea el scan si el modelo no es válido.
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
        MIN_AUC_TEST,
    )
except Exception as e:
    IMPORT_ERRORS.append(f"ophelia_v2_config: {e}")
    OPHELIA_V2_MODEL = 'data/ophelia_v2/model.pkl'
    OPHELIA_V2_METADATA = 'data/ophelia_v2/metadata.json'
    OPHELIA_V2_TRADES = 'data/ophelia_v2/trades.parquet'
    OPHELIA_V2_DAILY = 'data/ophelia_v2/daily_selection.parquet'
    OPHELIA_V2_REPORT = 'reports/OPHELIA_DAILY_CERTIFICATION_REPORT.md'
    TIMEZONE_AR = 'America/Argentina/Buenos_Aires'
    MIN_AUC_TEST = 0.55

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
.error-box {
    background: #f8d7da;
    border-left: 8px solid #dc3545;
    padding: 25px;
    border-radius: 8px;
    margin: 15px 0;
}
.error-box h2 {
    color: #721c24;
    margin-top: 0;
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


# ============================================================
# HEADER
# ============================================================
st.title("🌟 OPHELIA Precision Engine")
st.caption("Score como motor principal · 2 niveles · Ranking completo · 100% real")

ar_now = get_ar_time()
st.markdown(f"**🕐 Hora Argentina:** `{ar_now.strftime('%A, %d/%m/%Y %H:%M:%S')}`")

if IMPORT_ERRORS:
    with st.expander(f"⚠️ {len(IMPORT_ERRORS)} módulos no cargados (ver detalle)"):
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
# VALIDACIÓN DE CALIDAD DEL MODELO (AUC GATE)
# ============================================================
auc_test = metadata.get('auc_test', 0.5)
auc_train = metadata.get('auc_train', 0.5)
n_train = metadata.get('n_train', 0)
n_test = metadata.get('n_test', 0)

MODEL_IS_VALID = auc_test >= MIN_AUC_TEST


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("## 📊 OPHELIA Score")

    # Color según validez
    if MODEL_IS_VALID:
        st.success(f"✅ AUC test: {auc_test:.4f}")
    else:
        st.error(f"🚫 AUC test: {auc_test:.4f}")

    st.metric("AUC train", f"{auc_train:.4f}")
    st.metric("AUC test", f"{auc_test:.4f}")
    st.metric("N train", n_train)
    st.metric("N test", n_test)

    st.markdown("---")
    st.markdown("### 🎯 Thresholds")
    st.metric("OPHELIA", f"{metadata.get('ophelia_threshold', 0):.3f}")
    st.metric("STANDARD", f"{metadata.get('standard_threshold', 0):.3f}")

    st.markdown("---")
    st.markdown("### 📈 Performance (test)")
    st.metric("OPHELIA WR", f"{metadata.get('ophelia_wr_test', 0)*100:.2f}%")
    st.metric("STANDARD WR", f"{metadata.get('standard_wr_test', 0)*100:.2f}%")
    st.metric("OPHELIA/día", f"{metadata.get('ophelia_tpd_test', 0):.2f}")
    st.metric("STANDARD/día", f"{metadata.get('standard_tpd_test', 0):.2f}")

    st.markdown("---")
    st.caption("v3.0.0 · OPHELIA Precision Engine")


# ============================================================
# BANNER DE ESTADO DEL MODELO
# ============================================================
if not MODEL_IS_VALID:
    st.markdown('<div class="error-box">', unsafe_allow_html=True)
    st.markdown(f"# 🚫 MODELO NO VÁLIDO")
    st.markdown(f"**AUC test = {auc_test:.4f}** (mínimo requerido: {MIN_AUC_TEST})")
    st.markdown("")
    st.markdown("El OPHELIA Score **NO discrimina** entre trades ganadores y perdedores.")
    st.markdown("**No se debe usar para operar.**")
    st.markdown("")
    st.markdown("**Diagnóstico:**")
    if auc_train - auc_test > 0.15:
        st.markdown(f"- 🔴 **Overfitting**: train={auc_train:.4f} vs test={auc_test:.4f}")
    if n_train < 100 or n_test < 40:
        st.markdown(f"- 🟡 **Muestra insuficiente**: train={n_train}, test={n_test}")
    st.markdown("")
    st.markdown("**Acción recomendada:**")
    st.markdown("```bash")
    st.markdown("# Ya está aplicado en el repo: limit=10000, features=3")
    st.markdown("python run_ophelia_v2.py")
    st.markdown("```")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="success-box">', unsafe_allow_html=True)
    st.markdown(f"✅ **Modelo válido** — AUC test = {auc_test:.4f}")
    st.markdown('</div>', unsafe_allow_html=True)


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

    # AUC GATE
    if not MODEL_IS_VALID:
        st.error(f"""
        🚫 **Escaneo bloqueado** — AUC test = {auc_test:.4f} < {MIN_AUC_TEST}

        El modelo no puede usarse hasta que mejore su poder predictivo.

        **Esto es correcto.** El sistema te protege de operar con señales aleatorias.
        """)

    elif not SCORER_AVAILABLE or not DATA_AVAILABLE or not SIGNAL_AVAILABLE:
        st.warning("⚠️ Faltan módulos para el escaneo live.")

    else:
        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            if st.button("🔄 Escanear Ahora", type="primary", use_container_width=True):
                st.session_state.force_scan = True
        with col_info:
            if st.session_state.get('last_scan_time'):
                st.caption(f"Último scan: {st.session_state.last_scan_time}")

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

                            from core_engine import compute_adx, compute_atr

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
                                'ema_dist_15_atr': 0,
                                'ema_dist_50_atr': 0,
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
                        results_df['movement_type'] = 'CONTINUACION'
                        results_df = results_df.sort_values('ophelia_score', ascending=False).reset_index(drop=True)

                        st.session_state.scan_results = results_df
                        st.session_state.last_scan_time = get_ar_time().strftime('%H:%M:%S')

                    st.session_state.force_scan = False
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.session_state.force_scan = False

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

            if n_ophelia > 0:
                st.markdown("### 🌟 OPHELIA DETECTADO(S)")
                ophelia_alerts = scan_results[scan_results['tier'] == 'OPHELIA'].head(5)

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
- **⚙️ Leverage:** {lev_rec}x
- **🛑 SL:** {format_price(alert.get('sl_price'))}
- **🎯 TP:** {format_price(alert.get('tp_price'))}
                    """)
                    st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="no-ophelia">', unsafe_allow_html=True)
                st.markdown("### ⚪ NO OPHELIA DETECTADO")
                st.markdown(f"Ninguna de las {len(scan_results)} señales supera el threshold.")
                st.markdown("**Precisión > Frecuencia**")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Presioná 'Escanear Ahora' para analizar todos los activos.")


# ============================================================
# TAB 2: RANKING COMPLETO
# ============================================================
with tab_ranking:
    st.markdown("## 🏆 Ranking Completo — TODOS los activos")

    ranking_df = None
    source = ""

    if 'scan_results' in st.session_state and st.session_state.scan_results is not None:
        ranking_df = st.session_state.scan_results.copy()
        source = "LIVE (último escaneo)"
    elif daily_df is not None and not daily_df.empty:
        ranking_df = daily_df.copy()
        if 'ophelia_score' not in ranking_df.columns and 'score' in ranking_df.columns:
            ranking_df['ophelia_score'] = ranking_df['score']
        source = "HISTORICO"

    if ranking_df is None:
        st.warning("⚠️ No hay datos. Presioná 'Escanear Ahora' en la pestaña Live.")
    else:
        st.caption(f"Fuente: {source} · Total: {len(ranking_df)} activos")

        if 'tier' not in ranking_df.columns:
            ranking_df['tier'] = 'REJECTED'

        st.markdown("### 🟢 Ranking LONG")
        longs = ranking_df[ranking_df['direction'] == 'LONG'].sort_values(
            'ophelia_score', ascending=False
        ).reset_index(drop=True)

        if not longs.empty:
            cols_show = [c for c in ['symbol', 'ophelia_score', 'tier', 'regime', 'entry_price'] if c in longs.columns]
            longs_display = longs[cols_show].copy()
            longs_display.insert(0, 'Rank', range(1, len(longs_display) + 1))
            st.dataframe(longs_display, use_container_width=True, hide_index=True)
        else:
            st.info("Sin señales LONG.")

        st.markdown("---")

        st.markdown("### 🔴 Ranking SHORT")
        shorts = ranking_df[ranking_df['direction'] == 'SHORT'].sort_values(
            'ophelia_score', ascending=False
        ).reset_index(drop=True)

        if not shorts.empty:
            cols_show = [c for c in ['symbol', 'ophelia_score', 'tier', 'regime', 'entry_price'] if c in shorts.columns]
            shorts_display = shorts[cols_show].copy()
            shorts_display.insert(0, 'Rank', range(1, len(shorts_display) + 1))
            st.dataframe(shorts_display, use_container_width=True, hide_index=True)
        else:
            st.info("Sin señales SHORT.")

        st.markdown("---")

        # Descarga TXT
        txt_lines = []
        txt_lines.append("=" * 100)
        txt_lines.append("  OPHELIA — RANKING COMPLETO")
        txt_lines.append(f"  Generado: {get_ar_time().isoformat()}")
        txt_lines.append(f"  AUC test: {auc_test:.4f}")
        txt_lines.append("=" * 100)
        txt_lines.append("")

        txt_lines.append("--- LONG ---")
        for i, row in longs.iterrows():
            txt_lines.append(
                f"  #{i+1:<3} {row.get('symbol', ''):<15} "
                f"Score: {row.get('ophelia_score', 0):.4f}  "
                f"Tier: {row.get('tier', ''):<12} "
                f"Precio: {row.get('entry_price', 0):.6f}"
            )
        txt_lines.append("")

        txt_lines.append("--- SHORT ---")
        for i, row in shorts.iterrows():
            txt_lines.append(
                f"  #{i+1:<3} {row.get('symbol', ''):<15} "
                f"Score: {row.get('ophelia_score', 0):.4f}  "
                f"Tier: {row.get('tier', ''):<12} "
                f"Precio: {row.get('entry_price', 0):.6f}"
            )

        st.download_button(
            "📥 Descargar ranking_completo.txt",
            data='\n'.join(txt_lines),
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
                    })
                df_hours = pd.DataFrame(hours_data)
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=df_hours['Hora'],
                    y=df_hours['Trades'],
                    marker_color='#ff8c00',
                ))
                fig.update_layout(title="Distribución horaria (ARG)", height=400)
                st.plotly_chart(fig, use_container_width=True)

            top_hours = temporal.get('top_hours', {})
            if top_hours:
                st.markdown("### 🕐 Top 5 horas más frecuentes")
                for h, n in sorted(top_hours.items(), key=lambda x: -x[1])[:5]:
                    st.markdown(f"- **{int(h):02d}:00** — {n} trades")

        except Exception as e:
            st.error(f"Error: {e}")


# ============================================================
# TAB 4: HISTÓRICO
# ============================================================
with tab_trades:
    st.markdown("## 📊 Trades Históricos")

    if trades_df is None or trades_df.empty:
        st.warning("No hay trades.")
    else:
        n = len(trades_df)
        wr = trades_df['win'].mean() if 'win' in trades_df.columns else 0

        col1, col2, col3 = st.columns(3)
        col1.metric("Total trades", n)
        col2.metric("WR base", f"{wr*100:.2f}%")
        col3.metric("Features usados", len(metadata.get('features', [])))

        st.markdown("---")

        df_show = trades_df.head(100)
        st.dataframe(df_show, use_container_width=True)

        csv = df_show.to_csv(index=False)
        st.download_button(
            "📥 Descargar trades_historicos.txt",
            data=csv,
            file_name=f"ophelia_trades_{get_ar_time().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )


# ============================================================
# TAB 5: REPORTES TXT
# ============================================================
with tab_reports:
    st.markdown("## 📄 Reportes en formato TXT")

    if report_text:
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

    st.markdown("---")
    st.markdown("### 📁 Estado de archivos")
    for path, label in [
        (OPHELIA_V2_MODEL, "Modelo entrenado"),
        (OPHELIA_V2_METADATA, "Metadata"),
        (OPHELIA_V2_TRADES, "Trades históricos"),
        (OPHELIA_V2_DAILY, "Selección diaria"),
        (OPHELIA_V2_REPORT, "Certificación"),
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
st.caption(
    f"🌟 OPHELIA Precision Engine v3.0.0 · "
    f"Modo: {'✅ VÁLIDO' if MODEL_IS_VALID else '🚫 NO VÁLIDO'} · "
    f"Hora ARG: {get_ar_time().strftime('%Y-%m-%d %H:%M:%S')}"
)
