"""
ATHLETIX AI — Dashboard View 1: Analytics Overview
Executive analytics overview with minimalist light-grey background,
white rounded cards, lime accents (#C8F45A), and deep black typography (#171917).
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import (
    load_master_df,
    load_game_tracking_df,
    load_nested_cv_metrics,
    load_player_play_df,
    load_kinematics_df,
    load_dataset_inventory,
)
from src.dashboard.components import (
    render_editorial_header,
    render_kpi_card_v2,
    render_scientific_banner,
)


def render_page():
    render_editorial_header(
        title="Executive Analytics Overview",
        subtitle="Bridging NFL Combine RFID tracking with Next Gen Stats regular-season player performance.",
        tag="NFL BIG DATA BOWL 2027",
    )
    
    # Load verified datasets
    master_df = load_master_df()
    game_df = load_game_tracking_df()
    kinematics_df = load_kinematics_df()
    play_df = load_player_play_df()
    nested_df = load_nested_cv_metrics()
    
    # Calculate exact verified counts
    total_combine_prospects = len(master_df)                                       # 510 Combine attendees
    tracking_matched = len(game_df)                                                # 156 players with 2023 game tracking
    primary_cohort = len(master_df[master_df["is_eligible_50_snaps"] == True])     # 149 eligible primary cohort (>= 50 snaps)
    route_subcohort = play_df[play_df["separation_at_pass_forward"].notna()]["nfl_id"].nunique() # 51 route-separation skill sub-cohort
    total_drill_trials = len(kinematics_df)                                        # 6,310 total Combine drill trials
    regular_season_frames = "3.66M"                                                # 3,663,222 tracking frames at 10 Hz
    
    # Hero Feature Card (Dark with Lime Highlight)
    st.markdown(
        f"""
        <div class="athletix-card-dark">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 15px;">
                <div style="max-width: 750px;">
                    <div style="font-size: 0.78rem; font-weight: 700; color: #C8F45A; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                        CORE RESEARCH QUESTION
                    </div>
                    <div style="font-size: 1.55rem; font-weight: 800; letter-spacing: -0.02em; line-height: 1.3; color: #FFFFFF; margin-bottom: 12px;">
                        Can advanced movement analytics identify NFL prospects whose athletic performance is not fully described by traditional Combine measurements?
                    </div>
                    <div style="color: #A3A8A4; font-size: 0.92rem; line-height: 1.6;">
                        By integrating 10 Hz RFID Combine sensor tracking with regular-season Next Gen Stats, ATHLETIX AI evaluates 
                        continuous sprint velocity curves, change-of-direction apex deceleration, and the unconfounded 
                        <strong>Athletic Alpha</strong> residual across the 2023 rookie class.
                    </div>
                </div>
                <div style="background: rgba(200, 244, 90, 0.12); border: 1px solid rgba(200, 244, 90, 0.3); border-radius: 16px; padding: 1.2rem 1.4rem; min-width: 240px;">
                    <div style="font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #C8F45A; margin-bottom: 4px;">
                        PRIMARY FINDING
                    </div>
                    <div style="font-size: 1.6rem; font-weight: 800; color: #FFFFFF;">
                        R² = 0.9381
                    </div>
                    <div style="font-size: 0.78rem; color: #E5E7E5; margin-top: 4px;">
                        Traditional Combine baseline explains 93.8% of top game speed variance.
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # 6 Verified KPI Cards
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.markdown(render_kpi_card_v2("Combine Attendees", f"{total_combine_prospects}", "Invited Prospects"), unsafe_allow_html=True)
    with col2:
        st.markdown(render_kpi_card_v2("2023 Game Tracked", f"{tracking_matched}", "Rostered in Tracking", highlight_lime=True), unsafe_allow_html=True)
    with col3:
        st.markdown(render_kpi_card_v2("Primary Cohort", f"{primary_cohort}", "≥50 Scrimmage Snaps", highlight_lime=True), unsafe_allow_html=True)
    with col4:
        st.markdown(render_kpi_card_v2("Route Separation", f"{route_subcohort}", "Tracked Skill Players"), unsafe_allow_html=True)
    with col5:
        st.markdown(render_kpi_card_v2("Drill Trials", f"{total_drill_trials:,}", "10 Hz Combine Sensor"), unsafe_allow_html=True)
    with col6:
        st.markdown(render_kpi_card_v2("Tracking Volume", f"{regular_season_frames}", "10 Hz Game Frames"), unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Scientific Banner
    render_scientific_banner(
        "Important Empirical Finding",
        "Empirical nested cross-validation demonstrates that the Traditional Combine baseline (Model A, R² = 0.9381) "
        "statistically outperforms the current Hybrid model (Model C, R² = 0.9311; p = 0.0069) for predicting global in-game straight-line speed. "
        "Sensor features do not replace stopwatches for straight-line speed, but provide qualitative diagnostic insight into Change-of-Direction mechanics and Athletic Alpha."
    )
    
    # Two-Column Layout: Core Conclusions & Model Summary Table
    left_col, right_col = st.columns([3, 2])
    
    with left_col:
        st.markdown(
            """
            <div class="athletix-card">
                <h3 style="font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 1rem;">
                    Key Research Conclusions
                </h3>
                <div style="font-size: 0.9rem; line-height: 1.65; color: #171917;">
                    <p><strong>1. Stopwatches Are Exceptional Speed Proxies:</strong> Standard Combine drills (40-yard dash, 10-yard split, vertical jump) explain 93.8% of the variance in regular-season 95th percentile tracking speed.</p>
                    <p><strong>2. The Multicollinearity Penalty:</strong> Adding 11 collinear sensor velocity metrics (VIF &gt; 10) inflates estimation variance on small samples (N = 149), increasing out-of-fold generalization error (ΔRMSE = +0.021 yd/s, p = 0.0069).</p>
                    <p><strong>3. Athletic Alpha Isolates Translation:</strong> Residual decomposition (Actual P95 Speed minus Traditional Model Prediction) reveals an unconfounded metric that is orthogonal to draft capital, snap counts, and position groups.</p>
                    <p><strong>4. Change-of-Direction Diagnostics:</strong> In offensive skill players (N = 51), kinematic speed preservation ratio during cuts exhibits an exploratory correlation with positive Athletic Alpha (q ≈ 0.14), highlighting the role of apex deceleration mechanics.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
    with right_col:
        st.markdown(
            """
            <div class="athletix-card">
                <h3 style="font-size: 1.25rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 1rem;">
                    Model Performance Summary
                </h3>
            """,
            unsafe_allow_html=True,
        )
        if not nested_df.empty:
            st.dataframe(
                nested_df.rename(
                    columns={
                        "model": "Architecture",
                        "oof_r2": "Tuned R²",
                        "oof_rmse": "RMSE",
                        "oof_mae": "MAE",
                        "spearman": "Rank ρ",
                    }
                ).style.format({
                    "Tuned R²": "{:.4f}",
                    "RMSE": "{:.4f}",
                    "MAE": "{:.4f}",
                    "Rank ρ": "{:.4f}",
                }),
                use_container_width=True,
                hide_index=True,
            )
            st.caption("Nested 5-Fold Cross-Validation with Inner Ridge α Grid Search.")
        st.markdown('</div>', unsafe_allow_html=True)
