"""
ATHLETIX AI: Phase 1B, 1C, 1D In-Depth Inspection
=================================================
Calculates exact overlap, tracking kinematics, distributions, sampling rates,
and research feasibility variables using Polars.
"""

import json
from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np

DATA_DIR = Path("data/raw")
REPORTS_DIR = Path("reports")


def run_deep_inspection():
    print("=" * 80)
    print("PHASE 1B: PLAYER MATCHING & ENTITY RESOLUTION")
    print("=" * 80)
    
    players_lf = pl.scan_csv(DATA_DIR / "players.csv")
    combine_res_lf = pl.scan_csv(DATA_DIR / "combine_results.csv")
    combine_trk_lf = pl.scan_csv(DATA_DIR / "combine_tracking.csv")
    career_lf = pl.scan_csv(DATA_DIR / "player_career_successes.csv")
    play_lf = pl.scan_csv(DATA_DIR / "player_play.csv")
    game_trk_lf = pl.scan_csv(DATA_DIR / "game_tracking_2023.csv")
    
    # Extract unique IDs
    p_ids = set(players_lf.select("nfl_id").collect()["nfl_id"].to_list())
    c_res_ids = set(combine_res_lf.select("nfl_id").collect()["nfl_id"].to_list())
    c_trk_ids = set(combine_trk_lf.select("nfl_id").drop_nulls().unique().collect()["nfl_id"].to_list())
    career_ids = set(career_lf.select("nfl_id").collect()["nfl_id"].to_list())
    play_ids = set(play_lf.select("nfl_id").drop_nulls().unique().collect()["nfl_id"].to_list())
    game_trk_ids = set(game_trk_lf.select("nfl_id").drop_nulls().unique().collect()["nfl_id"].to_list())
    
    print(f"Total players in players.csv: {len(p_ids)}")
    print(f"Total in combine_results.csv: {len(c_res_ids)} | Overlap with players.csv: {len(p_ids & c_res_ids)}")
    print(f"Total in combine_tracking.csv: {len(c_trk_ids)} | Overlap with players.csv: {len(p_ids & c_trk_ids)}")
    print(f"Total in player_career_successes.csv: {len(career_ids)} | Overlap with players.csv: {len(p_ids & career_ids)}")
    print(f"Total in player_play.csv: {len(play_ids)} | Overlap with players.csv: {len(p_ids & play_ids)}")
    print(f"Total in game_tracking_2023.csv: {len(game_trk_ids)} | Overlap with players.csv: {len(p_ids & game_trk_ids)}")
    
    # Check draft years
    draft_years = players_lf.select("draft_year").collect()["draft_year"].value_counts().to_pandas()
    print("\nDraft Year distribution in players.csv:")
    print(draft_years)
    
    # Check positions
    positions = players_lf.select("nfl_position").collect()["nfl_position"].value_counts().to_pandas()
    print("\nPositions distribution in players.csv:")
    print(positions.head(10))

    # Career success summary
    career_df = career_lf.collect().to_pandas()
    print("\nCareer Successes summary:")
    print(career_df.describe())
    
    # Snaps > 0 count
    has_offensive = (career_df["career_offensive_snaps"] > 0).sum()
    has_defensive = (career_df["career_defensive_snaps"] > 0).sum()
    has_st = (career_df["career_special_teams_snaps"] > 0).sum()
    has_active = (career_df["career_games_active"] > 0).sum()
    has_started = (career_df["career_games_started"] > 0).sum()
    print(f"Active in >=1 game: {has_active} / 510 ({has_active/510*100:.1f}%)")
    print(f"Started >=1 game: {has_started} / 510 ({has_started/510*100:.1f}%)")
    print(f"Has offensive snaps: {has_offensive} | defensive: {has_defensive} | special teams: {has_st}")
    
    print("\n" + "=" * 80)
    print("PHASE 1C: TRACKING ANALYSIS")
    print("=" * 80)
    
    # Combine Tracking Details
    print("\n--- combine_tracking.csv Analysis ---")
    drill_types = combine_trk_lf.select("drill_type").collect()["drill_type"].value_counts().to_pandas()
    drill_names = combine_trk_lf.select("drill_name").collect()["drill_name"].value_counts().to_pandas()
    entity_types = combine_trk_lf.select("entity_type").collect()["entity_type"].value_counts().to_pandas()
    print("Drill Types:\n", drill_types)
    print("Drill Names:\n", drill_names)
    print("Entity Types:\n", entity_types)
    
    # Sample Combine Tracking kinematics
    c_trk_stats = combine_trk_lf.select([
        pl.col("x").min().alias("x_min"), pl.col("x").max().alias("x_max"),
        pl.col("y").min().alias("y_min"), pl.col("y").max().alias("y_max"),
        pl.col("s").min().alias("s_min"), pl.col("s").mean().alias("s_mean"),
        pl.col("s").quantile(0.50).alias("s_med"), pl.col("s").quantile(0.95).alias("s_p95"),
        pl.col("s").quantile(0.99).alias("s_p99"), pl.col("s").max().alias("s_max"),
        pl.col("a").min().alias("a_min"), pl.col("a").mean().alias("a_mean"),
        pl.col("a").quantile(0.50).alias("a_med"), pl.col("a").quantile(0.95).alias("a_p95"),
        pl.col("a").quantile(0.99).alias("a_p99"), pl.col("a").max().alias("a_max"),
        pl.col("dis").min().alias("dis_min"), pl.col("dis").max().alias("dis_max"),
    ]).collect().to_pandas()
    print("\nCombine Tracking Kinematic Ranges:")
    print(c_trk_stats.T)
    
    # Check frequency on combine tracking for a sample player & drill
    sample_c_trk = combine_trk_lf.filter(
        (pl.col("nfl_id") == list(c_trk_ids)[0])
    ).limit(30).collect().to_pandas()
    print("\nSample combine tracking timestamps:")
    print(sample_c_trk[["nfl_id", "drill_name", "time", "x", "y", "s", "a"]].head(10))
    sample_c_trk["dt"] = pd.to_datetime(sample_c_trk["time"]).diff().dt.total_seconds()
    print("Combine tracking time differences (dt) in seconds:")
    print(sample_c_trk["dt"].value_counts(dropna=False))

    # Game Tracking 2023 Details
    print("\n--- game_tracking_2023.csv Analysis ---")
    g_trk_null_nfl = game_trk_lf.filter(pl.col("nfl_id").is_null()).select(pl.len()).collect().item()
    print(f"game_tracking_2023.csv null nfl_id count (e.g. football): {g_trk_null_nfl}")
    
    g_trk_stats = game_trk_lf.select([
        pl.col("x").min().alias("x_min"), pl.col("x").max().alias("x_max"),
        pl.col("y").min().alias("y_min"), pl.col("y").max().alias("y_max"),
        pl.col("s").min().alias("s_min"), pl.col("s").mean().alias("s_mean"),
        pl.col("s").quantile(0.50).alias("s_med"), pl.col("s").quantile(0.95).alias("s_p95"),
        pl.col("s").quantile(0.99).alias("s_p99"), pl.col("s").max().alias("s_max"),
        pl.col("a").min().alias("a_min"), pl.col("a").mean().alias("a_mean"),
        pl.col("a").quantile(0.50).alias("a_med"), pl.col("a").quantile(0.95).alias("a_p95"),
        pl.col("a").quantile(0.99).alias("a_p99"), pl.col("a").max().alias("a_max"),
    ]).collect().to_pandas()
    print("\nGame Tracking 2023 Kinematic Ranges:")
    print(g_trk_stats.T)

    # Check sample dt on game tracking
    sample_g_trk = game_trk_lf.filter(pl.col("nfl_id") == list(game_trk_ids)[0]).limit(30).collect().to_pandas()
    sample_g_trk["dt"] = pd.to_datetime(sample_g_trk["time"]).diff().dt.total_seconds()
    print("\nGame tracking time differences (dt) in seconds:")
    print(sample_g_trk["dt"].value_counts(dropna=False))

    return {
        "p_ids": len(p_ids),
        "c_trk_stats": c_trk_stats.to_dict(),
        "g_trk_stats": g_trk_stats.to_dict(),
    }


if __name__ == "__main__":
    run_deep_inspection()
