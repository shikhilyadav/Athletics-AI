"""
ATHLETIX AI — Dashboard View 1: Research Overview
Design 2: Next-Gen Motion Intelligence Visual Direction
- Deep navy and graphite backgrounds (#080C14, #0F172A, #131D31)
- Electric blue (#38BDF8), cyan (#22D3EE), and violet (#8B5CF6) accents
- Premium sports-tech typography and NFL athlete motion imagery
- High-quality 6-grid KPI cards with verified project metrics
- Research performance spline charts & Model architecture comparison
- Signature Athletic Alpha residual translation visualization
- Next-Gen Biomechanical Lab & Player Comparison Studio feature cards
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import (
    load_master_df,
    load_game_tracking_df,
    load_nested_cv_metrics,
    load_player_play_df,
    load_kinematics_df,
    load_athletic_alpha,
)
from src.dashboard.components import (
    render_editorial_header,
    render_scientific_banner,
    render_model_architecture_card,
    render_key_findings_card,
)
from src.dashboard.charts import (
    plot_cohort_performance_trend,
    plot_athletic_alpha_overview,
)


def render_page():
    # Load verified datasets
    master_df = load_master_df()
    game_df = load_game_tracking_df()
    kinematics_df = load_kinematics_df()
    play_df = load_player_play_df()
    nested_df = load_nested_cv_metrics()
    alpha_df = load_athletic_alpha()
    
    # Calculate verified statistics from genuine datasets
    total_combine_prospects = len(master_df)                                       # 510
    tracking_matched = len(game_df)                                                # 156
    primary_cohort = len(master_df[master_df["is_eligible_50_snaps"] == True])     # 149
    route_subcohort = play_df[play_df["separation_at_pass_forward"].notna()]["nfl_id"].nunique() # 51
    total_drill_trials = len(kinematics_df)                                        # 6,310
    regular_season_frames = "3.66M"                                                # 3.66M
    
    # =========================================================================
    # 1. HERO BANNER: NEXT-GEN MOTION INTELLIGENCE
    # =========================================================================
    st.markdown(
        """
        <div style="margin-bottom: 2.2rem; position: relative; background: radial-gradient(circle at 65% 25%, rgba(34, 211, 238, 0.12) 0%, rgba(56, 189, 248, 0.05) 45%, transparent 70%); border: 1px solid #1E293B; border-radius: 20px; padding: 2.0rem 2.2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 24px;">
                <div style="max-width: 760px;">
                    <div style="font-size: 0.82rem; font-weight: 800; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.14em; margin-bottom: 10px;">
                        NEXT-GEN MOTION INTELLIGENCE //
                    </div>
                    <h1 style="font-size: 3.1rem; font-weight: 900; letter-spacing: -0.04em; line-height: 1.08; margin: 0 0 16px 0;">
                        <span style="font-style: italic; color: #FFFFFF;">DECODING MOVEMENT.</span><br>
                        <span style="font-style: italic; background: linear-gradient(135deg, #22D3EE 0%, #38BDF8 50%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; filter: drop-shadow(0 0 25px rgba(56, 189, 248, 0.35));">PREDICTING NFL IMPACT.</span>
                    </h1>
                    <p style="font-size: 1.05rem; color: #94A3B8; margin-top: 0; margin-bottom: 24px; line-height: 1.6; max-width: 630px;">
                        A research-driven sports intelligence platform that combines 10 Hz RFID biomechanics, motion science, and machine learning to evaluate NFL athletic performance.
                    </p>
                    <div style="display: flex; gap: 14px; align-items: center; flex-wrap: wrap;">
                        <div class="hero-cta-motion">Explore the Research ➔</div>
                        <div class="hero-cta-dark">Watch Demo ▶</div>
                    </div>
                </div>
                <div>
                    <div class="movement-intel-card" style="background: #0F172A; border-color: #1E293B;">
                        <div class="movement-intel-title" style="color: #FFFFFF; display: flex; justify-content: space-between; align-items: center;">
                            <span>Motion Intelligence</span>
                            <span style="font-size: 0.68rem; font-weight: 800; color: #22D3EE; background: rgba(34, 211, 238, 0.14); padding: 2px 8px; border-radius: 9999px;">10 HZ LIVE</span>
                        </div>
                        <div class="movement-intel-item" style="background: #080C14; border-color: #1E293B;">
                            <div class="movement-intel-icon" style="background: rgba(34, 211, 238, 0.15); color: #22D3EE;">🏃</div>
                            <div class="movement-intel-text">Sprint Mechanics</div>
                        </div>
                        <div class="movement-intel-item" style="background: #080C14; border-color: #1E293B;">
                            <div class="movement-intel-icon" style="background: rgba(56, 189, 248, 0.15); color: #38BDF8;">⚙️</div>
                            <div class="movement-intel-text">Change of Direction</div>
                        </div>
                        <div class="movement-intel-item" style="background: #080C14; border-color: #1E293B;">
                            <div class="movement-intel-icon" style="background: rgba(139, 92, 246, 0.15); color: #8B5CF6;">⚡</div>
                            <div class="movement-intel-text">Acceleration / Deceleration</div>
                        </div>
                        <div class="movement-intel-item" style="background: #080C14; border-color: #1E293B;">
                            <div class="movement-intel-icon" style="background: rgba(34, 211, 238, 0.15); color: #22D3EE;">🎯</div>
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
    # 2. 6-GRID KPI METRICS ROW (Design 2: Cyan & Electric Blue Highlights)
    # =========================================================================
    st.markdown(
        f"""
        <div class="kpi-dark-grid">
            <div class="kpi-dark-card" style="background: #0F172A; border-color: #1E293B;">
                <div class="kpi-dark-icon-wrap" style="background: #131D31; color: #38BDF8;">👥</div>
                <div>
                    <div class="kpi-dark-num">{total_combine_prospects}</div>
                    <div class="kpi-dark-label">Combine Prospects</div>
                </div>
            </div>
            <div class="kpi-dark-card kpi-dark-card-active" style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.18) 0%, rgba(15, 23, 42, 0.95) 100%); border: 1.5px solid #22D3EE; box-shadow: 0 0 22px rgba(34, 211, 238, 0.28);">
                <div class="kpi-dark-icon-wrap kpi-dark-icon-wrap-cyan">🏃</div>
                <div>
                    <div class="kpi-dark-num" style="color: #22D3EE;">{tracking_matched}</div>
                    <div class="kpi-dark-label" style="color: #FFFFFF; font-weight: 700;">In-Game Tracked</div>
                </div>
            </div>
            <div class="kpi-dark-card" style="background: #0F172A; border-color: #1E293B;">
                <div class="kpi-dark-icon-wrap" style="background: #131D31; color: #8B5CF6;">📚</div>
                <div>
                    <div class="kpi-dark-num">{primary_cohort}</div>
                    <div class="kpi-dark-label">Research Cohort</div>
                </div>
            </div>
            <div class="kpi-dark-card" style="background: #0F172A; border-color: #1E293B;">
                <div class="kpi-dark-icon-wrap" style="background: #131D31; color: #22D3EE;">🔬</div>
                <div>
                    <div class="kpi-dark-num">{route_subcohort}</div>
                    <div class="kpi-dark-label">Route Separation</div>
                </div>
            </div>
            <div class="kpi-dark-card" style="background: #0F172A; border-color: #1E293B;">
                <div class="kpi-dark-icon-wrap" style="background: #131D31; color: #38BDF8;">🏋️</div>
                <div>
                    <div class="kpi-dark-num">{total_drill_trials:,}</div>
                    <div class="kpi-dark-label">Drill Trials</div>
                </div>
            </div>
            <div class="kpi-dark-card" style="background: #0F172A; border-color: #1E293B;">
                <div class="kpi-dark-icon-wrap" style="background: #131D31; color: #8B5CF6;">💾</div>
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
    # 3. MIDDLE ANALYTICAL ROW (Research Performance & Models)
    # =========================================================================
    col_trend, col_model, col_findings = st.columns([10, 8, 7])
    
    with col_trend:
        # Card 1: Cohort Performance Trend
        trend_header_html = (
            '<div style="background: #0F172A; border: 1px solid #1E293B; border-radius: 18px 18px 0 0; padding: 1.2rem 1.4rem 0.4rem 1.4rem; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);">'
            '<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">'
            '<div style="display: flex; align-items: center; gap: 8px;">'
            '<span style="font-size: 1.1rem; color: #38BDF8;">📈</span>'
            '<span style="font-size: 1.08rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">Cohort Performance Trend</span>'
            '</div>'
            '<div style="display: flex; background: #080C14; border: 1px solid #1E293B; border-radius: 9999px; padding: 2px;">'
            '<span style="background: #38BDF8; color: #080C14; font-size: 0.68rem; font-weight: 800; padding: 2px 10px; border-radius: 9999px;">R²</span>'
            '<span style="color: #64748B; font-size: 0.68rem; font-weight: 700; padding: 2px 10px;">RMSE</span>'
            '</div>'
            '</div>'
            '</div>'
        )
        st.markdown(trend_header_html, unsafe_allow_html=True)
        st.plotly_chart(plot_cohort_performance_trend(nested_df, "R²"), use_container_width=True, config={"displayModeBar": False})

    with col_model:
        # Card 2: Model Architecture Comparison Table (Design 2 Component)
        st.markdown(render_model_architecture_card(), unsafe_allow_html=True)

    with col_findings:
        # Card 3: Key Research Findings Checklist (Design 2 Component)
        st.markdown(render_key_findings_card(), unsafe_allow_html=True)

    # =========================================================================
    # 4. SIGNATURE ATHLETIC ALPHA RESIDUAL VISUALIZATION
    # =========================================================================
    st.markdown(
        """
        <div class="dark-card" style="background: #0F172A; border-color: #1E293B; margin-top: 0.5rem; margin-bottom: 1.5rem;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.0rem; flex-wrap: wrap; gap: 12px;">
                <div>
                    <div style="font-size: 0.76rem; font-weight: 800; color: #8B5CF6; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 4px;">
                        RESIDUAL TRANSLATION INTELLIGENCE //
                    </div>
                    <div style="font-size: 1.35rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.02em;">
                        Athletic Alpha: In-Game Speed vs. Combine Projections
                    </div>
                    <div style="font-size: 0.85rem; color: #94A3B8; margin-top: 2px;">
                        Quantifying out-of-fold linear residual deltas: α = y_actual - ŷ_ModelA across the N=149 primary scrimmage cohort.
                    </div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span class="pill-badge pill-badge-cyan">Cyan: Overperformed Projections</span>
                    <span class="pill-badge pill-badge-violet">Violet: Underperformed Projections</span>
                </div>
            </div>
        """,
        unsafe_allow_html=True,
    )
    
    alpha_col1, alpha_col2 = st.columns([14, 9])
    
    with alpha_col1:
        if not alpha_df.empty:
            st.plotly_chart(plot_athletic_alpha_overview(alpha_df), use_container_width=True, config={"displayModeBar": False})
            
    with alpha_col2:
        if not alpha_df.empty:
            mean_alpha = alpha_df["athletic_alpha_raw"].mean()
            std_alpha = alpha_df["athletic_alpha_raw"].std()
            high_out = len(alpha_df[alpha_df["athletic_alpha_zscore"] >= 1.0])
            high_under = len(alpha_df[alpha_df["athletic_alpha_zscore"] <= -1.0])
            
            st.markdown(
                f"""
                <div style="background: #080C14; border: 1px solid #1E293B; border-radius: 14px; padding: 1.2rem; height: 260px; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.76rem; font-weight: 700; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">
                            Cohort Statistical Properties
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px;">
                            <div style="background: #0F172A; padding: 8px 12px; border-radius: 10px; border: 1px solid #1E293B;">
                                <div style="font-size: 0.72rem; color: #94A3B8;">Mean Alpha</div>
                                <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">{mean_alpha:.4f} <span style="font-size: 0.7rem; color: #94A3B8;">yd/s</span></div>
                            </div>
                            <div style="background: #0F172A; padding: 8px 12px; border-radius: 10px; border: 1px solid #1E293B;">
                                <div style="font-size: 0.72rem; color: #94A3B8;">Residual Spread</div>
                                <div style="font-size: 1.15rem; font-weight: 800; color: #FFFFFF;">{std_alpha:.4f} <span style="font-size: 0.7rem; color: #94A3B8;">yd/s</span></div>
                            </div>
                        </div>
                    </div>
                    <div style="font-size: 0.80rem; color: #94A3B8; line-height: 1.5; border-top: 1px solid #1E293B; padding-top: 8px;">
                        • <strong style="color: #22D3EE;">{high_out} High Overperformers</strong> (Z ≥ +1.0) game speed exceeded Combine expectations.<br>
                        • <strong style="color: #8B5CF6;">{high_under} High Underperformers</strong> (Z ≤ -1.0) observed game speed fell below projections.<br>
                        • Residuals reflect offensive scheme, pursuit geometry, and game context.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # 5. BOTTOM ROW: 3 FEATURE NAVIGATION CARDS (Next-Gen Sports Imagery)
    # =========================================================================
    f_col1, f_col2, f_col3 = st.columns(3)
    
    with f_col1:
        st.markdown(
            """
            <div class="feature-hero-card" style="background-image: linear-gradient(180deg, rgba(15,23,42,0.70) 0%, rgba(8,12,20,0.95) 100%), url('https://images.unsplash.com/photo-1541534741688-6078c6bfb5c5?auto=format&fit=crop&w=700&q=80'); background-size: cover; background-position: center; border-color: #1E293B;">
                <div class="feature-card-content">
                    <div class="feature-card-icon-pill" style="background: linear-gradient(135deg, #06B6D4 0%, #3B82F6 100%); color: #FFFFFF;">🏃</div>
                    <div class="feature-card-title-row">
                        <span class="feature-card-title">Biomechanical Lab</span>
                        <span class="pill-badge pill-badge-cyan" style="font-size: 0.68rem;">Hero Experience</span>
                    </div>
                    <div class="feature-card-desc">
                        Explore sprint curve modeling, COD turn preservation, and 3D motion kinematics.
                    </div>
                </div>
                <div class="feature-card-arrow-btn" style="background: #22D3EE; color: #080C14;">➔</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f_col2:
        st.markdown(
            """
            <div class="feature-hero-card" style="background-image: linear-gradient(180deg, rgba(15,23,42,0.70) 0%, rgba(8,12,20,0.95) 100%), url('https://images.unsplash.com/photo-1566577739112-5180d4bf9390?auto=format&fit=crop&w=700&q=80'); background-size: cover; background-position: center; border-color: #1E293B;">
                <div class="feature-card-content">
                    <div class="feature-card-icon-pill" style="background: linear-gradient(135deg, #8B5CF6 0%, #3B82F6 100%); color: #FFFFFF;">⚖️</div>
                    <div class="feature-card-title-row">
                        <span class="feature-card-title">Player Comparison Studio</span>
                        <span class="pill-badge pill-badge-violet" style="font-size: 0.68rem;">Signature Feature</span>
                    </div>
                    <div class="feature-card-desc">
                        Head-to-head multi-dimensional athletic matchup evaluation across verified NFL metrics.
                    </div>
                </div>
                <div class="feature-card-arrow-btn" style="background: #8B5CF6; color: #FFFFFF;">➔</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with f_col3:
        st.markdown(
            """
            <div class="feature-hero-card" style="background-image: linear-gradient(180deg, rgba(15,23,42,0.70) 0%, rgba(8,12,20,0.95) 100%), radial-gradient(circle at top right, rgba(56,189,248,0.2) 0%, transparent 60%); border-color: #1E293B;">
                <div class="feature-card-content">
                    <div class="feature-card-icon-pill" style="background: linear-gradient(135deg, #38BDF8 0%, #06B6D4 100%); color: #FFFFFF;">📚</div>
                    <div class="feature-card-title-row">
                        <span class="feature-card-title">Predictive Model Lab</span>
                        <span class="pill-badge pill-badge-blue" style="font-size: 0.68rem;">Machine Learning</span>
                    </div>
                    <div class="feature-card-desc">
                        Nested cross-validation benchmarks and bootstrap uncertainty quantification.
                    </div>
                </div>
                <div class="feature-card-arrow-btn" style="background: #38BDF8; color: #080C14;">➔</div>
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

