"""
ATHLETIX AI: Phase 2 Feature Pipeline Runner
============================================
Processes raw Combine tracking, Combine results, 2023 game tracking,
and player-play records into memory-efficient Parquet datasets.

Memory-safe for 8 GB RAM laptops using Polars streaming and chunked processing.
Generates:
1. data/processed/combine_kinematic_features.parquet
2. data/processed/combine_cod_features.parquet
3. data/processed/game_tracking_features_2023.parquet
4. data/processed/player_play_features.parquet
5. data/processed/combine_player_master.parquet
"""

import sys
import gc
from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np

from src.features.kinematics import KinematicFeatureExtractor
from src.features.cod_metrics import CODFeatureExtractor
from src.features.tracking_aggregators import TrackingAggregator

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def process_combine_features():
    print("\n[1/4] Processing Combine Sensor Tracking Features (Kinematics & COD)...")
    
    # Scan combine tracking, filtering strictly for PLAYER entities
    trk_lf = pl.scan_csv(RAW_DIR / "combine_tracking.csv", null_values=["NA", "null", ""]).filter(
        pl.col("entity_type") == "PLAYER"
    )
    
    # Collect tracking sorted by player, event, and time
    print("  -> Loading player tracking frames into memory...")
    trk_df = trk_lf.select([
        "draft_year", "nfl_id", "event_id", "drill_type", "drill_name", "attempt", "time", "s", "a", "dir"
    ]).sort(["nfl_id", "event_id", "time"]).collect()
    
    print(f"  -> Total player tracking frames loaded: {trk_df.height:,}")
    
    # Partition by (nfl_id, event_id, drill_type, drill_name, attempt)
    grouped = trk_df.partition_by(["nfl_id", "event_id", "drill_type", "drill_name", "attempt"], as_dict=False)
    print(f"  -> Total distinct drill trials to process: {len(grouped):,}")
    
    kinematic_records = []
    cod_records = []
    
    for trial_df in grouped:
        first_row = trial_df.row(0, named=True)
        nfl_id = first_row["nfl_id"]
        draft_year = first_row["draft_year"]
        event_id = first_row["event_id"]
        drill_type = first_row["drill_type"]
        drill_name = first_row["drill_name"]
        attempt = first_row["attempt"]
        
        is_straight = (drill_type == "FORTY_YARD_DASH") or ("GO_ROUTE" in str(drill_name))
        
        # 1. Kinematics
        kin_feats = KinematicFeatureExtractor.extract_trial_kinematics(trial_df, is_straight_sprint=is_straight)
        if kin_feats:
            rec = {
                "nfl_id": nfl_id,
                "draft_year": draft_year,
                "event_id": event_id,
                "drill_type": drill_type,
                "drill_name": drill_name,
                "attempt": attempt,
                **kin_feats
            }
            kinematic_records.append(rec)
            
        # 2. Change of Direction
        is_cod = (drill_type in ["THREE_CONE_DRILL", "SHORT_SHUTTLE"]) or any(k in str(drill_name) for k in ["ROUTE", "DRILL", "WAVE"])
        cod_feats = CODFeatureExtractor.extract_trial_cod_metrics(trial_df, is_cod_drill=is_cod)
        if cod_feats:
            rec_cod = {
                "nfl_id": nfl_id,
                "draft_year": draft_year,
                "event_id": event_id,
                "drill_type": drill_type,
                "drill_name": drill_name,
                "attempt": attempt,
                **cod_feats
            }
            cod_records.append(rec_cod)

    kin_df = pl.DataFrame(kinematic_records)
    cod_df = pl.DataFrame(cod_records)
    
    kin_path = PROCESSED_DIR / "combine_kinematic_features.parquet"
    cod_path = PROCESSED_DIR / "combine_cod_features.parquet"
    
    kin_df.write_parquet(kin_path)
    cod_df.write_parquet(cod_path)
    
    print(f"  -> Saved {kin_path.name}: {kin_df.height:,} rows, {kin_df.width} columns")
    print(f"  -> Saved {cod_path.name}: {cod_df.height:,} rows, {cod_df.width} columns")
    
    del trk_df, grouped, kinematic_records, cod_records
    gc.collect()
    return kin_df, cod_df


