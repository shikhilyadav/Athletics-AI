"""
ATHLETIX AI: Statistical Analysis & Cohort Profiling
===================================================
Prepares the primary research cohort (2023 Combine cohort with >= 50 snaps),
conducts sprint curve quality classification, generates sample inclusion/exclusion
statistics, checks multicollinearity, and explores primary and secondary targets.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, List
import polars as pl
import pandas as pd
import numpy as np
from scipy import stats

from src.config import PROCESSED_DATA_DIR, REPORTS_DIR, RANDOM_SEED


class StatisticalCohortProfiler:
    """Manages cohort inclusion/exclusion, sprint curve quality audits, and target analysis."""

    def __init__(self, master_path: Path = PROCESSED_DATA_DIR / "combine_player_master.parquet"):
        self.master_path = Path(master_path)
        self.df = pl.read_parquet(self.master_path)

    def generate_sample_inclusion_report(self) -> Dict[str, Any]:
        """
        Tracks player counts at every filtering step to ensure no silent drops.
        """
        step1_total = self.df.height
        step2_2023_cohort = self.df.filter(pl.col("draft_year") == 2023).height
        step3_tracked_active = self.df.filter(
            (pl.col("draft_year") == 2023) & (pl.col("game_speed_p95").is_not_null())
        ).height
        step4_eligible_50_snaps = self.df.filter(
            (pl.col("draft_year") == 2023) & (pl.col("is_eligible_50_snaps") == True)
        ).height
        
        # Route separation sub-cohort
        pp_df = pl.read_parquet(PROCESSED_DATA_DIR / "player_play_features.parquet")
        sep_players = pp_df.filter(pl.col("separation_at_pass_forward").is_not_null())["nfl_id"].n_unique()

        inclusion_data = {
            "total_prospects_master": step1_total,
            "future_cohorts_2024_2025": step1_total - step2_2023_cohort,
            "cohort_2023_total": step2_2023_cohort,
            "cohort_2023_untracked_inactive": step2_2023_cohort - step3_tracked_active,
            "cohort_2023_active_tracked": step3_tracked_active,
            "cohort_2023_under_50_snaps": step3_tracked_active - step4_eligible_50_snaps,
            "cohort_2023_primary_eligible": step4_eligible_50_snaps,
            "route_separation_subcohort_count": sep_players,
        }
        return inclusion_data

    def audit_sprint_curve_quality(self) -> Dict[str, Any]:
        """
        Classifies 40-yard dash sprint velocity curve fits into:
        - High Quality: R^2 >= 0.95
        - Acceptable: 0.85 <= R^2 < 0.95
        - Low Quality: R^2 < 0.85
        - Opt-Out / No Curve
        """
        cohort = self.df.filter(
            (pl.col("draft_year") == 2023) & (pl.col("is_eligible_50_snaps") == True)
        )
        total_eligible = cohort.height

        with_curve = cohort.filter(pl.col("forty_curve_r2").is_not_null())
        no_curve = cohort.filter(pl.col("forty_curve_r2").is_null()).height

        high_q = with_curve.filter(pl.col("forty_curve_r2") >= 0.95).height
        acc_q = with_curve.filter(
            (pl.col("forty_curve_r2") >= 0.85) & (pl.col("forty_curve_r2") < 0.95)
        ).height
        low_q = with_curve.filter(pl.col("forty_curve_r2") < 0.85).height

        return {
            "total_primary_cohort": total_eligible,
            "sprint_curve_opt_outs": no_curve,
            "sprint_curve_fitted": with_curve.height,
            "high_quality_r2_ge_095": high_q,
            "acceptable_quality_r2_085_095": acc_q,
            "low_quality_r2_lt_085": low_q,
        }

    def analyze_research_targets(self) -> pd.DataFrame:
        """
        Extracts summary distribution and normality metrics for primary and secondary targets.
        """
        cohort = self.df.filter(
            (pl.col("draft_year") == 2023) & (pl.col("is_eligible_50_snaps") == True)
        ).to_pandas()

        targets = [
            "game_speed_p95",
            "game_speed_p99",
            "game_speed_max",
            "high_speed_running_fraction",
            "game_speed_variability",
        ]

        stats_rows = []
        for t in targets:
            vals = cohort[t].dropna()
            shapiro_stat, shapiro_p = stats.shapiro(vals)
            stats_rows.append({
                "target_variable": t,
                "n_obs": len(vals),
                "mean": round(vals.mean(), 4),
                "std": round(vals.std(), 4),
                "median": round(vals.median(), 4),
                "iqr": round(vals.quantile(0.75) - vals.quantile(0.25), 4),
                "min": round(vals.min(), 4),
                "max": round(vals.max(), 4),
                "skewness": round(stats.skew(vals), 4),
                "kurtosis": round(stats.kurtosis(vals), 4),
                "shapiro_p_value": round(shapiro_p, 5),
                "is_normally_distributed": shapiro_p >= 0.05,
            })

        return pd.DataFrame(stats_rows)

    def check_multicollinearity(self, feature_cols: List[str]) -> pd.DataFrame:
        """
        Computes pairwise Spearman and Pearson correlations for selected features.
        """
        cohort = self.df.filter(
            (pl.col("draft_year") == 2023) & (pl.col("is_eligible_50_snaps") == True)
        ).select(feature_cols).to_pandas()

        corr_matrix = cohort.corr(method="spearman")
        return corr_matrix
