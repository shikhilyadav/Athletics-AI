"""
ATHLETIX AI — Dashboard View 2: Prospect Explorer
Clean NFL prospect discovery interface with minimalist light-grey background,
white rounded cards, lime accents (#C8F45A), and deep black typography (#171917).
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_master_df, load_athletic_alpha, load_game_tracking_df
from src.dashboard.metrics import (
    fmt_speed,
    fmt_accel,
    fmt_time,
    fmt_ratio,
    fmt_pct,
    fmt_dist_in,
    fmt_weight_lbs,
)
from src.dashboard.components import (
    render_editorial_header,
    render_scientific_banner,
)


def render_page():
    render_editorial_header(
        title="NFL Scouting Prospect Explorer",
        subtitle="Search, filter, and inspect verified Combine test measurements and 10 Hz sensor kinematics across 510 attendees.",
        tag="PROSPECT INTELLIGENCE",
    )
    
    master_df = load_master_df()
    alpha_df = load_athletic_alpha()
    game_df = load_game_tracking_df()
    
    if master_df.empty:
        st.error("Player master dataset could not be loaded.")
        return

    # Merge alpha data if available
    df = master_df.copy()
    if not alpha_df.empty:
        alpha_sub = alpha_df[["nfl_id", "athletic_alpha_raw", "athletic_alpha_zscore", "athletic_alpha_tier"]]
        df = df.merge(alpha_sub, on="nfl_id", how="left")
        
    # Merge active_movement_frames from game tracking if available
    if not game_df.empty:
        game_sub = game_df[["nfl_id", "active_movement_frames"]]
        df = df.merge(game_sub, on="nfl_id", how="left")

    # Filter Bar Container
    st.markdown('<div class="dark-card" style="padding: 1.2rem 1.6rem;">', unsafe_allow_html=True)
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    
    with f_col1:
        search_query = st.text_input("🔍 Search Name, College, or NFL ID", placeholder="e.g. Flowers, Wright, Tennessee, 55867")
    with f_col2:
        pos_list = ["All Positions"] + sorted(df["nfl_position"].dropna().unique().tolist())
        selected_pos = st.selectbox("Position", pos_list)
    with f_col3:
        cohort_filter = st.selectbox(
            "Research Cohort Status",
            ["All Prospects (510)", "Primary Cohort (≥50 Snaps, 149)", "Untracked in 2023 Games (354)"]
        )
    with f_col4:
        draft_options = ["All Draft Statuses", "Drafted (Rounds 1-7)", "Undrafted (UDFA)"]
        selected_draft = st.selectbox("Draft Status", draft_options)
    st.markdown('</div>', unsafe_allow_html=True)

    # Apply filters
    filtered_df = df.copy()
    
    if search_query:
        q = search_query.strip().lower()
        filtered_df = filtered_df[
            filtered_df["display_name"].astype(str).str.lower().str.contains(q) |
            filtered_df["nfl_id"].astype(str).str.contains(q) |
            filtered_df["college_name"].astype(str).str.lower().str.contains(q)
        ]
        
    if selected_pos != "All Positions":
        filtered_df = filtered_df[filtered_df["nfl_position"] == selected_pos]
        
    if cohort_filter == "Primary Cohort (≥50 Snaps, 149)":
        filtered_df = filtered_df[filtered_df["is_eligible_50_snaps"] == True]
    elif cohort_filter == "Untracked in 2023 Games (354)":
        filtered_df = filtered_df[filtered_df["game_target_cohort_status"] != "2023_EVALUATED_ROOKIE"]
        
    if selected_draft == "Drafted (Rounds 1-7)":
        filtered_df = filtered_df[filtered_df["draft_round"].notna()]
    elif selected_draft == "Undrafted (UDFA)":
        filtered_df = filtered_df[filtered_df["draft_round"].isna()]

    st.markdown(
        f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; margin-top: 1rem;">
            <span style="font-size: 0.85rem; font-weight: 800; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.06em;">PROSPECT ROSTER</span>
            <span class="pill-badge pill-badge-lime">Showing {len(filtered_df)} of {len(df)} Prospects</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Display Master Roster Table with Custom Column Formatting
    display_cols = [
        "display_name", "nfl_position", "college_name",
        "draft_round", "draft_overall_pick", "forty", "combine_max_speed",
        "game_speed_p95", "verified_scrimmage_snaps"
    ]
    if "athletic_alpha_raw" in filtered_df.columns:
        display_cols.append("athletic_alpha_raw")

    df_table = filtered_df[display_cols].copy()
    df_table["draft_round"] = df_table["draft_round"].apply(lambda x: f"R{int(x)}" if pd.notna(x) else "UDFA")

    column_config = {
        "display_name": st.column_config.TextColumn("Player Name", width="medium"),
        "nfl_position": st.column_config.TextColumn("Pos", width="small"),
        "college_name": st.column_config.TextColumn("College", width="medium"),
        "draft_round": st.column_config.TextColumn("Round", width="small"),
        "draft_overall_pick": st.column_config.NumberColumn("Pick #", width="small", format="#%d"),
        "forty": st.column_config.NumberColumn("40yd Dash", width="small", format="%.2f s"),
        "combine_max_speed": st.column_config.NumberColumn("Max Sensor", width="small", format="%.2f yd/s"),
        "game_speed_p95": st.column_config.NumberColumn("Game P95", width="small", format="%.2f yd/s"),
        "verified_scrimmage_snaps": st.column_config.NumberColumn(
            "Career Snaps (23–25)",
            width="medium",
            format="%d",
            help="Total verified scrimmage snaps across 2023-2025 player_play.csv"
        ),
        "athletic_alpha_raw": st.column_config.NumberColumn(
            "Athletic Alpha",
            width="small",
            format="%+.2f yd/s",
            help="Out-of-fold residual speed delta (y - ŷ_ModelA)"
        ),
    }

    st.dataframe(
        df_table,
        column_config=column_config,
        use_container_width=True,
        height=340,
        hide_index=True,
    )
    st.caption("ℹ️ *Note: 'Career Snaps (23–25)' represents verified non-nullified scrimmage snaps across the 2023–2025 seasons in player_play.csv. All 149 primary cohort prospects met the ≥50 verified snap threshold.*")

    # Detailed Player Card Inspector
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="dark-card">', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #FFFFFF; font-weight: 800; font-size: 1.3rem; margin-bottom: 1.2rem;'>📋 Prospect Biomechanical & Performance Dossier</h3>", unsafe_allow_html=True)

    if filtered_df.empty:
        st.info("No prospects match the filter criteria.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    # Select player to inspect
    player_options = filtered_df["display_name"] + " (" + filtered_df["nfl_id"].astype(str) + " - " + filtered_df["nfl_position"].fillna("?") + " - " + filtered_df["college_name"].fillna("N/A") + ")"
    selected_player_str = st.selectbox("Select Prospect for Deep-Dive Inspection", player_options)
    
    selected_nfl_id = int(selected_player_str.split("(")[1].split(" -")[0])
    p = df[df["nfl_id"] == selected_nfl_id].iloc[0]

    # Player Header Dossier
    dossier_col1, dossier_col2, dossier_col3 = st.columns([2, 2, 2])
    with dossier_col1:
        st.markdown(f"<h2 style='color: #FFFFFF; font-weight: 900; margin: 0 0 6px 0;'>{p['display_name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"**Position:** <span style='color: #C8F45A; font-weight: 700;'>{p['nfl_position']}</span> (Combine: {p['combine_position']})", unsafe_allow_html=True)
        st.markdown(f"**College:** {p['college_name']} ({p.get('college_conference', 'N/A')})")
        pick_str = f"Round {int(p['draft_round'])}, Pick #{int(p['draft_overall_pick'])}" if pd.notna(p['draft_round']) else "Undrafted Free Agent (UDFA)"
        st.markdown(f"**Draft Selection:** {pick_str}")
        
    with dossier_col2:
        st.markdown("<h4 style='color: #FFFFFF;'>Physical Measurements</h4>", unsafe_allow_html=True)
        st.markdown(f"**Height:** {p['combine_height']} inches")
        st.markdown(f"**Weight:** {fmt_weight_lbs(p['combine_weight'])}")
        st.markdown(f"**Arm Length:** {fmt_dist_in(p['arm_length'])}")
        st.markdown(f"**Hand Size:** {fmt_dist_in(p['hand_size'])}")

    with dossier_col3:
        st.markdown("<h4 style='color: #FFFFFF;'>NFL Tracking & Opportunity</h4>", unsafe_allow_html=True)
        snap_val = int(p['verified_scrimmage_snaps']) if pd.notna(p['verified_scrimmage_snaps']) else 0
        st.markdown(f"**Career Scrimmage Snaps (23–25):** {snap_val:,} snaps")
        if pd.notna(p.get("active_movement_frames")):
            st.markdown(f"**2023 Active Tracking Frames:** {int(p['active_movement_frames']):,} frames")
        st.markdown(f"**Primary Cohort Status:** {'✅ Eligible (≥50 Snaps)' if p['is_eligible_50_snaps'] else '❌ Ineligible (<50 Snaps)'}")
        if pd.notna(p.get("athletic_alpha_raw")):
            alpha_val = p["athletic_alpha_raw"]
            st.markdown(f"**Athletic Alpha:** <span style='font-size:1.15rem; font-weight:800; color:#0B0E11; background:#C8F45A; padding:2px 8px; border-radius:6px;'>{alpha_val:+.2f} yd/s</span>", unsafe_allow_html=True)
            st.caption(f"Tier: {p.get('athletic_alpha_tier', 'N/A')}")
        else:
            st.markdown("**Athletic Alpha:** *Unavailable (Outside Primary Cohort)*")

    # Detailed 3-Pillar Breakdown
    st.markdown("<br>", unsafe_allow_html=True)
    pillar1, pillar2, pillar3 = st.columns(3)

    with pillar1:
        st.markdown("<h5 style='color: #C8F45A;'>1. Traditional Combine Drills</h5>", unsafe_allow_html=True)
        st.markdown(f"- **40-Yard Dash:** {fmt_time(p['forty'])}")
        st.markdown(f"- **10-Yard Split:** {fmt_time(p['ten_yd_split'])}")
        st.markdown(f"- **Vertical Jump:** {fmt_dist_in(p['vertical'])}")
        st.markdown(f"- **Broad Jump:** {fmt_dist_in(p['broad_jump'])}")
        st.markdown(f"- **3-Cone Drill:** {fmt_time(p['three_cone'])}")
        st.markdown(f"- **20-Yard Shuttle:** {fmt_time(p['short_shuttle'])}")
        st.markdown(f"- **Bench Press:** {int(p['bench_reps']) if pd.notna(p['bench_reps']) else 'N/A'} reps")

    with pillar2:
        st.markdown("<h5 style='color: #C8F45A;'>2. Sensor Kinematics & COD</h5>", unsafe_allow_html=True)
        st.markdown(f"- **Max Sensor Speed:** {fmt_speed(p['combine_max_speed'])}")
        st.markdown(f"- **Mean Sensor Speed:** {fmt_speed(p['combine_mean_speed'])}")
        st.markdown(f"- **Max Acceleration:** {fmt_accel(p['combine_max_accel'])}")
        st.markdown(f"- **Mean Positive Jerk:** {p['combine_mean_pos_jerk']:.2f} yd/s³" if pd.notna(p['combine_mean_pos_jerk']) else "- **Mean Positive Jerk:** N/A")
        st.markdown(f"- **COD Apex Speed:** {fmt_speed(p['combine_mean_cod_apex_speed'])}")
        st.markdown(f"- **Speed Preservation Ratio:** {fmt_ratio(p['combine_mean_speed_preservation_ratio'])}")
        st.markdown(f"- **Peak Angular Velocity:** {p['combine_peak_angular_velocity']:.1f}°/s" if pd.notna(p['combine_peak_angular_velocity']) else "- **Peak Angular Velocity:** N/A")

    with pillar3:
        st.markdown("<h5 style='color: #C8F45A;'>3. Regular-Season Tracking (2023)</h5>", unsafe_allow_html=True)
        st.markdown(f"- **Game 95th Pct Speed:** {fmt_speed(p['game_speed_p95'])}")
        st.markdown(f"- **Game 99th Pct Speed:** {fmt_speed(p['game_speed_p99'])}")
        st.markdown(f"- **Game Max Speed:** {fmt_speed(p['game_speed_max'])}")
        st.markdown(f"- **High-Speed Running %:** {fmt_pct(p['high_speed_running_fraction'])}")
        st.markdown(f"- **Sprint Curve Tau (τ):** {fmt_time(p['forty_curve_tau'])}")
        st.markdown(f"- **Sprint Curve Asymptotic Vmax:** {fmt_speed(p['forty_curve_vmax'])}")
        st.markdown(f"- **Sprint Curve Fit Quality R²:** {p['forty_curve_r2']:.4f}" if pd.notna(p['forty_curve_r2']) else "- **Sprint Curve Fit:** Not Fitted")

    st.markdown('</div>', unsafe_allow_html=True)
    
    render_scientific_banner(
        "Data Traceability Notice",
        f"All metrics for {p['display_name']} are loaded directly from data/processed/combine_player_master.parquet and verified source files. "
        "Missing values indicate tests not attempted at the Combine or lack of regular-season snaps. No values are estimated or imputed in this view."
    )
