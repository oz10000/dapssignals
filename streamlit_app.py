# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from pathlib import Path
import os

from data_engine import DataEngine
from config import (INITIAL_CAPITAL, DEFAULT_PARAMS, VERSION,
                    PROJECT_NAME, TIMEFRAME, SYMBOLS)
from signal_engine import Signal, rank_signals, classify_by_tier
from ophelia_lab.report_generator import ReportGenerator

st.set_page_config(page_title=f"{PROJECT_NAME}", page_icon="🌟", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #fafafa; }
.tier-ophelia { background: linear-gradient(90deg, #ffd700, #ff8c00); color: #000; padding: 10px; border-radius: 8px; font-weight: bold; }
.tier-s { background: #e8f5e9; padding: 8px; border-left: 5px solid #4caf50; }
.tier-a { background: #fff3e0; padding: 8px; border-left: 5px solid #ff9800; }
.tier-b { background: #ffebee; padding: 8px; border-left: 5px solid #f44336; }
</style>
""", unsafe_allow_html=True)

st.title(f"🌟 {PROJECT_NAME} v{VERSION}")
st.caption("Clasificación: 🌟 OPHELIA → 🥇 S-TIER → 🥈 A-TIER → 🥉 B-TIER")

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.header("⚙️ Config")
    st.caption(f"Capital: ${INITIAL_CAPITAL:,.2f}")
    st.caption(f"Timeframe: {TIMEFRAME}")
    st.caption(f"Activos: {len(SYMBOLS)}")
    st.markdown("---")

    if st.button("🔄 Escanear Mercado", type="primary", use_container_width=True):
        st.session_state.force_scan = True

    if st.button("📊 Generar Reporte TXT", use_container_width=True):
        with st.spinner("Generando reporte..."):
            try:
                path = ReportGenerator.generate_txt('reports/full_report.txt')
                st.success(f"✅ Reporte creado en {path}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")
    st.caption("📁 Archivos generados se guardan en `reports/`")

# ============================================================
# INICIALIZACIÓN
# ============================================================
if 'data_engine' not in st.session_state:
    st.session_state.data_engine = DataEngine()
    st.session_state.signals = []
    st.session_state.last_scan = None
    st.session_state.data_dict = {}

# ============================================================
# ESCANEO
# ============================================================
if st.session_state.get('force_scan') or st.session_state.last_scan is None:
    with st.spinner("🔍 Escaneando..."):
        de = st.session_state.data_engine
        signals = []
        data_dict = {}
        progress = st.progress(0)
        for i, sym in enumerate(SYMBOLS):
            df = de.fetch_ohlcv(sym, limit=300)
            if df is not None and not df.empty:
                data_dict[sym] = df
                s = Signal(sym, df, DEFAULT_PARAMS)
                signals.append(s.to_dict())
            progress.progress((i + 1) / len(SYMBOLS))

        st.session_state.data_dict = data_dict
        st.session_state.signals = rank_signals(signals)
        st.session_state.last_scan = datetime.now().strftime("%H:%M:%S")
        st.session_state.force_scan = False

ranked = st.session_state.signals
classified = classify_by_tier(ranked)

# ============================================================
# PESTAÑAS
# ============================================================
tab1, tab2, tab3 = st.tabs(["📈 Señales en Vivo", "🧪 Backtest & Métricas", "📄 Reportes y Descargas"])

# ============================================================
# TAB 1 — SEÑALES EN VIVO
# ============================================================
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
        display = df[['rank_label', 'symbol', 'tier', 'direction', 'score',
                      'adx', 'ker', 'regime', 'confidence',
                      'entry_price', 'sl_price', 'tp_price',
                      'tp_percent', 'sl_percent', 'estimated_time_to_trade']]
        st.dataframe(display, use_container_width=True, height=500)
    else:
        st.info("Presiona 'Escanear Mercado'")

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
                st.dataframe(df_t[['symbol', 'direction', 'score', 'adx', 'ker', 'regime', 'confidence']])
            else:
                st.caption("Sin señales")

# ============================================================
# TAB 2 — BACKTEST & MÉTRICAS
# ============================================================
with tab2:
    st.header("🧪 Backtest & Métricas Validadas")
    st.caption("Estos datos provienen de `run_lab.py` (backtest realista con comisión + slippage).")

    # Backtest metrics
    bt_path = Path('data/optimization/backtest_metrics.json')
    if bt_path.exists():
        import json
        bt = json.loads(bt_path.read_text())

        if bt.get('status') == 'VALIDATED':
            st.success(f"✅ Backtest validado — {bt.get('n_trades', 0)} trades")

            cols = st.columns(4)
            cols[0].metric("Win Rate", f"{bt.get('win_rate', 0):.2%}")
            cols[1].metric("Profit Factor", f"{bt.get('profit_factor', 0):.3f}")
            cols[2].metric("Sharpe", f"{bt.get('sharpe', 0):.3f}")
            cols[3].metric("Max DD", f"{bt.get('max_drawdown_pct', 0):.2f}%")

            cols = st.columns(3)
            cols[0].metric("Expectancy", f"{bt.get('expectancy_pct', 0):.4f}%")
            cols[1].metric("Avg Win", f"{bt.get('avg_win_pct', 0):.4f}%")
            cols[2].metric("Avg Loss", f"{bt.get('avg_loss_pct', 0):.4f}%")

            if 'by_tier' in bt and bt['by_tier']:
                st.subheader("📊 Desglose por Tier")
                tier_df = pd.DataFrame([
                    {'Tier': k, 'N': v['n'], 'WR': f"{v['wr']:.2%}", 'Avg PnL': f"{v['avg_pnl']:.4f}%"}
                    for k, v in bt['by_tier'].items()
                ])
                st.dataframe(tier_df, use_container_width=True)
        else:
            st.warning("⚠️ Backtest no validado. Ejecutá `python run_lab.py`")
    else:
        st.info("❌ No hay métricas de backtest. Ejecutá `python run_lab.py` primero.")

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
            fig.add_trace(go.Scatter(y=equity, mode='lines', name='Equity', line=dict(color='green')))
            fig.update_layout(title="Curva de Equity", xaxis_title="Trade #", yaxis_title="Capital ($)")
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("❌ No hay trades. Ejecutá `python run_lab.py`")

    st.markdown("---")

    # Monte Carlo
    mc_path = Path('data/optimization/monte_carlo.json')
    if mc_path.exists():
        import json
        mc = json.loads(mc_path.read_text())
        st.subheader("🎲 Monte Carlo")
        cols = st.columns(4)
        cols[0].metric("Ruin Prob", f"{mc.get('ruin_probability', 0):.2%}")
        cols[1].metric("Mean Final", f"${mc.get('mean_final', 0):,.0f}")
        cols[2].metric("P5 Final", f"${mc.get('p5_final', 0):,.0f}")
        cols[3].metric("P95 Final", f"${mc.get('p95_final', 0):,.0f}")

# ============================================================
# TAB 3 — REPORTES Y DESCARGAS
# ============================================================
with tab3:
    st.header("📄 Reportes y Descargas")
    st.caption("Descargá el reporte completo en TXT para revisar todas las métricas.")

    # Botón generar
    if st.button("🔄 Regenerar Reporte TXT", type="primary"):
        with st.spinner("Generando..."):
            try:
                path = ReportGenerator.generate_txt('reports/full_report.txt')
                st.success(f"✅ Generado: {path}")
            except Exception as e:
                st.error(f"Error: {e}")

    st.markdown("---")

    # Descargas disponibles
    report_path = Path('reports/full_report.txt')
    if report_path.exists():
        st.subheader("📥 Descargar Reporte Completo")
        content = report_path.read_text(encoding='utf-8')
        st.download_button(
            label="📥 Descargar full_report.txt",
            data=content,
            file_name=f"daps_ophelia_report_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )
        with st.expander("👁️ Vista previa del reporte"):
            st.code(content[:3000], language='text')
    else:
        st.warning("⚠️ No existe `reports/full_report.txt`. Presioná 'Regenerar Reporte TXT'.")

    st.markdown("---")

    # Otros reportes
    st.subheader("📁 Otros archivos generados")
    for f in ['reports/CERTIFICATION_REPORT.md', 'reports/MONTE_CARLO_REPORT.md',
              'data/optimization/backtest_metrics.json',
              'data/optimization/walk_forward.json',
              'data/optimization/trailing_optimal.csv',
              'data/optimization/break_even_optimal.csv',
              'data/optimization/leverage_optimal.csv']:
        p = Path(f)
        status = "✅" if p.exists() else "❌"
        size = f"{p.stat().st_size} bytes" if p.exists() else "no existe"
        st.caption(f"{status} `{f}` — {size}")

st.markdown("---")
st.caption(f"DAPS Ω × Ophelia v{VERSION} — Escaneado: {st.session_state.last_scan}")
