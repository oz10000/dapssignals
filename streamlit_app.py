# streamlit_app.py
"""
DAPS Ω × Ophelia Research Lab — Dashboard
Detecta si el pipeline corrió y muestra mensajes claros.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import json

from data_engine import DataEngine
from config import (INITIAL_CAPITAL, DEFAULT_PARAMS, VERSION,
                    PROJECT_NAME, TIMEFRAME, SYMBOLS)
from signal_engine import Signal, rank_signals, classify_by_tier
from ophelia_lab.report_generator import ReportGenerator
from ophelia_lab.operational_report import OperationalReport

st.set_page_config(page_title=f"{PROJECT_NAME}", page_icon="🌟", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #fafafa; }
.tier-ophelia { background: linear-gradient(90deg, #ffd700, #ff8c00); color: #000; padding: 10px; border-radius: 8px; font-weight: bold; }
.warning-box { background: #fff3cd; border-left: 5px solid #ffc107; padding: 15px; border-radius: 5px; margin: 10px 0; }
.info-box { background: #d1ecf1; border-left: 5px solid #17a2b8; padding: 15px; border-radius: 5px; margin: 10px 0; }
.success-box { background: #d4edda; border-left: 5px solid #28a745; padding: 15px; border-radius: 5px; margin: 10px 0; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════
def pipeline_has_run() -> bool:
    """Detecta si run_lab.py ya se ejecutó alguna vez."""
    return Path('data/optimization/backtest_metrics.json').exists()


def get_pipeline_status() -> dict:
    """Devuelve el estado de cada archivo generado por el pipeline."""
    files = {
        'backtest_metrics.json': 'data/optimization/backtest_metrics.json',
        'trades.parquet': 'data/trades/trades.parquet',
        'monte_carlo.json': 'data/optimization/monte_carlo.json',
        'walk_forward.json': 'data/optimization/walk_forward.json',
        'trailing_optimal.csv': 'data/optimization/trailing_optimal.csv',
        'break_even_optimal.csv': 'data/optimization/break_even_optimal.csv',
        'leverage_optimal.csv': 'data/optimization/leverage_optimal.csv',
        'full_report.txt': 'reports/full_report.txt',
        'OPHELIA_OPERATIONAL_REPORT.md': 'reports/OPHELIA_OPERATIONAL_REPORT.md',
        'CERTIFICATION_REPORT.md': 'reports/CERTIFICATION_REPORT.md',
        'MONTE_CARLO_REPORT.md': 'reports/MONTE_CARLO_REPORT.md',
    }
    status = {}
    for name, path in files.items():
        p = Path(path)
        status[name] = {
            'exists': p.exists(),
            'size': p.stat().st_size if p.exists() else 0,
            'path': path,
        }
    return status


# ══════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════
st.title(f"🌟 {PROJECT_NAME} v{VERSION}")
st.caption("Clasificación: 🌟 OPHELIA → 🥇 S-TIER → 🥈 A-TIER → 🥉 B-TIER")


# ══════════════════════════════════════════════════════════════
# VERIFICACIÓN DE ESTADO DEL PIPELINE
# ══════════════════════════════════════════════════════════════
pipeline_ran = pipeline_has_run()

if not pipeline_ran:
    st.markdown("""
    <div class="warning-box">
    <h3>⚠️ El pipeline NO ha sido ejecutado</h3>
    <p>Los reportes aparecerán vacíos (<code>❌ NO VALIDADO</code>) hasta que ejecutes el pipeline.</p>
    <p><strong>Para ejecutarlo, hacé una de estas cosas:</strong></p>
    <ol>
        <li><strong>Localmente:</strong> <code>python run_lab.py</code></li>
        <li><strong>En GitHub:</strong> Ir a <em>Actions → Manual Pipeline Run → Run workflow</em></li>
        <li><strong>En GitHub (automático):</strong> Los workflows corren a las 06:00 UTC (daily), lunes 04:00 UTC (weekly), y día 1 del mes 03:00 UTC (monthly)</li>
    </ol>
    <p>Después de ejecutar, descargá los artifacts de GitHub y colocalos en las carpetas <code>data/</code> y <code>reports/</code>.</p>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.header("⚙️ Config")
    st.caption(f"Capital: ${INITIAL_CAPITAL:,.2f}")
    st.caption(f"Timeframe: {TIMEFRAME}")
    st.caption(f"Activos: {len(SYMBOLS)}")
    st.markdown("---")

    # Indicador de pipeline
    if pipeline_ran:
        st.success("✅ Pipeline ejecutado")
    else:
        st.warning("⚠️ Pipeline no ejecutado")

    st.markdown("---")

    if st.button("🔄 Escanear Mercado", type="primary", use_container_width=True):
        st.session_state.force_scan = True

    if st.button("📊 Generar full_report.txt", use_container_width=True):
        with st.spinner("Generando..."):
            try:
                path = ReportGenerator.generate_txt('reports/full_report.txt')
                st.success(f"✅ {path}")
            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("📋 Generar Reporte Operativo", use_container_width=True):
        with st.spinner("Generando..."):
            try:
                path = OperationalReport().generate()
                st.success(f"✅ {path}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.caption("📁 Archivos se guardan en `reports/`")


# ══════════════════════════════════════════════════════════════
# INICIALIZACIÓN
# ══════════════════════════════════════════════════════════════
if 'data_engine' not in st.session_state:
    with st.spinner("Inicializando DataEngine..."):
        st.session_state.data_engine = DataEngine()
        st.session_state.signals = []
        st.session_state.last_scan = None
        st.session_state.data_dict = {}


# ══════════════════════════════════════════════════════════════
# ESCANEO
# ══════════════════════════════════════════════════════════════
if st.session_state.get('force_scan') or st.session_state.last_scan is None:
    with st.spinner("🔍 Escaneando activos..."):
        de = st.session_state.data_engine
        signals = []
        data_dict = {}
        progress = st.progress(0)
        status = st.empty()

        for i, sym in enumerate(SYMBOLS):
            status.text(f"Escaneando {sym} ({i+1}/{len(SYMBOLS)})...")
            try:
                df = de.fetch_ohlcv(sym, limit=300)
                if df is not None and not df.empty:
                    data_dict[sym] = df
                    s = Signal(sym, df, DEFAULT_PARAMS)
                    signals.append(s.to_dict())
            except Exception:
                pass
            progress.progress((i + 1) / len(SYMBOLS))

        status.empty()
        progress.empty()

        st.session_state.data_dict = data_dict
        st.session_state.signals = rank_signals(signals)
        st.session_state.last_scan = datetime.now().strftime("%H:%M:%S")
        st.session_state.force_scan = False

ranked = st.session_state.signals
classified = classify_by_tier(ranked)


# ══════════════════════════════════════════════════════════════
# PESTAÑAS
# ══════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Señales en Vivo",
    "🧪 Backtest & Métricas",
    "📄 Reportes y Descargas",
    "🔧 Estado del Pipeline",
])


