"""
ATHLETIX AI: Kinematic Feature Engineering
==========================================
Extracts continuous biomechanical kinematics and fits mono-exponential velocity curves
from high-frequency (10 Hz) Combine RFID sensor tracking.

Mathematical Definitions:
- Maximum Velocity: v_max = max(s_t)
- Mean Velocity: v_mean = mean(s_t | s_t >= 0.5 yd/s)
- Initial Acceleration: a_init = mean(a_t, t in [0.0, 1.0]s)
- Burst Latency: t_{a_max} = argmax_t(a_t) * dt
- Mean Positive Jerk: j_pos = mean(da/dt | da/dt > 0)
- Mono-Exponential Sprint Velocity Profile:
    v(t) = v_max * (1 - exp(-t / tau))
    where tau is the acceleration time constant (s).
"""

from typing import Dict, Any, Tuple, Optional
import numpy as np
import polars as pl
from scipy.optimize import curve_fit


def mono_exponential_velocity(t: np.ndarray, v_max: float, tau: float) -> np.ndarray:
    """Mono-exponential sprint velocity model."""
    return v_max * (1.0 - np.exp(-t / np.maximum(tau, 1e-4)))


class KinematicFeatureExtractor:
    """Extracts kinematic and sprint acceleration features from 10 Hz tracking sequences."""

    DT = 0.10  # 10 Hz sampling period

    @staticmethod
    def compute_tangential_acceleration(speeds: np.ndarray, dt: float = 0.10) -> np.ndarray:
        """
        Computes signed tangential acceleration: a_tan = (s_t - s_{t-1}) / dt.
        Positive values indicate acceleration; negative values indicate deceleration.
        """
        if len(speeds) < 2:
            return np.zeros_like(speeds)
        a_tan = np.diff(speeds, prepend=speeds[0]) / dt
        return a_tan

    @staticmethod
    def compute_jerk(accels: np.ndarray, dt: float = 0.10) -> np.ndarray:
        """Computes rate of change of acceleration: j = (a_t - a_{t-1}) / dt."""
        if len(accels) < 2:
            return np.zeros_like(accels)
        jerk = np.diff(accels, prepend=accels[0]) / dt
        return jerk

    @classmethod
    def fit_sprint_velocity_curve(
        cls, times: np.ndarray, speeds: np.ndarray
    ) -> Dict[str, Any]:
        """
        Fits v(t) = v_max * (1 - exp(-t / tau)) to straight-line sprint speed profiles.
        Returns fitted v_max, tau, R^2, and fit status.
        """
        if len(speeds) < 10 or np.nanmax(speeds) < 3.0:
            return {
                "curve_vmax": None,
                "curve_tau": None,
                "curve_r2": None,
                "curve_fit_status": "INSUFFICIENT_DATA",
            }

        # Normalize time to start at 0.0
        t = times - times[0]
        v = speeds

        # Initial parameter estimates
        v_init = float(np.nanmax(v))
        tau_init = 1.2

        try:
            popt, _ = curve_fit(
                mono_exponential_velocity,
                t,
                v,
                p0=[v_init, tau_init],
                bounds=([3.0, 0.1], [14.0, 5.0]),
                maxfev=2000,
            )
            v_max_fit, tau_fit = popt

            # Calculate R^2
            pred_v = mono_exponential_velocity(t, v_max_fit, tau_fit)
            ss_res = np.sum((v - pred_v) ** 2)
            ss_tot = np.sum((v - np.mean(v)) ** 2)
            r2 = float(1.0 - (ss_res / (ss_tot + 1e-8))) if ss_tot > 0 else 0.0

            return {
                "curve_vmax": round(float(v_max_fit), 4),
                "curve_tau": round(float(tau_fit), 4),
                "curve_r2": round(float(r2), 4),
                "curve_fit_status": "SUCCESS",
            }
        except Exception:
            return {
                "curve_vmax": None,
                "curve_tau": None,
                "curve_r2": None,
                "curve_fit_status": "FAILED_CONVERGENCE",
            }

    @classmethod
    def extract_trial_kinematics(
        cls,
        trial_df: pl.DataFrame,
        is_straight_sprint: bool = False,
    ) -> Dict[str, Any]:
        """
        Extracts comprehensive kinematics from a single drill trial.
        Expects sorted frames with columns ['s', 'a'] and optionally ['time'].
        """
        if trial_df.is_empty():
            return {}

        speeds = trial_df["s"].to_numpy()
        accels = trial_df["a"].to_numpy()
        n_frames = len(speeds)

        if n_frames < 3:
            return {}

        # 1. Velocity metrics
        v_max = float(np.nanmax(speeds))
        active_speeds = speeds[speeds >= 0.5]
        v_mean = float(np.nanmean(active_speeds)) if len(active_speeds) > 0 else float(np.nanmean(speeds))

        # 2. Acceleration metrics
        a_max = float(np.nanmax(accels))
        a_var = float(np.nanstd(accels))

        # Initial acceleration: mean acceleration over first 1.0 second (10 frames)
        first_sec_frames = min(10, n_frames)
        a_init = float(np.nanmean(accels[:first_sec_frames]))

        # 3. Temporal latencies
        idx_v_max = int(np.nanargmax(speeds))
        t_v_max = round(idx_v_max * cls.DT, 3)

        # Time to 90% of v_max
        v_90_thresh = 0.90 * v_max
        idx_90 = np.where(speeds >= v_90_thresh)[0]
        t_reach_90_vmax = round(float(idx_90[0] * cls.DT), 3) if len(idx_90) > 0 else t_v_max

        # Burst latency: time to peak acceleration
        idx_a_max = int(np.nanargmax(accels))
        burst_latency = round(idx_a_max * cls.DT, 3)

        # 4. Jerk (rate of force development proxy)
        jerk = cls.compute_jerk(accels, cls.DT)
        pos_jerk = jerk[jerk > 0]
        mean_pos_jerk = float(np.nanmean(pos_jerk)) if len(pos_jerk) > 0 else 0.0

        # 5. Deceleration characteristics (tangential deceleration)
        a_tan = cls.compute_tangential_acceleration(speeds, cls.DT)
        decel_frames = a_tan[a_tan < 0]
        max_decel = float(np.nanmin(a_tan)) if len(a_tan) > 0 else 0.0
        mean_decel = float(np.nanmean(decel_frames)) if len(decel_frames) > 0 else 0.0
        decel_fraction = float(np.mean(a_tan < -1.0))

        features = {
            "v_max": round(v_max, 4),
            "v_mean": round(v_mean, 4),
            "a_init": round(a_init, 4),
            "a_max": round(a_max, 4),
            "a_var": round(a_var, 4),
            "t_v_max": t_v_max,
            "t_reach_90_vmax": t_reach_90_vmax,
            "burst_latency": burst_latency,
            "mean_pos_jerk": round(mean_pos_jerk, 4),
            "max_decel": round(max_decel, 4),
            "mean_decel": round(mean_decel, 4),
            "decel_fraction": round(decel_fraction, 4),
            "trial_duration_sec": round(n_frames * cls.DT, 2),
        }

        # 6. Straight-line sprint velocity curve fitting
        if is_straight_sprint:
            t_axis = np.arange(n_frames) * cls.DT
            curve_results = cls.fit_sprint_velocity_curve(t_axis, speeds)
            features.update(curve_results)
        else:
            features.update({
                "curve_vmax": None,
                "curve_tau": None,
                "curve_r2": None,
                "curve_fit_status": "NOT_APPLICABLE_NON_SPRINT_DRILL",
            })

        return features
