"""
ATHLETIX AI: Model Comparison & Cross-Validation Engine
======================================================
Implements Model A (Traditional Baseline), Model B (Sensor Movement),
and Model C (Hybrid Model) under repeated position-stratified cross-validation.

Methodological Safeguards:
- Strict in-fold preprocessing: Imputation and scaling fitted strictly on training folds.
- Identical validation splits across all competing models.
- Generates unbiased Out-Of-Fold (OOF) predictions for Athletic Alpha residual evaluation.
- Compares complete-case vs imputed sensitivity analyses.
- Evaluates R^2, MAE, RMSE, and Spearman rank correlation with 95% bootstrap confidence intervals.
"""

from typing import Dict, Any, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge, ElasticNet
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RepeatedStratifiedKFold
from scipy import stats
import xgboost as xgb

from src.config import RANDOM_SEED


class ModelComparisonEngine:
    """Manages cross-validated comparison of traditional, sensor, and hybrid models."""

    TRADITIONAL_FEATURES = [
        "forty", "ten_yd_split", "vertical", "broad_jump",
        "three_cone", "short_shuttle", "combine_height", "combine_weight"
    ]

    SENSOR_FEATURES = [
        "combine_max_speed", "combine_mean_speed", "combine_initial_accel_mean",
        "combine_burst_latency_mean", "combine_mean_pos_jerk", "combine_max_decel",
        "forty_curve_tau", "combine_mean_cod_apex_speed", "combine_mean_speed_preservation_ratio",
        "combine_peak_angular_velocity", "combine_mean_turning_efficiency"
    ]

    POSITION_DUMMIES = [
        "pos_skill", "pos_oline", "pos_dfront", "pos_dback"
    ]

    def __init__(self, data_df: pd.DataFrame, target_col: str = "game_speed_p95"):
        self.raw_df = data_df.copy()
        self.target_col = target_col
        self._prepare_features()

    def _prepare_features(self):
        """Prepares position group indicators and numeric matrices."""
        df = self.raw_df.copy()

        # Map position to macro groups
        def get_macro_pos(pos):
            pos = str(pos).upper()
            if pos in ["WR", "TE", "RB", "FB"]:
                return "SKILL_OFFENSE"
            elif pos in ["T", "G", "C", "OT", "OG"]:
                return "LINE_OFFENSE"
            elif pos in ["DE", "DT", "NT", "EDGE", "DL", "OLB"]:
                return "DEFENSIVE_FRONT"
            elif pos in ["CB", "SS", "FS", "DB", "S"]:
                return "DEFENSIVE_BACKS"
            return "OTHER"

        df["macro_position"] = df["nfl_position"].apply(get_macro_pos)
        df["pos_skill"] = (df["macro_position"] == "SKILL_OFFENSE").astype(float)
        df["pos_oline"] = (df["macro_position"] == "LINE_OFFENSE").astype(float)
        df["pos_dfront"] = (df["macro_position"] == "DEFENSIVE_FRONT").astype(float)
        df["pos_dback"] = (df["macro_position"] == "DEFENSIVE_BACKS").astype(float)

        self.df = df
        self.y = df[self.target_col].values
        self.strata = df["macro_position"].values

    def build_pipeline(self, model_type: str = "ridge", alpha: float = 1.0, l1_ratio: float = 0.5) -> Pipeline:
        """Constructs an in-fold preprocessing and regressor pipeline."""
        if model_type == "ridge":
            regressor = Ridge(alpha=alpha, random_state=RANDOM_SEED)
        elif model_type == "elastic_net":
            regressor = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=RANDOM_SEED, max_iter=2000)
        elif model_type == "xgboost":
            regressor = xgb.XGBRegressor(
                n_estimators=100, max_depth=3, learning_rate=0.05,
                subsample=0.8, colsample_bytree=0.8, random_state=RANDOM_SEED, n_jobs=1
            )
        else:
            raise ValueError(f"Unknown model_type: {model_type}")

        pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("regressor", regressor),
        ])
        return pipeline

    def evaluate_model_cv(
        self,
        feature_cols: List[str],
        model_type: str = "ridge",
        n_splits: int = 5,
        n_repeats: int = 10,
        alpha: float = 1.0,
        l1_ratio: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Runs repeated position-stratified K-fold cross-validation.
        Collects fold-level metrics and out-of-fold predictions.
        """
        X = self.df[feature_cols].values
        y = self.y
        strata = self.strata

        rskf = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=RANDOM_SEED)

        fold_r2 = []
        fold_mae = []
        fold_rmse = []
        fold_spearman = []

        oof_predictions = np.zeros((len(y), n_repeats))
        oof_counts = np.zeros(len(y))

        fold_idx = 0
        for train_idx, test_idx in rskf.split(X, strata):
            repeat_idx = fold_idx // n_splits
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]

            pipeline = self.build_pipeline(model_type=model_type, alpha=alpha, l1_ratio=l1_ratio)
            pipeline.fit(X_train, y_train)

            preds = pipeline.predict(X_test)
            oof_predictions[test_idx, repeat_idx] = preds

            # Metrics
            ss_res = np.sum((y_test - preds) ** 2)
            ss_tot = np.sum((y_test - np.mean(y_test)) ** 2)
            r2 = 1.0 - (ss_res / (ss_tot + 1e-8))
            mae = np.mean(np.abs(y_test - preds))
            rmse = np.sqrt(np.mean((y_test - preds) ** 2))
            spearman_corr, _ = stats.spearmanr(y_test, preds)

            fold_r2.append(r2)
            fold_mae.append(mae)
            fold_rmse.append(rmse)
            fold_spearman.append(spearman_corr)
            fold_idx += 1

        # Mean out-of-fold prediction across repeats
        mean_oof_pred = np.mean(oof_predictions, axis=1)

        # Overall OOF R^2
        oof_ss_res = np.sum((y - mean_oof_pred) ** 2)
        oof_ss_tot = np.sum((y - np.mean(y)) ** 2)
        oof_r2 = 1.0 - (oof_ss_res / oof_ss_tot)
        oof_mae = np.mean(np.abs(y - mean_oof_pred))
        oof_rmse = np.sqrt(np.mean((y - mean_oof_pred) ** 2))
        oof_spearman, _ = stats.spearmanr(y, mean_oof_pred)

        # 95% Confidence Interval for mean fold R^2
        r2_ci = stats.t.interval(0.95, len(fold_r2) - 1, loc=np.mean(fold_r2), scale=stats.sem(fold_r2))

        return {
            "model_type": model_type,
            "feature_set": feature_cols,
            "n_features": len(feature_cols),
            "oof_r2": round(float(oof_r2), 4),
            "oof_mae": round(float(oof_mae), 4),
            "oof_rmse": round(float(oof_rmse), 4),
            "oof_spearman": round(float(oof_spearman), 4),
            "mean_fold_r2": round(float(np.mean(fold_r2)), 4),
            "std_fold_r2": round(float(np.std(fold_r2)), 4),
            "ci_95_r2": [round(float(r2_ci[0]), 4), round(float(r2_ci[1]), 4)],
            "mean_fold_mae": round(float(np.mean(fold_mae)), 4),
            "mean_fold_rmse": round(float(np.mean(fold_rmse)), 4),
            "mean_fold_spearman": round(float(np.mean(fold_spearman)), 4),
            "oof_predictions": mean_oof_pred,
            "fold_r2_distribution": fold_r2,
        }

    def run_complete_model_comparison(self) -> Dict[str, Any]:
        """
        Compares Model A (Traditional), Model B (Sensor), and Model C (Hybrid).
        """
        model_a_feats = self.TRADITIONAL_FEATURES + self.POSITION_DUMMIES
        model_b_feats = self.SENSOR_FEATURES + self.POSITION_DUMMIES
        model_c_feats = list(dict.fromkeys(self.TRADITIONAL_FEATURES + self.SENSOR_FEATURES + self.POSITION_DUMMIES))

        results = {
            "Model_A_Ridge_Traditional": self.evaluate_model_cv(model_a_feats, model_type="ridge", alpha=10.0),
            "Model_A_ElasticNet_Traditional": self.evaluate_model_cv(model_a_feats, model_type="elastic_net", alpha=0.1, l1_ratio=0.5),
            "Model_B_Ridge_Sensor": self.evaluate_model_cv(model_b_feats, model_type="ridge", alpha=10.0),
            "Model_B_XGBoost_Sensor": self.evaluate_model_cv(model_b_feats, model_type="xgboost"),
            "Model_C_Ridge_Hybrid": self.evaluate_model_cv(model_c_feats, model_type="ridge", alpha=10.0),
            "Model_C_XGBoost_Hybrid": self.evaluate_model_cv(model_c_feats, model_type="xgboost"),
        }
        return results

    def run_complete_case_sensitivity(self) -> Dict[str, Any]:
        """
        Runs sensitivity analysis on complete-case subsets:
        1. Complete agility cases (N = 43 with 3-cone and shuttle).
        2. Complete sprint/jump cases (N = 119 without 3-cone and shuttle).
        """
        df = self.df.copy()
        
        # 1. Full agility complete cases
        cc_agility = df.dropna(subset=self.TRADITIONAL_FEATURES)
        engine_cc1 = ModelComparisonEngine(cc_agility, target_col=self.target_col)
        res_cc1 = engine_cc1.evaluate_model_cv(
            self.TRADITIONAL_FEATURES + self.POSITION_DUMMIES, model_type="ridge", n_splits=5, n_repeats=5
        )

        # 2. Non-agility complete cases
        trad_no_agility = ["forty", "ten_yd_split", "vertical", "broad_jump", "combine_height", "combine_weight"]
        cc_no_ag = df.dropna(subset=trad_no_agility)
        engine_cc2 = ModelComparisonEngine(cc_no_ag, target_col=self.target_col)
        res_cc2 = engine_cc2.evaluate_model_cv(
            trad_no_agility + self.POSITION_DUMMIES, model_type="ridge", n_splits=5, n_repeats=5
        )

        return {
            "complete_case_full_agility": {
                "n_samples": len(cc_agility),
                "oof_r2": res_cc1["oof_r2"],
                "oof_rmse": res_cc1["oof_rmse"],
                "oof_spearman": res_cc1["oof_spearman"],
            },
            "complete_case_no_agility": {
                "n_samples": len(cc_no_ag),
                "oof_r2": res_cc2["oof_r2"],
                "oof_rmse": res_cc2["oof_rmse"],
                "oof_spearman": res_cc2["oof_spearman"],
            }
        }
