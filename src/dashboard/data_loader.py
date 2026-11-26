"""
ATHLETIX AI — Dashboard Data Loader
Cached, memory-optimized data access layer for Streamlit dashboard.
"""

from pathlib import Path
from typing import Optional
import pandas as pd
import polars as pl
import streamlit as st

DATA_DIR = Path("data/processed")
MODELS_DIR = Path("models/saved")
AUDIT_MODELS_DIR = Path("models/saved/phase3_1_audit")
REPORTS_DIR = Path("reports")


@st.cache_data(show_spinner=False)
def load_master_df() -> pd.DataFrame:
    """Load the 510-prospect Combine Player Master dataset."""
    path = DATA_DIR / "combine_player_master.parquet"
    if not path.exists():
        st.error(f"Master dataset missing at {path}")
        return pd.DataFrame()
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def load_kinematics_df() -> pd.DataFrame:
    """Load the 6,310-trial Combine Kinematic features dataset."""
    path = DATA_DIR / "combine_kinematic_features.parquet"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def load_cod_df() -> pd.DataFrame:
    """Load the 6,310-trial Combine Change-of-Direction features dataset."""
    path = DATA_DIR / "combine_cod_features.parquet"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def load_game_tracking_df() -> pd.DataFrame:
    """Load the 156-player 2023 Game Tracking features dataset."""
    path = DATA_DIR / "game_tracking_features_2023.parquet"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def load_player_play_df() -> pd.DataFrame:
    """Load the 50,462-play Player Play context dataset (subsetted for memory)."""
    path = DATA_DIR / "player_play_features.parquet"
    if not path.exists():
        return pd.DataFrame()
    # Read using polars with projection to keep memory minimal
    cols = [
        "nfl_id", "game_id", "play_id", "lined_up_position",
        "separation_at_pass_forward", "player_get_off", "time_to_pressure",
        "play_max_speed", "play_total_distance"
    ]
    df = pl.read_parquet(path, columns=cols).to_pandas()
    return df


@st.cache_data(show_spinner=False)
def load_oof_predictions() -> pd.DataFrame:
    """Load the 149-player out-of-fold predictions."""
    path = MODELS_DIR / "oof_predictions.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_athletic_alpha() -> pd.DataFrame:
    """Load the 149-player Athletic Alpha residuals dataset."""
    path = MODELS_DIR / "athletic_alpha_residuals.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_model_metrics() -> pd.DataFrame:
    """Load Phase 3 unadjusted cross-validation model metrics."""
    path = MODELS_DIR / "model_comparison_metrics.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_nested_cv_metrics() -> pd.DataFrame:
    """Load Phase 3.1 rigorously tuned Nested CV model metrics."""
    path = AUDIT_MODELS_DIR / "nested_cv_model_metrics.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_fdr_correlations() -> pd.DataFrame:
    """Load Phase 3.1 Benjamini-Hochberg FDR corrected sensor correlations."""
    path = AUDIT_MODELS_DIR / "fdr_corrected_correlations.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_feature_importance() -> pd.DataFrame:
    """Load Model C feature importances."""
    path = MODELS_DIR / "feature_importance.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_vif_analysis() -> pd.DataFrame:
    """Load Multicollinearity VIF analysis."""
    path = MODELS_DIR / "vif_analysis.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)


@st.cache_data(show_spinner=False)
def load_dataset_inventory() -> pd.DataFrame:
    """Load the actual competition dataset inventory."""
    path = REPORTS_DIR / "actual_dataset_inventory.csv"
    if not path.exists():
        return pd.DataFrame()
    return pd.read_csv(path)
