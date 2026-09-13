# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

from data_engine import DataEngine
from config import (INITIAL_CAPITAL, DEFAULT_PARAMS, VERSION,
                    PROJECT_NAME, TIMEFRAME, SYMBOLS)
from signal_engine import Signal, rank_signals, classify_by_tier

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
st.caption(f"Clasificación: 🌟 OPHELIA → 🥇 S-TIER → 🥈 A-TIER → 🥉 B-TIER")

# Sidebar
with st.sidebar:
    st.header("⚙️ Config")
    st.caption(f"Capital: ${INITIAL_CAPITAL:,.2f}")
    st.caption(f"Timeframe: {TIMEFRAME}")
    st.caption(f"Activos: {len(SYMBOLS)}")
    st.markdown("---")
    if st.button("🔄 Escanear Mercado", type="primary", use_container_width=True):
        st.session_state.force_scan = True

# Init
if 'data_engine' not in st.session_state:
    st.session_state.data_engine = DataEngine()
    st.session_state.signals = []
    st.session_state.last_scan = None
    st.session_state.data_dict = {}

# Escanear
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
            progress.progress((i+1)/len(SYMBOLS))

        st.session_state.data_dict = data_dict
        st.session_state.signals = rank_signals(signals)
        st.session_state.last_scan = datetime.now().strftime("%H:%M:%S")
        st.session_state.force_scan = False

ranked = st.session_state.signals
classified = classify_by_tier(ranked)

# Métricas
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🌟 OPHELIA", len(classified['ophelia']))
col2.metric("🥇 Tier S", len(classified['s']))
col3.metric("🥈 Tier A", len(classified['a']))
col4.metric("🥉 Tier B", len(classified['b']))
col5.metric("⏱️ Último scan", st.session_state.last_scan or "Nunca")

st.markdown("---")

# Tabla de ranking
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

# Detalles por tier
st.markdown("---")
st.subheader("🌟 Señales OPHELIA (máxima calidad)")
if classified['ophelia']:
    for s in classified['ophelia'][:5]:
        with st.expander(f"🌟 {s['symbol']} — {s['direction']} | Score {s['score']:.3f} | ADX {s['adx']:.1f}"):
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

st.markdown("---")
st.caption(f"DAPS Ω × Ophelia v{VERSION} — Escaneado: {st.session_state.last_scan}")