def process_game_and_play_features():
    print("\n[2/4] Processing NFL In-Game Tracking & Play Features...")
    
    # 1. Snap eligibility from player_play.csv
    print("  -> Calculating 50-snap scrimmage eligibility...")
    eligibility_df = TrackingAggregator.calculate_snap_eligibility(
        RAW_DIR / "player_play.csv", min_snaps=50
    )
    eligible_count = eligibility_df.filter(pl.col("is_eligible_50_snaps")).height
    print(f"  -> Players with >= 50 verified scrimmage snaps: {eligible_count} / {eligibility_df.height}")
    
    # 2. Season tracking aggregation for 2023
    print("  -> Aggregating player season tracking from game_tracking_2023.csv...")
    player_tracking_df = TrackingAggregator.aggregate_player_season_tracking(
        RAW_DIR / "game_tracking_2023.csv", eligibility_df
    )
    game_feat_path = PROCESSED_DIR / "game_tracking_features_2023.parquet"
    player_tracking_df.write_parquet(game_feat_path)
    print(f"  -> Saved {game_feat_path.name}: {player_tracking_df.height:,} rows, {player_tracking_df.width} columns")
    
    # 3. Play-level features
    print("  -> Generating play-level features (game_id, play_id, nfl_id)...")
    play_features_df = TrackingAggregator.aggregate_play_level_features(
        RAW_DIR / "game_tracking_2023.csv", RAW_DIR / "player_play.csv"
    )
    play_feat_path = PROCESSED_DIR / "player_play_features.parquet"
    play_features_df.write_parquet(play_feat_path)
    print(f"  -> Saved {play_feat_path.name}: {play_features_df.height:,} rows, {play_features_df.width} columns")
    
    gc.collect()
    return player_tracking_df, eligibility_df


def build_combine_player_master(kin_df: pl.DataFrame, cod_df: pl.DataFrame, player_trk_df: pl.DataFrame):
    print("\n[3/4] Building Combine Player Master Dataset (All 510 Prospects)...")
    
    players_df = pl.read_csv(RAW_DIR / "players.csv", null_values=["NA", "null", ""])
    combine_res = pl.read_csv(RAW_DIR / "combine_results.csv", null_values=["NA", "null", ""])
    
    # Aggregate Kinematics per player (40yd dash curve + peak speed/accel)
    forty_curves = kin_df.filter(
        (pl.col("drill_type") == "FORTY_YARD_DASH") & (pl.col("curve_fit_status") == "SUCCESS")
    ).group_by("nfl_id").agg([
        pl.col("curve_vmax").mean().alias("forty_curve_vmax"),
        pl.col("curve_tau").mean().alias("forty_curve_tau"),
        pl.col("curve_r2").mean().alias("forty_curve_r2"),
    ])
    
    general_kin = kin_df.group_by("nfl_id").agg([
        pl.col("v_max").max().alias("combine_max_speed"),
        pl.col("v_mean").mean().alias("combine_mean_speed"),
        pl.col("a_max").max().alias("combine_max_accel"),
        pl.col("a_init").mean().alias("combine_initial_accel_mean"),
        pl.col("burst_latency").mean().alias("combine_burst_latency_mean"),
        pl.col("mean_pos_jerk").mean().alias("combine_mean_pos_jerk"),
        pl.col("max_decel").min().alias("combine_max_decel"),
    ])
    
    # Aggregate COD per player
    general_cod = cod_df.group_by("nfl_id").agg([
        pl.col("mean_apex_speed").mean().alias("combine_mean_cod_apex_speed"),
        pl.col("mean_speed_preservation_ratio").mean().alias("combine_mean_speed_preservation_ratio"),
        pl.col("peak_angular_velocity_deg_s").max().alias("combine_peak_angular_velocity"),
        pl.col("turning_efficiency_index").mean().alias("combine_mean_turning_efficiency"),
    ])
    
    # Prepare 2023 game tracking targets (strictly for 2023 cohort)
    trk_targets = player_trk_df.select([
        "nfl_id", "game_speed_p95", "game_speed_p99", "game_speed_max",
        "game_speed_variability", "high_speed_running_fraction",
        "verified_scrimmage_snaps", "is_eligible_50_snaps"
    ])
    
    # Join everything onto master players roster
    master = (
        players_df.join(combine_res, on=["nfl_id", "draft_year"], how="left")
        .join(general_kin, on="nfl_id", how="left")
        .join(forty_curves, on="nfl_id", how="left")
        .join(general_cod, on="nfl_id", how="left")
        .join(trk_targets, on="nfl_id", how="left")
        .with_columns([
            # Explicit research cohort target status
            pl.when(pl.col("draft_year") == 2023)
            .then(
                pl.when(pl.col("game_speed_p95").is_not_null())
                .then(pl.lit("2023_EVALUATED_ROOKIE"))
                .otherwise(pl.lit("2023_INACTIVE_ROOKIE"))
            )
            .when(pl.col("draft_year") == 2024)
            .then(pl.lit("FUTURE_COHORT_2024_UNAVAILABLE"))
            .otherwise(pl.lit("FUTURE_COHORT_2025_UNAVAILABLE"))
            .alias("game_target_cohort_status")
        ])
    )
    
    master_path = PROCESSED_DIR / "combine_player_master.parquet"
    master.write_parquet(master_path)
    print(f"  -> Saved {master_path.name}: {master.height} players, {master.width} columns")
    return master


if __name__ == "__main__":
    kin_df, cod_df = process_combine_features()
    player_trk_df, eligibility_df = process_game_and_play_features()
    master_df = build_combine_player_master(kin_df, cod_df, player_trk_df)
    print("\n[4/4] Phase 2 Feature Pipeline Successfully Completed!")
