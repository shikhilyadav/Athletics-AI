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

    # Step 2: Four Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "1. Sprint Intelligence",
        "2. Change of Direction",
        "3. Acceleration & Deceleration",
        "4. Player Analysis",
    ])

    # =========================================================================
    # TAB 1: SPRINT INTELLIGENCE
    # =========================================================================
    with tab1:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        render_section_header(
            title="Mono-Exponential Sprint Curve Modeling",
            subtitle="Evaluating 10 Hz RFID velocity rise dynamics: v(t) = vmax × (1 - exp(-t/τ))",
            badge="10 HZ SPRINT FIT",
        )
        
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
                <div style="background: #F5F7F5; border-radius: 16px; padding: 1.2rem; border: 1px solid #E5E7E5; font-size: 0.82rem; color: #171917; line-height: 1.6;">
                    <strong style="font-size: 0.9rem;">Methodological Integrity Standards:</strong><br>
                    • <strong>Total Trials vs. 40yd Sprints:</strong> The Combine dataset contains <strong>6,310 trials</strong> across all drills. Only <strong>793 trials</strong> represent straight-line 40-yard dashes.<br>
                    • <strong>Asymptotic Vmax Parameter:</strong> <code>vmax</code> is an extrapolation ceiling parameter; it is not constrained to be the instantaneous peak speed reached during 40 yards.<br>
                    • <strong>Time Constant (τ):</strong> Reflects acceleration burst duration (smaller τ indicates steeper initial rise and earlier velocity plateau).<br>
                    • <strong>Convergence Caution:</strong> Do <em>not</em> treat algorithm convergence as proof of good fit. Five prospects converged with R² &lt; 0.95 due to stride stumble, early pull-up, or tracking noise.
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Interactive Prospect Sprint Curve Visualizer
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        render_section_header(
            title="Interactive Sprint Velocity Visualizer",
            subtitle="Inspect individual prospect modeled curves against observed sensor peaks and split times.",
            badge="INTERACTIVE KINEMATICS",
        )
        
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
        
        # Fit Tier Classification
        if r2_fit >= 0.98:
            fit_tier = "Exceptional (R² ≥ 0.98)"
            badge_color = "lime"
        elif r2_fit >= 0.95:
            fit_tier = "High Fit (R² ≥ 0.95)"
            badge_color = "lime"
        else:
            fit_tier = "Moderate/Low (R² < 0.95)"
            badge_color = "red"
            
        # KPI Row for Selected Prospect
        k1, k2, k3, k4, k5, k6 = st.columns(6)
        with k1:
            st.markdown(render_kpi_card_v2("40-Yard Time", fmt_time(forty_time), "Stopwatch"), unsafe_allow_html=True)
        with k2:
            st.markdown(render_kpi_card_v2("10-Yard Split", fmt_time(ten_split), "Initial Burst"), unsafe_allow_html=True)
        with k3:
            st.markdown(render_kpi_card_v2("Observed Peak", fmt_speed(obs_max_speed), "10 Hz Sensor"), unsafe_allow_html=True)
        with k4:
            st.markdown(render_kpi_card_v2("Asymptotic Vmax", fmt_speed(vmax_param), "Fitted Ceiling", highlight_lime=True), unsafe_allow_html=True)
        with k5:
            st.markdown(render_kpi_card_v2("Time Constant (τ)", fmt_time(tau_val), "Burst Rate"), unsafe_allow_html=True)
        with k6:
            st.markdown(render_kpi_card_v2("Goodness of Fit", f"{r2_fit:.4f}", fit_tier, highlight_lime=(r2_fit >= 0.98)), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # High-Fidelity Velocity Curve
        st.plotly_chart(plot_sprint_velocity_interactive(p_row), use_container_width=True)
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
            <div style="background: #F5F7F5; border-radius: 16px; padding: 1.2rem; border: 1px solid #E5E7E5; font-size: 0.82rem; color: #171917; line-height: 1.6; margin-top: 1rem;">
                <strong style="font-size: 0.9rem;">Measurement Definitions & Physical Boundaries:</strong><br>
                • <strong>Tangential Acceleration vs. Vector Norm:</strong> Tangential acceleration is the signed scalar derivative of speed along the athlete's movement path: <code>a_tangential = dv/dt</code>. 
                Do not confuse this with total acceleration vector norm <code>||a|| = √(ax² + ay²)</code>, which conflates forward propulsion with lateral turning centripetal acceleration.<br>
                • <strong>Theoretical Initial Drive <code>a(0) = vmax / τ</code>:</strong> Derived analytically from the mono-exponential velocity function at <code>t = 0</code>. Represents the maximum mechanical rate of speed acquisition at zero velocity.<br>
                • <strong>Positive Jerk Proxy (yd/s³):</strong> Computed as the mean positive first derivative of acceleration <code>da/dt</code> during the sprint initiation phase, serving as a kinematic proxy for rate of force development (RFD).<br>
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
            <div style="background: #FFFFFF; border: 1px solid #E5E7E5; border-radius: 20px; padding: 1.4rem 1.6rem; margin-bottom: 1.4rem; box-shadow: 0 4px 16px rgba(0,0,0,0.03);">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <div style="font-size: 1.7rem; font-weight: 800; color: #171917; letter-spacing: -0.03em; line-height: 1.1;">{p['display_name']}</div>
                        <div style="font-size: 0.88rem; font-weight: 600; color: #858B86; margin-top: 4px;">
                            {p['nfl_position'] or 'N/A'} • {p['college_name'] or 'Unknown College'} • Class of {int(p['draft_year']) if pd.notna(p['draft_year']) else '2023'}
                        </div>
                    </div>
                    <div style="display: flex; gap: 8px; align-items: center;">
                        {fit_badge}
                        <span class="pill-badge pill-badge-dark">{draft_info}</span>
                    </div>
                </div>
                <div style="display: flex; gap: 20px; margin-top: 1rem; padding-top: 0.8rem; border-top: 1px solid #F0F2F0; font-size: 0.82rem; color: #5B615C;">
                    <div><strong>Height:</strong> {fmt_dist_in(p.get('combine_height'))}</div>
                    <div><strong>Weight:</strong> {fmt_weight_lbs(p.get('combine_weight'))}</div>
                    <div><strong>Arm Length:</strong> {fmt_dist_in(p.get('arm_length'))}</div>
                    <div><strong>Hand Size:</strong> {fmt_dist_in(p.get('hand_size'))}</div>
                    <div><strong>Verified Scrimmage Snaps:</strong> {int(p['verified_scrimmage_snaps']) if pd.notna(p['verified_scrimmage_snaps']) else 0}</div>
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
            <div style="background: #FAFDF5; border: 1px solid #B8E64B; border-radius: 18px; padding: 1.2rem 1.5rem;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
                    <span style="font-size: 1rem;">⚡</span>
                    <strong style="font-size: 0.95rem; color: #171917;">Biomechanical Movement Profile Summary: {p['display_name']}</strong>
                </div>
                <div style="font-size: 0.85rem; color: #363B37; line-height: 1.6;">
                    • <strong>Sprint Signature:</strong> Reached an observed maximum speed of <strong>{fmt_speed(p.get('combine_max_speed'))}</strong> with an asymptotic modeled velocity of <strong>{fmt_speed(p.get('forty_curve_vmax'))}</strong> and time constant τ = <strong>{fmt_time(p.get('forty_curve_tau'))}</strong> (Curve Fit R² = <strong>{r2_summary_str}</strong>).<br>
                    • <strong>Agility & Preservation:</strong> Averaged <strong>{fmt_speed(p.get('combine_mean_cod_apex_speed'))}</strong> at turn apex with a speed preservation ratio of <strong>{fmt_ratio(p.get('combine_mean_speed_preservation_ratio'))}</strong> and peak angular velocity of <strong>{ang_vel_str}</strong>.<br>
                    • <strong>Force Development:</strong> Peak positive forward acceleration reached <strong>{fmt_accel(p.get('combine_max_accel'))}</strong> with initial drive of <strong>{fmt_accel(p.get('combine_initial_accel_mean'))}</strong> and braking deceleration of <strong>{fmt_accel(p.get('combine_max_decel'))}</strong>.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)
