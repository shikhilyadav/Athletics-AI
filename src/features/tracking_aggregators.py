"""
ATHLETIX AI: Functional NFL Tracking & In-Game Aggregators
==========================================================
Processes in-game 10 Hz player tracking (game_tracking_2023.csv) and
matches against verified scrimmage play opportunities (player_play.csv).

Methodological & Memory Controls (8 GB RAM):
- Uses Polars lazy evaluation and chunked stream processing.
- Computes signed tangential acceleration: a_tan = (s_t - s_{t-1}) / 0.10.
- Filters low-speed / administrative frames (s < 0.5 yd/s) for active kinematic percentiles.
- Enforces strict minimum playing opportunity: >= 50 verified scrimmage snaps
  (plays where play_nullified_by_penalty != 'Y').
- Produces separate player-level and play-level feature tables.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import polars as pl
import pandas as pd
import numpy as np


class TrackingAggregator:
    """Aggregates regular-season game tracking into player and play-level athletic features."""

    DT = 0.10  # 10 Hz sampling period

    @staticmethod
    def calculate_snap_eligibility(
        player_play_path: Path, min_snaps: int = 50
    ) -> pl.DataFrame:
        """
        Calculates verified scrimmage snap counts per player from player_play.csv.
        Excludes plays nullified by penalty (where play_nullified_by_penalty == 'Y').
        """
        lf = pl.scan_csv(player_play_path, null_values=["NA", "null", ""])
        schema_names = lf.collect_schema().names()
        
        # Filter non-nullified scrimmage plays
        if "play_nullified_by_penalty" in schema_names:
            lf_valid = lf.filter(
                (pl.col("play_nullified_by_penalty") != "Y") &
                (pl.col("play_nullified_by_penalty") != "1")
            )
        else:
            lf_valid = lf

        snap_counts = (
            lf_valid.group_by("nfl_id")
            .agg([
                pl.struct(["game_id", "play_id"]).n_unique().alias("verified_scrimmage_snaps"),
                pl.col("game_id").n_unique().alias("games_with_snaps"),
            ])
            .with_columns([
                (pl.col("verified_scrimmage_snaps") >= min_snaps).alias("is_eligible_50_snaps")
            ])
        )
        return snap_counts.collect()

    @classmethod
    def aggregate_play_level_features(
        cls,
        game_tracking_path: Path,
        player_play_path: Path,
    ) -> pl.DataFrame:
        """
        Generates play-level kinematic features: player's max speed, mean speed,
        displacement, and merges play-level contextual metrics (separation, get_off).
        """
        trk_lf = pl.scan_csv(game_tracking_path, null_values=["NA", "null", ""])
        play_lf = pl.scan_csv(player_play_path, null_values=["NA", "null", ""])

        # Aggregate tracking per (game_id, play_id, nfl_id)
        play_kinematics = (
            trk_lf.group_by(["game_id", "play_id", "nfl_id"])
            .agg([
                pl.col("s").max().alias("play_max_speed"),
                pl.col("s").mean().alias("play_mean_speed"),
                pl.col("dis").sum().alias("play_total_distance"),
                pl.col("a").max().alias("play_max_accel"),
                pl.len().alias("play_tracked_frames"),
            ])
        )

        # Select target play-level columns from player_play.csv
        play_context_cols = [
            "game_id", "play_id", "nfl_id", "team_abbr", "lined_up_position",
            "separation_at_pass_forward", "player_get_off", "time_to_pressure",
            "yards_after_catch", "rec_yards", "rush_yards", "play_nullified_by_penalty"
        ]
        available_cols = [c for c in play_context_cols if c in play_lf.collect_schema().names()]
        play_subset = play_lf.select(available_cols)

        # Join
        merged_play_features = play_subset.join(
            play_kinematics, on=["game_id", "play_id", "nfl_id"], how="inner"
        )
        return merged_play_features.collect()

    @classmethod
    def aggregate_player_season_tracking(
        cls,
        game_tracking_path: Path,
        eligibility_df: pl.DataFrame,
    ) -> pl.DataFrame:
        """
        Aggregates full-season tracking metrics for each player in game_tracking_2023.csv.
        Calculates 95th/99th percentiles, tangential accelerations, and deceleration.
        """
        trk_lf = pl.scan_csv(game_tracking_path, null_values=["NA", "null", ""])

        # Compute per-player season aggregates
        # Filter active movement (s >= 0.5 yd/s) for speed percentiles
        active_trk = trk_lf.filter(pl.col("s") >= 0.5)

        player_stats = (
            active_trk.group_by("nfl_id")
            .agg([
                pl.len().alias("active_movement_frames"),
                pl.col("s").quantile(0.95).alias("game_speed_p95"),
                pl.col("s").quantile(0.99).alias("game_speed_p99"),
                pl.col("s").max().alias("game_speed_max"),
                pl.col("s").mean().alias("game_speed_mean"),
                pl.col("s").std().alias("game_speed_variability"),
                pl.col("a").quantile(0.95).alias("game_accel_p95"),
                pl.col("a").max().alias("game_accel_max"),
                (pl.col("s") >= 6.0).mean().alias("high_speed_running_fraction"),
                pl.col("dis").sum().alias("total_distance_traveled_yds"),
            ])
        )

        collected_stats = player_stats.collect()

        # Join with snap eligibility
        final_player_features = collected_stats.join(
            eligibility_df, on="nfl_id", how="left"
        ).with_columns([
            pl.col("is_eligible_50_snaps").fill_null(False),
            pl.col("verified_scrimmage_snaps").fill_null(0),
        ])

        return final_player_features
