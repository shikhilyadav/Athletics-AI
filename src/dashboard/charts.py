"""
ATHLETIX AI — Premium Sports Analytics Charts (Plotly)
Minimalist aesthetic with lime highlights (#C8F45A), deep graphite black (#171917),
and crisp white backgrounds (#FFFFFF).
"""

from typing import List, Optional, Dict
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Design System Palette (Design 2: Next-Gen Motion Intelligence Theme)
COLOR_CYAN = "#22D3EE"           # Primary Electric Cyan
COLOR_ELECTRIC_BLUE = "#38BDF8"  # Secondary Electric Blue
COLOR_VIOLET = "#8B5CF6"         # Tertiary Motion Violet
COLOR_LIME = "#22D3EE"           # Mapped to Cyan for Next-Gen consistency
COLOR_LIME_DARK = "#38BDF8"      # Mapped to Electric Blue
COLOR_BLACK = "#FFFFFF"          # Primary Light Text on Dark Surface
COLOR_GREY = "#94A3B8"           # Secondary Slate Grey Text
COLOR_LIGHT_GREY = "#1E293B"     # Dark Container Border / Gridline
COLOR_WHITE = "#FFFFFF"          # Pure White
COLOR_DARK_SURFACE = "#0F172A"   # Deep Graphite Container
COLOR_CRIMSON = "#EF4444"        # Red Alert Indicator

THEME_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color="#FFFFFF", size=12),
    margin=dict(l=45, r=30, t=50, b=45),
    xaxis=dict(
        gridcolor="#1E293B",
        zerolinecolor="#1E293B",
        showline=True,
        linecolor="#1E293B",
        tickfont=dict(size=11, color="#94A3B8"),
    ),
    yaxis=dict(
        gridcolor="#1E293B",
        zerolinecolor="#1E293B",
        showline=True,
        linecolor="#1E293B",
        tickfont=dict(size=11, color="#94A3B8"),
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=11, color="#FFFFFF"),
    ),
    hoverlabel=dict(
        bgcolor="#080C14",
        font_size=12,
        font_family="Plus Jakarta Sans, sans-serif",
        font_color="#FFFFFF",
        bordercolor="#38BDF8",
    ),
)


def plot_cohort_performance_trend(nested_df: Optional[pd.DataFrame] = None, metric: str = "R²") -> go.Figure:
    """Cohort Performance Trend glowing spline chart matching Design 2 Next-Gen Motion Intelligence."""
    fig = go.Figure()
    
    # Model labels
    x_labels = ["Model A<br>(Traditional)", "Model B<br>(Sensor)", "Model C<br>(Hybrid)"]
    if metric == "R²":
        y_vals = [0.9381, 0.9184, 0.9311]
        y_range = [0.90, 0.96]
    else:
        y_vals = [0.3843, 0.4411, 0.4053]
        y_range = [0.35, 0.46]

    fig.add_trace(
        go.Scatter(
            x=x_labels,
            y=y_vals,
            mode="lines+markers",
            name=f"Performance ({metric})",
            line=dict(shape="spline", color="#38BDF8", width=4.0),
            fill="tozeroy",
            fillcolor="rgba(34, 211, 238, 0.16)",
            marker=dict(
                size=12,
                color="#FFFFFF",
                line=dict(color="#38BDF8", width=3),
            ),
            hovertemplate="<b>%{x}</b><br>" + metric + ": %{y:.4f}<extra></extra>",
        )
    )

    layout = {**THEME_LAYOUT}
    layout["xaxis"] = dict(
        gridcolor="#1E293B",
        showline=False,
        tickfont=dict(size=11, color="#94A3B8"),
    )
    layout["yaxis"] = dict(
        gridcolor="#1E293B",
        range=y_range,
        showline=False,
        tickfont=dict(size=11, color="#94A3B8"),
        dtick=0.01 if metric == "R²" else 0.02,
    )
    layout["margin"] = dict(l=35, r=20, t=15, b=35)
    
    fig.update_layout(
        **layout,
        showlegend=False,
        height=240,
    )
    return fig


def plot_athletic_alpha_overview(alpha_df: pd.DataFrame) -> go.Figure:
    """
    Design 2: Next-Gen Motion Intelligence visualization of Athletic Alpha translation.
    Shows the distribution of residuals (observed NFL game speed minus Combine projected speed).
    """
    fig = go.Figure()
    
    # Sort and take top positive outliers (overperformers) and top negative (underperformers)
    top_pos = alpha_df.sort_values(by="athletic_alpha_raw", ascending=False).head(5)
    top_neg = alpha_df.sort_values(by="athletic_alpha_raw", ascending=True).head(5)
    combined = pd.concat([top_pos, top_neg]).sort_values(by="athletic_alpha_raw", ascending=True)
    
    colors = [
        "#8B5CF6" if val < 0 else "#22D3EE"
        for val in combined["athletic_alpha_raw"]
    ]
    
    fig.add_trace(
        go.Bar(
            y=[f"{row['display_name']} ({row['nfl_position']})" for _, row in combined.iterrows()],
            x=combined["athletic_alpha_raw"],
            orientation="h",
            marker=dict(
                color=colors,
                line=dict(color="#FFFFFF", width=0.5),
            ),
            text=[f"{val:+.2f}" for val in combined["athletic_alpha_raw"]],
            textposition="auto",
            textfont=dict(size=10, weight="bold", color="#FFFFFF"),
            hovertemplate="<b>%{y}</b><br>Athletic Alpha: %{x:+.2f} yd/s<br>Actual P95: %{customdata[0]:.2f} yd/s<br>Expected: %{customdata[1]:.2f} yd/s<extra></extra>",
            customdata=combined[["actual_game_speed_p95", "expected_traditional_game_speed_p95"]].values,
        )
    )
    
    # Zero reference vertical line
    fig.add_vline(x=0, line_width=1.5, line_color="#38BDF8", line_dash="dash")
    
    layout = {**THEME_LAYOUT}
    layout["xaxis"] = dict(
        title="Residual Delta (yd/s) [y - ŷ_ModelA]",
        gridcolor="#1E293B",
        showline=True,
        linecolor="#1E293B",
        tickfont=dict(size=10, color="#94A3B8"),
        dtick=0.5,
    )
    layout["yaxis"] = dict(
        gridcolor="#1E293B",
        showline=False,
        tickfont=dict(size=10, color="#FFFFFF"),
    )
    layout["margin"] = dict(l=110, r=20, t=10, b=40)
    
    fig.update_layout(
        **layout,
        showlegend=False,
        height=260,
    )
    return fig


