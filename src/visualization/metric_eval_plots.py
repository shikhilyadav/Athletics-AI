"""Plots for residual distribution, Bland-Altman agreement, and SHAP summaries."""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np


def plot_residual_analysis(residuals_df: pd.DataFrame, metric_label: str = "Peak Game Speed (yd/s)") -> go.Figure:
    """
    Scatter plot comparing Traditional Combine Predicted vs Actual Game Performance.
    Points above the identity line represents athletes whose potential was underestimated.
    """
    fig = go.Figure()

    pred_col = [c for c in residuals_df.columns if c.startswith("expected_from_traditional")][0]
    actual_col = [c for c in residuals_df.columns if c.startswith("actual_")][0]

    min_val = min(residuals_df[pred_col].min(), residuals_df[actual_col].min())
    max_val = max(residuals_df[pred_col].max(), residuals_df[actual_col].max())

    # Identity line
    fig.add_trace(go.Scatter(
        x=[min_val, max_val],
        y=[min_val, max_val],
        mode="lines",
        line=dict(dash="dash", color="gray"),
        name="Traditional Expectation Line",
    ))

    # Players
    fig.add_trace(go.Scatter(
        x=residuals_df[pred_col],
        y=residuals_df[actual_col],
        mode="markers",
        marker=dict(
            size=9,
            color=residuals_df["residual_zscore"],
            colorscale="Plasma",
            showscale=True,
            colorbar=dict(title="Residual Z-Score (Athletic Alpha)"),
        ),
        text=[f"Player: {p}<br>Actual: {act:.2f}<br>Traditional Exp: {exp:.2f}<br>Residual Z: {z:.2f}"
              for p, act, exp, z in zip(
                  residuals_df.get("displayName", residuals_df.index),
                  residuals_df[actual_col],
                  residuals_df[pred_col],
                  residuals_df["residual_zscore"]
              )],
        hoverinfo="text",
        name="Prospects",
    ))

    fig.update_layout(
        title=f"Residual Potential Analysis: {metric_label}",
        xaxis=dict(title="Expected Performance (Traditional Combine Model)"),
        yaxis=dict(title="Actual Regular-Season Performance (NGS Tracking)"),
        template="plotly_dark",
        width=850,
        height=600,
    )
    return fig
