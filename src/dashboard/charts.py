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

# Design System Palette
COLOR_LIME = "#C8F45A"         # Primary Electric Lime
COLOR_LIME_DARK = "#8CCB42"    # Secondary Forest Lime
COLOR_BLACK = "#171917"        # Primary Deep Black
COLOR_GREY = "#858B86"         # Secondary Slate Grey
COLOR_LIGHT_GREY = "#E5E7E5"   # Subtle Grid Line
COLOR_WHITE = "#FFFFFF"        # White Container
COLOR_CRIMSON = "#E53E3E"      # Red Alert

THEME_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans, Inter, sans-serif", color=COLOR_BLACK, size=12),
    margin=dict(l=45, r=30, t=50, b=45),
    xaxis=dict(
        gridcolor=COLOR_LIGHT_GREY,
        zerolinecolor=COLOR_LIGHT_GREY,
        showline=True,
        linecolor=COLOR_LIGHT_GREY,
        tickfont=dict(size=11, color=COLOR_GREY),
    ),
    yaxis=dict(
        gridcolor=COLOR_LIGHT_GREY,
        zerolinecolor=COLOR_LIGHT_GREY,
        showline=True,
        linecolor=COLOR_LIGHT_GREY,
        tickfont=dict(size=11, color=COLOR_GREY),
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1,
        font=dict(size=11),
    ),
    hoverlabel=dict(
        bgcolor=COLOR_BLACK,
        font_size=12,
        font_family="Plus Jakarta Sans, sans-serif",
        font_color=COLOR_WHITE,
    ),
)


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
    
    colors = [COLOR_LIGHT_GREY, COLOR_GREY, COLOR_LIME_DARK, COLOR_LIME]
    fig = go.Figure(
        go.Bar(
            x=counts.index,
            y=counts.values,
            marker_color=colors,
            marker_line=dict(color=COLOR_BLACK, width=1.5),
            text=counts.values,
            textposition="auto",
            textfont=dict(family="Plus Jakarta Sans", weight="bold", color=COLOR_BLACK),
        )
    )
    fig.update_layout(
        **THEME_LAYOUT,
        title=dict(text="Sprint Velocity Curve Fit Quality (418 Evaluated Prospects)", font=dict(size=14, weight=700)),
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
        ("Speed (Combine Max)", "combine_max_speed", True),
        ("Explosion (Vertical)", "vertical", True),
        ("Burst (10yd Split)", "ten_yd_split", False),     # lower is better
        ("COD Preservation", "combine_mean_speed_preservation_ratio", True),
        ("Angular Velocity", "combine_peak_angular_velocity", True),
        ("In-Game P95 Speed", "game_speed_p95", True),
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
    
    p1_name = f"{p1['display_name']} ({p1['nfl_position']})"
    p2_name = f"{p2['display_name']} ({p2['nfl_position']})"
    
    fig = go.Figure()
    
    fig.add_trace(
        go.Scatterpolar(
            r=p1_closed,
            theta=categories_closed,
            fill='toself',
            name=p1_name,
            line=dict(color=COLOR_BLACK, width=2.5),
            fillcolor="rgba(23, 25, 23, 0.25)",
        )
    )
    
    fig.add_trace(
        go.Scatterpolar(
            r=p2_closed,
            theta=categories_closed,
            fill='toself',
            name=p2_name,
            line=dict(color=COLOR_LIME_DARK, width=2.5),
            fillcolor="rgba(200, 244, 90, 0.45)",
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10, color=COLOR_GREY),
                gridcolor=COLOR_LIGHT_GREY,
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=COLOR_BLACK, weight="bold"),
                gridcolor=COLOR_LIGHT_GREY,
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif"),
        title=dict(text="Relative Athletic Percentile Profile (0–100th %ile Cohort Rank)", font=dict(size=14, weight=700)),
        legend=dict(orientation="h", y=-0.15, xanchor="center", x=0.5),
        margin=dict(l=40, r=40, t=60, b=60),
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
        
        # Modeled Sprint Curve
        fig.add_trace(
            go.Scatter(
                x=t_arr,
                y=v_arr,
                mode="lines",
                name=f"Fitted Model: v(t)",
                line=dict(color=COLOR_BLACK, width=3.5),
                hovertemplate="Time: %{x:.2f} s<br>Velocity: %{y:.2f} yd/s<extra></extra>",
            )
        )
        
        # Asymptotic Ceiling Vmax
        fig.add_hline(
            y=vmax,
            line_dash="dot",
            line_color=COLOR_LIME_DARK,
            line_width=2,
            annotation_text=f"Asymptotic Ceiling Vmax = {vmax:.2f} yd/s",
            annotation_position="bottom right",
            annotation_font=dict(size=11, color=COLOR_BLACK, weight="bold"),
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
                    marker=dict(size=12, color=COLOR_LIME, line=dict(color=COLOR_BLACK, width=2)),
                    text=[f"10yd: {v_10:.1f} yd/s"],
                    textposition="top left",
                    textfont=dict(size=11, weight="bold", color=COLOR_BLACK),
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
                    marker=dict(size=12, color=COLOR_BLACK, line=dict(color=COLOR_LIME, width=2)),
                    text=[f"40yd: {v_40:.1f} yd/s"],
                    textposition="bottom right",
                    textfont=dict(size=11, weight="bold", color=COLOR_BLACK),
                    hovertemplate="40-Yard Finish: %{x:.2f} s<br>Velocity: %{y:.2f} yd/s<extra></extra>",
                )
            )

    # Observed Peak Speed
    if pd.notna(obs_vmax) and obs_vmax > 0:
        fig.add_hline(
            y=obs_vmax,
            line_dash="dash",
            line_color=COLOR_GREY,
            line_width=1.5,
            annotation_text=f"Observed Sensor Peak = {obs_vmax:.2f} yd/s",
            annotation_position="top left",
            annotation_font=dict(size=11, color=COLOR_GREY),
        )

    layout_args = {**THEME_LAYOUT}
    layout_args["legend"] = dict(orientation="h", y=-0.2, xanchor="center", x=0.5)
    fig.update_layout(
        **layout_args,
        title=dict(
            text=f"Sprint Velocity Dynamics: {p_name} ({p_pos})",
            font=dict(size=15, weight=700),
        ),
        xaxis_title="Elapsed Time from Sensor Start (seconds)",
        yaxis_title="Kinematic Velocity (yd/s)",
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
                name="Fitted Tangential Acceleration a(t)",
                line=dict(color=COLOR_BLACK, width=3.5),
                fill="tozeroy",
                fillcolor="rgba(200, 244, 90, 0.20)",
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
                marker=dict(size=11, color=COLOR_LIME_DARK, line=dict(color=COLOR_BLACK, width=2)),
                text=[f"a(0): {a_0:.1f} yd/s²"],
                textposition="top right",
                textfont=dict(size=11, weight="bold", color=COLOR_BLACK),
            )
        )

    # Observed Peak Acceleration
    if pd.notna(obs_max_accel) and obs_max_accel > 0:
        fig.add_hline(
            y=obs_max_accel,
            line_dash="dot",
            line_color=COLOR_LIME_DARK,
            line_width=2,
            annotation_text=f"Observed Sensor Max Accel = {obs_max_accel:.2f} yd/s²",
            annotation_position="bottom right",
            annotation_font=dict(size=11, color=COLOR_BLACK),
        )

    # Observed Initial Acceleration
    if pd.notna(obs_init_accel) and obs_init_accel > 0:
        fig.add_hline(
            y=obs_init_accel,
            line_dash="dash",
            line_color=COLOR_GREY,
            line_width=1.5,
            annotation_text=f"Observed 1st-Step Init Accel = {obs_init_accel:.2f} yd/s²",
            annotation_position="top right",
            annotation_font=dict(size=11, color=COLOR_GREY),
        )

    layout_args = {**THEME_LAYOUT}
    layout_args["legend"] = dict(orientation="h", y=-0.2, xanchor="center", x=0.5)
    fig.update_layout(
        **layout_args,
        title=dict(
            text=f"Tangential Acceleration Profile: {p_name} ({p_pos})",
            font=dict(size=15, weight=700),
        ),
        xaxis_title="Elapsed Time from Sensor Start (seconds)",
        yaxis_title="Tangential Acceleration (yd/s²)",
        showlegend=True,
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
        "20-Yard Shuttle (180° Cuts)": COLOR_BLACK,
        "3-Cone Drill (90° & 180° Cuts)": COLOR_LIME_DARK,
        "Position Skill Drills (Curved / Cut)": COLOR_GREY,
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
    fig.update_traces(marker=dict(size=6, line=dict(width=0.8, color=COLOR_BLACK)))
    
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
                        color=COLOR_LIME,
                        symbol="star",
                        line=dict(color=COLOR_BLACK, width=2),
                    ),
                    text=p_cod["drill_name"],
                    hovertemplate="<b>Selected Prospect</b><br>Drill: %{text}<br>Apex Speed: %{x:.2f} yd/s<br>Speed Preservation: %{y:.3f}<extra></extra>",
                )
            )

    layout_cod = {**THEME_LAYOUT}
    layout_cod["legend"] = dict(orientation="h", y=-0.2, xanchor="center", x=0.5)
    fig.update_layout(
        **layout_cod,
        title=dict(text="Change-of-Direction Dynamics: Apex Velocity vs. Speed Preservation Ratio", font=dict(size=14, weight=700)),
        xaxis_title="Turn Apex Velocity (yd/s)",
        yaxis_title="Kinematic Speed Preservation Ratio (vexit / ventry)",
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
            line=dict(color=COLOR_BLACK, width=2.5),
            fillcolor="rgba(200, 244, 90, 0.45)",
            marker=dict(size=7, color=COLOR_LIME_DARK, line=dict(color=COLOR_BLACK, width=1.5)),
            hovertemplate="<b>%{theta}</b>: %{r:.1f}th Percentile<extra></extra>",
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=9, color=COLOR_GREY),
                gridcolor=COLOR_LIGHT_GREY,
            ),
            angularaxis=dict(
                tickfont=dict(size=11, color=COLOR_BLACK, weight="bold"),
                gridcolor=COLOR_LIGHT_GREY,
            ),
            bgcolor="rgba(0,0,0,0)",
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Plus Jakarta Sans, sans-serif"),
        title=dict(
            text=f"Biomechanical Attribute Profile: {p_name} (vs. {comp_label})",
            font=dict(size=14, weight=700),
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
