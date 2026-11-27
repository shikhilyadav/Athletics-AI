"""
ATHLETIX AI — Dashboard View 1: Research Overview
Exact implementation of the visual reference image:
- Hero Banner: "Beyond the Combine. Understand the Athlete." with neon lime italics
- 6-Grid KPI Metrics Bar (with '156 In-Game Tracked' highlighted in green)
- Middle Analytical Row: Cohort Performance Trend (spline chart), Model Architecture Comparison (with Traditional A highlighted), Key Research Findings checklist
- Bottom Row: 3 Feature Navigation Cards (Biomechanical Lab, Player Comparison Studio, Model Performance) with sports graphics and circular arrows
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import (
    load_master_df,
    load_game_tracking_df,
    load_nested_cv_metrics,
    load_player_play_df,
    load_kinematics_df,
)
from src.dashboard.components import (
    render_editorial_header,
    render_scientific_banner,
)
from src.dashboard.charts import (
    plot_cohort_performance_trend,
)


def render_page():
    # Load verified datasets
    master_df = load_master_df()
    game_df = load_game_tracking_df()
    kinematics_df = load_kinematics_df()
    play_df = load_player_play_df()
    nested_df = load_nested_cv_metrics()
    
    # Calculate verified statistics
    total_combine_prospects = len(master_df)                                       # 510
    tracking_matched = len(game_df)                                                # 156
    primary_cohort = len(master_df[master_df["is_eligible_50_snaps"] == True])     # 149
    route_subcohort = play_df[play_df["separation_at_pass_forward"].notna()]["nfl_id"].nunique() # 51
    total_drill_trials = len(kinematics_df)                                        # 6,310
    regular_season_frames = "3.66M"                                                # 3.66M
    
    # =========================================================================
    # 1. HERO BANNER: "DECODING MOVEMENT. PREDICTING NFL IMPACT."
    # =========================================================================
    st.markdown(
        """
        <div style="margin-bottom: 2.2rem; position: relative; background: radial-gradient(circle at 65% 30%, rgba(200, 244, 90, 0.10) 0%, transparent 65%); padding: 0.5rem 0 0.8rem 0;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 24px;">
                <div style="max-width: 760px;">
                    <div style="font-size: 0.82rem; font-weight: 800; color: #C8F45A; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 8px;">
                        RESEARCH OVERVIEW //
                    </div>
                    <h1 style="font-size: 2.9rem; font-weight: 900; letter-spacing: -0.04em; line-height: 1.08; margin: 0 0 14px 0;">
                        <span style="font-style: italic; color: #FFFFFF;">DECODING MOVEMENT.</span><br>
                        <span style="font-style: italic; color: #C8F45A; text-shadow: 0 0 28px rgba(200, 244, 90, 0.35);">PREDICTING NFL IMPACT.</span>
                    </h1>
                    <p style="font-size: 1.02rem; color: #94A3B8; margin-top: 0; margin-bottom: 22px; line-height: 1.55; max-width: 620px;">
                        A research-driven platform that combines biomechanics, movement science, and AI to evaluate NFL athletic performance.
                    </p>
                    <div style="display: flex; gap: 14px; align-items: center;">
                        <div class="hero-cta-lime">Explore the Research ➔</div>
                        <div class="hero-cta-dark">Watch Demo ▶</div>
                    </div>
                </div>
                <div>
                    <div class="movement-intel-card">
                        <div class="movement-intel-title">Movement Intelligence</div>
                        <div class="movement-intel-item">
                            <div class="movement-intel-icon">🏃</div>
                            <div class="movement-intel-text">Sprint Mechanics</div>
                        </div>
                        <div class="movement-intel-item">
                            <div class="movement-intel-icon">⚙️</div>
                            <div class="movement-intel-text">Change of Direction</div>
                        </div>
                        <div class="movement-intel-item">
                            <div class="movement-intel-icon">⚡</div>
                            <div class="movement-intel-text">Acceleration / Deceleration</div>
                        </div>
                        <div class="movement-intel-item">
                            <div class="movement-intel-icon">🎯</div>
                            <div class="movement-intel-text">Movement Efficiency</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================================
    # 2. 6-GRID KPI METRICS ROW (Matching Reference Exactly)
    # =========================================================================
    st.markdown(
        f"""
        <div class="kpi-dark-grid">
            <div class="kpi-dark-card">
                <div class="kpi-dark-icon-wrap">👥</div>
                <div>
                    <div class="kpi-dark-num">{total_combine_prospects}</div>
                    <div class="kpi-dark-label">Combine Prospects</div>
                </div>
            </div>
            <div class="kpi-dark-card kpi-dark-card-active">
                <div class="kpi-dark-icon-wrap kpi-dark-icon-wrap-lime">🏃</div>
                <div>
                    <div class="kpi-dark-num" style="color: #C8F45A;">{tracking_matched}</div>
                    <div class="kpi-dark-label" style="color: #FFFFFF; font-weight: 700;">In-Game Tracked</div>
                </div>
            </div>
            <div class="kpi-dark-card">
                <div class="kpi-dark-icon-wrap">📚</div>
                <div>
                    <div class="kpi-dark-num">{primary_cohort}</div>
                    <div class="kpi-dark-label">Research Cohort</div>
                </div>
            </div>
            <div class="kpi-dark-card">
                <div class="kpi-dark-icon-wrap">🔬</div>
                <div>
                    <div class="kpi-dark-num">{route_subcohort}</div>
                    <div class="kpi-dark-label">Route Separation</div>
                </div>
            </div>
            <div class="kpi-dark-card">
                <div class="kpi-dark-icon-wrap">🏋️</div>
                <div>
                    <div class="kpi-dark-num">{total_drill_trials:,}</div>
                    <div class="kpi-dark-label">Drill Trials</div>
                </div>
            </div>
            <div class="kpi-dark-card">
                <div class="kpi-dark-icon-wrap">💾</div>
                <div>
                    <div class="kpi-dark-num">{regular_season_frames}</div>
                    <div class="kpi-dark-label">Tracking Frames</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =========================================================================
    # 3. MIDDLE ANALYTICAL ROW (3 Cards Across)
    # =========================================================================
    col_trend, col_model, col_findings = st.columns([10, 8, 7])
    
    with col_trend:
        # Card 1: Cohort Performance Trend
        st.markdown(
            """
            <div class="dark-card" style="min-height: 330px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span style="font-size: 1.1rem; color: #C8F45A;">📈</span>
                        <span style="font-size: 1.08rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                            Cohort Performance Trend
                        </span>
                    </div>
                    <div style="display: flex; background: #0B0E11; border: 1px solid #242D38; border-radius: 9999px; padding: 2px;">
                        <span style="background: #C8F45A; color: #0B0E11; font-size: 0.68rem; font-weight: 800; padding: 2px 10px; border-radius: 9999px;">R²</span>
                        <span style="color: #64748B; font-size: 0.68rem; font-weight: 700; padding: 2px 10px;">RMSE</span>
                    </div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.plotly_chart(plot_cohort_performance_trend(nested_df, "R²"), use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_model:
        # Card 2: Model Architecture Comparison Table (With Traditional Row Highlighted)
        st.markdown(
            """
            <div class="dark-card" style="min-height: 330px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 1.2rem;">
                    <span style="font-size: 1.1rem; color: #C8F45A;">📚</span>
                    <span style="font-size: 1.08rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                        Model Architecture Comparison
                    </span>
                </div>
                
                <table style="width: 100%; border-collapse: separate; border-spacing: 0 8px; font-size: 0.88rem;">
                    <thead>
                        <tr style="color: #8B949E; text-transform: uppercase; font-size: 0.72rem; letter-spacing: 0.06em;">
                            <th style="text-align: left; padding: 0 10px 8px 10px;">Model</th>
                            <th style="text-align: right; padding: 0 10px 8px 10px;">R² (OOF)</th>
                            <th style="text-align: right; padding: 0 10px 8px 10px;">RMSE (yd/s)</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="background: rgba(200, 244, 90, 0.18); border: 1px solid rgba(200, 244, 90, 0.4); color: #FFFFFF; font-weight: 700;">
                            <td style="padding: 10px; border-top-left-radius: 12px; border-bottom-left-radius: 12px; color: #C8F45A; font-weight: 800;">
                                Traditional (A)
                            </td>
                            <td style="text-align: right; padding: 10px; color: #C8F45A; font-weight: 800;">
                                0.9381
                            </td>
                            <td style="text-align: right; padding: 10px; border-top-right-radius: 12px; border-bottom-right-radius: 12px; color: #C8F45A; font-weight: 800;">
                                0.3843
                            </td>
                        </tr>
                        <tr style="color: #D1D5DB; background: rgba(255, 255, 255, 0.02);">
                            <td style="padding: 10px; border-top-left-radius: 12px; border-bottom-left-radius: 12px;">Sensor Only (B)</td>
                            <td style="text-align: right; padding: 10px;">0.9184</td>
                            <td style="text-align: right; padding: 10px; border-top-right-radius: 12px; border-bottom-right-radius: 12px;">0.4411</td>
                        </tr>
                        <tr style="color: #D1D5DB; background: rgba(255, 255, 255, 0.02);">
                            <td style="padding: 10px; border-top-left-radius: 12px; border-bottom-left-radius: 12px;">Hybrid (C)</td>
                            <td style="text-align: right; padding: 10px;">0.9311</td>
                            <td style="text-align: right; padding: 10px; border-top-right-radius: 12px; border-bottom-right-radius: 12px;">0.4053</td>
                        </tr>
                    </tbody>
                </table>
                <div style="font-size: 0.72rem; color: #64748B; margin-top: 14px; line-height: 1.4;">
                    Evaluated via repeated nested 5-fold cross-validation on the N=149 primary scrimmage cohort.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_findings:
        # Card 3: Key Research Findings Checklist
        st.markdown(
            """
            <div class="dark-card" style="min-height: 330px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 1.2rem;">
                    <span style="font-size: 1.1rem; color: #C8F45A;">🎯</span>
                    <span style="font-size: 1.08rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                        Key Research Findings
                    </span>
                </div>
                
                <div style="display: flex; flex-direction: column; gap: 14px; font-size: 0.88rem; color: #D1D5DB; line-height: 1.45;">
                    <div style="display: flex; align-items: flex-start; gap: 10px;">
                        <span style="width: 20px; height: 20px; border-radius: 50%; background: #C8F45A; color: #0B0E11; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 900; flex-shrink: 0; margin-top: 1px;">✓</span>
                        <span>Traditional combine testing remains a strong predictor.</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 10px;">
                        <span style="width: 20px; height: 20px; border-radius: 50%; background: #C8F45A; color: #0B0E11; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 900; flex-shrink: 0; margin-top: 1px;">✓</span>
                        <span>Movement features add complementary value.</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 10px;">
                        <span style="width: 20px; height: 20px; border-radius: 50%; background: #C8F45A; color: #0B0E11; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 900; flex-shrink: 0; margin-top: 1px;">✓</span>
                        <span>Athletic Alpha identifies over- and under-performers.</span>
                    </div>
                    <div style="display: flex; align-items: flex-start; gap: 10px;">
                        <span style="width: 20px; height: 20px; border-radius: 50%; background: #C8F45A; color: #0B0E11; display: flex; align-items: center; justify-content: center; font-size: 0.72rem; font-weight: 900; flex-shrink: 0; margin-top: 1px;">✓</span>
                        <span>Biomechanical metrics explain meaningful variance.</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # =========================================================================
    # 4. BOTTOM ROW: 3 FEATURE NAVIGATION CARDS (With Real Sports Imagery)
    # =========================================================================
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        st.markdown(
            """
            <div class="feature-hero-card" style="background-image: linear-gradient(180deg, rgba(22,27,34,0.65) 0%, rgba(11,14,17,0.92) 100%), url('https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?auto=format&fit=crop&w=700&q=80'); background-size: cover; background-position: center;">
                <div class="feature-card-content">
                    <div class="feature-card-icon-pill">🏃</div>
                    <div class="feature-card-title-row">
                        <span class="feature-card-title">Biomechanical Lab</span>
                        <span style="background: rgba(200,244,90,0.18); color: #C8F45A; border: 1px solid rgba(200,244,90,0.35); font-size: 0.68rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">Hero Experience</span>
                    </div>
                    <div class="feature-card-desc">
                        Explore sprint, COD, acceleration, and deceleration mechanics.
                    </div>
                </div>
                <div class="feature-card-arrow-btn">➔</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f_col2:
        st.markdown(
            """
            <div class="feature-hero-card" style="background-image: linear-gradient(180deg, rgba(22,27,34,0.65) 0%, rgba(11,14,17,0.92) 100%), url('https://images.unsplash.com/photo-1566577739112-5180d4bf9390?auto=format&fit=crop&w=700&q=80'); background-size: cover; background-position: center;">
                <div class="feature-card-content">
                    <div class="feature-card-icon-pill">⚖️</div>
                    <div class="feature-card-title-row">
                        <span class="feature-card-title">Player Comparison Studio</span>
                        <span style="background: rgba(200,244,90,0.18); color: #C8F45A; border: 1px solid rgba(200,244,90,0.35); font-size: 0.68rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">Signature Feature</span>
                    </div>
                    <div class="feature-card-desc">
                        Compare two prospects with verified movement and performance metrics.
                    </div>
                </div>
                <div class="feature-card-arrow-btn">➔</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f_col3:
        st.markdown(
            """
            <div class="feature-hero-card" style="background-image: linear-gradient(180deg, rgba(22,27,34,0.70) 0%, rgba(11,14,17,0.92) 100%), radial-gradient(circle at top right, rgba(200,244,90,0.2) 0%, transparent 60%);">
                <div class="feature-card-content">
                    <div class="feature-card-icon-pill">📚</div>
                    <div class="feature-card-title-row">
                        <span class="feature-card-title">Model Performance</span>
                    </div>
                    <div class="feature-card-desc">
                        Evaluate and compare predictive models with statistical validation.
                    </div>
                </div>
                <div class="feature-card-arrow-btn">➔</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Scientific Caution & Integrity Banner
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    render_scientific_banner(
        "Scientific Boundary Notice",
        "Empirical nested cross-validation demonstrates that the Traditional Combine baseline (Model A, R² = 0.9381) "
        "statistically outperforms the current Hybrid model (Model C, R² = 0.9311; p = 0.0069) for predicting global in-game straight-line speed. "
        "Sensor features do not replace stopwatches for straight-line speed, but provide qualitative diagnostic insight into Change-of-Direction mechanics and Athletic Alpha."
    )
