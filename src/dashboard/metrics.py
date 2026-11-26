"""
ATHLETIX AI — Dashboard Metrics & Formatting Helpers
Handles statistical aggregation and display formatting.
"""

from typing import Any, Union
import numpy as np
import pandas as pd


def fmt_speed(val: Any) -> str:
    """Format speed values to yd/s."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        return f"{float(val):.2f} yd/s"
    except (ValueError, TypeError):
        return "N/A"


def fmt_accel(val: Any) -> str:
    """Format acceleration values to yd/s²."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        return f"{float(val):.2f} yd/s²"
    except (ValueError, TypeError):
        return "N/A"


def fmt_time(val: Any) -> str:
    """Format timing values to seconds."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        return f"{float(val):.2f} s"
    except (ValueError, TypeError):
        return "N/A"


def fmt_ratio(val: Any) -> str:
    """Format dimensionless ratio."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        return f"{float(val):.3f}"
    except (ValueError, TypeError):
        return "N/A"


def fmt_pct(val: Any) -> str:
    """Format percentage value."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        return f"{float(val)*100:.1f}%"
    except (ValueError, TypeError):
        return "N/A"


def fmt_dist_in(val: Any) -> str:
    """Format inches."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        return f'{float(val):.1f}"'
    except (ValueError, TypeError):
        return "N/A"


def fmt_weight_lbs(val: Any) -> str:
    """Format pounds."""
    if val is None or pd.isna(val):
        return "N/A"
    try:
        return f"{int(round(float(val)))} lbs"
    except (ValueError, TypeError):
        return "N/A"


def get_tier_color(tier: str) -> str:
    """Return styling color for Athletic Alpha tier."""
    if "High Outperformer" in str(tier):
        return "#0A5C36"  # Deep Emerald
    elif "Moderate Outperformer" in str(tier):
        return "#1B8A5A"  # Forest Green
    elif "High Underperformer" in str(tier):
        return "#C53030"  # Crimson Red
    elif "Moderate Underperformer" in str(tier):
        return "#DD6B20"  # Dark Amber
    return "#4A5568"      # Slate Grey
