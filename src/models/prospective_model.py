"""
Advanced Movement Model (Combine Sensor Tracking)
=================================================
Trained with full micro-movement sensor features extracted from Combine drills
(kinematics, jerk, COD apex velocities, acceleration curves).
"""

from typing import List, Optional
import numpy as np
import pandas as pd

try:
    from xgboost import XGBRegressor
    HAS_XGBOOST = True
except ImportError:
    XGBRegressor = None
    HAS_XGBOOST = False


class AdvancedMovementModel:
    """Predicts regular-season athletic outcomes using advanced combine tracking sensor features."""

    def __init__(self, n_estimators: int = 150, max_depth: int = 4, learning_rate: float = 0.05):
        if not HAS_XGBOOST:
            raise ImportError("XGBoost is required for AdvancedMovementModel. Install with 'pip install xgboost'.")
        self.model = XGBRegressor(
            n_estimators=n_estimators,
            max_depth=max_depth,
            learning_rate=learning_rate,
            random_state=42,
            objective="reg:squarederror",
            n_jobs=-1,
        )
        self.feature_names: List[str] = []
        self.is_fitted = False

    def fit(self, X: pd.DataFrame, y: pd.Series, feature_names: Optional[List[str]] = None):
        if feature_names is not None:
            self.feature_names = feature_names
            X_in = X[self.feature_names]
        else:
            self.feature_names = list(X.columns)
            X_in = X

        self.model.fit(X_in, y)
        self.is_fitted = True
        return self

    def predict(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError("Model must be fitted before predict.")
        return self.model.predict(X[self.feature_names])
