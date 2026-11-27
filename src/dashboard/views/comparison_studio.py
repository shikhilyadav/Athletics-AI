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
    
    # Defaults: Will Anderson Jr. vs. Lukas Van Ness (matching reference image)
    default_p1_idx = 0
    default_p2_idx = min(1, len(all_player_labels) - 1)
    
    for i, lbl in enumerate(all_player_labels):
        if "Will Anderson" in lbl or "Anderson" in lbl:
            default_p1_idx = i
            break
            
    for i, lbl in enumerate(all_player_labels):
        if "Van Ness" in lbl:
            default_p2_idx = i
            break
            
    sel_col1, sel_mid, sel_col2 = st.columns([10, 1, 10])
    with sel_col1:
        p1_label = st.selectbox("Select Athlete 1 (Baseline)", all_player_labels, index=default_p1_idx)
    with sel_mid:
        st.markdown('<div style="text-align: center; font-size: 1.5rem; margin-top: 1.8rem; color: #C8F45A;">⇄</div>', unsafe_allow_html=True)
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
            <div style="background: #161B22; border: 1px solid #242D38; border-radius: 18px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem; box-shadow: 0 8px 24px rgba(0,0,0,0.35);">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div class="bio-avatar-circle">👤</div>
                    <div style="flex-grow: 1;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em;">
                            ATHLETE 1 • {p1['nfl_position']} (BASELINE)
                        </div>
                        <div style="font-size: 1.55rem; font-weight: 800; letter-spacing: -0.03em; color: #FFFFFF;">
                            {p1['display_name']}
                        </div>
                        <div style="color: #94A3B8; font-size: 0.82rem;">
                            {p1['college_name']} • {pick1}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="pill-badge pill-badge-lime">40yd: {fmt_time(p1['forty'])}</span>
                    </div>
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
            <div style="background: linear-gradient(135deg, rgba(200, 244, 90, 0.09) 0%, #161B22 100%); border: 1.5px solid #C8F45A; border-radius: 18px; padding: 1.2rem 1.5rem; margin-bottom: 1.2rem; box-shadow: 0 0 20px rgba(200, 244, 90, 0.15);">
                <div style="display: flex; align-items: center; gap: 14px;">
                    <div class="bio-avatar-circle" style="border-color: #A78BFA;">👤</div>
                    <div style="flex-grow: 1;">
                        <div style="font-size: 0.72rem; font-weight: 700; color: #C8F45A; text-transform: uppercase; letter-spacing: 0.08em;">
                            ATHLETE 2 • {p2['nfl_position']} (CHALLENGER)
                        </div>
                        <div style="font-size: 1.55rem; font-weight: 800; letter-spacing: -0.03em; color: #FFFFFF;">
                            {p2['display_name']}
                        </div>
                        <div style="color: #94A3B8; font-size: 0.82rem;">
                            {p2['college_name']} • {pick2}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="pill-badge pill-badge-lime" style="background:#A78BFA; color:#0B0E11;">40yd: {fmt_time(p2['forty'])}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Visual Comparison Studio: Radar Chart on Left vs Head-to-Head Table on Right (Matching Image)
    r_col1, r_col2 = st.columns([1, 1])
    
    with r_col1:
        st.markdown('<div class="athletix-card" style="height: 100%;">', unsafe_allow_html=True)
        st.plotly_chart(plot_radar_comparison(p1, p2, df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with r_col2:
        st.markdown('<div class="athletix-card" style="height: 100%;">', unsafe_allow_html=True)
        
        p1_short = p1['display_name'].split()[-1]
        p2_short = p2['display_name'].split()[-1]
        
        comparison_metrics = [
            ("40-Yard Dash (s)", "forty", fmt_time, True),
            ("Vertical Jump (in)", "vertical", fmt_dist_in, False),
            ("Broad Jump (in)", "broad_jump", fmt_dist_in, False),
            ("Max Speed (yd/s)", "combine_max_speed", fmt_speed, False),
            ("COD Apex Speed (yd/s)", "combine_mean_cod_apex_speed", fmt_speed, False),
            ("Speed Preservation", "combine_mean_speed_preservation_ratio", fmt_ratio, False),
            ("Athletic Alpha (yd/s)", "athletic_alpha_raw", lambda x: f"{x:+.2f}" if pd.notna(x) else "N/A", False),
        ]
        
        table_html = f"""
        <table style="width: 100%; border-collapse: collapse; font-size: 0.86rem; color: #FFFFFF;">
            <thead>
                <tr style="border-bottom: 1px solid #242D38; color: #94A3B8; font-size: 0.76rem; text-transform: uppercase;">
                    <th style="text-align: left; padding: 10px 8px;">Metric</th>
                    <th style="text-align: center; padding: 10px 8px; color: #C8F45A;">{p1_short}</th>
                    <th style="text-align: center; padding: 10px 8px; color: #A78BFA;">{p2_short}</th>
                    <th style="text-align: right; padding: 10px 8px;">Δ (A - B)</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for label, col, fmt_func, lower_is_better in comparison_metrics:
            v1 = p1.get(col)
            v2 = p2.get(col)
            
            delta_str = "—"
            delta_color = "#94A3B8"
            if pd.notna(v1) and pd.notna(v2):
                diff = v1 - v2
                delta_str = f"{diff:+.2f}"
                if (diff > 0 and not lower_is_better) or (diff < 0 and lower_is_better):
                    delta_color = "#C8F45A"
                elif diff != 0:
                    delta_color = "#A78BFA"
            
            is_alpha = (col == "athletic_alpha_raw")
            if is_alpha:
                row_style = "background: #C8F45A; color: #0B0E11; font-weight: 800; border-radius: 8px;"
                cell_style = "padding: 10px 8px; color: #0B0E11; font-weight: 800;"
            else:
                row_style = "border-bottom: 1px solid #1C232B;"
                cell_style = "padding: 9px 8px;"
                
            table_html += f"""
                <tr style="{row_style}">
                    <td style="{cell_style} text-align: left;">{label}</td>
                    <td style="{cell_style} text-align: center;">{fmt_func(v1)}</td>
                    <td style="{cell_style} text-align: center;">{fmt_func(v2)}</td>
                    <td style="{cell_style} text-align: right; {f'color:{delta_color};' if not is_alpha else ''}">{delta_str}</td>
                </tr>
            """
            
        table_html += """
            </tbody>
        </table>
        """
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    render_scientific_banner(
        "Scientific & Normalization Methodology",
        "1. All comparative data points are loaded strictly from verified Combine sensor feeds and official competition files. "
        "Missing test results indicate drills the athlete did not attempt at the Combine; under no circumstances are missing values estimated or fabricated. "
        "2. Delta indicators (Athlete 2 minus Athlete 1) reflect pure observed physical differences. "
        "3. Athletic Alpha is model-relative and quantifies in-game translation relative to traditional Combine projections."
    )