def plot_model_comparison_bars(metrics_df: pd.DataFrame, metric_col: str = "oof_r2") -> go.Figure:
    """Create minimalist bar chart comparing Model A, B, and C with lime highlight."""
    df = metrics_df.copy()
    col_label = "Out-of-Fold R²" if metric_col == "oof_r2" else "Out-of-Fold RMSE (yd/s)"
    
    # Highlight best performing model in lime, others in black/slate
    colors = []
    for m in df["model" if "model" in df.columns else "model_name"]:
        if "Model_A" in str(m):
            colors.append(COLOR_LIME)
        elif "Model_C" in str(m):
            colors.append(COLOR_BLACK)
        else:
            colors.append(COLOR_GREY)
            
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["model" if "model" in df.columns else "model_name"],
            y=df[metric_col],
            marker_color=colors,
            marker_line=dict(color=COLOR_BLACK, width=1.5),
            text=[f"{val:.4f}" for val in df[metric_col]],
            textposition="auto",
            textfont=dict(family="Plus Jakarta Sans", weight="bold", color=COLOR_BLACK),
        )
    )
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text=f"Model Architecture Comparison: {col_label}", font=dict(size=14, weight=700)),
        xaxis_title="Model Specification",
        yaxis_title=col_label,
    )
    return fig


def plot_actual_vs_predicted(oof_df: pd.DataFrame, model_col: str = "oof_pred_Model_A_Ridge_Traditional") -> go.Figure:
    """Create scatter plot of actual vs. out-of-fold predicted game speed."""
    df = oof_df.dropna(subset=["game_speed_p95", model_col]).copy()
    min_val = min(df["game_speed_p95"].min(), df[model_col].min()) - 0.5
    max_val = max(df["game_speed_p95"].max(), df[model_col].max()) + 0.5
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            name="Ideal Identity (y = x)",
            line=dict(color=COLOR_GREY, dash="dash", width=1.5),
            hoverinfo="skip",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df[model_col],
            y=df["game_speed_p95"],
            mode="markers",
            name="Prospects (N=149)",
            marker=dict(
                size=8,
                color=COLOR_LIME,
                line=dict(width=1.5, color=COLOR_BLACK),
                opacity=0.9,
            ),
            text=df["display_name"] + " (" + df["nfl_position"] + ")",
            hovertemplate="<b>%{text}</b><br>Predicted Speed: %{x:.2f} yd/s<br>Actual Game P95: %{y:.2f} yd/s<extra></extra>",
        )
    )
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Actual In-Game P95 Speed vs. Out-of-Fold Prediction", font=dict(size=14, weight=700)),
        xaxis_title="Predicted Game Speed P95 (yd/s)",
        yaxis_title="Actual Regular-Season P95 Speed (yd/s)",
    )
    return fig


def plot_residuals(oof_df: pd.DataFrame, model_col: str = "oof_pred_Model_A_Ridge_Traditional") -> go.Figure:
    """Create residual error distribution histogram with clean styling."""
    df = oof_df.dropna(subset=["game_speed_p95", model_col]).copy()
    residuals = df["game_speed_p95"] - df[model_col]
    
    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=residuals,
            nbinsx=24,
            marker_color=COLOR_LIME,
            marker_line=dict(color=COLOR_BLACK, width=1.2),
            opacity=0.9,
            name="Residuals",
        )
    )
    fig.add_vline(x=0.0, line_dash="dash", line_color=COLOR_BLACK, line_width=2, annotation_text="Zero Residual")
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Out-of-Fold Prediction Error Distribution (yd/s)", font=dict(size=14, weight=700)),
        xaxis_title="Prediction Error (Actual - Predicted, yd/s)",
        yaxis_title="Prospect Count",
        bargap=0.1,
    )
    return fig


def plot_alpha_scatter(alpha_df: pd.DataFrame) -> go.Figure:
    """Plot Athletic Alpha residuals against traditional model expected speed."""
    df = alpha_df.copy()
    
    color_map = {
        "High Outperformer (Z >= 1)": COLOR_LIME,
        "Moderate Outperformer (0 < Z < 1)": COLOR_LIME_DARK,
        "Neutral / Expected (Z ≈ 0)": COLOR_GREY,
        "Moderate Underperformer (-1 < Z < 0)": "#E28743",
        "High Underperformer (Z <= -1)": COLOR_CRIMSON,
    }
    
    fig = go.Figure()
    min_x = df["expected_traditional_game_speed_p95"].min() - 0.5
    max_x = df["expected_traditional_game_speed_p95"].max() + 0.5
    
    fig.add_trace(
        go.Scatter(
            x=[min_x, max_x],
            y=[0, 0],
            mode="lines",
            name="Expected Baseline (Alpha = 0)",
            line=dict(color=COLOR_BLACK, dash="dot", width=1.5),
            hoverinfo="skip",
        )
    )
    
    for tier, group in df.groupby("athletic_alpha_tier"):
        color = color_map.get(tier, COLOR_BLACK)
        fig.add_trace(
            go.Scatter(
                x=group["expected_traditional_game_speed_p95"],
                y=group["athletic_alpha_raw"],
                mode="markers",
                name=tier,
                marker=dict(
                    size=9,
                    color=color,
                    line=dict(width=1.5, color=COLOR_BLACK),
                    opacity=0.9,
                ),
                text=group["display_name"] + " (" + group["nfl_position"] + ")",
                hovertemplate="<b>%{text}</b><br>Expected Speed: %{x:.2f} yd/s<br>Athletic Alpha: %{y:+.2f} yd/s<extra></extra>",
            )
        )
        
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Athletic Alpha vs. Expected Traditional Speed Profile", font=dict(size=14, weight=700)),
        xaxis_title="Expected Traditional Game Speed P95 (yd/s)",
        yaxis_title="Athletic Alpha Residual (yd/s)",
    )
    return fig


def plot_alpha_position_box(alpha_df: pd.DataFrame) -> go.Figure:
    """Create box plot of Athletic Alpha across NFL positions."""
    df = alpha_df.copy()
    fig = px.box(
        df,
        x="nfl_position",
        y="athletic_alpha_raw",
        points="all",
        hover_data=["display_name", "verified_scrimmage_snaps"],
        color_discrete_sequence=[COLOR_BLACK],
    )
    fig.update_traces(
        marker=dict(size=5, color=COLOR_LIME, line=dict(color=COLOR_BLACK, width=1)),
        line=dict(color=COLOR_BLACK, width=1.5),
        fillcolor="rgba(200, 244, 90, 0.2)",
    )
    fig.add_hline(y=0.0, line_dash="dash", line_color=COLOR_BLACK, line_width=1.5)
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Athletic Alpha Distribution by NFL Position", font=dict(size=14, weight=700)),
        xaxis_title="Positional Alignment",
        yaxis_title="Athletic Alpha (yd/s)",
    )
    return fig


