"""
ATHLETIX AI: Athletic Alpha Residual Evaluation Engine
======================================================
Calculates strictly Out-Of-Fold (OOF) residuals from Model A (Traditional Combine Baseline)
to evaluate player-level outperformance relative to conventional stopwatch expectations.

Formula:
    Athletic Alpha_i = Y_{actual, i} - Y_hat_{OOF, Model A, i}
    Alpha Z-Score_i = (Athletic Alpha_i - mean(Alpha)) / std(Alpha)

Scientific Guardrails:
- Strictly derived from out-of-fold cross-validated predictions (zero in-sample bias).
- Evaluates statistical association with draft capital, playing time, and continuous sensor mechanics.
- Does not label residuals as "proven latent athletic potential", but rather as
  measured functional tracking outperformance relative to traditional Combine projections.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
import pandas as pd
from scipy import stats


class ResidualPotentialEvaluator:
    """Evaluates Out-Of-Fold residuals (Athletic Alpha) from baseline traditional scouting models."""

    @staticmethod
    def compute_athletic_alpha(
        player_df: pd.DataFrame,
        actual_targets: np.ndarray,
        oof_traditional_predictions: np.ndarray,
        metric_name: str = "game_speed_p95",
    ) -> pd.DataFrame:
        """
        Computes player-level Athletic Alpha out-of-fold residual table.
        """
        results = player_df[[
            "nfl_id", "display_name", "nfl_position", "draft_round", "draft_overall_pick",
            "verified_scrimmage_snaps"
        ]].copy()

        residuals = actual_targets - oof_traditional_predictions
        res_mean = np.mean(residuals)
        res_std = np.std(residuals)

        results[f"actual_{metric_name}"] = np.round(actual_targets, 4)
        results[f"expected_traditional_{metric_name}"] = np.round(oof_traditional_predictions, 4)
        results["athletic_alpha_raw"] = np.round(residuals, 4)
        results["athletic_alpha_zscore"] = np.round((residuals - res_mean) / (res_std if res_std > 0 else 1.0), 4)

        # Athletic Alpha Tiers
        results["athletic_alpha_tier"] = pd.cut(
            results["athletic_alpha_zscore"],
            bins=[-np.inf, -1.0, 0.0, 1.0, np.inf],
            labels=["Underperformer (Z < -1)", "Slight Underperformer (-1 <= Z < 0)",
                    "Slight Outperformer (0 <= Z < 1)", "High Outperformer (Z >= 1)"]
        )

        return results.sort_values(by="athletic_alpha_raw", ascending=False).reset_index(drop=True)

    @staticmethod
    def analyze_residual_distribution(residuals: np.ndarray) -> Dict[str, Any]:
        """Performs statistical tests on the residual distribution."""
        shapiro_stat, shapiro_p = stats.shapiro(residuals)
        return {
            "n_observations": len(residuals),
            "mean": round(float(np.mean(residuals)), 5),
            "std": round(float(np.std(residuals)), 5),
            "median": round(float(np.median(residuals)), 5),
            "skewness": round(float(stats.skew(residuals)), 4),
            "kurtosis": round(float(stats.kurtosis(residuals)), 4),
            "shapiro_wilk_stat": round(float(shapiro_stat), 4),
            "shapiro_wilk_p_value": round(float(shapiro_p), 5),
            "is_normally_distributed": bool(shapiro_p >= 0.05),
        }

    @staticmethod
    def correlate_with_sensor_features(
        alpha_df: pd.DataFrame, master_df: pd.DataFrame, sensor_cols: List[str]
    ) -> pd.DataFrame:
        """
        Determines which Combine sensor movement features correlate with positive Athletic Alpha.
        """
        merged = alpha_df[["nfl_id", "athletic_alpha_raw"]].merge(master_df[["nfl_id"] + sensor_cols], on="nfl_id")
        
        corrs = []
        for col in sensor_cols:
            clean_s = merged[["athletic_alpha_raw", col]].dropna()
            if len(clean_s) > 10:
                spearman_r, p_val = stats.spearmanr(clean_s["athletic_alpha_raw"], clean_s[col])
                pearson_r, p_pearson = stats.pearsonr(clean_s["athletic_alpha_raw"], clean_s[col])
                corrs.append({
                    "sensor_feature": col,
                    "spearman_correlation": round(float(spearman_r), 4),
                    "spearman_p_value": round(float(p_val), 5),
                    "pearson_correlation": round(float(pearson_r), 4),
                    "n_available": len(clean_s),
                })
        
        return pd.DataFrame(corrs).sort_values(by="spearman_correlation", ascending=False).reset_index(drop=True)

    @staticmethod
    def profile_by_position(alpha_df: pd.DataFrame) -> pd.DataFrame:
        """Calculates Athletic Alpha statistics by NFL position."""
        pos_summary = alpha_df.groupby("nfl_position").agg(
            player_count=("athletic_alpha_raw", "count"),
            mean_alpha=("athletic_alpha_raw", "mean"),
            std_alpha=("athletic_alpha_raw", "std"),
            median_alpha=("athletic_alpha_raw", "median"),
            pct_positive=("athletic_alpha_raw", lambda x: np.mean(x > 0) * 100)
        ).round(4).reset_index().sort_values(by="mean_alpha", ascending=False)
        return pos_summary
