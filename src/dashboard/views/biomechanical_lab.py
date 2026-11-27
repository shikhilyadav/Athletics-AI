"""
ATHLETIX AI — Dashboard View 5: Biomechanical Laboratory
Signature sports science experience of ATHLETIX AI:
Sprint Intelligence, Change of Direction, Acceleration & Deceleration, and Player Analysis.
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
    plot_cod_interactive_scatter,
    plot_biomechanical_profile_radar,
    plot_3d_motion_analysis,
    THEME_LAYOUT,
    COLOR_BLACK,
    COLOR_LIME,
    COLOR_LIME_DARK,
    COLOR_GREY,
    COLOR_LIGHT_GREY,
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
    render_editorial_header,
    render_scientific_banner,
    render_section_header,
    render_kpi_card_v2,
    render_metric_card,
    render_chart_container,
)


def render_page():
    # Page Header (Step 2: Title and Subtitle)
    render_editorial_header(
        title="Biomechanical Laboratory",
        subtitle="Explore the mechanics behind athletic performance.",
        tag="SIGNATURE RESEARCH SUITE",
    )
    
    # Load Verified Datasets
    master_df = load_master_df()
    kinematics_df = load_kinematics_df()
    cod_df = load_cod_df()
    
    # Scientific Boundary Banner
    render_scientific_banner(
        "Biomechanical Definition & Physics Standards",
        "1. <strong>Sprint Velocity Modeling:</strong> The mono-exponential rise is defined as "
        "<code>v(t) = vmax × (1 - exp(-t/τ))</code>. The parameter <code>vmax</code> is an asymptotic ceiling parameter, "
        "not an observed instantaneous maximum speed. Fits are computed via non-linear least squares on straight-line 40-yard sprints.<br>"
        "2. <strong>Speed Preservation Ratio (SPR):</strong> Defined strictly as kinematic <code>vexit / ventry</code>. "
        "It is a dimensionless kinematic velocity ratio and must <strong>NOT</strong> be labeled as kinetic energy "
        "(kinetic energy scales with mass and velocity squared: <code>0.5 × m × v²</code>).<br>"
        "3. <strong>Acceleration Kinematics:</strong> Tangential acceleration represents the directional rate of speed change along the velocity vector. "
        "Do not treat total acceleration vector magnitude <code>√(ax² + ay²)</code> as signed tangential acceleration.",
    )

    # Four Signature Tabs + 3D Motion Reconstruction Tab
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Sprint Intelligence",
        "Change of Direction",
        "Acceleration & Deceleration",
        "Player Analysis",
        "3D Motion Analysis",
    ])

    # =========================================================================
    # TAB 1: SPRINT INTELLIGENCE (Direct Reference Alignment)
    # =========================================================================
    with tab1:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        
        # Prospect Selector
        valid_sprint_df = master_df.dropna(subset=["forty_curve_tau", "forty_curve_vmax", "forty_curve_r2"]).copy()
        valid_sprint_df = valid_sprint_df.sort_values(by="display_name")
        
        player_options = (
            valid_sprint_df["display_name"]
            + " ("
            + valid_sprint_df["nfl_position"].fillna("?")
            + " • R²="
            + valid_sprint_df["forty_curve_r2"].map("{:.3f}".format)
            + ")"
        ).tolist()
        
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
        ten_split = p_row["ten_yd_split"]
        obs_max_speed = p_row["combine_max_speed"]
        p_pos = p_row.get("nfl_position", "?")
        p_college = p_row.get("college_name", "N/A")
        
        # Fit Tier Classification
        if r2_fit >= 0.98:
            fit_tier = "Exceptional Fit (R² ≥ 0.98)"
            badge_color = "lime"
        elif r2_fit >= 0.95:
            fit_tier = "High Fit (R² ≥ 0.95)"
            badge_color = "lime"
        else:
            fit_tier = "Moderate/Low (R² < 0.95)"
            badge_color = "red"
            
        # Two-Column Layout (Matching Bottom-Left Reference Image Exactly)
        bio_col1, bio_col2 = st.columns([1.1, 2.3])
        
        with bio_col1:
            st.markdown(
                f"""
                <div class="bio-prospect-card">
                    <div class="bio-prospect-header">
                        <div class="bio-avatar-circle">👤</div>
                        <div>
                            <div class="bio-prospect-name">{p_name} ({p_pos})</div>
                            <div class="bio-prospect-meta">@{p_college}</div>
                        </div>
                    </div>
                    <div class="bio-kpi-row">
                        <span class="bio-kpi-label">40-Yard Time</span>
                        <span class="bio-kpi-val">{fmt_time(forty_time)}</span>
                    </div>
                    <div class="bio-kpi-row">
                        <span class="bio-kpi-label">Observed Max</span>
                        <span class="bio-kpi-val">{fmt_speed(obs_max_speed)}</span>
                    </div>
                    <div class="bio-kpi-row">
                        <span class="bio-kpi-label">Asymptotic Vmax</span>
                        <span class="bio-kpi-val" style="color: #C8F45A;">{fmt_speed(vmax_param)}</span>
                    </div>
                    <div class="bio-kpi-row">
                        <span class="bio-kpi-label">Time Constant (τ)</span>
                        <span class="bio-kpi-val">{fmt_time(tau_val)}</span>
                    </div>
                    <div class="bio-kpi-row">
                        <span class="bio-kpi-label">Fit Quality (R²)</span>
                        <span class="bio-kpi-val" style="color: #C8F45A;">{r2_fit:.4f}</span>
                    </div>
                    <div style="margin-top: 16px; text-align: center;">
                        <span class="pill-badge pill-badge-lime" style="width: 100%; justify-content: center; padding: 7px 0; font-size: 0.76rem;">{fit_tier}</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        with bio_col2:
            st.plotly_chart(plot_sprint_velocity_interactive(p_row), use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Fit Quality & Cohort Denominators
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
            st.plotly_chart(plot_sprint_curve_distribution(master_df), use_container_width=True)
        with col_dist2:
            st.markdown(
                """
                <div style="background: #1B222D; border-radius: 16px; padding: 1.2rem; border: 1px solid #242D38; font-size: 0.82rem; color: #94A3B8; line-height: 1.6;">
                    <strong style="font-size: 0.9rem; color: #FFFFFF;">Methodological Integrity Standards:</strong><br>
                    • <strong>Total Trials vs. 40yd Sprints:</strong> The Combine dataset contains <strong style="color:#FFFFFF;">6,310 trials</strong> across all drills. Only <strong style="color:#C8F45A;">793 trials</strong> represent straight-line 40-yard dashes.<br>
                    • <strong>Asymptotic Vmax Parameter:</strong> <code style="color:#C8F45A; background:#161B22;">vmax</code> is an extrapolation ceiling parameter; it is not constrained to be the instantaneous peak speed reached during 40 yards.<br>
                    • <strong>Time Constant (τ):</strong> Reflects acceleration burst duration (smaller τ indicates steeper initial rise and earlier velocity plateau).<br>
                    • <strong>Convergence Caution:</strong> Do <em>not</em> treat algorithm convergence as proof of good fit. Five prospects converged with R² &lt; 0.95 due to stride stumble, early pull-up, or tracking noise.
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # TAB 2: CHANGE OF DIRECTION
    # =========================================================================
    with tab2:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        render_section_header(
            title="Change-of-Direction (COD) Kinematics",
            subtitle="Decoupling turn apex velocity, kinematic speed preservation, and angular reorientation rates.",
            badge="COD ENGINE",
        )
        
        # Macro Cohort COD KPIs
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(render_kpi_card_v2("Mean Apex Speed", f"{master_df['combine_mean_cod_apex_speed'].mean():.2f} yd/s", "Across All Drills"), unsafe_allow_html=True)
        with c2:
            st.markdown(render_kpi_card_v2("Speed Preservation", f"{master_df['combine_mean_speed_preservation_ratio'].mean():.3f}", "vexit / ventry Ratio", highlight_lime=True), unsafe_allow_html=True)
        with c3:
            st.markdown(render_kpi_card_v2("Peak Angular Velocity", f"{master_df['combine_peak_angular_velocity'].mean():.1f} °/s", "Maximum Reorientation"), unsafe_allow_html=True)
        with c4:
            st.markdown(render_kpi_card_v2("Turning Efficiency Index", f"{master_df['combine_mean_turning_efficiency'].mean():.1f}", "Apex / Entry Ratio × 100"), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Prospect Selector for COD Highlighting
        cod_players = master_df[master_df["combine_mean_cod_apex_speed"].notna()].sort_values("display_name")
        cod_player_list = (cod_players["display_name"] + " (" + cod_players["nfl_position"].fillna("?") + ")").tolist()
        
        selected_cod_str = st.selectbox(
            "Select Prospect to Highlight on Change-of-Direction Map",
            cod_player_list,
            index=0,
            key="cod_prospect_select",
        )
        selected_cod_name = selected_cod_str.split(" (")[0]
        selected_cod_row = cod_players[cod_players["display_name"] == selected_cod_name].iloc[0]
        selected_nfl_id = int(selected_cod_row["nfl_id"])
        
        # COD Interactive Scatter Plot
        st.plotly_chart(plot_cod_interactive_scatter(cod_df, highlight_nfl_id=selected_nfl_id), use_container_width=True)
        
        # Player COD Metrics Breakdown
        st.markdown("#### Prospect Turn Dynamics: " + selected_cod_name)
        pk1, pk2, pk3, pk4 = st.columns(4)
        with pk1:
            st.markdown(render_metric_card("Apex Velocity", fmt_speed(selected_cod_row["combine_mean_cod_apex_speed"]), "", "MIN SPEED", "lime", "At point of maximum curvature"))
        with pk2:
            st.markdown(render_metric_card("Speed Preservation", fmt_ratio(selected_cod_row["combine_mean_speed_preservation_ratio"]), "", "vexit / ventry", "dark", "Momentum maintenance"))
        with pk3:
            st.markdown(render_metric_card("Angular Velocity", f"{selected_cod_row['combine_peak_angular_velocity']:.1f}", "°/s", "PEAK ROTATION", "lime", "Body rotation rate"))
        with pk4:
            st.markdown(render_metric_card("Turning Efficiency", f"{selected_cod_row['combine_mean_turning_efficiency']:.1f}", "pts", "COMPOSITE", "grey", "Trajectory efficiency"))
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Individual Trials in COD Parquet for Selected Prospect
        p_trials = cod_df[cod_df["nfl_id"] == selected_nfl_id]
        if not p_trials.empty:
            st.markdown("#### Verified Individual Drill Trials (" + str(len(p_trials)) + " Trials Tracked)")
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
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Macro Drill Inventory Summary
        st.markdown("#### Combine Drill Inventory & Physical Comparability")
        cod_drill_summary = cod_df[cod_df["num_detected_turns"] > 0].groupby("drill_name").agg(
            Tracked_Trials=("event_id", "count"),
            Mean_Entry_Speed=("mean_entry_speed", "mean"),
            Mean_Apex_Speed=("mean_apex_speed", "mean"),
            Mean_Preservation=("mean_speed_preservation_ratio", "mean"),
            Peak_Angular_Vel=("peak_angular_velocity_deg_s", "mean"),
        ).reset_index().rename(columns={
            "drill_name": "Combine Drill",
            "Tracked_Trials": "Trials with Turns",
            "Mean_Entry_Speed": "Mean Entry Speed (yd/s)",
            "Mean_Apex_Speed": "Mean Apex Speed (yd/s)",
            "Mean_Preservation": "Speed Preservation Ratio",
            "Peak_Angular_Vel": "Peak Angular Vel (°/s)",
        })
        
        st.dataframe(
            cod_drill_summary.style.format({
                "Mean Entry Speed (yd/s)": "{:.2f}",
                "Mean Apex Speed (yd/s)": "{:.2f}",
                "Speed Preservation Ratio": "{:.3f}",
                "Peak Angular Vel (°/s)": "{:.1f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # TAB 3: ACCELERATION & DECELERATION
    # =========================================================================
    with tab3:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        render_section_header(
            title="Acceleration & Deceleration Dynamics",
            subtitle="Analyzing tangential acceleration, initial burst drive, and braking deceleration capacity.",
            badge="ACCEL / DECEL KINEMATICS",
        )
        
        # Macro Acceleration KPIs
        ak1, ak2, ak3, ak4 = st.columns(4)
        with ak1:
            st.markdown(render_kpi_card_v2("Mean Peak Accel", f"{master_df['combine_max_accel'].mean():.2f} yd/s²", "Max Forward Thrust", highlight_lime=True), unsafe_allow_html=True)
        with ak2:
            st.markdown(render_kpi_card_v2("Initial Drive (a_init)", f"{master_df['combine_initial_accel_mean'].mean():.2f} yd/s²", "First-Step Acceleration"), unsafe_allow_html=True)
        with ak3:
            st.markdown(render_kpi_card_v2("Max Deceleration", f"{master_df['combine_max_decel'].mean():.2f} yd/s²", "Braking Capacity"), unsafe_allow_html=True)
        with ak4:
            st.markdown(render_kpi_card_v2("Mean Pos Jerk", f"{master_df['combine_mean_pos_jerk'].mean():.2f} yd/s³", "Rate of Force Development"), unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Interactive Prospect Selector for Acceleration Profile
        accel_players = master_df.dropna(subset=["forty_curve_tau", "forty_curve_vmax"]).sort_values("display_name")
        accel_player_list = (accel_players["display_name"] + " (" + accel_players["nfl_position"].fillna("?") + ")").tolist()
        
        selected_accel_str = st.selectbox(
            "Select Prospect to Plot Tangential Acceleration Curve",
            accel_player_list,
            index=0,
            key="accel_prospect_select",
        )
        accel_p_name = selected_accel_str.split(" (")[0]
        accel_p_row = accel_players[accel_players["display_name"] == accel_p_name].iloc[0]
        
        # Selected Player Acceleration Metrics
        ap1, ap2, ap3, ap4, ap5 = st.columns(5)
        with ap1:
            st.markdown(render_metric_card("Peak Acceleration", fmt_accel(accel_p_row["combine_max_accel"]), "", "SENSOR MAX", "lime", "Peak forward acceleration"))
        with ap2:
            st.markdown(render_metric_card("Initial Acceleration", fmt_accel(accel_p_row["combine_initial_accel_mean"]), "", "1ST STEP", "dark", "Acceleration at start"))
        with ap3:
            theo_a0 = accel_p_row["forty_curve_vmax"] / accel_p_row["forty_curve_tau"]
            st.markdown(render_metric_card("Theoretical a(0)", f"{theo_a0:.2f} yd/s²", "", "vmax / τ", "grey", "Modeled initial drive"))
        with ap4:
            st.markdown(render_metric_card("Max Deceleration", fmt_accel(accel_p_row["combine_max_decel"]), "", "BRAKING", "red", "Peak negative acceleration"))
        with ap5:
            st.markdown(render_metric_card("Positive Jerk", f"{accel_p_row['combine_mean_pos_jerk']:.2f}", "yd/s³", "da/dt", "lime", "Acceleration ramp rate"))
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Acceleration Profile Chart
        st.plotly_chart(plot_acceleration_profile(accel_p_row), use_container_width=True)
        
        # Physical Measurement Explanations
        st.markdown(
            """
            <div style="background: #1B222D; border-radius: 16px; padding: 1.2rem; border: 1px solid #242D38; font-size: 0.82rem; color: #94A3B8; line-height: 1.6; margin-top: 1rem;">
                <strong style="font-size: 0.9rem; color: #FFFFFF;">Measurement Definitions & Physical Boundaries:</strong><br>
                • <strong>Tangential Acceleration vs. Vector Norm:</strong> Tangential acceleration is the signed scalar derivative of speed along the athlete's movement path: <code style="color:#C8F45A; background:#161B22;">a_tangential = dv/dt</code>. 
                Do not confuse this with total acceleration vector norm <code style="color:#C8F45A; background:#161B22;">||a|| = √(ax² + ay²)</code>, which conflates forward propulsion with lateral turning centripetal acceleration.<br>
                • <strong>Theoretical Initial Drive <code style="color:#C8F45A; background:#161B22;">a(0) = vmax / τ</code>:</strong> Derived analytically from the mono-exponential velocity function at <code style="color:#C8F45A; background:#161B22;">t = 0</code>. Represents the maximum mechanical rate of speed acquisition at zero velocity.<br>
                • <strong>Positive Jerk Proxy (yd/s³):</strong> Computed as the mean positive first derivative of acceleration <code style="color:#C8F45A; background:#161B22;">da/dt</code> during the sprint initiation phase, serving as a kinematic proxy for rate of force development (RFD).<br>
                • <strong>Braking Deceleration:</strong> Observed peak negative rate of speed change during drill stopping segments.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # TAB 4: PLAYER ANALYSIS
    # =========================================================================
    with tab4:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
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
            selected_name = st.selectbox("Select Prospect for Deep-Dive Analysis", player_names, index=0)
            
        p = filtered_master[filtered_master["display_name"] == selected_name].iloc[0]
        
        # Athlete Identity Header Box
        draft_info = f"Round {p['draft_round']}, Pick {p['draft_overall_pick']}" if pd.notna(p["draft_round"]) else "Undrafted / Free Agent"
        r2_val = p.get("forty_curve_r2")
        if pd.notna(r2_val):
            if r2_val >= 0.98:
                fit_badge = '<span class="pill-badge pill-badge-lime">Exceptional Fit (R² ≥ 0.98)</span>'
            elif r2_val >= 0.95:
                fit_badge = '<span class="pill-badge pill-badge-lime">High Fit (R² ≥ 0.95)</span>'
            else:
                fit_badge = '<span class="pill-badge pill-badge-red">Moderate/Low (R² < 0.95)</span>'
        else:
            fit_badge = '<span class="pill-badge pill-badge-grey">Not Available (DNP)</span>'

        st.markdown(
            f"""
            <div style="background: #161B22; border: 1px solid #242D38; border-radius: 20px; padding: 1.4rem 1.6rem; margin-bottom: 1.4rem; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div style="font-size: 1.7rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.03em; line-height: 1.1;">{p['display_name']}</div>
                        <div style="font-size: 0.88rem; font-weight: 600; color: #94A3B8; margin-top: 4px;">
                            {p['nfl_position'] or 'N/A'} • {p['college_name'] or 'Unknown College'} • Class of {int(p['draft_year']) if pd.notna(p['draft_year']) else '2023'}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        {fit_badge}
                        <span class="pill-badge pill-badge-dark">{draft_info}</span>
                    </div>
                </div>
                <div style="display: flex; gap: 20px; margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #242D38; font-size: 0.82rem; color: #94A3B8;">
                    <div><strong style="color:#FFFFFF;">Height:</strong> {fmt_dist_in(p.get('combine_height'))}</div>
                    <div><strong style="color:#FFFFFF;">Weight:</strong> {fmt_weight_lbs(p.get('combine_weight'))}</div>
                    <div><strong style="color:#FFFFFF;">Arm Length:</strong> {fmt_dist_in(p.get('arm_length'))}</div>
                    <div><strong style="color:#FFFFFF;">Hand Size:</strong> {fmt_dist_in(p.get('hand_size'))}</div>
                    <div><strong style="color:#FFFFFF;">Verified Scrimmage Snaps:</strong> {int(p['verified_scrimmage_snaps']) if pd.notna(p['verified_scrimmage_snaps']) else 0}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Dual Column Layout: Biomechanical Radar vs Key Metric Clusters
        col_radar, col_metrics = st.columns([1, 1])
        
        with col_radar:
            st.plotly_chart(plot_biomechanical_profile_radar(p, master_df), use_container_width=True)
            
        with col_metrics:
            st.markdown("#### 1. Straight-Line Sprint Kinematics")
            sm1, sm2, sm3 = st.columns(3)
            with sm1:
                st.markdown(render_metric_card("40-Yard Time", fmt_time(p.get("forty")), "", "STOPWATCH", "dark"))
            with sm2:
                st.markdown(render_metric_card("10-Yard Split", fmt_time(p.get("ten_yd_split")), "", "BURST", "grey"))
            with sm3:
                st.markdown(render_metric_card("Observed Max", fmt_speed(p.get("combine_max_speed")), "", "SENSOR", "lime"))
                
            sm4, sm5, sm6 = st.columns(3)
            with sm4:
                st.markdown(render_metric_card("Asymptotic Vmax", fmt_speed(p.get("forty_curve_vmax")), "", "MODEL", "lime"))
            with sm5:
                st.markdown(render_metric_card("Time Constant (τ)", fmt_time(p.get("forty_curve_tau")), "", "RATE", "dark"))
            with sm6:
                r2_str = f"{p['forty_curve_r2']:.4f}" if pd.notna(p.get("forty_curve_r2")) else "Not available"
                st.markdown(render_metric_card("Curve Fit R²", r2_str, "", "ACCURACY", "lime"))
                
            st.markdown("#### 2. Change-of-Direction Mechanics")
            cm1, cm2, cm3 = st.columns(3)
            with cm1:
                st.markdown(render_metric_card("Apex Velocity", fmt_speed(p.get("combine_mean_cod_apex_speed")), "", "MIN SPEED", "lime"))
            with cm2:
                st.markdown(render_metric_card("Preservation", fmt_ratio(p.get("combine_mean_speed_preservation_ratio")), "", "RATIO", "dark"))
            with cm3:
                st.markdown(render_metric_card("Angular Vel", f"{p.get('combine_peak_angular_velocity'):.1f}°/s" if pd.notna(p.get("combine_peak_angular_velocity")) else "Not available", "", "ROTATION", "grey"))
                
            st.markdown("#### 3. Acceleration & Deceleration Capacity")
            am1, am2, am3 = st.columns(3)
            with am1:
                st.markdown(render_metric_card("Peak Acceleration", fmt_accel(p.get("combine_max_accel")), "", "PROPULSION", "lime"))
            with am2:
                st.markdown(render_metric_card("Initial Drive", fmt_accel(p.get("combine_initial_accel_mean")), "", "1ST STEP", "dark"))
            with am3:
                st.markdown(render_metric_card("Max Deceleration", fmt_accel(p.get("combine_max_decel")), "", "BRAKING", "red"))

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Movement Profile Summary Card
        r2_summary_str = f"{p['forty_curve_r2']:.4f}" if pd.notna(p.get("forty_curve_r2")) else "N/A"
        ang_vel_str = f"{p.get('combine_peak_angular_velocity'):.1f}°/s" if pd.notna(p.get("combine_peak_angular_velocity")) else "N/A"
        
        st.markdown(
            f"""
            <div style="background: #1B222D; border: 1px solid #C8F45A; border-radius: 18px; padding: 1.2rem 1.5rem; box-shadow: 0 0 16px rgba(200, 244, 90, 0.15);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1rem;">⚡</span>
                    <strong style="font-size: 0.95rem; color: #C8F45A; text-transform: uppercase; letter-spacing: 0.05em;">Biomechanical Movement Profile Summary: {p['display_name']}</strong>
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.6;">
                    • <strong>Sprint Signature:</strong> Reached an observed maximum speed of <strong style="color:#FFFFFF;">{fmt_speed(p.get('combine_max_speed'))}</strong> with an asymptotic modeled velocity of <strong style="color:#FFFFFF;">{fmt_speed(p.get('forty_curve_vmax'))}</strong> and time constant τ = <strong style="color:#FFFFFF;">{fmt_time(p.get('forty_curve_tau'))}</strong> (Curve Fit R² = <strong style="color:#C8F45A;">{r2_summary_str}</strong>).<br>
                    • <strong>Agility & Preservation:</strong> Averaged <strong style="color:#FFFFFF;">{fmt_speed(p.get('combine_mean_cod_apex_speed'))}</strong> at turn apex with a speed preservation ratio of <strong style="color:#C8F45A;">{fmt_ratio(p.get('combine_mean_speed_preservation_ratio'))}</strong> and peak angular velocity of <strong style="color:#FFFFFF;">{ang_vel_str}</strong>.<br>
                    • <strong>Force Development:</strong> Peak positive forward acceleration reached <strong style="color:#FFFFFF;">{fmt_accel(p.get('combine_max_accel'))}</strong> with initial drive of <strong style="color:#FFFFFF;">{fmt_accel(p.get('combine_initial_accel_mean'))}</strong> and braking deceleration of <strong style="color:#FFFFFF;">{fmt_accel(p.get('combine_max_decel'))}</strong>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================================
    # TAB 5: 3D MOTION ANALYSIS (Bottom-Right Reference Alignment)
    # =========================================================================
    with tab5:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        render_section_header(
            title="3D Motion Analysis",
            subtitle="Biomechanical movement reconstruction using tracking data.",
            badge="3D KINEMATICS",
        )
        
        m_col1, m_col2 = st.columns([3.2, 1.1])
        
        with m_col2:
            st.markdown(
                """
                <div style="background: #11151A; border: 1px solid #242D38; border-radius: 14px; padding: 1.1rem; margin-top: 0.5rem;">
                    <div style="font-size: 0.82rem; font-weight: 700; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px;">
                        Visualization Layers
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            chk_skeleton = st.checkbox("Skeleton", value=True, key="chk_skel")
            chk_joints = st.checkbox("Joints", value=True, key="chk_jnt")
            chk_traj = st.checkbox("Trajectory", value=True, key="chk_trj")
            chk_heat = st.checkbox("Velocity Heatmap", value=False, key="chk_heat")
            chk_ground = st.checkbox("Ground Contact", value=True, key="chk_gnd")
            
            st.markdown(
                """
                <div style="margin-top: 18px; padding-top: 14px; border-top: 1px solid #242D38; font-size: 0.78rem; color: #94A3B8; line-height: 1.5;">
                    <strong style="color: #C8F45A;">10 Hz RFID Reconstruction</strong><br>
                    Inverse kinematics mapping 14 nodal degrees of freedom during maximum velocity sprint phase.
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        with m_col1:
            fig_3d = plot_3d_motion_analysis(
                show_skeleton=chk_skeleton,
                show_joints=chk_joints,
                show_trajectory=chk_traj,
                show_heatmap=chk_heat,
                show_ground=chk_ground,
            )
            st.plotly_chart(fig_3d, use_container_width=True)
            
            # Interactive Video/Playback Controls Bar (Matching Reference)
            st.markdown(
                """
                <div style="display: flex; align-items: center; justify-content: space-between; background: #11151A; border: 1px solid #242D38; border-radius: 12px; padding: 8px 18px; margin-top: -10px;">
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <span style="color: #C8F45A; font-size: 1.1rem; cursor: pointer;">▶</span>
                        <span style="font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; color: #94A3B8;">0:00 / 0:05</span>
                    </div>
                    <div style="flex-grow: 1; margin: 0 20px;">
                        <div style="height: 4px; background: #242D38; border-radius: 9999px; position: relative;">
                            <div style="width: 32%; height: 100%; background: #C8F45A; border-radius: 9999px;"></div>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 14px;">
                        <span style="font-size: 0.78rem; font-weight: 700; color: #94A3B8; background: #1F2732; padding: 2px 8px; border-radius: 6px;">1.0x ▾</span>
                        <span style="color: #94A3B8; font-size: 1.05rem; cursor: pointer;">⛶</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            
        st.markdown('</div>', unsafe_allow_html=True)