# ══════════════════════════════════════════════════════════════
# TAB 1 — SEÑALES EN VIVO
# ══════════════════════════════════════════════════════════════
with tab1:
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🌟 OPHELIA", len(classified['ophelia']))
    col2.metric("🥇 Tier S", len(classified['s']))
    col3.metric("🥈 Tier A", len(classified['a']))
    col4.metric("🥉 Tier B", len(classified['b']))
    col5.metric("⏱️ Último scan", st.session_state.last_scan or "Nunca")

    st.markdown("---")
    st.subheader("🏆 Ranking por Calidad")

    if ranked:
        df = pd.DataFrame(ranked)
        display_cols = ['rank_label', 'symbol', 'tier', 'direction', 'score',
                        'adx', 'ker', 'regime', 'confidence',
                        'entry_price', 'sl_price', 'tp_price',
                        'tp_percent', 'sl_percent', 'estimated_time_to_trade']
        available = [c for c in display_cols if c in df.columns]
        st.dataframe(df[available], use_container_width=True, height=500)
    else:
        st.info("Presiona 'Escanear Mercado' en el sidebar")

    st.markdown("---")
    st.subheader("🌟 Señales OPHELIA (máxima calidad)")

    if classified['ophelia']:
        for s in classified['ophelia'][:5]:
            with st.expander(f"🌟 {s['symbol']} — {s['direction']} | Score {s['score']:.3f}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("Entrada", f"${s['entry_price']:.4f}")
                c1.metric("SL", f"${s['sl_price']:.4f} ({s['sl_percent']:.2f}%)")
                c1.metric("TP", f"${s['tp_price']:.4f} ({s['tp_percent']:.2f}%)")
                c2.metric("Régimen", s['regime'])
                c2.metric("Confianza", f"{s['confidence']:.1f}%")
                c2.metric("Persistencia", f"{s['persistence']:.1f}%")
                c3.metric("Trailing Act.", f"{s['trailing_activation']*100:.2f}%")
                c3.metric("Trailing Dist.", f"{s['trailing_distance']*100:.2f}%")
                c3.metric("BE Trigger", f"{s['break_even_trigger']*100:.2f}%")
    else:
        st.info("No hay señales OPHELIA en este momento")

    st.markdown("---")
    st.subheader("🥇🥈🥉 Tiers S / A / B")

    for tier_label, tier_key, color in [("S-TIER", 's', '🟢'), ("A-TIER", 'a', '🟠'), ("B-TIER", 'b', '🔴')]:
        with st.expander(f"{color} {tier_label} — {len(classified[tier_key])} señales"):
            if classified[tier_key]:
                df_t = pd.DataFrame(classified[tier_key])
                cols = [c for c in ['symbol', 'direction', 'score', 'adx', 'ker', 'regime', 'confidence']
                        if c in df_t.columns]
                st.dataframe(df_t[cols])
            else:
                st.caption("Sin señales")


# ══════════════════════════════════════════════════════════════
# TAB 2 — BACKTEST & MÉTRICAS
# ══════════════════════════════════════════════════════════════
with tab2:
    st.header("🧪 Backtest & Métricas Validadas")

    if not pipeline_ran:
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ Pipeline no ejecutado</h3>
        <p>Esta sección se llena automáticamente cuando corrés <code>python run_lab.py</code> o esperás a que GitHub Actions lo ejecute.</p>
        <p><strong>Mientras tanto, no hay métricas disponibles.</strong></p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.caption("Datos generados por `run_lab.py` (backtest realista con comisión + slippage).")

        # Backtest metrics
        bt_path = Path('data/optimization/backtest_metrics.json')
        if bt_path.exists():
            bt = json.loads(bt_path.read_text(encoding='utf-8'))

            if bt.get('status') == 'VALIDATED':
                st.success(f"✅ Backtest validado — {bt.get('n_trades', 0)} trades")

                cols = st.columns(4)
                cols[0].metric("Win Rate", f"{bt.get('win_rate', 0):.4f}")
                cols[1].metric("Profit Factor", f"{bt.get('profit_factor', 0):.4f}")
                cols[2].metric("Sharpe", f"{bt.get('sharpe', 0):.4f}")
                cols[3].metric("Max DD", f"{bt.get('max_drawdown_pct', 0):.4f}%")

                cols = st.columns(3)
                cols[0].metric("Expectancy", f"{bt.get('expectancy_pct', 0):.4f}%")
                cols[1].metric("Avg Win", f"{bt.get('avg_win_pct', 0):.4f}%")
                cols[2].metric("Avg Loss", f"{bt.get('avg_loss_pct', 0):.4f}%")

                if 'by_tier' in bt and bt['by_tier']:
                    st.subheader("📊 Desglose por Tier")
                    tier_df = pd.DataFrame([
                        {'Tier': k, 'N': v['n'], 'WR': f"{v['wr']:.4f}",
                         'Avg PnL': f"{v['avg_pnl']:.4f}%"}
                        for k, v in bt['by_tier'].items()
                    ])
                    st.dataframe(tier_df, use_container_width=True)
            else:
                st.warning("⚠️ Backtest no validado. Ejecutá `python run_lab.py`")

        st.markdown("---")

        # Trades
        trades_path = Path('data/trades/trades.parquet')
        if trades_path.exists():
            trades = pd.read_parquet(trades_path)
            st.subheader(f"📈 Últimos trades ({len(trades)} totales)")
            st.dataframe(trades.tail(50), use_container_width=True)

            if 'net_pnl_pct' in trades.columns and len(trades) > 0:
                equity = INITIAL_CAPITAL * (1 + trades['net_pnl_pct']).cumprod()
                fig = go.Figure()
                fig.add_trace(go.Scatter(y=equity, mode='lines', name='Equity',
                                         line=dict(color='green')))
                fig.update_layout(title="Curva de Equity",
                                  xaxis_title="Trade #",
                                  yaxis_title="Capital ($)")
                st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Monte Carlo
        mc_path = Path('data/optimization/monte_carlo.json')
        if mc_path.exists():
            mc = json.loads(mc_path.read_text(encoding='utf-8'))
            st.subheader("🎲 Monte Carlo")
            cols = st.columns(4)
            cols[0].metric("Ruin Prob", f"{mc.get('ruin_probability', 0):.4f}")
            cols[1].metric("Mean Final", f"${mc.get('mean_final', 0):,.0f}")
            cols[2].metric("P5 Final", f"${mc.get('p5_final', 0):,.0f}")
            cols[3].metric("P95 Final", f"${mc.get('p95_final', 0):,.0f}")


# ══════════════════════════════════════════════════════════════
# TAB 3 — REPORTES Y DESCARGAS
# ══════════════════════════════════════════════════════════════
with tab3:
    st.header("📄 Reportes y Descargas")

    if not pipeline_ran:
        st.markdown("""
        <div class="warning-box">
        <h3>⚠️ No hay reportes para descargar</h3>
        <p>Ejecutá <code>python run_lab.py</code> primero, o esperá a GitHub Actions.</p>
        <p>Los botones de abajo generan reportes <em>vacíos</em> si no hay datos.</p>
        </div>
        """, unsafe_allow_html=True)

    st.caption("Descargá los reportes completos con todas las métricas reales.")

    # Botones
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🔄 Generar full_report.txt", use_container_width=True):
            with st.spinner("Generando..."):
                try:
                    path = ReportGenerator.generate_txt('reports/full_report.txt')
                    st.success(f"✅ {path}")
                except Exception as e:
                    st.error(f"Error: {e}")
    with col_b:
        if st.button("🔄 Generar OPHELIA_OPERATIONAL_REPORT.md", use_container_width=True):
            with st.spinner("Generando..."):
                try:
                    path = OperationalReport().generate()
                    st.success(f"✅ {path}")
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")

    # Descarga: full_report.txt
    report_txt = Path('reports/full_report.txt')
    if report_txt.exists():
        st.subheader("📥 Reporte Completo (TXT)")
        content = report_txt.read_text(encoding='utf-8')
        st.download_button(
            label="📥 Descargar full_report.txt",
            data=content,
            file_name=f"daps_ophelia_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True,
        )
        with st.expander("👁️ Vista previa"):
            st.code(content[:3000], language='text')
    else:
        st.warning("⚠️ No existe `reports/full_report.txt`")

    st.markdown("---")

    # Descarga: OPHELIA_OPERATIONAL_REPORT.md
    op_report = Path('reports/OPHELIA_OPERATIONAL_REPORT.md')
    if op_report.exists():
        st.subheader("📋 Reporte Operativo (MD)")
        content = op_report.read_text(encoding='utf-8')
        st.download_button(
            label="📥 Descargar OPHELIA_OPERATIONAL_REPORT.md",
            data=content,
            file_name=f"ophelia_operational_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )
        with st.expander("👁️ Vista previa"):
            st.markdown(content[:3000])
    else:
        st.warning("⚠️ No existe `reports/OPHELIA_OPERATIONAL_REPORT.md`")


# ══════════════════════════════════════════════════════════════
# TAB 4 — ESTADO DEL PIPELINE
# ══════════════════════════════════════════════════════════════
with tab4:
    st.header("🔧 Estado del Pipeline")
    st.caption("Estado detallado de cada archivo generado por `run_lab.py`.")

    status = get_pipeline_status()

    # Resumen
    total = len(status)
    present = sum(1 for v in status.values() if v['exists'])
    st.metric("Archivos presentes", f"{present}/{total}")

    if present == total:
        st.markdown('<div class="success-box"><strong>✅ Todos los archivos generados</strong></div>',
                    unsafe_allow_html=True)
    elif present > 0:
        st.markdown(f'<div class="warning-box"><strong>⚠️ Pipeline parcialmente ejecutado ({present}/{total})</strong></div>',
                    unsafe_allow_html=True)
    else:
        st.markdown('<div class="warning-box"><strong>❌ Pipeline no ejecutado</strong></div>',
                    unsafe_allow_html=True)

    st.markdown("---")

    # Tabla de estado
    st.subheader("📁 Detalle por archivo")
    rows = []
    for name, info in status.items():
        rows.append({
            'Archivo': name,
            'Estado': '✅' if info['exists'] else '❌',
            'Tamaño': f"{info['size']:,} bytes" if info['exists'] else '—',
            'Ruta': info['path'],
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.markdown("---")

    # Instrucciones
    st.subheader("🚀 ¿Cómo ejecutar el pipeline?")
    st.markdown("""
    ### Opción 1: Localmente (más rápido)
    ```bash
    # En la terminal del proyecto
    python diagnose.py      # Verifica que todo esté OK
    python run_lab.py       # Ejecuta el pipeline completo
