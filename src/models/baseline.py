"""
Traditional Combine Baseline Model
==================================
Establishes the statistical baseline using only traditional Combine measurements:
- 40-yard dash
- 10-yard and 20-yard splits
- Vertical jump & broad jump
- 20-yard shuttle & 3-cone drill
- Height, weight, BMI
Used to predict on-field athletic targets (e.g. game_speed_p95, burst acceleration).
"""

from typing import List, Tuple
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline


class TraditionalCombineBaseline:
    """Predicts regular-season athletic performance using ONLY traditional combine features."""

    DEFAULT_FEATURES = [
        "forty_yard_dash",
        "ten_yard_split",
        "twenty_yard_split",
        "vertical_jump",
        "broad_jump",
        "three_cone",
        "shuttle",
        "weight",
        "height_inches",
    ]

    def __init__(self, features: List[str] = None, alpha: float = 1.0):
        self.features = features or self.DEFAULT_FEATURES
        self.model = Pipeline([
            ("scaler", StandardScaler()),
            ("regressor", Ridge(alpha=alpha, random_state=42))
        ])
        self.is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series):
        available_cols = [c for c in self.features if c in X.columns]
        if not available_cols:
            raise ValueError(f"None of {self.features} found in feature matrix.")
        self.available_features_ = available_cols
        self.model.fit(X[self.available_features_].fillna(X[self.available_features_].median()), y)
        self.is_fitted = True
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict.")
        return self.model.predict(X[self.available_features_].fillna(X[self.available_features_].median()))