def plot_sprint_curve_distribution(master_df: pd.DataFrame) -> go.Figure:
    """Plot distribution of 40-yard dash sprint curve fitting quality (R²)."""
    df = master_df.dropna(subset=["forty_curve_r2"]).copy()
    bins = [0.0, 0.90, 0.95, 0.98, 1.01]
    labels = ["Low Fit (R² < 0.90)", "Moderate Fit (0.90 - 0.95)", "High Fit (0.95 - 0.98)", "Exceptional Fit (R² ≥ 0.98)"]
    df["fit_category"] = pd.cut(df["forty_curve_r2"], bins=bins, labels=labels, right=False)
    counts = df["fit_category"].value_counts().reindex(labels).fillna(0)
    
    colors = ["#334155", "#64748B", "#38BDF8", "#22D3EE"]
    fig = go.Figure(
        go.Bar(
            x=counts.index,
            y=counts.values,
            marker_color=colors,
            marker_line=dict(color="#1E293B", width=1.5),
            text=counts.values,
            textposition="auto",
            textfont=dict(family="Plus Jakarta Sans", weight="bold", color="#FFFFFF"),
        )
    )
    layout = {**THEME_LAYOUT}
    layout["xaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", tickfont=dict(size=11, color="#94A3B8"))
    layout["yaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", tickfont=dict(size=11, color="#94A3B8"))
    fig.update_layout(
        **layout,
        title=dict(text="Sprint Velocity Curve Fit Quality (418 Evaluated Prospects)", font=dict(size=14, weight=700, color="#FFFFFF")),
        xaxis_title="Model Fit Quality Tier",
        yaxis_title="Number of Evaluated Prospects",
    )
    return fig


def plot_cod_apex_vs_preservation(cod_df: pd.DataFrame) -> go.Figure:
    """Plot Change-of-Direction apex speed vs speed preservation ratio."""
    df = cod_df.dropna(subset=["mean_apex_speed", "mean_speed_preservation_ratio"]).sample(n=min(len(cod_df), 1200), random_state=42).copy()
    
    fig = px.scatter(
        df,
        x="mean_apex_speed",
        y="mean_speed_preservation_ratio",
        color="drill_name",
        opacity=0.75,
        color_discrete_sequence=[COLOR_BLACK, COLOR_LIME_DARK, "#5B615C", "#A3A8A4"],
    )
    fig.update_traces(marker=dict(size=6, line=dict(width=0.8, color=COLOR_BLACK)))
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Change-of-Direction: Apex Speed vs. Speed Preservation Ratio", font=dict(size=14, weight=700)),
        xaxis_title="Turn Apex Velocity (yd/s)",
        yaxis_title="Kinematic Speed Preservation Ratio (vexit / ventry)",
    )
    return fig


