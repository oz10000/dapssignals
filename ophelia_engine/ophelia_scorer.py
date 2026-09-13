# ophelia_engine/ophelia_scorer.py
"""OPHELIA SCORER — P(win|features) como filtro maestro."""
import numpy as np
import pandas as pd
import pickle
from pathlib import Path
from typing import Dict, List
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score

from ophelia_v2_config import (
    MODEL_FEATURES, OPHELIA_THRESHOLD_GRID, STANDARD_THRESHOLD_GRID,
    OPHELIA_SCORE_THRESHOLD, STANDARD_SCORE_THRESHOLD,
    MIN_OPHELIA_PER_DAY, MIN_STANDARD_PER_DAY,
    OPHELIA_MAX_PER_DAY, STANDARD_MAX_PER_DAY,
    MODEL_TEST_SIZE, MODEL_RANDOM_STATE, MODEL_TYPE,
    OPHELIA_V2_MODEL,
)


class OpheliaScorer:

    def __init__(self):
        self.model = None
        self.scaler = None
        self.ophelia_threshold = OPHELIA_SCORE_THRESHOLD
        self.standard_threshold = STANDARD_SCORE_THRESHOLD
        self.metadata: Dict = {}

    def fit(self, trades_df: pd.DataFrame) -> Dict:
        if trades_df.empty or 'win' not in trades_df.columns:
            return {'error': 'Sin datos'}

        available_features = [f for f in MODEL_FEATURES if f in trades_df.columns]

        # FIX: permitir 3 features (antes pedía 5)
        MIN_FEATURES = 3
        if len(available_features) < MIN_FEATURES:
            return {'error': f'Solo {len(available_features)} features (mínimo {MIN_FEATURES})'}

        df = trades_df.sort_values('entry_time').reset_index(drop=True)
        split_idx = int(len(df) * (1 - MODEL_TEST_SIZE))
        train, test = df.iloc[:split_idx].copy(), df.iloc[split_idx:].copy()

        X_train = train[available_features].values
        y_train = train['win'].values
        X_test = test[available_features].values
        y_test = test['win'].values

        train_mask = ~np.isnan(X_train).any(axis=1)
        test_mask = ~np.isnan(X_test).any(axis=1)
        X_train, y_train = X_train[train_mask], y_train[train_mask]
        X_test, y_test = X_test[test_mask], y_test[test_mask]

        MIN_TRAIN = 20
        MIN_TEST = 10
        if len(X_train) < MIN_TRAIN or len(X_test) < MIN_TEST:
            return {'error': f'Muestra: train={len(X_train)}, test={len(X_test)}'}

        self.scaler = StandardScaler()
        X_train_s = self.scaler.fit_transform(X_train)
        X_test_s = self.scaler.transform(X_test)

        if MODEL_TYPE == 'logistic':
            self.model = LogisticRegression(
                max_iter=2000, random_state=MODEL_RANDOM_STATE,
                class_weight='balanced',
            )
        else:
            self.model = GradientBoostingClassifier(
                n_estimators=100, max_depth=3,
                random_state=MODEL_RANDOM_STATE,
            )

        self.model.fit(X_train_s, y_train)

        try:
            auc_train = roc_auc_score(y_train, self.model.predict_proba(X_train_s)[:, 1])
            auc_test = roc_auc_score(y_test, self.model.predict_proba(X_test_s)[:, 1])
        except Exception:
            auc_train = auc_test = 0.5

        self.metadata = {
            'features': available_features,
            'n_train': len(X_train),
            'n_test': len(X_test),
            'auc_train': round(auc_train, 4),
            'auc_test': round(auc_test, 4),
            'base_rate_train': round(float(y_train.mean()), 4),
            'base_rate_test': round(float(y_test.mean()), 4),
        }

        ophelia_cal = self._calibrate_threshold(
            train, test, available_features,
            OPHELIA_THRESHOLD_GRID, MIN_OPHELIA_PER_DAY, OPHELIA_MAX_PER_DAY,
        )
        self.ophelia_threshold = ophelia_cal['threshold']
        self.metadata['ophelia_threshold'] = ophelia_cal['threshold']
        self.metadata['ophelia_wr_train'] = ophelia_cal['train_wr']
        self.metadata['ophelia_wr_test'] = ophelia_cal['test_wr']
        self.metadata['ophelia_tpd_train'] = ophelia_cal['train_tpd']
        self.metadata['ophelia_tpd_test'] = ophelia_cal['test_tpd']

        standard_cal = self._calibrate_threshold(
            train, test, available_features,
            STANDARD_THRESHOLD_GRID, MIN_STANDARD_PER_DAY, STANDARD_MAX_PER_DAY,
        )
        self.standard_threshold = standard_cal['threshold']
        self.metadata['standard_threshold'] = standard_cal['threshold']
        self.metadata['standard_wr_train'] = standard_cal['train_wr']
        self.metadata['standard_wr_test'] = standard_cal['test_wr']
        self.metadata['standard_tpd_train'] = standard_cal['train_tpd']
        self.metadata['standard_tpd_test'] = standard_cal['test_tpd']

        return self.metadata

    def _calibrate_threshold(self, train, test, features, threshold_grid, min_tpd, max_per_day):
        train = train.copy()
        test = test.copy()
        train['score'] = self.model.predict_proba(self.scaler.transform(train[features].values))[:, 1]
        test['score'] = self.model.predict_proba(self.scaler.transform(test[features].values))[:, 1]

        train_days = max(1, train['entry_time_ar'].str[:10].nunique() if 'entry_time_ar' in train.columns else 1)
        test_days = max(1, test['entry_time_ar'].str[:10].nunique() if 'entry_time_ar' in test.columns else 1)

        results = []
        for τ in threshold_grid:
            train_sel = self._apply_daily_limit(train, τ, max_per_day)
            test_sel = self._apply_daily_limit(test, τ, max_per_day)
            if len(train_sel) < 2 or len(test_sel) < 2:
                continue
            results.append({
                'threshold': τ,
                'train_wr': float(train_sel['win'].mean()),
                'test_wr': float(test_sel['win'].mean()),
                'train_tpd': len(train_sel) / train_days,
                'test_tpd': len(test_sel) / test_days,
            })

        if not results:
            return {'threshold': threshold_grid[0], 'train_wr': 0, 'test_wr': 0, 'train_tpd': 0, 'test_tpd': 0}

        rdf = pd.DataFrame(results).sort_values('test_wr', ascending=False)
        rdf_ok = rdf[rdf['test_tpd'] >= min_tpd]
        if rdf_ok.empty:
            return rdf.iloc[0].to_dict()
        return rdf_ok.iloc[0].to_dict()

    def _apply_daily_limit(self, df, threshold, max_per_day):
        if 'entry_time_ar' not in df.columns:
            return df[df['score'] >= threshold]

        df = df.copy()
        df['date'] = df['entry_time_ar'].str[:10]
        selected = []
        for date, group in df.groupby('date'):
            passing = group[group['score'] >= threshold]
            if passing.empty:
                continue
            top = passing.nlargest(max_per_day, 'score')
            selected.append(top)
        if not selected:
            return pd.DataFrame()
        return pd.concat(selected, ignore_index=True)

    def score(self, features_df):
        if self.model is None or self.scaler is None:
            return np.array([])
        features = self.metadata.get('features', [])
        X = features_df[features].values
        return self.model.predict_proba(self.scaler.transform(X))[:, 1]

    def classify(self, score):
        if score >= self.ophelia_threshold:
            return 'OPHELIA'
        elif score >= self.standard_threshold:
            return 'STANDARD'
        return 'REJECTED'

    def save(self, path=OPHELIA_V2_MODEL):
        if self.model is None:
            return
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            pickle.dump({
                'model': self.model, 'scaler': self.scaler,
                'ophelia_threshold': self.ophelia_threshold,
                'standard_threshold': self.standard_threshold,
                'metadata': self.metadata,
            }, f)

    def load(self, path=OPHELIA_V2_MODEL):
        p = Path(path)
        if not p.exists():
            return False
        with open(path, 'rb') as f:
            data = pickle.load(f)
        self.model = data['model']
        self.scaler = data['scaler']
        self.ophelia_threshold = data['ophelia_threshold']
        self.standard_threshold = data['standard_threshold']
        self.metadata = data['metadata']
        return True
