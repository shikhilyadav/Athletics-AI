"""
ATHLETIX AI: Phase 2 Feature Engineering Unit Tests
===================================================
Tests core biomechanical mathematics, circular trigonometry,
jerk derivatives, mono-exponential sprint curve fitting,
turn detection, and player-level aggregation logic.
"""

import pytest
import numpy as np
import polars as pl
from pathlib import Path

from src.features.kinematics import KinematicFeatureExtractor, mono_exponential_velocity
from src.features.cod_metrics import CODFeatureExtractor
from src.features.tracking_aggregators import TrackingAggregator


def test_mono_exponential_velocity_function():
    """Verifies theoretical asymptote of sprint velocity curve."""
    t = np.array([0.0, 1.0, 2.0, 5.0, 10.0])
    v_max = 10.0
    tau = 1.0
    v = mono_exponential_velocity(t, v_max, tau)
    
    assert v[0] == 0.0  # Zero speed at start
    assert np.isclose(v[1], 10.0 * (1.0 - np.exp(-1.0)), atol=1e-4)
    assert np.isclose(v[-1], 10.0, atol=1e-3)  # Converges to v_max


def test_tangential_acceleration_and_jerk():
    """Verifies numerical derivative calculations for acceleration and jerk."""
    # Speeds increasing linearly by 1 yd/s every 0.1s: a = 10 yd/s^2
    speeds = np.array([0.0, 1.0, 2.0, 3.0, 4.0])
    dt = 0.10
    a_tan = KinematicFeatureExtractor.compute_tangential_acceleration(speeds, dt)
    assert np.allclose(a_tan[1:], 10.0)

    # Constant acceleration -> zero jerk
    jerk = KinematicFeatureExtractor.compute_jerk(a_tan, dt)
    assert np.allclose(jerk[2:], 0.0)


def test_sprint_velocity_curve_fitting():
    """Tests mono-exponential sprint curve fitting on synthetic ground truth."""
    t = np.arange(0, 4.5, 0.1)
    true_vmax = 10.2
    true_tau = 1.15
    speeds = mono_exponential_velocity(t, true_vmax, true_tau) + np.random.normal(0, 0.02, len(t))

    fit_res = KinematicFeatureExtractor.fit_sprint_velocity_curve(t, speeds)
    assert fit_res["curve_fit_status"] == "SUCCESS"
    assert np.isclose(fit_res["curve_vmax"], true_vmax, atol=0.25)
    assert np.isclose(fit_res["curve_tau"], true_tau, atol=0.25)
    assert fit_res["curve_r2"] > 0.95


def test_circular_angle_diff_boundary_wrapping():
    """
    CRITICAL TEST: Verifies that 355° to 5° is calculated as +10° change,
    NOT -350° or +350°.
    """
    prev = np.array([355.0, 10.0, 180.0, 0.0])
    curr = np.array([5.0, 350.0, 170.0, 359.0])
    
    diff = CODFeatureExtractor.circular_angle_diff(curr, prev)
    
    # 355 -> 5 is +10 deg
    assert np.isclose(diff[0], 10.0)
    # 10 -> 350 is -20 deg
    assert np.isclose(diff[1], -20.0)
    # 180 -> 170 is -10 deg
    assert np.isclose(diff[2], -10.0)
    # 0 -> 359 is -1 deg
    assert np.isclose(diff[3], -1.0)


def test_turn_detection_and_preservation_ratio():
    """Tests turn detection around an apex with entry and exit deceleration/acceleration."""
    # Simulate a 180 degree cut: speeds drop, direction flips from 0 to 180
    n = 15
    speeds = np.array([6.0, 5.5, 4.0, 2.5, 2.0, 2.2, 3.5, 5.0, 5.8, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0])
    directions = np.array([0.0, 0.0, 10.0, 45.0, 90.0, 140.0, 175.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0, 180.0])
    
    turns = CODFeatureExtractor.detect_turns(speeds, directions, min_angular_velocity=30.0, min_entry_speed=1.5)
    assert len(turns) >= 1
    t0 = turns[0]
    assert t0["v_apex"] <= 2.5
    assert t0["v_entry"] >= 4.0
    assert t0["speed_preservation_ratio"] < 1.0


def test_snap_eligibility_counting(tmp_path):
    """Verifies that plays nullified by penalty are excluded and >=50 snap rule works."""
    dummy_data = pl.DataFrame({
        "game_id": [1, 1, 1, 2, 2],
        "play_id": [10, 20, 30, 40, 50],
        "nfl_id": [99999, 99999, 99999, 99999, 99999],
        "play_nullified_by_penalty": ["N", "N", "Y", "N", "N"],  # 1 nullified
    })
    csv_file = tmp_path / "test_player_play.csv"
    dummy_data.write_csv(csv_file)

    res = TrackingAggregator.calculate_snap_eligibility(csv_file, min_snaps=4)
    row = res.filter(pl.col("nfl_id") == 99999).to_dicts()[0]
    assert row["verified_scrimmage_snaps"] == 4  # 5 total - 1 nullified = 4
    assert row["is_eligible_50_snaps"] is True  # 4 >= 4 threshold
