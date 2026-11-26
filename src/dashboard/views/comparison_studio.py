"""
ATHLETIX AI — Dashboard Page: Player Comparison Studio (Signature Feature)
Head-to-head two-player biomechanical & performance matchup studio.
"""

import streamlit as st
import pandas as pd
import numpy as np
from src.dashboard.data_loader import load_master_df, load_athletic_alpha
from src.dashboard.charts import plot_radar_comparison, plot_sprint_curve_overlay
from src.dashboard.components import render_editorial_header, render_scientific_banner
from src.dashboard.metrics import fmt_speed, fmt_accel, fmt_time, fmt_ratio, fmt_dist_in, fmt_weight_lbs


def render_page():
    render_editorial_header(
        title="Player Comparison Studio",
        subtitle="Multi-dimensional head-to-head athletic and kinematic evaluation across verified Combine & NFL game metrics.",
        tag="SIGNATURE FEATURE",
    )
    
    master_df = load_master_df()
    alpha_df = load_athletic_alpha()
    
    if master_df.empty:
        st.error("Player master dataset could not be loaded.")
        return
        
    df = master_df.copy()
    if not alpha_df.empty:
        alpha_sub = alpha_df[["nfl_id", "athletic_alpha_raw", "athletic_alpha_zscore", "athletic_alpha_tier"]]
        df = df.merge(alpha_sub, on="nfl_id", how="left")
        
    # Prospect Selector Bar
    st.markdown('<div class="athletix-card" style="padding: 1.2rem 1.6rem;">', unsafe_allow_html=True)
    sel_col1, sel_col2 = st.columns(2)
    
    # Format player labels
    df["selector_label"] = (
        df["display_name"] + " (" + 
        df["nfl_position"].fillna("?") + " • " + 
        df["college_name"].fillna("N/A") + ")"
    )
    all_player_labels = df.sort_values(by="display_name")["selector_label"].tolist()
    
    # Defaults: Zay Flowers vs. Quentin Johnston (or Cam Smith vs. another prospect)
    default_p1_idx = 0
    default_p2_idx = min(1, len(all_player_labels) - 1)
    
    for i, lbl in enumerate(all_player_labels):
        if "Flowers" in lbl:
            default_p1_idx = i
        if "Johnston" in lbl:
            default_p2_idx = i
            
    with sel_col1:
        p1_label = st.selectbox("Select Athlete 1 (Baseline)", all_player_labels, index=default_p1_idx)
    with sel_col2:
        p2_label = st.selectbox("Select Athlete 2 (Challenger)", all_player_labels, index=default_p2_idx)
    st.markdown('</div>', unsafe_allow_html=True)
    
    p1 = df[df["selector_label"] == p1_label].iloc[0]
    p2 = df[df["selector_label"] == p2_label].iloc[0]
    
    # Side-by-Side Athlete Header Cards
    h_col1, h_col2 = st.columns(2)
    
    with h_col1:
        pick1 = f"Round {int(p1['draft_round'])}, Pick #{int(p1['draft_overall_pick'])}" if pd.notna(p1['draft_round']) else "Undrafted Free Agent"
        alpha1_str = f"{p1['athletic_alpha_raw']:+.2f} yd/s" if pd.notna(p1.get('athletic_alpha_raw')) else "N/A"
        st.markdown(
            f"""
            <div class="athletix-card-dark">
                <div style="font-size: 0.76rem; font-weight: 700; color: #C8F45A; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                    ATHLETE 1 • {p1['nfl_position']}
                </div>
                <div style="font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 4px;">
                    {p1['display_name']}
                </div>
                <div style="color: #A3A8A4; font-size: 0.9rem; margin-bottom: 12px;">
                    {p1['college_name']} • {pick1}
                </div>
                <div style="display: flex; gap: 12px; margin-top: 10px;">
                    <span class="pill-badge pill-badge-lime">40yd: {fmt_time(p1['forty'])}</span>
                    <span class="pill-badge pill-badge-dark" style="background:#282B28;">Alpha: {alpha1_str}</span>
                    <span class="pill-badge pill-badge-dark" style="background:#282B28;">{fmt_weight_lbs(p1['combine_weight'])}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with h_col2:
        pick2 = f"Round {int(p2['draft_round'])}, Pick #{int(p2['draft_overall_pick'])}" if pd.notna(p2['draft_round']) else "Undrafted Free Agent"
        alpha2_str = f"{p2['athletic_alpha_raw']:+.2f} yd/s" if pd.notna(p2.get('athletic_alpha_raw')) else "N/A"
        st.markdown(
            f"""
            <div class="athletix-card-lime">
                <div style="font-size: 0.76rem; font-weight: 700; color: #171917; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                    ATHLETE 2 • {p2['nfl_position']}
                </div>
                <div style="font-size: 1.85rem; font-weight: 800; letter-spacing: -0.03em; margin-bottom: 4px; color: #171917;">
                    {p2['display_name']}
                </div>
                <div style="color: #4A5248; font-size: 0.9rem; margin-bottom: 12px;">
                    {p2['college_name']} • {pick2}
                </div>
                <div style="display: flex; gap: 12px; margin-top: 10px;">
                    <span class="pill-badge pill-badge-dark">40yd: {fmt_time(p2['forty'])}</span>
                    <span class="pill-badge" style="background:#FFFFFF; color:#171917;">Alpha: {alpha2_str}</span>
                    <span class="pill-badge" style="background:#FFFFFF; color:#171917;">{fmt_weight_lbs(p2['combine_weight'])}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Visual Comparison Studio: Radar Chart & Sprint Curves
    r_col1, r_col2 = st.columns([1, 1])
    with r_col1:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_radar_comparison(p1, p2, df), use_container_width=True)
        st.caption("ℹ️ *Percentile normalization: Standardized percentile rank [0, 100] calculated across all 510 Combine prospects. For 10-yard split, lower stopwatch times yield higher burst percentiles.*")
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r_col2:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_sprint_curve_overlay(p1, p2), use_container_width=True)
        st.caption("ℹ️ *Sprint Rise Dynamics: Modeled continuous velocity profiles v(t) = vmax(1 - e^-t/τ) fitted via non-linear least squares. Dotted horizontal lines indicate asymptotic model velocity ceilings.*")
        st.markdown('</div>', unsafe_allow_html=True)

    # Detailed Side-by-Side Metric Table with Difference Badges
    st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
    st.markdown("### 📊 Head-to-Head Metric Dissection & Delta Analysis")
    
    comparison_metrics = [
        # (Label, Column, FormatFunc, LowerIsBetter, Unit)
        ("40-Yard Dash", "forty", fmt_time, True, "s"),
        ("10-Yard Split", "ten_yd_split", fmt_time, True, "s"),
        ("Vertical Jump", "vertical", fmt_dist_in, False, 'in'),
        ("Broad Jump", "broad_jump", fmt_dist_in, False, 'in'),
        ("3-Cone Drill", "three_cone", fmt_time, True, "s"),
        ("20-Yard Shuttle", "short_shuttle", fmt_time, True, "s"),
        ("Combine Max Speed", "combine_max_speed", fmt_speed, False, "yd/s"),
        ("Initial Acceleration (First 0.5s)", "combine_initial_accel_mean", fmt_accel, False, "yd/s²"),
        ("Sprint Time Constant (τ)", "forty_curve_tau", fmt_time, True, "s"),
        ("Asymptotic Velocity (Vmax)", "forty_curve_vmax", fmt_speed, False, "yd/s"),
        ("COD Apex Speed", "combine_mean_cod_apex_speed", fmt_speed, False, "yd/s"),
        ("Speed Preservation Ratio", "combine_mean_speed_preservation_ratio", fmt_ratio, False, "ratio"),
        ("Peak Angular Velocity", "combine_peak_angular_velocity", lambda x: f"{x:.1f}°/s" if pd.notna(x) else "N/A", False, "deg/s"),
        ("NFL Game P95 Speed", "game_speed_p95", fmt_speed, False, "yd/s"),
        ("Athletic Alpha (Residual)", "athletic_alpha_raw", lambda x: f"{x:+.2f} yd/s" if pd.notna(x) else "N/A", False, "yd/s"),
    ]
    
    rows = []
    for label, col, fmt_func, lower_is_better, unit in comparison_metrics:
        v1 = p1.get(col)
        v2 = p2.get(col)
        
        # Calculate delta
        delta_str = "—"
        advantage = "Tied / Neutral"
        if pd.notna(v1) and pd.notna(v2):
            diff = v2 - v1
            if diff != 0:
                delta_str = f"{diff:+.2f} {unit}"
                if lower_is_better:
                    advantage = f"{p2['display_name']} Faster" if diff < 0 else f"{p1['display_name']} Faster"
                else:
                    advantage = f"{p2['display_name']} Superior" if diff > 0 else f"{p1['display_name']} Superior"
                    
        rows.append({
            "Biomechanical Dimension": label,
            f"{p1['display_name']} (Athlete 1)": fmt_func(v1),
            f"{p2['display_name']} (Athlete 2)": fmt_func(v2),
            "Delta (A2 - A1)": delta_str,
            "Advantage": advantage,
        })
        
    comp_df = pd.DataFrame(rows)
    st.dataframe(comp_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    render_scientific_banner(
        "Scientific & Normalization Methodology",
        "1. All comparative data points are loaded strictly from verified Combine sensor feeds and official competition files. "
        "Missing test results indicate drills the athlete did not attempt at the Combine; under no circumstances are missing values estimated or fabricated. "
        "2. Delta indicators (Athlete 2 minus Athlete 1) reflect pure observed physical differences. "
        "3. Athletic Alpha is model-relative and quantifies in-game translation relative to traditional Combine projections."
    )
