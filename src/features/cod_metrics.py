"""
ATHLETIX AI: Change of Direction (COD) & Agility Engine
======================================================
Extracts biomechanical turning mechanics, circular heading changes,
and agility efficiency from 10 Hz Combine sensor trajectories.

Circular Angle Mathematics:
- Circular Difference:
    Delta_theta = ((theta_2 - theta_1 + 180) % 360) - 180
    Absolute Angular Change: |Delta_theta| in [0, 180] deg
    Angular Velocity: omega = |Delta_theta| / dt (deg/s)

Turn Detection Methodology:
1. Calculates circular angular velocity omega_t at each 10 Hz frame.
2. Identifies turn apex candidates as local speed minima within high angular rate zones (omega >= 45 deg/s).
3. Defines a temporal turn window [t_apex - 3, t_apex + 3] (0.6s total).
4. Extracts entry speed, apex speed, exit speed, direction-change magnitude, and speed preservation ratio.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import polars as pl


class CODFeatureExtractor:
    """Calculates agility and change-of-direction mechanics using circular geometry."""

    DT = 0.10  # 10 Hz sampling period

    @staticmethod
    def circular_angle_diff(angle_curr: np.ndarray, angle_prev: np.ndarray) -> np.ndarray:
        """
        Calculates signed circular angular difference in degrees (-180, +180].
        Correctly wraps around the 0°/360° boundary.
        """
        diff = (angle_curr - angle_prev + 180.0) % 360.0 - 180.0
        return diff

    @classmethod
    def compute_angular_velocity(cls, directions: np.ndarray, dt: float = 0.10) -> Tuple[np.ndarray, np.ndarray]:
        """
        Computes signed angular differences and absolute angular velocity (deg/s).
        """
        if len(directions) < 2:
            return np.zeros_like(directions), np.zeros_like(directions)
        
        # Shift and circular diff
        prev_dir = np.roll(directions, 1)
        prev_dir[0] = directions[0]
        signed_diff = cls.circular_angle_diff(directions, prev_dir)
        signed_diff[0] = 0.0
        
        angular_velocity = np.abs(signed_diff) / dt
        return signed_diff, angular_velocity

    @classmethod
    def detect_turns(
        cls,
        speeds: np.ndarray,
        directions: np.ndarray,
        min_angular_velocity: float = 45.0,
        min_entry_speed: float = 1.5,
    ) -> List[Dict[str, Any]]:
        """
        Detects distinct turn events using localized speed apex and circular direction changes.
        """
        n_frames = len(speeds)
        if n_frames < 7:
            return []

        signed_diff, omega = cls.compute_angular_velocity(directions, cls.DT)
        turns = []

        # Find candidate apex frames: local minimum in speed where omega is elevated
        for i in range(3, n_frames - 3):
            # Speed local minimum check
            is_local_min = (speeds[i] <= speeds[i - 1]) and (speeds[i] <= speeds[i + 1])
            # High turning rate or high cumulative turn over +/- 3 frames
            window_turn_mag = np.sum(np.abs(signed_diff[i - 3 : i + 4]))
            
            if is_local_min and (omega[i] >= min_angular_velocity or window_turn_mag >= 40.0):
                # Extract entry, apex, exit
                v_entry = float(np.nanmax(speeds[i - 3 : i]))
                v_apex = float(speeds[i])
                v_exit = float(np.nanmax(speeds[i + 1 : i + 4]))

                if v_entry >= min_entry_speed:
                    # Direction change magnitude through window
                    mag_turn = float(np.sum(np.abs(signed_diff[i - 3 : i + 4])))
                    peak_omega = float(np.nanmax(omega[i - 3 : i + 4]))
                    preservation_ratio = float(v_apex / np.maximum(v_entry, 0.5))

                    turns.append({
                        "apex_frame": i,
                        "v_entry": v_entry,
                        "v_apex": v_apex,
                        "v_exit": v_exit,
                        "speed_preservation_ratio": preservation_ratio,
                        "turn_magnitude_deg": mag_turn,
                        "peak_angular_velocity": peak_omega,
                    })

        # Deduplicate consecutive apexes within 3 frames
        filtered_turns = []
        for t in turns:
            if not filtered_turns or (t["apex_frame"] - filtered_turns[-1]["apex_frame"] > 3):
                filtered_turns.append(t)

        return filtered_turns

    @classmethod
    def extract_trial_cod_metrics(
        cls,
        trial_df: pl.DataFrame,
        is_cod_drill: bool = True,
    ) -> Dict[str, Any]:
        """
        Extracts aggregated Change-of-Direction features from a single drill trial.
        Expects columns ['s', 'dir'] and optionally ['o'].
        """
        if trial_df.is_empty():
            return {}

        speeds = trial_df["s"].to_numpy()
        directions = trial_df["dir"].to_numpy()
        n_frames = len(speeds)

        if n_frames < 7:
            return {}

        signed_diff, omega = cls.compute_angular_velocity(directions, cls.DT)
        mean_omega = float(np.nanmean(omega))
        peak_omega = float(np.nanmax(omega))

        detected_turns = cls.detect_turns(speeds, directions)
        num_turns = len(detected_turns)

        if num_turns > 0:
            entry_speeds = [t["v_entry"] for t in detected_turns]
            apex_speeds = [t["v_apex"] for t in detected_turns]
            exit_speeds = [t["v_exit"] for t in detected_turns]
            ratios = [t["speed_preservation_ratio"] for t in detected_turns]
            mags = [t["turn_magnitude_deg"] for t in detected_turns]

            mean_entry_speed = float(np.mean(entry_speeds))
            mean_apex_speed = float(np.mean(apex_speeds))
            min_apex_speed = float(np.min(apex_speeds))
            mean_exit_speed = float(np.mean(exit_speeds))
            mean_preservation_ratio = float(np.mean(ratios))
            mean_turn_magnitude = float(np.mean(mags))
            total_turn_magnitude = float(np.sum(mags))

            # Movement consistency: std of preservation ratios across turns
            consistency = float(np.std(ratios)) if num_turns > 1 else 0.0

            # Turning efficiency index: v_apex * magnitude / duration
            turning_efficiency = float((mean_apex_speed * mean_turn_magnitude) / 0.6)

        else:
            mean_entry_speed = None
            mean_apex_speed = None
            min_apex_speed = None
            mean_exit_speed = None
            mean_preservation_ratio = None
            mean_turn_magnitude = None
            total_turn_magnitude = 0.0
            consistency = None
            turning_efficiency = None

        return {
            "num_detected_turns": num_turns,
            "mean_entry_speed": round(mean_entry_speed, 4) if mean_entry_speed is not None else None,
            "mean_apex_speed": round(mean_apex_speed, 4) if mean_apex_speed is not None else None,
            "min_apex_speed": round(min_apex_speed, 4) if min_apex_speed is not None else None,
            "mean_exit_speed": round(mean_exit_speed, 4) if mean_exit_speed is not None else None,
            "mean_speed_preservation_ratio": round(mean_preservation_ratio, 4) if mean_preservation_ratio is not None else None,
            "mean_turn_magnitude_deg": round(mean_turn_magnitude, 2) if mean_turn_magnitude is not None else None,
            "total_turn_magnitude_deg": round(total_turn_magnitude, 2),
            "peak_angular_velocity_deg_s": round(peak_omega, 2),
            "mean_angular_velocity_deg_s": round(mean_omega, 2),
            "movement_consistency_std": round(consistency, 4) if consistency is not None else None,
            "turning_efficiency_index": round(turning_efficiency, 4) if turning_efficiency is not None else None,
        }
