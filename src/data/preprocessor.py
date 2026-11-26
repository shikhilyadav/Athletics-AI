"""
Tracking Preprocessing and Coordinate Standardization
=====================================================
Harmonizes coordinate systems (playDirection left/right normalization)
and temporal alignment across 10 Hz RFID frames.
"""

import pandas as pd
import numpy as np
from src.config import FIELD_X_MAX, FIELD_Y_MAX, FRAME_INTERVAL_SEC


class TrackingPreprocessor:
    """Standardizes coordinates, orientations, and frame sequencing for tracking data."""

    @staticmethod
    def standardize_play_direction(df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardizes coordinate system so offensive direction of play is always towards the right (increasing x).
        For plays where playDirection == 'left':
            x_adj = 120 - x
            y_adj = 160/3 - y (53.333 - y)
            dir_adj = (dir + 180) % 360
            o_adj = (o + 180) % 360
        """
        df = df.copy()
        if "playDirection" not in df.columns:
            return df

        left_mask = df["playDirection"] == "left"
        if left_mask.any():
            df.loc[left_mask, "x"] = FIELD_X_MAX - df.loc[left_mask, "x"]
            df.loc[left_mask, "y"] = FIELD_Y_MAX - df.loc[left_mask, "y"]

            if "dir" in df.columns:
                df.loc[left_mask, "dir"] = (df.loc[left_mask, "dir"] + 180.0) % 360.0
            if "o" in df.columns:
                df.loc[left_mask, "o"] = (df.loc[left_mask, "o"] + 180.0) % 360.0

        return df

    @staticmethod
    def compute_derivatives(df: pd.DataFrame, id_cols=("gameId", "playId", "nflId")) -> pd.DataFrame:
        """
        Computes numerical velocity, acceleration, and jerk if not pre-computed or to verify sensor integrity.
        dt = 0.1s (10 Hz).
        """
        df = df.copy()
        df = df.sort_values(list(id_cols) + ["frameId"])

        # Groupby diff for displacement and velocity
        grouped = df.groupby(list(id_cols))
        dx = grouped["x"].diff()
        dy = grouped["y"].diff()
        computed_s = np.sqrt(dx**2 + dy**2) / FRAME_INTERVAL_SEC
        computed_a = grouped["s"].diff() / FRAME_INTERVAL_SEC
        jerk = grouped["a"].diff() / FRAME_INTERVAL_SEC

        df["computed_speed"] = computed_s
        df["computed_accel"] = computed_a
        df["jerk"] = jerk
        return df
