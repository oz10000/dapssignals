# ophelia_engine/daily_selector.py
"""
Daily Selector v3 — Ranking OPHELIA/STANDARD + clasificación.
"""
import pandas as pd
import numpy as np
from typing import Dict
from datetime import datetime
import pytz

from ophelia_v2_config import (
    OPHELIA_MAX_PER_DAY, STANDARD_MAX_PER_DAY,
    COOLDOWN_MINUTES_PER_SYMBOL, MAX_TRADES_PER_DAY_PER_SYMBOL,
    SESSION_SPLIT_HOUR, TIMEZONE_AR,
)


class DailySelector:

    def __init__(self, scorer):
        self.scorer = scorer
        self.tz = pytz.timezone(TIMEZONE_AR)

    # ============================================================
    # SELECCIÓN CON RANKING
    # ============================================================
    def select_from_history(self, trades_df: pd.DataFrame) -> pd.DataFrame:
        """Selecciona y rankea trades OPHELIA + STANDARD."""
        if trades_df.empty:
            return pd.DataFrame()

        df = trades_df.copy()
        df['ophelia_score'] = self.scorer.score(df)

        # Clasificar nivel
        df['level'] = df['ophelia_score'].apply(self.scorer.classify)

        # Fecha ARG
        df['date'] = df['entry_time_ar'].str[:10] if 'entry_time_ar' in df.columns else 'unknown'

        # Tipo de movimiento
        df['movement_type'] = df.apply(self._classify_movement, axis=1)

        # Session (mañana/tarde)
        df['session'] = df['hour'].apply(
            lambda h: 'morning' if h < SESSION_SPLIT_HOUR else 'afternoon'
        )

        # Seleccionar por día y por nivel
        all_selected = []
        for date, group in df.groupby('date'):
            # OPHELIA del día
            ophelia = group[group['level'] == 'OPHELIA'].copy()
            if not ophelia.empty:
                ophelia = self._apply_cooldown(ophelia.sort_values('entry_time'))
                ophelia_top = ophelia.nlargest(OPHELIA_MAX_PER_DAY, 'ophelia_score').copy()
                ophelia_top['ophelia_rank'] = range(1, len(ophelia_top) + 1)
                ophelia_top['tier'] = 'OPHELIA'
                all_selected.append(ophelia_top)

            # STANDARD del día (excluyendo los ya tomados como OPHELIA)
            ophelia_ids = set(ophelia_top.index) if not ophelia.empty else set()
            standard = group[(group['level'] == 'STANDARD') & (~group.index.isin(ophelia_ids))].copy()
            if not standard.empty:
                standard = self._apply_cooldown(standard.sort_values('entry_time'))
                standard_top = standard.nlargest(STANDARD_MAX_PER_DAY, 'ophelia_score').copy()
                standard_top['ophelia_rank'] = range(1, len(standard_top) + 1)
                standard_top['tier'] = 'STANDARD'
                all_selected.append(standard_top)

        if not all_selected:
            return pd.DataFrame()

        result = pd.concat(all_selected, ignore_index=True)
        return result.sort_values(['entry_time']).reset_index(drop=True)

    def select_today(self, today_candidates: pd.DataFrame) -> pd.DataFrame:
        """Selecciona top-N de los candidatos de hoy."""
        if today_candidates.empty:
            return pd.DataFrame()

        df = today_candidates.copy()
        df['ophelia_score'] = self.scorer.score(df)
        df['level'] = df['ophelia_score'].apply(self.scorer.classify)
        df['movement_type'] = df.apply(self._classify_movement, axis=1)
        df['session'] = df['hour'].apply(
            lambda h: 'morning' if h < SESSION_SPLIT_HOUR else 'afternoon'
        )

        ophelia = df[df['level'] == 'OPHELIA'].nlargest(OPHELIA_MAX_PER_DAY, 'ophelia_score').copy()
        if not ophelia.empty:
            ophelia['ophelia_rank'] = range(1, len(ophelia) + 1)
            ophelia['tier'] = 'OPHELIA'

        standard = df[df['level'] == 'STANDARD'].nlargest(STANDARD_MAX_PER_DAY, 'ophelia_score').copy()
        if not standard.empty:
            standard['ophelia_rank'] = range(1, len(standard) + 1)
            standard['tier'] = 'STANDARD'

        return pd.concat([ophelia, standard], ignore_index=True)

    # ============================================================
    # RANKING LONG / SHORT
    # ============================================================
    def get_rankings(self, selected: pd.DataFrame) -> Dict:
        """Separa el ranking LONG y SHORT."""
        if selected.empty:
            return {'long': pd.DataFrame(), 'short': pd.DataFrame()}

        longs = selected[selected['direction'] == 'LONG'].sort_values(
            'ophelia_score', ascending=False
        ).reset_index(drop=True)
        shorts = selected[selected['direction'] == 'SHORT'].sort_values(
            'ophelia_score', ascending=False
        ).reset_index(drop=True)

        return {'long': longs, 'short': shorts}

    # ============================================================
    # COOLDOWN
    # ============================================================
    def _apply_cooldown(self, df: pd.DataFrame) -> pd.DataFrame:
        if df.empty:
            return df
        df = df.sort_values('entry_time').copy()
        keep = []
        last_time = {}
        for idx, row in df.iterrows():
            sym = row.get('symbol')
            t = row.get('entry_time')
            if sym in last_time:
                try:
                    delta = (pd.to_datetime(t) - pd.to_datetime(last_time[sym])).total_seconds() / 60
                    if delta < COOLDOWN_MINUTES_PER_SYMBOL:
                        continue
                except Exception:
                    pass
            keep.append(idx)
            last_time[sym] = t
        return df.loc[keep]

    # ============================================================
    # CLASIFICACIÓN DEL MOVIMIENTO
    # ============================================================
    def _classify_movement(self, row) -> str:
        """
        CONTINUACIÓN: dirección alineada con tendencia mayor (EMA50 slope)
        REVERSIÓN: dirección contra tendencia mayor
        """
        try:
            ema50_dist = row.get('ema_dist_50_atr', 0)
            direction = row.get('direction', 'LONG')
            # Distancia a EMA50 > 0 → precio arriba de EMA50 → tendencia alcista
            if direction == 'LONG' and ema50_dist > 0:
                return 'CONTINUACIÓN'
            elif direction == 'SHORT' and ema50_dist < 0:
                return 'CONTINUACIÓN'
            else:
                return 'REVERSIÓN'
        except Exception:
            return 'UNKNOWN'
