"""Visualization module for 2D trajectories, field orientation, and speed heatmaps."""
import plotly.graph_objects as go
import pandas as pd
from src.config import FIELD_X_MAX, FIELD_Y_MAX


def plot_drill_trajectory(drill_df: pd.DataFrame, title: str = "Drill Trajectory (10 Hz Sensor Tracking)") -> go.Figure:
    """
    Renders an interactive Plotly trajectory of a combine drill or game play,
    colored by instantaneous speed.
    """
    fig = go.Figure()

    # Scatter trajectory
    fig.add_trace(go.Scatter(
        x=drill_df["x"],
        y=drill_df["y"],
        mode="lines+markers",
        marker=dict(
            size=6,
            color=drill_df["s"],
            colorscale="Viridis",
            showscale=True,
            colorbar=dict(title="Speed (yd/s)"),
        ),
        line=dict(color="rgba(100, 100, 100, 0.4)", width=2),
        text=[f"Frame: {f}<br>Speed: {s:.2f} yd/s<br>Accel: {a:.2f} yd/s²"
              for f, s, a in zip(drill_df.get("frameId", range(len(drill_df))), drill_df["s"], drill_df["a"])],
        hoverinfo="text",
        name="Athlete Trajectory",
    ))

    fig.update_layout(
        title=title,
        xaxis=dict(title="Field X (Yards)", range=[0, FIELD_X_MAX]),
        yaxis=dict(title="Field Y (Yards)", range=[0, FIELD_Y_MAX], scaleanchor="x", scaleratio=1),
        template="plotly_dark",
        width=950,
        height=500,
    )
    return fig