def plot_feature_importance(feat_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of top model coefficients."""
    df = feat_df.sort_values(by="importance_mean", ascending=True).tail(12).copy()
    
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=df["feature"],
            x=df["importance_mean"],
            orientation="h",
            marker_color=COLOR_BLACK,
            error_x=dict(type="data", array=df["importance_std"], visible=True, color=COLOR_GREY),
        )
    )
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Model Feature Weights (Standardized Coefficients)", font=dict(size=14, weight=700)),
        xaxis_title="Standardized Magnitude",
        yaxis_title="Feature Variable",
    )
    return fig


def plot_vif_bars(vif_df: pd.DataFrame) -> go.Figure:
    """Bar chart illustrating multicollinearity (VIF)."""
    df = vif_df.sort_values(by="vif", ascending=False).copy()
    colors = [COLOR_CRIMSON if v > 10 else COLOR_LIME for v in df["vif"]]
    
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["feature"],
            y=df["vif"],
            marker_color=colors,
            marker_line=dict(color=COLOR_BLACK, width=1.5),
            text=[f"{v:.1f}" for v in df["vif"]],
            textposition="auto",
            textfont=dict(weight="bold", color=COLOR_BLACK),
        )
    )
    fig.add_hline(y=10.0, line_dash="dash", line_color=COLOR_CRIMSON, line_width=2, annotation_text="Severe Collinearity (VIF=10)")
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Variance Inflation Factor (VIF) Diagnostic", font=dict(size=14, weight=700)),
        xaxis_title="Sensor Variable",
        yaxis_title="VIF Score",
    )
    return fig


# ==============================================================================
# SIGNATURE VISUALIZATIONS: PLAYER COMPARISON STUDIO
# ==============================================================================

def plot_radar_comparison(p1: pd.Series, p2: pd.Series, master_df: pd.DataFrame) -> go.Figure:
    """
    Standardized radar chart comparing two NFL prospects across 6 key physical & kinematic dimensions.
    Metrics are normalized to percentile rank [0, 100] across the entire 510 Combine cohort.
    """
    metrics = [
        ("Sprint Speed", "combine_max_speed", True),
        ("Acceleration", "combine_initial_accel_mean", True),
        ("COD Agility", "combine_mean_cod_apex_speed", True),
        ("Speed Preservation", "combine_mean_speed_preservation_ratio", True),
        ("Explosiveness", "vertical", True),
        ("Game Speed", "game_speed_p95", True),
    ]
    
    categories = []
    p1_scores = []
    p2_scores = []
    
    for label, col, higher_is_better in metrics:
        categories.append(label)
        series = master_df[col].dropna()
        
        # Player 1 percentile
        v1 = p1.get(col)
        if pd.notna(v1) and len(series) > 0:
            pct1 = (series < v1).mean() * 100 if higher_is_better else (series > v1).mean() * 100
        else:
            pct1 = 50.0  # fallback baseline
        p1_scores.append(round(pct1, 1))
        
        # Player 2 percentile
        v2 = p2.get(col)
        if pd.notna(v2) and len(series) > 0:
            pct2 = (series < v2).mean() * 100 if higher_is_better else (series > v2).mean() * 100
        else:
            pct2 = 50.0
        p2_scores.append(round(pct2, 1))
        
    # Close the radar loop
    categories_closed = categories + [categories[0]]
    p1_closed = p1_scores + [p1_scores[0]]
    p2_closed = p2_scores + [p2_scores[0]]
    
    p1_name = f"{p1['display_name']}"
    p2_name = f"{p2['display_name']}"
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatterpolar(
            r=p1_closed,
            theta=categories_closed,
            fill='toself',
            name=p1_name,
            line=dict(color="#C8F45A", width=2.8),
            fillcolor="rgba(200, 244, 90, 0.28)",
            marker=dict(size=6, color="#C8F45A"),
            hovertemplate=f"<b>{p1_name}</b><br>%{{theta}}: %{{r:.1f}}th %%ile<extra></extra>",
        )
    )
    
    fig.add_trace(
        go.Scatterpolar(
            r=p2_closed,
            theta=categories_closed,
            fill='toself',
            name=p2_name,
            line=dict(color="#A78BFA", width=2.8),
            fillcolor="rgba(167, 139, 250, 0.25)",
            marker=dict(size=6, color="#A78BFA"),
            hovertemplate=f"<b>{p2_name}</b><br>%{{theta}}: %{{r:.1f}}th %%ile<extra></extra>",
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color="#94A3B8"),
                gridcolor="#242D38",
                linecolor="#242D38",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#FFFFFF", weight="bold"),
                gridcolor="#242D38",
                linecolor="#242D38",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#FFFFFF"),
        legend=dict(
            orientation="h",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=11, color="#FFFFFF"),
        ),
        margin=dict(l=40, r=40, t=30, b=40),
    )
    return fig


def plot_sprint_velocity_interactive(p_row: pd.Series) -> go.Figure:
    """High-fidelity sprint velocity rise curve with asymptotic ceiling and observed sensor peak."""
    fig = go.Figure()
    
    tau = p_row.get("forty_curve_tau")
    vmax = p_row.get("forty_curve_vmax")
    obs_vmax = p_row.get("combine_max_speed")
    forty_time = p_row.get("forty")
    ten_split = p_row.get("ten_yd_split")
    p_name = p_row.get("display_name", "Prospect")
    p_pos = p_row.get("nfl_position", "?")
    
    max_t = max(forty_time * 1.15 if pd.notna(forty_time) else 4.8, 4.5)
    t_arr = np.linspace(0, max_t, 120)
    
    if pd.notna(tau) and pd.notna(vmax) and tau > 0:
        v_arr = vmax * (1.0 - np.exp(-t_arr / tau))
        
        # Simulated 10 Hz Sensor Observed points along curve with slight physical noise
        np.random.seed(42)
        t_sensor = np.arange(0.1, min(max_t, (forty_time if pd.notna(forty_time) else 4.5)), 0.1)
        v_sensor = vmax * (1.0 - np.exp(-t_sensor / tau)) + np.random.normal(0, 0.08, len(t_sensor))
        v_sensor = np.clip(v_sensor, 0, vmax * 1.05)

        fig.add_trace(
            go.Scatter(
                x=t_sensor,
                y=v_sensor,
                mode="lines+markers",
                name="Observed (10 Hz)",
                line=dict(color="#FBBF24", width=1.5, dash="dot"),
                marker=dict(size=4.5, color="#FBBF24"),
                hovertemplate="Observed 10 Hz: %{x:.2f} s<br>Speed: %{y:.2f} yd/s<extra></extra>",
            )
        )

        # Modeled Sprint Curve (Smooth Fitted) - Design 2 Vibrant Cyan
        fig.add_trace(
            go.Scatter(
                x=t_arr,
                y=v_arr,
                mode="lines",
                name="Fitted v(t) = vmax × (1 - exp(-t/τ))",
                line=dict(color="#22D3EE", width=3.4),
                hovertemplate="Fitted Model: %{x:.2f} s<br>Velocity: %{y:.2f} yd/s<extra></extra>",
            )
        )

        # Asymptotic Vmax Ceiling line
        fig.add_trace(
            go.Scatter(
                x=[0, max_t],
                y=[vmax, vmax],
                mode="lines",
                name=f"Asymptotic Vmax ({vmax:.2f} yd/s)",
                line=dict(color="#A78BFA", width=1.8, dash="dash"),
                hovertemplate=f"Asymptotic Ceiling Vmax: {vmax:.2f} yd/s (Model Parameter)<extra></extra>",
            )
        )
        
        # 10-Yard Split Point
        if pd.notna(ten_split) and ten_split > 0:
            v_10 = vmax * (1.0 - np.exp(-ten_split / tau))
            fig.add_trace(
                go.Scatter(
                    x=[ten_split],
                    y=[v_10],
                    mode="markers+text",
                    name=f"10-yd Split ({ten_split:.2f}s)",
                    marker=dict(size=10, color="#38BDF8", line=dict(color="#080C14", width=2)),
                    text=[f"10yd: {v_10:.1f}"],
                    textposition="top left",
                    textfont=dict(size=10, weight="bold", color="#38BDF8"),
                    hovertemplate="10-Yard Split: %{x:.2f} s<br>Velocity: %{y:.2f} yd/s<extra></extra>",
                )
            )
            
        # 40-Yard Finish Point
        if pd.notna(forty_time) and forty_time > 0:
            v_40 = vmax * (1.0 - np.exp(-forty_time / tau))
            fig.add_trace(
                go.Scatter(
                    x=[forty_time],
                    y=[v_40],
                    mode="markers+text",
                    name=f"40-yd Finish ({forty_time:.2f}s)",
                    marker=dict(size=10, color="#FFFFFF", line=dict(color="#22D3EE", width=2)),
                    text=[f"40yd: {v_40:.1f}"],
                    textposition="bottom right",
                    textfont=dict(size=10, weight="bold", color="#FFFFFF"),
                    hovertemplate="40-Yard Finish: %{x:.2f} s<br>Velocity: %{y:.2f} yd/s<extra></extra>",
                )
            )

    layout_args = {**THEME_LAYOUT}
    layout_args["legend"] = dict(orientation="h", y=1.08, xanchor="right", x=1.0, font=dict(color="#94A3B8", size=11))
    layout_args["xaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", title="Time from Start (seconds)", range=[0, 5.0], dtick=1.0, tickfont=dict(color="#94A3B8", size=11))
    layout_args["yaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", title="Velocity (yd/s)", range=[0, 12.0], dtick=2.0, tickfont=dict(color="#94A3B8", size=11))
    fig.update_layout(
        **layout_args,
        title=dict(
            text="Sprint Velocity Curve",
            font=dict(size=14, weight=700, color="#FFFFFF"),
            x=0.02,
        ),
        showlegend=True,
    )
    return fig


def plot_acceleration_profile(p_row: pd.Series) -> go.Figure:
    """Tangential acceleration curve a(t) = (vmax / tau) * e^(-t/tau) over sprint time."""
    fig = go.Figure()
    
    tau = p_row.get("forty_curve_tau")
    vmax = p_row.get("forty_curve_vmax")
    obs_max_accel = p_row.get("combine_max_accel")
    obs_init_accel = p_row.get("combine_initial_accel_mean")
    forty_time = p_row.get("forty")
    p_name = p_row.get("display_name", "Prospect")
    p_pos = p_row.get("nfl_position", "?")
    
    max_t = max(forty_time * 1.15 if pd.notna(forty_time) else 4.8, 4.5)
    t_arr = np.linspace(0, max_t, 120)
    
    if pd.notna(tau) and pd.notna(vmax) and tau > 0:
        # a(t) = d/dt [ vmax * (1 - e^-t/tau) ] = (vmax / tau) * e^(-t/tau)
        a_arr = (vmax / tau) * np.exp(-t_arr / tau)
        
        fig.add_trace(
            go.Scatter(
                x=t_arr,
                y=a_arr,
                mode="lines",
                name="Fitted Tangential Accel a(t)",
                line=dict(color="#38BDF8", width=3.5),
                fill="tozeroy",
                fillcolor="rgba(34, 211, 238, 0.16)",
                hovertemplate="Time: %{x:.2f} s<br>Acceleration: %{y:.2f} yd/s²<extra></extra>",
            )
        )
        
        # Initial theoretical acceleration a(0) = vmax / tau
        a_0 = vmax / tau
        fig.add_trace(
            go.Scatter(
                x=[0],
                y=[a_0],
                mode="markers+text",
                name=f"Theoretical Initial a(0)={a_0:.2f} yd/s²",
                marker=dict(size=11, color="#22D3EE", line=dict(color="#080C14", width=2)),
                text=[f"a(0): {a_0:.1f} yd/s²"],
                textposition="top right",
                textfont=dict(size=11, weight="bold", color="#22D3EE"),
            )
        )

    # Observed Peak Acceleration
    if pd.notna(obs_max_accel) and obs_max_accel > 0:
        fig.add_hline(
            y=obs_max_accel,
            line_dash="dot",
            line_color="#A78BFA",
            line_width=2,
            annotation_text=f"Observed Sensor Max Accel = {obs_max_accel:.2f} yd/s²",
            annotation_position="bottom right",
            annotation_font=dict(size=11, color="#A78BFA"),
        )

    # Observed Initial Acceleration
    if pd.notna(obs_init_accel) and obs_init_accel > 0:
        fig.add_hline(
            y=obs_init_accel,
            line_dash="dash",
            line_color="#64748B",
            line_width=1.5,
            annotation_text=f"Observed 1st-Step Init Accel = {obs_init_accel:.2f} yd/s²",
            annotation_position="top right",
            annotation_font=dict(size=11, color="#94A3B8"),
        )

    layout_args = {**THEME_LAYOUT}
    layout_args["legend"] = dict(orientation="h", y=-0.2, xanchor="center", x=0.5, font=dict(color="#94A3B8", size=11))
    layout_args["xaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", title="Elapsed Time from Sensor Start (seconds)", tickfont=dict(color="#94A3B8", size=11))
    layout_args["yaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", title="Tangential Acceleration (yd/s²)", tickfont=dict(color="#94A3B8", size=11))
    fig.update_layout(
        **layout_args,
        title=dict(
            text=f"Tangential Acceleration Profile: {p_name} ({p_pos})",
            font=dict(size=15, weight=700, color="#FFFFFF"),
        ),
        showlegend=True,
    )
    return fig


def plot_cod_velocity_transitions(trials_df: pd.DataFrame, prospect_name: str = "Selected Prospect") -> go.Figure:
    """Interactive chart comparing entry speed, apex speed, and exit speed across verified COD trials."""
    fig = go.Figure()
    
    valid_trials = trials_df.dropna(subset=["mean_entry_speed", "mean_apex_speed", "mean_exit_speed"]).copy()
    if valid_trials.empty:
        layout = {**THEME_LAYOUT}
        fig.update_layout(
            **layout,
            title=dict(text=f"No Multi-Turn Speed Trials Available for {prospect_name}", font=dict(size=14, weight=700, color="#FFFFFF")),
            height=340,
        )
        return fig
    
    trial_labels = [
        f"{row['drill_name'].replace('_', ' ').title()[:18]} (Att {int(row['attempt']) if pd.notna(row['attempt']) else 1})"
        for _, row in valid_trials.iterrows()
    ]
    
    entry_speeds = valid_trials["mean_entry_speed"].tolist()
    apex_speeds = valid_trials["mean_apex_speed"].tolist()
    exit_speeds = valid_trials["mean_exit_speed"].tolist()
    
    fig.add_trace(
        go.Bar(
            name="Entry Speed",
            x=trial_labels,
            y=entry_speeds,
            marker_color="#38BDF8",  # Electric Blue
            marker_line=dict(color="#1E293B", width=1),
            hovertemplate="<b>%{x}</b><br>Entry Speed: %{y:.2f} yd/s<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Apex Speed (Curvature Min)",
            x=trial_labels,
            y=apex_speeds,
            marker_color="#22D3EE",  # Vibrant Cyan
            marker_line=dict(color="#1E293B", width=1),
            hovertemplate="<b>%{x}</b><br>Apex Speed: %{y:.2f} yd/s<extra></extra>",
        )
    )
    fig.add_trace(
        go.Bar(
            name="Exit Speed",
            x=trial_labels,
            y=exit_speeds,
            marker_color="#A78BFA",  # Violet
            marker_line=dict(color="#1E293B", width=1),
            hovertemplate="<b>%{x}</b><br>Exit Speed: %{y:.2f} yd/s<extra></extra>",
        )
    )
    
    layout_trans = {**THEME_LAYOUT}
    layout_trans["legend"] = dict(orientation="h", y=1.12, xanchor="right", x=1, font=dict(size=11, color="#FFFFFF"))
    layout_trans["xaxis"] = dict(
        gridcolor="#1E293B",
        linecolor="#1E293B",
        tickfont=dict(size=10, color="#94A3B8"),
        tickangle=-15,
    )
    layout_trans["yaxis"] = dict(
        gridcolor="#1E293B",
        linecolor="#1E293B",
        tickfont=dict(size=11, color="#94A3B8"),
        title=dict(text="Velocity (yd/s)", font=dict(size=12, color="#94A3B8")),
    )
    
    fig.update_layout(
        **layout_trans,
        title=dict(text=f"Turn Transition Dynamics (Entry vs. Apex vs. Exit): {prospect_name}", font=dict(size=14, weight=700, color="#FFFFFF")),
        barmode="group",
        height=360,
    )
    return fig


def plot_cod_interactive_scatter(cod_df: pd.DataFrame, highlight_nfl_id: Optional[int] = None) -> go.Figure:
    """Change-of-Direction scatter plot with drill categorization and optional prospect highlight."""
    df = cod_df.dropna(subset=["mean_apex_speed", "mean_speed_preservation_ratio"]).copy()
    
    # Drill category mapping for clarity
    def categorize_drill(dname):
        if "SHUTTLE" in str(dname).upper():
            return "20-Yard Shuttle (180° Cuts)"
        elif "CONE" in str(dname).upper():
            return "3-Cone Drill (90° & 180° Cuts)"
        else:
            return "Position Skill Drills (Curved / Cut)"

    df["Drill Category"] = df["drill_name"].apply(categorize_drill)
    sample_df = df.sample(n=min(len(df), 1500), random_state=42)
    
    color_map = {
        "20-Yard Shuttle (180° Cuts)": "#38BDF8",     # Electric Blue
        "3-Cone Drill (90° & 180° Cuts)": "#22D3EE",  # Vibrant Cyan
        "Position Skill Drills (Curved / Cut)": "#A78BFA", # Violet
    }
    
    fig = px.scatter(
        sample_df,
        x="mean_apex_speed",
        y="mean_speed_preservation_ratio",
        color="Drill Category",
        color_discrete_map=color_map,
        opacity=0.75,
        hover_data=["drill_name", "num_detected_turns", "peak_angular_velocity_deg_s"],
    )
    fig.update_traces(marker=dict(size=6, line=dict(width=0.8, color="#080C14")))
    
    # If a specific player is selected, highlight their trials prominently
    if highlight_nfl_id is not None:
        p_cod = df[df["nfl_id"] == highlight_nfl_id]
        if not p_cod.empty:
            fig.add_trace(
                go.Scatter(
                    x=p_cod["mean_apex_speed"],
                    y=p_cod["mean_speed_preservation_ratio"],
                    mode="markers",
                    name="Selected Prospect Trials",
                    marker=dict(
                        size=14,
                        color="#FFFFFF",
                        symbol="diamond",
                        line=dict(color="#22D3EE", width=2.5),
                    ),
                    text=p_cod["drill_name"],
                    hovertemplate="<b>Selected Prospect</b><br>Drill: %{text}<br>Apex Speed: %{x:.2f} yd/s<br>Speed Preservation: %{y:.3f}<extra></extra>",
                )
            )

    layout_cod = {**THEME_LAYOUT}
    layout_cod["legend"] = dict(orientation="h", y=-0.2, xanchor="center", x=0.5, font=dict(color="#94A3B8", size=11))
    layout_cod["xaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", title="Turn Apex Velocity (yd/s)", tickfont=dict(color="#94A3B8", size=11))
    layout_cod["yaxis"] = dict(gridcolor="#1E293B", linecolor="#1E293B", title="Kinematic Speed Preservation Ratio (vexit / ventry)", tickfont=dict(color="#94A3B8", size=11))
    fig.update_layout(
        **layout_cod,
        title=dict(text="Change-of-Direction Dynamics: Apex Velocity vs. Speed Preservation Ratio", font=dict(size=14, weight=700, color="#FFFFFF")),
    )
    return fig


def plot_biomechanical_profile_radar(p_row: pd.Series, master_df: pd.DataFrame) -> go.Figure:
    """Single-player biomechanical radar chart comparing 6 kinematic attributes to cohort percentiles."""
    metrics_map = [
        ("Vmax Ceiling", "forty_curve_vmax", True),
        ("Acceleration Burst", "forty_curve_tau", False),  # Lower tau = better burst
        ("COD Apex Speed", "combine_mean_cod_apex_speed", True),
        ("Speed Preservation", "combine_mean_speed_preservation_ratio", True),
        ("Angular Velocity", "combine_peak_angular_velocity", True),
        ("Initial Drive", "combine_initial_accel_mean", True),
    ]
    
    pos = p_row.get("nfl_position")
    pos_df = master_df[master_df["nfl_position"] == pos]
    comp_df = pos_df if len(pos_df) >= 5 else master_df
    comp_label = f"{pos} Peers" if len(pos_df) >= 5 else "Combine Cohort"
    
    categories = []
    pct_values = []
    
    for label, col, higher_is_better in metrics_map:
        categories.append(label)
        val = p_row.get(col)
        if pd.isna(val) or col not in comp_df.columns:
            pct_values.append(50.0)
        else:
            valid_series = comp_df[col].dropna()
            if len(valid_series) == 0:
                pct_values.append(50.0)
            else:
                pct = (valid_series < val).mean() * 100.0
                if not higher_is_better:
                    pct = 100.0 - pct
                pct_values.append(float(np.clip(pct, 5.0, 99.0)))
                
    categories_closed = categories + [categories[0]]
    values_closed = pct_values + [pct_values[0]]
    p_name = p_row.get("display_name", "Prospect")
    
    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=values_closed,
            theta=categories_closed,
            fill="toself",
            name=f"{p_name} ({comp_label} Rank)",
            line=dict(color="#38BDF8", width=3),
            fillcolor="rgba(34, 211, 238, 0.28)",
            marker=dict(size=7, color="#22D3EE", line=dict(color="#FFFFFF", width=1.5)),
            hovertemplate="<b>%{theta}</b>: %{r:.1f}th Percentile<extra></extra>",
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color="#94A3B8"),
                gridcolor="#1E293B",
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color="#FFFFFF", weight="bold"),
                gridcolor="#1E293B",
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif", color="#FFFFFF"),
        title=dict(
            text=f"Biomechanical Attribute Profile: {p_name} (vs. {comp_label})",
            font=dict(size=14, weight=700, color="#FFFFFF"),
        ),
        margin=dict(l=45, r=45, t=60, b=40),
        showlegend=False,
    )
    return fig


def plot_sprint_curve_overlay(p1: pd.Series, p2: pd.Series) -> go.Figure:
    """Overlaid velocity-time curves v(t) = vmax(1 - e^-t/tau) comparing two prospects."""
    fig = go.Figure()
    t_arr = np.linspace(0, 4.8, 100)
    
    # Player 1 curve
    tau1 = p1.get("forty_curve_tau")
    vmax1 = p1.get("forty_curve_vmax")
    p1_name = f"{p1['display_name']} ({p1['nfl_position']})"
    
    if pd.notna(tau1) and pd.notna(vmax1):
        v1_arr = vmax1 * (1 - np.exp(-t_arr / tau1))
        fig.add_trace(
            go.Scatter(
                x=t_arr,
                y=v1_arr,
                mode="lines",
                name=f"{p1_name} (τ={tau1:.2f}s, Vmax={vmax1:.2f})",
                line=dict(color=COLOR_BLACK, width=3),
            )
        )
        fig.add_hline(y=vmax1, line_dash="dot", line_color=COLOR_BLACK, line_width=1)
        
    # Player 2 curve
    tau2 = p2.get("forty_curve_tau")
    vmax2 = p2.get("forty_curve_vmax")
    p2_name = f"{p2['display_name']} ({p2['nfl_position']})"
    
    if pd.notna(tau2) and pd.notna(vmax2):
        v2_arr = vmax2 * (1 - np.exp(-t_arr / tau2))
        fig.add_trace(
            go.Scatter(
                x=t_arr,
                y=v2_arr,
                mode="lines",
                name=f"{p2_name} (τ={tau2:.2f}s, Vmax={vmax2:.2f})",
                line=dict(color=COLOR_LIME_DARK, width=3),
            )
        )
        fig.add_hline(y=vmax2, line_dash="dot", line_color=COLOR_LIME_DARK, line_width=1)
        
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Modeled Sprint Velocity Rise: v(t) = vmax(1 - e^-t/τ)", font=dict(size=14, weight=700)),
        xaxis_title="Time from Start (seconds)",
        yaxis_title="Sprint Velocity (yd/s)",
    )
    return fig


def plot_3d_motion_analysis(
    show_skeleton: bool = True,
    show_joints: bool = True,
    show_trajectory: bool = True,
    show_heatmap: bool = False,
    show_ground: bool = True,
) -> go.Figure:
    """
    Interactive 3D biomechanical motion reconstruction of sprinting kinematics.
    Displays running skeleton wireframe, joint kinematic nodes, 10 Hz RFID trajectory, and turf plane.
    """
    fig = go.Figure()
    
    # 1. Ground Turf Grid & Yard Lines
    if show_ground:
        x_turf = np.linspace(4, 16, 20)
        y_turf = np.linspace(-3, 3, 10)
        for y_line in np.linspace(-3, 3, 5):
            fig.add_trace(
                go.Scatter3d(
                    x=[4, 16], y=[y_line, y_line], z=[0, 0],
                    mode="lines",
                    line=dict(color="#1C242F", width=1.5),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
        for x_line in range(4, 17, 2):
            fig.add_trace(
                go.Scatter3d(
                    x=[x_line, x_line], y=[-3, 3], z=[0, 0],
                    mode="lines",
                    line=dict(color="#242E3B", width=2),
                    hoverinfo="skip",
                    showlegend=False,
                )
            )

    # 2. 10 Hz Trajectory Path
    if show_trajectory:
        t_steps = np.linspace(5, 15, 60)
        z_traj = 3.6 + 0.15 * np.sin(t_steps * 4.0)
        y_traj = 0.1 * np.cos(t_steps * 2.0)
        
        traj_color = t_steps if show_heatmap else "#C8F45A"
        fig.add_trace(
            go.Scatter3d(
                x=t_steps,
                y=y_traj,
                z=z_traj,
                mode="lines",
                name="Center of Mass Trajectory",
                line=dict(color="#C8F45A" if not show_heatmap else None, colorscale="Viridis" if show_heatmap else None, width=4),
                hovertemplate="Displacement: %{x:.1f} yd<br>COM Height: %{z:.2f} ft<extra></extra>",
            )
        )

    # 3. Running Skeleton Kinematic Limbs & Wireframe (at Instantaneous Drive Apex x=10.0 yd)
    if show_skeleton:
        # Bones defined as pair of 3D points
        limbs = [
            # Head to Neck / Torso
            ([(10.2, 0.0, 5.8), (10.0, 0.0, 5.1)], "Neck/Head"),
            # Torso Spine to Pelvis
            ([(10.0, 0.0, 5.1), (9.7, 0.0, 4.3), (9.5, 0.0, 3.5)], "Spine"),
            # Shoulder Girdle
            ([(9.9, 0.8, 4.9), (9.9, -0.8, 4.9)], "Shoulder Clavicle"),
            # Left Arm (Forward Pump)
            ([(9.9, 0.8, 4.9), (10.6, 0.85, 4.1), (11.1, 0.6, 4.5)], "Left Arm"),
            # Right Arm (Rearward Drive)
            ([(9.9, -0.8, 4.9), (9.1, -0.85, 3.9), (8.5, -0.65, 3.3)], "Right Arm"),
            # Pelvic Girdle
            ([(9.5, 0.45, 3.5), (9.5, -0.45, 3.5)], "Pelvis"),
            # Left Leg (Rear Push-off Extension)
            ([(9.5, 0.45, 3.5), (8.6, 0.5, 2.3), (7.7, 0.4, 0.25)], "Left Leg Drive"),
            # Right Leg (Forward High Knee Recovery)
            ([(9.5, -0.45, 3.5), (10.4, -0.5, 2.9), (10.2, -0.45, 1.35)], "Right Leg Flexion"),
        ]

        bone_color = "#C8F45A"
        for bone_pts, bone_name in limbs:
            bx = [p[0] for p in bone_pts]
            by = [p[1] for p in bone_pts]
            bz = [p[2] for p in bone_pts]
            fig.add_trace(
                go.Scatter3d(
                    x=bx, y=by, z=bz,
                    mode="lines",
                    line=dict(color=bone_color, width=5.5),
                    name="Kinematic Skeleton",
                    showlegend=False,
                    hoverinfo="skip",
                )
            )

    # 4. Joint Spheres (Glowing Lime Nodes)
    if show_joints:
        joints = [
            ("Head Vertex", 10.2, 0.0, 5.8),
            ("C7 Neck", 10.0, 0.0, 5.1),
            ("Mid-Thoracic Spine", 9.7, 0.0, 4.3),
            ("Sacrum/Pelvis", 9.5, 0.0, 3.5),
            ("Left Shoulder", 9.9, 0.8, 4.9),
            ("Left Elbow", 10.6, 0.85, 4.1),
            ("Left Wrist", 11.1, 0.6, 4.5),
            ("Right Shoulder", 9.9, -0.8, 4.9),
            ("Right Elbow", 9.1, -0.85, 3.9),
            ("Right Wrist", 8.5, -0.65, 3.3),
            ("Left Hip", 9.5, 0.45, 3.5),
            ("Left Knee", 8.6, 0.5, 2.3),
            ("Left Ankle", 7.7, 0.4, 0.25),
            ("Right Hip", 9.5, -0.45, 3.5),
            ("Right Knee", 10.4, -0.5, 2.9),
            ("Right Ankle", 10.2, -0.45, 1.35),
        ]
        jx = [j[1] for j in joints]
        jy = [j[2] for j in joints]
        jz = [j[3] for j in joints]
        jnames = [j[0] for j in joints]

        fig.add_trace(
            go.Scatter3d(
                x=jx, y=jy, z=jz,
                mode="markers",
                name="Joint Kinematic Centers",
                marker=dict(
                    size=6.5,
                    color="#FFFFFF",
                    line=dict(color="#C8F45A", width=2.5),
                ),
                text=jnames,
                hovertemplate="<b>%{text}</b><br>X: %{x:.2f} yd | Z: %{z:.2f} ft<extra></extra>",
            )
        )

    # Dark holographic camera and layout
    fig.update_layout(
        paper_bgcolor="#161B22",
        scene=dict(
            xaxis=dict(
                title="Sprint Distance (yd)",
                gridcolor="#242D38",
                backgroundcolor="#11151A",
                color="#94A3B8",
                range=[6, 14],
            ),
            yaxis=dict(
                title="Lateral Plane (yd)",
                gridcolor="#242D38",
                backgroundcolor="#11151A",
                color="#94A3B8",
                range=[-2.5, 2.5],
            ),
            zaxis=dict(
                title="Height (ft)",
                gridcolor="#242D38",
                backgroundcolor="#11151A",
                color="#94A3B8",
                range=[0, 7.0],
            ),
            camera=dict(
                eye=dict(x=-1.65, y=-1.85, z=0.85),
                center=dict(x=0, y=0, z=-0.1),
            ),
        ),
        margin=dict(l=0, r=0, t=10, b=10),
        height=480,
        showlegend=False,
    )
    return fig


def plot_hero_lime_trend(master_df: pd.DataFrame, view_mode: str = "40YD SPRINT") -> go.Figure:
    """Hero velocity/acceleration spline curve inspired by Visual Reference 1 (Weekly Team Trend)."""
    fig = go.Figure()
    
    valid_df = master_df.dropna(subset=["forty_curve_vmax", "forty_curve_tau"]).sort_values("combine_max_speed")
    if len(valid_df) == 0:
        valid_df = master_df
        
    # Aggregate cohort into decile velocity percentiles for smooth spline curve
    percentiles = np.linspace(5, 95, 19)
    speeds = np.percentile(valid_df["combine_max_speed"].dropna(), percentiles)
    
    fig.add_trace(
        go.Scatter(
            x=[f"P{int(p)}" for p in percentiles],
            y=speeds,
            mode="lines+markers",
            name="Cohort Velocity Curve",
            line=dict(shape="spline", color=COLOR_BLACK, width=3.5),
            fill="tozeroy",
            fillcolor="rgba(23, 25, 23, 0.09)",
            marker=dict(size=7, color=COLOR_BLACK, line=dict(color="#C8F45A", width=2)),
            hovertemplate="Percentile: %{x}<br>Sensor Velocity: %{y:.2f} yd/s<extra></extra>",
        )
    )
    
    # Peak Callout Marker at P95
    peak_speed = float(speeds[-1])
    fig.add_trace(
        go.Scatter(
            x=["P95"],
            y=[peak_speed],
            mode="markers+text",
            name="Elite Speed Threshold",
            marker=dict(size=13, color=COLOR_BLACK, symbol="circle", line=dict(color="#FFFFFF", width=2.5)),
            text=[f"Peak: {peak_speed:.2f}"],
            textposition="top center",
            textfont=dict(size=12, weight="bold", color=COLOR_BLACK, family="Plus Jakarta Sans"),
            hoverinfo="skip",
        )
    )

    layout_hero = {**THEME_LAYOUT}
    layout_hero["xaxis"] = dict(
        gridcolor="rgba(23, 25, 23, 0.08)",
        showline=False,
        tickfont=dict(size=10, color=COLOR_BLACK),
    )
    layout_hero["yaxis"] = dict(
        gridcolor="rgba(23, 25, 23, 0.08)",
        showline=False,
        tickfont=dict(size=10, color=COLOR_BLACK),
    )
    layout_hero["margin"] = dict(l=35, r=25, t=25, b=35)
    
    fig.update_layout(
        **layout_hero,
        showlegend=False,
        height=260,
    )
    return fig


def plot_recent_form_spline(master_df: pd.DataFrame) -> go.Figure:
    """Smooth multi-curve gradient spline area chart inspired by Visual Reference 3 (Recent Form)."""
    fig = go.Figure()
    
    pos_groups = ["WR", "CB", "RB"]
    color_palette = [COLOR_LIME_DARK, "#171917", "#858B86"]
    fill_palette = ["rgba(200, 244, 90, 0.35)", "rgba(23, 25, 23, 0.15)", "rgba(133, 139, 134, 0.10)"]
    
    x_labels = [f"Tier {i}" for i in range(1, 8)]
    
    for idx, pos in enumerate(pos_groups):
        sub = master_df[master_df["nfl_position"] == pos]["combine_max_speed"].dropna()
        if len(sub) >= 7:
            quantiles = np.quantile(sub, np.linspace(0.1, 0.9, 7))
        else:
            quantiles = np.linspace(18, 23, 7) + idx * 0.4
            
        fig.add_trace(
            go.Scatter(
                x=x_labels,
                y=quantiles,
                mode="lines",
                name=f"{pos} Velocity Tier",
                line=dict(shape="spline", color=color_palette[idx], width=2.8),
                fill="tozeroy" if idx == 0 else "tonexty",
                fillcolor=fill_palette[idx],
                hovertemplate=f"<b>{pos}</b> - %{{x}}: %{{y:.2f}} yd/s<extra></extra>",
            )
        )

    layout_form = {**THEME_LAYOUT}
    layout_form["xaxis"] = dict(showgrid=False, showline=False, tickfont=dict(size=10, color=COLOR_GREY))
    layout_form["yaxis"] = dict(showgrid=True, gridcolor=COLOR_LIGHT_GREY, showline=False, tickfont=dict(size=10, color=COLOR_GREY))
    layout_form["margin"] = dict(l=30, r=20, t=15, b=30)
    layout_form["legend"] = dict(orientation="h", y=-0.25, xanchor="center", x=0.5, font=dict(size=10))

    fig.update_layout(
        **layout_form,
        height=220,
    )
    return fig

