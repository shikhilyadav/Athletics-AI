"""
ATHLETIX AI: Phase 2 Empirical Feature Distribution Inspector
=============================================================
Calculates exact statistics across all generated Parquet feature tables
to provide empirical grounding for quality and eligibility reports.
"""

from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np

PROCESSED_DIR = Path("data/processed")


def inspect_feature_distributions():
    print("=" * 80)
    print("INSPECTING PARQUET FEATURE DISTRIBUTIONS")
    print("=" * 80)
    
    # 1. Kinematic Features
    kin_df = pl.read_parquet(PROCESSED_DIR / "combine_kinematic_features.parquet")
    print(f"\n1. Combine Kinematic Features ({kin_df.height:,} trials across {kin_df['nfl_id'].n_unique()} players):")
    kin_num_cols = ["v_max", "v_mean", "a_init", "a_max", "burst_latency", "mean_pos_jerk", "max_decel", "trial_duration_sec"]
    print(kin_df.select([pl.col(c).mean().round(3).alias(f"{c}_mean") for c in kin_num_cols]))
    print(kin_df.select([pl.col(c).quantile(0.95).round(3).alias(f"{c}_p95") for c in kin_num_cols]))
    
    # Curve fitting stats
    sprint_df = kin_df.filter(pl.col("drill_type") == "FORTY_YARD_DASH")
    print(f"\n40-Yard Dash Sprint Trials: {sprint_df.height:,}")
    curve_status = sprint_df["curve_fit_status"].value_counts()
    print("Sprint curve fitting statuses:\n", curve_status)
    success_curves = sprint_df.filter(pl.col("curve_fit_status") == "SUCCESS")
    print("Curve Fit Stats (SUCCESS):")
    print(success_curves.select([
        pl.col("curve_vmax").mean().round(3).alias("vmax_fit_mean"),
        pl.col("curve_tau").mean().round(3).alias("tau_fit_mean"),
        pl.col("curve_r2").mean().round(4).alias("r2_fit_mean"),
        pl.col("curve_r2").min().round(4).alias("r2_fit_min"),
    ]))

    # 2. COD Features
    cod_df = pl.read_parquet(PROCESSED_DIR / "combine_cod_features.parquet")
    print(f"\n2. Combine COD Features ({cod_df.height:,} trials across {cod_df['nfl_id'].n_unique()} players):")
    cod_num_cols = ["num_detected_turns", "mean_entry_speed", "mean_apex_speed", "mean_speed_preservation_ratio", "peak_angular_velocity_deg_s", "turning_efficiency_index"]
    print(cod_df.select([pl.col(c).drop_nulls().mean().round(3).alias(f"{c}_mean") for c in cod_num_cols]))
    print(cod_df.select([pl.col(c).drop_nulls().quantile(0.95).round(3).alias(f"{c}_p95") for c in cod_num_cols]))

    # 3. Game Tracking Features (2023)
    game_df = pl.read_parquet(PROCESSED_DIR / "game_tracking_features_2023.parquet")
    print(f"\n3. 2023 Game Tracking Features ({game_df.height} players):")
    game_num_cols = ["game_speed_p95", "game_speed_p99", "game_speed_max", "game_accel_p95", "high_speed_running_fraction", "verified_scrimmage_snaps"]
    print(game_df.select([pl.col(c).mean().round(3).alias(f"{c}_mean") for c in game_num_cols]))
    eligible_game_players = game_df.filter(pl.col("is_eligible_50_snaps")).height
    print(f"Eligible players with >= 50 snaps: {eligible_game_players} / {game_df.height} ({eligible_game_players/game_df.height*100:.1f}%)")

    # 4. Play-Level Features
    play_df = pl.read_parquet(PROCESSED_DIR / "player_play_features.parquet")
    print(f"\n4. Player-Play Features ({play_df.height:,} player-plays):")
    play_num_cols = ["play_max_speed", "play_total_distance", "play_max_accel"]
    print(play_df.select([pl.col(c).mean().round(3).alias(f"{c}_mean") for c in play_num_cols]))

    # 5. Master Combine Table
    master_df = pl.read_parquet(PROCESSED_DIR / "combine_player_master.parquet")
    print(f"\n5. Combine Player Master ({master_df.height} prospects, {master_df.width} columns):")
    cohort_status = master_df["game_target_cohort_status"].value_counts()
    print("Cohort target status distribution:\n", cohort_status)
    eligible_by_cohort = master_df.group_by(["draft_year", "game_target_cohort_status"]).agg([
        pl.len().alias("player_count"),
        pl.col("is_eligible_50_snaps").sum().alias("eligible_50_snaps_count"),
        pl.col("combine_max_speed").mean().round(2).alias("avg_combine_max_speed"),
        pl.col("forty_curve_vmax").drop_nulls().mean().round(2).alias("avg_forty_curve_vmax"),
    ]).sort(["draft_year", "game_target_cohort_status"])
    print("\nMaster Cohort Summary:\n", eligible_by_cohort)


if __name__ == "__main__":
    inspect_feature_distributions()
