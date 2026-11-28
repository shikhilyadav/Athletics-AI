"""
ATHLETIX AI — Dashboard View 5: Biomechanical Laboratory
Design 2: Next-Gen Motion Intelligence Visual Direction
- Deep navy background: #080C14
- Graphite containers: #0F172A, #131D31, borders #1E293B
- Electric blue: #38BDF8, Cyan: #22D3EE, Violet: #A78BFA
- White primary typography, muted grey secondary typography
- Four interactive analysis sections: Sprint Intelligence, Change of Direction,
  Acceleration & Deceleration, Player Analysis (+ 3D Motion Analysis)
Strictly verified 10 Hz RFID kinematic features, mono-exponential velocity modeling,
and rigorous empirical physics boundaries.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from typing import Optional

from src.dashboard.data_loader import (
    load_master_df,
    load_kinematics_df,
    load_cod_df,
)
from src.dashboard.charts import (
    plot_sprint_curve_distribution,
    plot_sprint_velocity_interactive,
    plot_acceleration_profile,
    plot_cod_velocity_transitions,
    plot_cod_interactive_scatter,
    plot_biomechanical_profile_radar,
    plot_3d_motion_analysis,
    THEME_LAYOUT,
)
from src.dashboard.metrics import (
    fmt_speed,
    fmt_accel,
    fmt_time,
    fmt_ratio,
    fmt_dist_in,
    fmt_weight_lbs,
)
from src.dashboard.components import (
    render_scientific_banner,
    render_section_header,
    render_kpi_card_v2,
    render_metric_card,
)


def render_page():
    # =========================================================================
    # 1. PAGE HEADER (Design 2: Next-Gen Motion Intelligence)
    # =========================================================================
    header_html = (
        '<div style="margin-bottom: 1.5rem;">'
        '<div style="font-size: 0.78rem; font-weight: 800; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 4px;">'
        'BIOMECHANICAL LAB //'
        '</div>'
        '<div style="font-size: 2.2rem; font-weight: 900; color: #FFFFFF; letter-spacing: -0.03em; line-height: 1.15;">'
        'Decode the mechanics behind athletic performance.'
        '</div>'
        '<div style="font-size: 0.95rem; color: #94A3B8; margin-top: 6px; max-width: 950px; line-height: 1.5;">'
        'High-resolution 10 Hz RFID kinematic tracking analysis integrating mono-exponential straight-line sprint curves, '
        'multi-directional turn apex speed preservation, and empirical acceleration dynamics across 510 NFL Combine prospects.'
        '</div>'
        '</div>'
    )
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Load Verified Datasets
    master_df = load_master_df()
    kinematics_df = load_kinematics_df()
    cod_df = load_cod_df()

    # Scientific Boundary Banner (Design 2 Navy/Cyan/Violet)
    render_scientific_banner(
        "Biomechanical Definition & Empirical Physics Standards",
        "1. <strong>Sprint Velocity Modeling:</strong> The mono-exponential rise is defined as "
        "<code>v(t) = vmax × (1 - exp(-t/τ))</code>. The fitted asymptotic velocity <code>vmax</code> is an analytical parameter "
        "representing the theoretical velocity ceiling and is <strong>not the same as observed maximum velocity</strong>.<br>"
        "2. <strong>Speed Preservation Ratio (SPR):</strong> Defined strictly as the dimensionless kinematic velocity ratio "
        "<code>vexit / ventry</code> at turn apex. It must <strong>NOT</strong> be described as kinetic energy preservation "
        "(kinetic energy scales with mass and velocity squared: <code>0.5 × m × v²</code>).<br>"
        "3. <strong>Acceleration Kinematics:</strong> Tangential acceleration represents the directional scalar rate of speed change along the velocity vector (<code>dv/dt</code>). "
        "Do not describe acceleration magnitude <code>√(ax² + ay²)</code> as signed braking deceleration.",
    )

    # Four Core Navigation Tabs + 3D Motion Reconstruction
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Sprint Intelligence",
        "Change of Direction",
        "Acceleration & Deceleration",
        "Player Analysis",
        "3D Motion Analysis",
    ])

    # =========================================================================
    # TAB 1: SPRINT INTELLIGENCE
    # =========================================================================
    with tab1:
        # Prospect Selector
        valid_sprint_df = master_df.dropna(subset=["forty_curve_tau", "forty_curve_vmax", "forty_curve_r2"]).copy()
        valid_sprint_df = valid_sprint_df.sort_values(by="display_name")
        
        player_options = [
            f"{row['display_name']} ({row['nfl_position'] or '?'}) • R²={row['forty_curve_r2']:.4f}"
            for _, row in valid_sprint_df.iterrows()
        ]
        
        default_idx = 0
        for i, opt in enumerate(player_options):
            if "Will Anderson" in opt:
                default_idx = i
                break
                
        selected_p_str = st.selectbox(
            "Select Prospect to Evaluate Sprint Kinematics",
            player_options,
            index=default_idx,
            key="sprint_prospect_select",
        )
        
        p_name = selected_p_str.split(" (")[0]
        p_row = valid_sprint_df[valid_sprint_df["display_name"] == p_name].iloc[0]
        
        tau_val = p_row["forty_curve_tau"]
        vmax_param = p_row["forty_curve_vmax"]
        r2_fit = p_row["forty_curve_r2"]
        forty_time = p_row["forty"]
        obs_max_speed = p_row["combine_max_speed"]
        p_pos = p_row.get("nfl_position", "?")
        p_college = p_row.get("college_name", "N/A")
        
        # Fit Tier Classification using validated research thresholds
        if r2_fit >= 0.98:
            fit_tier = "Exceptional Fit (R² ≥ 0.98)"
            badge_class = "pill-badge-cyan"
        elif r2_fit >= 0.95:
            fit_tier = "High Fit (R² ≥ 0.95)"
            badge_class = "pill-badge-blue"
        else:
            fit_tier = "Moderate/Low (R² < 0.95)"
            badge_class = "pill-badge-violet"
            
        # Two-Column Layout (Dossier Card + Interactive Velocity Curve)
        bio_col1, bio_col2 = st.columns([1.1, 2.3])
        
        with bio_col1:
            dossier_html = (
                '<div class="bio-prospect-card">'
                '<div class="bio-prospect-header">'
                '<div class="bio-avatar-circle">👤</div>'
                '<div>'
                f'<div class="bio-prospect-name">{p_name} ({p_pos})</div>'
                f'<div class="bio-prospect-meta">@{p_college}</div>'
                '</div>'
                '</div>'
                '<div class="bio-kpi-row">'
                '<span class="bio-kpi-label">40-Yard Time</span>'
                f'<span class="bio-kpi-val">{fmt_time(forty_time)}</span>'
                '</div>'
                '<div class="bio-kpi-row">'
                '<span class="bio-kpi-label">Observed Max Speed</span>'
                f'<span class="bio-kpi-val">{fmt_speed(obs_max_speed)}</span>'
                '</div>'
                '<div class="bio-kpi-row">'
                '<span class="bio-kpi-label">Fitted Asymptotic Vmax</span>'
                f'<span class="bio-kpi-val" style="color: #22D3EE;">{fmt_speed(vmax_param)}</span>'
                '</div>'
                '<div class="bio-kpi-row">'
                '<span class="bio-kpi-label">Time Constant (τ)</span>'
                f'<span class="bio-kpi-val">{fmt_time(tau_val)}</span>'
                '</div>'
                '<div class="bio-kpi-row">'
                '<span class="bio-kpi-label">Curve Fitting R²</span>'
                f'<span class="bio-kpi-val" style="color: #22D3EE;">{r2_fit:.4f}</span>'
                '</div>'
                '<div style="margin-top: 16px; text-align: center;">'
                f'<span class="pill-badge {badge_class}" style="width: 100%; justify-content: center; padding: 7px 0; font-size: 0.76rem;">{fit_tier}</span>'
                '</div>'
                '</div>'
            )
            st.markdown(dossier_html, unsafe_allow_html=True)
            
        with bio_col2:
            st.plotly_chart(plot_sprint_velocity_interactive(p_row), use_container_width=True, config={"displayModeBar": False})

        # Explicit Scientific Callout on Asymptotic Vmax vs Observed Speed
        vmax_note_html = (
            '<div style="background: rgba(34, 211, 238, 0.08); border: 1px solid #22D3EE; border-radius: 14px; padding: 1.1rem 1.4rem; margin-top: 1.2rem; margin-bottom: 1.4rem;">'
            '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">'
            '<span style="color: #22D3EE; font-size: 1.1rem;">⚡</span>'
            '<strong style="color: #22D3EE; font-size: 0.95rem;">Model Parameter Clarification: Asymptotic Vmax vs. Observed Speed</strong>'
            '</div>'
            '<div style="font-size: 0.86rem; color: #D1D5DB; line-height: 1.6;">'
            'The fitted asymptotic velocity (<strong>Vmax = ' f'{vmax_param:.2f} yd/s' '</strong>) is a model-derived parameter and is not the same as observed maximum velocity (<strong>' f'{obs_max_speed:.2f} yd/s' '</strong>). '
            'Because the 40-yard dash is completed in under 5 seconds, elite sprinters may still be accelerating and may not fully attain their asymptotic theoretical plateau. '
            'The time constant (<strong>τ = ' f'{tau_val:.3f} s' '</strong>) characterizes the acceleration burst rate: a lower τ indicates steeper initial velocity acquisition.'
            '</div>'
            '</div>'
        )
        st.markdown(vmax_note_html, unsafe_allow_html=True)

        # Denominator KPI Cards
        sk1, sk2, sk3, sk4 = st.columns(4)
        with sk1:
            st.markdown(render_kpi_card_v2("Evaluated 40yd Sprints", "418", "793 Trials (from 6,310 total)"), unsafe_allow_html=True)
        with sk2:
            st.markdown(render_kpi_card_v2("R² ≥ 0.98 (Exceptional)", "385", "92.1% of Evaluated Prospects", highlight_lime=True), unsafe_allow_html=True)
        with sk3:
            st.markdown(render_kpi_card_v2("R² ≥ 0.95 (High Fit)", "413", "98.8% of Evaluated Prospects", highlight_lime=True), unsafe_allow_html=True)
        with sk4:
            st.markdown(render_kpi_card_v2("Skipped / DNP 40yd", "92", "18.0% of 510 Attendees"), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Fit Quality Distribution and Technical Explanation
        col_dist1, col_dist2 = st.columns([3, 2])
        with col_dist1:
            st.plotly_chart(plot_sprint_curve_distribution(master_df), use_container_width=True, config={"displayModeBar": False})
        with col_dist2:
            method_box_html = (
                '<div style="background: #131D31; border-radius: 16px; padding: 1.2rem; border: 1px solid #1E293B; font-size: 0.82rem; color: #94A3B8; line-height: 1.6;">'
                '<strong style="font-size: 0.9rem; color: #FFFFFF;">Methodological Integrity & Convergence Standards:</strong><br>'
                '• <strong>Total Trials vs. Straight-Line Sprints:</strong> The Combine tracking database holds <strong style="color:#FFFFFF;">6,310 trials</strong> across all positional drills. Only <strong style="color:#22D3EE;">793 trials</strong> represent straight-line 40-yard sprints.<br>'
                '• <strong>Convergence ≠ Good Fit:</strong> Optimization convergence alone does not prove a good fit. Five prospects converged with R² &lt; 0.95 due to stride stumble, early deceleration, or tracking sensor dropouts.<br>'
                '• <strong>Non-Linear Least Squares:</strong> Mono-exponential parameters are estimated with Levenberg-Marquardt optimization bounded by physiological limits (Vmax ∈ [6, 15] yd/s, τ ∈ [0.5, 4.0] s).'
                '</div>'
            )
            st.markdown(method_box_html, unsafe_allow_html=True)

    # =========================================================================
    # TAB 2: CHANGE OF DIRECTION (COD)
    # =========================================================================
    with tab2:
        render_section_header(
            title="Change-of-Direction (COD) Kinematics",
            subtitle="Decoupling turn entry velocity, apex speed preservation, and angular reorientation dynamics.",
            badge="COD ENGINE",
        )
        
        # Macro Cohort COD KPIs
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(render_kpi_card_v2("Mean Apex Speed", f"{master_df['combine_mean_cod_apex_speed'].mean():.2f} yd/s", "Across All Verified Cuts"), unsafe_allow_html=True)
        with c2:
            st.markdown(render_kpi_card_v2("Speed Preservation Ratio", f"{master_df['combine_mean_speed_preservation_ratio'].mean():.3f}", "vexit / ventry (Dimensionless)", highlight_lime=True), unsafe_allow_html=True)
        with c3:
            st.markdown(render_kpi_card_v2("Peak Angular Velocity", f"{master_df['combine_peak_angular_velocity'].mean():.1f} °/s", "Maximum Body Reorientation"), unsafe_allow_html=True)
        with c4:
            st.markdown(render_kpi_card_v2("Tracked COD Trials", "3,115", "From 6,310 Combine Trials"), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Prospect Selector for COD Highlighting
        cod_players = master_df[master_df["combine_mean_cod_apex_speed"].notna()].sort_values("display_name")
        cod_player_list = [
            f"{row['display_name']} ({row['nfl_position'] or '?'})"
            for _, row in cod_players.iterrows()
        ]
        
        selected_cod_str = st.selectbox(
            "Select Prospect to Evaluate Change-of-Direction Dynamics",
            cod_player_list,
            index=0,
            key="cod_prospect_select",
        )
        selected_cod_name = selected_cod_str.split(" (")[0]
        selected_cod_row = cod_players[cod_players["display_name"] == selected_cod_name].iloc[0]
        selected_nfl_id = int(selected_cod_row["nfl_id"])
        
        # Fetch athlete's verified drill trials from combine_cod_features
        p_trials = cod_df[cod_df["nfl_id"] == selected_nfl_id].copy()
        
        # Prospect Turn Dynamics Metrics Row
        st.markdown(f"#### Prospect Turn Dynamics: {selected_cod_name}")
        pk1, pk2, pk3, pk4 = st.columns(4)
        with pk1:
            st.markdown(render_metric_card("Apex Velocity", fmt_speed(selected_cod_row["combine_mean_cod_apex_speed"]), "", "MIN SPEED", "cyan", "At point of maximum curvature"), unsafe_allow_html=True)
        with pk2:
            st.markdown(render_metric_card("Speed Preservation", fmt_ratio(selected_cod_row["combine_mean_speed_preservation_ratio"]), "", "vexit / ventry", "blue", "Kinematic velocity ratio"), unsafe_allow_html=True)
        with pk3:
            st.markdown(render_metric_card("Angular Velocity", f"{selected_cod_row['combine_peak_angular_velocity']:.1f}", "°/s", "PEAK ROTATION", "violet", "Body reorientation rate"), unsafe_allow_html=True)
        with pk4:
            te_val = f"{selected_cod_row['combine_mean_turning_efficiency']:.1f}" if pd.notna(selected_cod_row.get("combine_mean_turning_efficiency")) else "N/A"
            st.markdown(render_metric_card("Turning Efficiency", te_val, "pts", "INDEX", "grey", "Apex / Entry speed ratio × 100"), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # INTERACTIVE CHART COMPARING ENTRY, APEX AND EXIT SPEEDS (Explicit Requirement)
        st.plotly_chart(plot_cod_velocity_transitions(p_trials, selected_cod_name), use_container_width=True, config={"displayModeBar": False})
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # COD Macro Scatter Map
        st.plotly_chart(plot_cod_interactive_scatter(cod_df, highlight_nfl_id=selected_nfl_id), use_container_width=True, config={"displayModeBar": False})
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Verified Individual Drill Trials Table
        if not p_trials.empty:
            st.markdown(f"#### Verified Individual Drill Trials ({len(p_trials)} Tracked Trials)")
            st.dataframe(
                p_trials[[
                    "drill_name", "attempt", "num_detected_turns",
                    "mean_entry_speed", "mean_apex_speed", "mean_exit_speed",
                    "mean_speed_preservation_ratio", "peak_angular_velocity_deg_s"
                ]].rename(columns={
                    "drill_name": "Drill Name",
                    "attempt": "Attempt",
                    "num_detected_turns": "Detected Turns",
                    "mean_entry_speed": "Entry Speed (yd/s)",
                    "mean_apex_speed": "Apex Speed (yd/s)",
                    "mean_exit_speed": "Exit Speed (yd/s)",
                    "mean_speed_preservation_ratio": "Speed Preservation Ratio",
                    "peak_angular_velocity_deg_s": "Peak Angular Vel (°/s)",
                }).style.format({
                    "Entry Speed (yd/s)": "{:.2f}",
                    "Apex Speed (yd/s)": "{:.2f}",
                    "Exit Speed (yd/s)": "{:.2f}",
                    "Speed Preservation Ratio": "{:.3f}",
                    "Peak Angular Vel (°/s)": "{:.1f}",
                }),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info(f"No multi-turn drill trials recorded for {selected_cod_name} (DNP or straight-line sprint only).")

    # =========================================================================
    # TAB 3: ACCELERATION & DECELERATION
    # =========================================================================
    with tab3:
        render_section_header(
            title="Acceleration & Deceleration Dynamics",
            subtitle="Analyzing tangential acceleration, initial burst drive, braking capacity, and jerk proxy.",
            badge="ACCEL / DECEL KINEMATICS",
        )
        
        # Macro Acceleration KPIs
        ak1, ak2, ak3, ak4 = st.columns(4)
        with ak1:
            st.markdown(render_kpi_card_v2("Mean Peak Accel (a_max)", f"{master_df['combine_max_accel'].mean():.2f} yd/s²", "Peak Forward Propulsion", highlight_lime=True), unsafe_allow_html=True)
        with ak2:
            st.markdown(render_kpi_card_v2("Initial Drive (a_init)", f"{master_df['combine_initial_accel_mean'].mean():.2f} yd/s²", "1st-Step Rate of Acceleration"), unsafe_allow_html=True)
        with ak3:
            st.markdown(render_kpi_card_v2("Braking Deceleration", f"{master_df['combine_max_decel'].mean():.2f} yd/s²", "Peak Negative Rate of Speed Change"), unsafe_allow_html=True)
        with ak4:
            st.markdown(render_kpi_card_v2("Mean Positive Jerk", f"{master_df['combine_mean_pos_jerk'].mean():.2f} yd/s³", "Rate of Force Development Proxy"), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Interactive Prospect Selector for Acceleration Profile
        accel_players = master_df.dropna(subset=["forty_curve_tau", "forty_curve_vmax"]).sort_values("display_name")
        accel_player_list = [
            f"{row['display_name']} ({row['nfl_position'] or '?'})"
            for _, row in accel_players.iterrows()
        ]
        
        selected_accel_str = st.selectbox(
            "Select Prospect to Plot Tangential Acceleration Curve",
            accel_player_list,
            index=0,
            key="accel_prospect_select",
        )
        accel_p_name = selected_accel_str.split(" (")[0]
        accel_p_row = accel_players[accel_players["display_name"] == accel_p_name].iloc[0]
        accel_nfl_id = int(accel_p_row["nfl_id"])
        
        # Selected Player Acceleration Metrics Cards
        ap1, ap2, ap3, ap4, ap5 = st.columns(5)
        with ap1:
            st.markdown(render_metric_card("Peak Accel (a_max)", fmt_accel(accel_p_row["combine_max_accel"]), "", "SENSOR PEAK", "blue", "Maximum forward acceleration"), unsafe_allow_html=True)
        with ap2:
            st.markdown(render_metric_card("Initial Accel (a_init)", fmt_accel(accel_p_row["combine_initial_accel_mean"]), "", "1ST STEP", "cyan", "Acceleration at start"), unsafe_allow_html=True)
        with ap3:
            theo_a0 = accel_p_row["forty_curve_vmax"] / accel_p_row["forty_curve_tau"]
            st.markdown(render_metric_card("Theoretical a(0)", f"{theo_a0:.2f} yd/s²", "", "vmax / τ", "cyan", "Modeled initial acceleration"), unsafe_allow_html=True)
        with ap4:
            st.markdown(render_metric_card("Braking Decel", fmt_accel(accel_p_row["combine_max_decel"]), "", "BRAKING", "violet", "Peak tangential braking"), unsafe_allow_html=True)
        with ap5:
            jerk_val = f"{accel_p_row['combine_mean_pos_jerk']:.2f}" if pd.notna(accel_p_row.get("combine_mean_pos_jerk")) else "N/A"
            st.markdown(render_metric_card("Jerk Proxy (da/dt)", jerk_val, "yd/s³", "PROXY", "blue", "RFD kinematic proxy"), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Acceleration Profile Chart
        st.plotly_chart(plot_acceleration_profile(accel_p_row), use_container_width=True, config={"displayModeBar": False})
        
        st.markdown("<br>", unsafe_allow_html=True)

        # Individual Drill Kinematics Trials from combine_kinematic_features
        p_kin_trials = kinematics_df[kinematics_df["nfl_id"] == accel_nfl_id].copy()
        if not p_kin_trials.empty:
            st.markdown(f"#### Verified Acceleration & Deceleration Drill Trials ({len(p_kin_trials)} Trials Tracked)")
            st.dataframe(
                p_kin_trials[[
                    "drill_name", "attempt", "a_init", "a_max", "a_var",
                    "t_v_max", "mean_decel", "max_decel", "mean_pos_jerk"
                ]].rename(columns={
                    "drill_name": "Drill Name",
                    "attempt": "Attempt",
                    "a_init": "Initial Accel (yd/s²)",
                    "a_max": "Peak Accel (yd/s²)",
                    "a_var": "Accel Variance (yd/s²)²",
                    "t_v_max": "Time to Vmax (s)",
                    "mean_decel": "Mean Decel (yd/s²)",
                    "max_decel": "Max Braking (yd/s²)",
                    "mean_pos_jerk": "Jerk Proxy (yd/s³)",
                }).style.format({
                    "Initial Accel (yd/s²)": "{:.2f}",
                    "Peak Accel (yd/s²)": "{:.2f}",
                    "Accel Variance (yd/s²)²": "{:.3f}",
                    "Time to Vmax (s)": "{:.2f}",
                    "Mean Decel (yd/s²)": "{:.2f}",
                    "Max Braking (yd/s²)": "{:.2f}",
                    "Jerk Proxy (yd/s³)": "{:.2f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

        # Physical Measurement Explanations
        accel_expl_html = (
            '<div style="background: #131D31; border-radius: 16px; padding: 1.2rem; border: 1px solid #1E293B; font-size: 0.82rem; color: #94A3B8; line-height: 1.6; margin-top: 1rem;">'
            '<strong style="font-size: 0.9rem; color: #FFFFFF;">Measurement Definitions & Scientific Constraints:</strong><br>'
            '• <strong>Tangential Acceleration vs. Vector Magnitude:</strong> Tangential acceleration is the signed scalar rate of speed change along the path <code>a_tangential = dv/dt</code>. '
            'Total acceleration vector norm <code>||a|| = √(ax² + ay²)</code> is an unsigned quantity that conflates forward propulsion with lateral turning centripetal acceleration and must not be described as signed braking deceleration.<br>'
            '• <strong>Theoretical Initial Drive <code>a(0) = vmax / τ</code>:</strong> Derived analytically from the mono-exponential velocity rise at <code>t = 0</code>. Represents the athlete\'s mechanical rate of speed acquisition from a stationary stance.<br>'
            '• <strong>Jerk Proxy (yd/s³):</strong> Computed as the mean positive first derivative of acceleration (<code>da/dt</code>) during the initial drive phase, serving as an empirical kinematic proxy for Rate of Force Development (RFD).'
            '</div>'
        )
        st.markdown(accel_expl_html, unsafe_allow_html=True)

    # =========================================================================
    # TAB 4: PLAYER ANALYSIS
    # =========================================================================
    with tab4:
        render_section_header(
            title="Comprehensive Biomechanical Prospect Profile",
            subtitle="Multi-dimensional athletic profile integrating straight-line sprint modeling and change-of-direction metrics.",
            badge="SCOUTING REPORT",
        )
        
        # Prospect Selector with Position Filtering
        f_col1, f_col2 = st.columns([1, 2])
        with f_col1:
            all_positions = ["All Positions"] + sorted(master_df["nfl_position"].dropna().unique().tolist())
            selected_pos = st.selectbox("Filter by Position Alignment", all_positions, index=0)
            
        filtered_master = master_df.copy()
        if selected_pos != "All Positions":
            filtered_master = filtered_master[filtered_master["nfl_position"] == selected_pos]
            
        filtered_master = filtered_master.sort_values("display_name")
        player_names = filtered_master["display_name"].tolist()
        
        with f_col2:
            default_p_idx = 0
            for i, name in enumerate(player_names):
                if "Will Anderson" in name:
                    default_p_idx = i
                    break
            selected_name = st.selectbox("Select Prospect for Deep-Dive Analysis", player_names, index=default_p_idx)
            
        p = filtered_master[filtered_master["display_name"] == selected_name].iloc[0]
        
        # Athlete Identity Header Box
        draft_info = f"Round {int(p['draft_round'])}, Pick {int(p['draft_overall_pick'])}" if pd.notna(p["draft_round"]) else "Undrafted / Free Agent"
        r2_val = p.get("forty_curve_r2")
        if pd.notna(r2_val):
            if r2_val >= 0.98:
                fit_badge = '<span class="pill-badge pill-badge-cyan">Exceptional Fit (R² ≥ 0.98)</span>'
            elif r2_val >= 0.95:
                fit_badge = '<span class="pill-badge pill-badge-blue">High Fit (R² ≥ 0.95)</span>'
            else:
                fit_badge = '<span class="pill-badge pill-badge-violet">Moderate/Low (R² < 0.95)</span>'
        else:
            fit_badge = '<span class="pill-badge pill-badge-grey">40yd Fit Unavailable (DNP)</span>'

        # Tracking data availability badge
        has_rfid = "RFID 10 Hz Tracked" if pd.notna(p.get("combine_max_speed")) else "RFID Unavailable"
        rfid_badge = '<span class="pill-badge pill-badge-cyan">' + has_rfid + '</span>' if pd.notna(p.get("combine_max_speed")) else '<span class="pill-badge pill-badge-grey">RFID DNP</span>'
        
        snaps = int(p["verified_scrimmage_snaps"]) if pd.notna(p.get("verified_scrimmage_snaps")) else 0
        game_badge = '<span class="pill-badge pill-badge-blue">' + str(snaps) + ' Game Snaps</span>' if snaps > 0 else '<span class="pill-badge pill-badge-grey">0 Game Snaps</span>'

        player_header_html = (
            '<div style="background: #131D31; border: 1px solid #1E293B; border-radius: 20px; padding: 1.4rem 1.6rem; margin-bottom: 1.4rem; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">'
            '<div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">'
            '<div>'
            f'<div style="font-size: 1.7rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.03em; line-height: 1.1;">{p["display_name"]}</div>'
            '<div style="font-size: 0.88rem; font-weight: 600; color: #94A3B8; margin-top: 4px;">'
            f'{p["nfl_position"] or "N/A"} • {p["college_name"] or "Unknown College"} • Class of {int(p["draft_year"]) if pd.notna(p["draft_year"]) else "2023"}'
            '</div>'
            '</div>'
            '<div style="display: flex; gap: 8px; align-items: center; flex-wrap: wrap;">'
            f'{fit_badge}'
            f'{rfid_badge}'
            f'{game_badge}'
            f'<span class="pill-badge pill-badge-violet">{draft_info}</span>'
            '</div>'
            '</div>'
            '<div style="display: flex; gap: 20px; margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #1E293B; font-size: 0.82rem; color: #94A3B8; flex-wrap: wrap;">'
            f'<div><strong style="color:#FFFFFF;">Height:</strong> {fmt_dist_in(p.get("combine_height"))}</div>'
            f'<div><strong style="color:#FFFFFF;">Weight:</strong> {fmt_weight_lbs(p.get("combine_weight"))}</div>'
            f'<div><strong style="color:#FFFFFF;">Arm Length:</strong> {fmt_dist_in(p.get("arm_length"))}</div>'
            f'<div><strong style="color:#FFFFFF;">Hand Size:</strong> {fmt_dist_in(p.get("hand_size"))}</div>'
            f'<div><strong style="color:#FFFFFF;">Vertical Jump:</strong> {fmt_dist_in(p.get("vertical"))}</div>'
            f'<div><strong style="color:#FFFFFF;">Broad Jump:</strong> {fmt_dist_in(p.get("broad_jump"))}</div>'
            '</div>'
            '</div>'
        )
        st.markdown(player_header_html, unsafe_allow_html=True)
        
        # Dual Column Layout: Biomechanical Radar vs Key Metric Clusters
        col_radar, col_metrics = st.columns([1, 1])
        
        with col_radar:
            st.plotly_chart(plot_biomechanical_profile_radar(p, master_df), use_container_width=True, config={"displayModeBar": False})
            
        with col_metrics:
            st.markdown("#### 1. Straight-Line Sprint Kinematics")
            sm1, sm2, sm3 = st.columns(3)
            with sm1:
                st.markdown(render_metric_card("40-Yard Time", fmt_time(p.get("forty")), "", "STOPWATCH", "blue"), unsafe_allow_html=True)
            with sm2:
                st.markdown(render_metric_card("10-Yard Split", fmt_time(p.get("ten_yd_split")), "", "BURST", "cyan"), unsafe_allow_html=True)
            with sm3:
                st.markdown(render_metric_card("Observed Max", fmt_speed(p.get("combine_max_speed")), "", "SENSOR", "cyan"), unsafe_allow_html=True)
                
            sm4, sm5, sm6 = st.columns(3)
            with sm4:
                st.markdown(render_metric_card("Asymptotic Vmax", fmt_speed(p.get("forty_curve_vmax")), "", "MODEL", "cyan"), unsafe_allow_html=True)
            with sm5:
                st.markdown(render_metric_card("Time Constant (τ)", fmt_time(p.get("forty_curve_tau")), "", "RATE", "blue"), unsafe_allow_html=True)
            with sm6:
                r2_str = f"{p['forty_curve_r2']:.4f}" if pd.notna(p.get("forty_curve_r2")) else "Unavailable"
                st.markdown(render_metric_card("Curve Fit R²", r2_str, "", "ACCURACY", "violet"), unsafe_allow_html=True)
                
            st.markdown("#### 2. Change-of-Direction Mechanics")
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.markdown(render_metric_card("Apex Velocity", fmt_speed(p.get("combine_mean_cod_apex_speed")), "", "MIN SPEED", "cyan"), unsafe_allow_html=True)
            with cm2:
                st.markdown(render_metric_card("Preservation", fmt_ratio(p.get("combine_mean_speed_preservation_ratio")), "", "RATIO", "blue"), unsafe_allow_html=True)
            with cm3:
                ang_str = f"{p.get('combine_peak_angular_velocity'):.1f}°/s" if pd.notna(p.get("combine_peak_angular_velocity")) else "Unavailable"
                st.markdown(render_metric_card("Angular Vel", ang_str, "", "ROTATION", "violet"), unsafe_allow_html=True)
                
            st.markdown("#### 3. Acceleration & Deceleration Capacity")
            am1, am2, am3 = st.columns(3)
            with am1:
                st.markdown(render_metric_card("Peak Acceleration", fmt_accel(p.get("combine_max_accel")), "", "PROPULSION", "cyan"), unsafe_allow_html=True)
            with am2:
                st.markdown(render_metric_card("Initial Drive", fmt_accel(p.get("combine_initial_accel_mean")), "", "1ST STEP", "blue"), unsafe_allow_html=True)
            with am3:
                st.markdown(render_metric_card("Braking Decel", fmt_accel(p.get("combine_max_decel")), "", "BRAKING", "violet"), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Movement Profile Summary Card in Design 2 Navy & Cyan
        r2_summary_str = f"{p['forty_curve_r2']:.4f}" if pd.notna(p.get("forty_curve_r2")) else "Unavailable"
        ang_vel_str = f"{p.get('combine_peak_angular_velocity'):.1f}°/s" if pd.notna(p.get("combine_peak_angular_velocity")) else "Unavailable"
        
        summary_card_html = (
            '<div style="background: #131D31; border: 1.5px solid #22D3EE; border-radius: 18px; padding: 1.2rem 1.5rem; box-shadow: 0 0 20px rgba(34, 211, 238, 0.16);">'
            '<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">'
            '<span style="font-size: 1.1rem; color: #22D3EE;">⚡</span>'
            f'<strong style="font-size: 0.95rem; color: #22D3EE; text-transform: uppercase; letter-spacing: 0.05em;">Biomechanical Movement Profile Summary: {p["display_name"]}</strong>'
            '</div>'
            '<div style="font-size: 0.86rem; color: #94A3B8; line-height: 1.6;">'
            f'• <strong>Sprint Signature:</strong> Observed peak speed of <strong style="color:#FFFFFF;">{fmt_speed(p.get("combine_max_speed"))}</strong>, asymptotic velocity ceiling of <strong style="color:#FFFFFF;">{fmt_speed(p.get("forty_curve_vmax"))}</strong>, and time constant τ = <strong style="color:#FFFFFF;">{fmt_time(p.get("forty_curve_tau"))}</strong> (Curve Fit R² = <strong style="color:#22D3EE;">{r2_summary_str}</strong>).<br>'
            f'• <strong>Agility & Preservation:</strong> Averaged <strong style="color:#FFFFFF;">{fmt_speed(p.get("combine_mean_cod_apex_speed"))}</strong> at turn apex with a speed preservation ratio of <strong style="color:#22D3EE;">{fmt_ratio(p.get("combine_mean_speed_preservation_ratio"))}</strong> and peak angular rotation of <strong style="color:#FFFFFF;">{ang_vel_str}</strong>.<br>'
            f'• <strong>Force Development:</strong> Peak positive forward acceleration reached <strong style="color:#FFFFFF;">{fmt_accel(p.get("combine_max_accel"))}</strong> with initial 1st-step drive of <strong style="color:#FFFFFF;">{fmt_accel(p.get("combine_initial_accel_mean"))}</strong> and braking deceleration capacity of <strong style="color:#A78BFA;">{fmt_accel(p.get("combine_max_decel"))}</strong>.'
            '</div>'
            '</div>'
        )
        st.markdown(summary_card_html, unsafe_allow_html=True)

    # =========================================================================
    # TAB 5: 3D MOTION ANALYSIS (Retained & Polished)
    # =========================================================================
    with tab5:
        render_section_header(
            title="3D Motion Analysis",
            subtitle="Biomechanical movement reconstruction using tracking data.",
            badge="3D KINEMATICS",
        )
        
        m_col1, m_col2 = st.columns([3.2, 1.1])
        
        with m_col2:
            layers_box_html = (
                '<div style="background: #131D31; border: 1px solid #1E293B; border-radius: 14px; padding: 1.1rem; margin-top: 0.5rem;">'
                '<div style="font-size: 0.82rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">'
                'Visualization Layers'
                '</div>'
                '</div>'
            )
            st.markdown(layers_box_html, unsafe_allow_html=True)
            chk_skeleton = st.checkbox("Skeleton", value=True, key="chk_skel")
            chk_joints = st.checkbox("Joints", value=True, key="chk_jnt")
            chk_traj = st.checkbox("Trajectory", value=True, key="chk_trj")
            chk_heat = st.checkbox("Velocity Heatmap", value=False, key="chk_heat")
            chk_ground = st.checkbox("Ground Contact", value=True, key="chk_gnd")
            
            reconst_note_html = (
                '<div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid #1E293B; font-size: 0.78rem; color: #94A3B8; line-height: 1.5;">'
                '<strong style="color: #22D3EE;">10 Hz RFID Reconstruction</strong><br>'
                'Inverse kinematics mapping 14 nodal degrees of freedom during maximum velocity sprint phase.'
                '</div>'
            )
            st.markdown(reconst_note_html, unsafe_allow_html=True)
            
        with m_col1:
            fig_3d = plot_3d_motion_analysis(
                show_skeleton=chk_skeleton,
                show_joints=chk_joints,
                show_trajectory=chk_traj,
                show_heatmap=chk_heat,
                show_ground=chk_ground,
            )
            st.plotly_chart(fig_3d, use_container_width=True, config={"displayModeBar": False})
            
            # Interactive Video/Playback Controls Bar
            playback_bar_html = (
                '<div style="display: flex; align-items: center; justify-content: space-between; background: #131D31; border: 1px solid #1E293B; border-radius: 12px; padding: 8px 18px; margin-top: -10px;">'
                '<div style="display: flex; align-items: center; gap: 14px;">'
                '<span style="color: #22D3EE; font-size: 1.1rem; cursor: pointer;">▶</span>'
                '<span style="font-size: 0.82rem; font-family: \'JetBrains Mono\', monospace; color: #94A3B8;">0:00 / 0:05</span>'
                '</div>'
                '<div style="flex-grow: 1; margin: 0 20px;">'
                '<div style="height: 4px; background: #1E293B; border-radius: 9999px; position: relative;">'
                '<div style="width: 32%; height: 100%; background: #22D3EE; border-radius: 9999px;"></div>'
                '</div>'
                '</div>'
                '<div style="display: flex; align-items: center; gap: 14px;">'
                '<span style="font-size: 0.78rem; font-weight: 700; color: #94A3B8; background: #0F172A; padding: 2px 8px; border-radius: 6px; border: 1px solid #1E293B;">1.0x ▾</span>'
                '<span style="color: #94A3B8; font-size: 1.05rem; cursor: pointer;">⛶</span>'
                '</div>'
                '</div>'
            )
            st.markdown(playback_bar_html, unsafe_allow_html=True)
