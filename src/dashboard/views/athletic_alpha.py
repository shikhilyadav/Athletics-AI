"""
ATHLETIX AI — Dashboard View 4: Athletic Alpha Explorer
Leaderboards, residual decomposition, and unconfounded athletic translation analysis
with minimalist light-grey background, white rounded cards, and lime accents (#C8F45A).
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_athletic_alpha
from src.dashboard.charts import plot_alpha_scatter, plot_alpha_position_box
from src.dashboard.components import (
    render_editorial_header,
    render_scientific_banner,
    render_kpi_card_v2,
)


def render_page():
    render_editorial_header(
        title="Athletic Alpha: Residual Translation Intelligence",
        subtitle="Decomposing the delta between observed NFL game tracking speed and traditional Combine projections.",
        tag="RESIDUAL INTELLIGENCE",
    )
    
    alpha_df = load_athletic_alpha()
    
    if alpha_df.empty:
        st.error("Athletic Alpha residuals dataset not found.")
        return

    # Critical Scientific Definition & Non-Causal Banner
    render_scientific_banner(
        "Scientific Definition & Non-Causal Boundary",
        "Athletic Alpha represents the difference between observed regular-season game-tracking performance (95th percentile speed) "
        "and a traditional Combine model's out-of-fold prediction: α = y - ŷ_ModelA. "
        "It is strictly model-relative and does not establish hidden athletic potential, guaranteed draft value, or causality. "
        "Players with negative residuals are not 'busts', and players with positive residuals are not guaranteed 'steals'—"
        "residuals reflect game context, offensive scheme, pursuit angles, and unmodeled biomechanical factors."
    )

    # Top KPI Summary Cards
    mean_alpha = alpha_df["athletic_alpha_raw"].mean()
    std_alpha = alpha_df["athletic_alpha_raw"].std()
    high_outperformers = len(alpha_df[alpha_df["athletic_alpha_zscore"] >= 1.0])
    high_underperformers = len(alpha_df[alpha_df["athletic_alpha_zscore"] <= -1.0])
    
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(render_kpi_card_v2("Mean Alpha", f"{mean_alpha:.4f} yd/s", "Strictly Mean-Zero Residual"), unsafe_allow_html=True)
    with k2:
        st.markdown(render_kpi_card_v2("Residual Std Dev", f"{std_alpha:.4f} yd/s", "Cross-Cohort Spread"), unsafe_allow_html=True)
    with k3:
        st.markdown(render_kpi_card_v2("High Overperformers", f"{high_outperformers}", "Z ≥ +1.00", highlight_lime=True), unsafe_allow_html=True)
    with k4:
        st.markdown(render_kpi_card_v2("High Underperformers", f"{high_underperformers}", "Z ≤ -1.00"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Interactive Visualizations inside Rounded Card Containers
    sc_col1, sc_col2 = st.columns([3, 2])
    with sc_col1:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_alpha_scatter(alpha_df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with sc_col2:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.plotly_chart(plot_alpha_position_box(alpha_df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Filters Bar
    st.markdown('<div class="athletix-card" style="padding: 1.2rem 1.6rem;">', unsafe_allow_html=True)
    st.markdown("#### Filter Athletic Alpha Leaderboards")
    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        search_query = st.text_input("Search Name or NFL ID", placeholder="e.g. Dell, Smith, 55867", key="alpha_search")
    with f_col2:
        pos_list = ["All Positions"] + sorted(alpha_df["nfl_position"].dropna().unique().tolist())
        selected_pos = st.selectbox("Position Filter", pos_list, key="alpha_pos")
    with f_col3:
        tier_list = ["All Tiers"] + sorted(alpha_df["athletic_alpha_tier"].dropna().unique().tolist())
        selected_tier = st.selectbox("Athletic Alpha Tier", tier_list, key="alpha_tier")
    st.markdown('</div>', unsafe_allow_html=True)

    filtered_alpha = alpha_df.copy()
    if search_query:
        q = search_query.strip().lower()
        filtered_alpha = filtered_alpha[
            filtered_alpha["display_name"].astype(str).str.lower().str.contains(q) |
            filtered_alpha["nfl_id"].astype(str).str.contains(q)
        ]
    if selected_pos != "All Positions":
        filtered_alpha = filtered_alpha[filtered_alpha["nfl_position"] == selected_pos]
    if selected_tier != "All Tiers":
        filtered_alpha = filtered_alpha[filtered_alpha["athletic_alpha_tier"] == selected_tier]

    # Two-Column Leaderboards
    lead_col1, lead_col2 = st.columns(2)

    with lead_col1:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                <span style="font-weight: 800; font-size: 1.05rem;">Top Positive Residuals (Actual > Predicted)</span>
                <span class="pill-badge pill-badge-lime">OVERPERFORMERS</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        pos_leaders = filtered_alpha.sort_values(by="athletic_alpha_raw", ascending=False).head(10)
        st.dataframe(
            pos_leaders[[
                "display_name", "nfl_position", "actual_game_speed_p95",
                "expected_traditional_game_speed_p95", "athletic_alpha_raw", "verified_scrimmage_snaps"
            ]].rename(
                columns={
                    "display_name": "Prospect",
                    "nfl_position": "Pos",
                    "actual_game_speed_p95": "Actual P95",
                    "expected_traditional_game_speed_p95": "Pred P95",
                    "athletic_alpha_raw": "Alpha (yd/s)",
                    "verified_scrimmage_snaps": "Snaps (23–25)",
                }
            ).style.format({
                "Actual P95": "{:.2f} yd/s",
                "Pred P95": "{:.2f} yd/s",
                "Alpha (yd/s)": "+{:.2f} yd/s",
                "Snaps (23–25)": "{:.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with lead_col2:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown(
            """
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                <span style="font-weight: 800; font-size: 1.05rem;">Top Negative Residuals (Actual < Predicted)</span>
                <span class="pill-badge pill-badge-dark">UNDERPERFORMERS</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        neg_leaders = filtered_alpha.sort_values(by="athletic_alpha_raw", ascending=True).head(10)
        st.dataframe(
            neg_leaders[[
                "display_name", "nfl_position", "actual_game_speed_p95",
                "expected_traditional_game_speed_p95", "athletic_alpha_raw", "verified_scrimmage_snaps"
            ]].rename(
                columns={
                    "display_name": "Prospect",
                    "nfl_position": "Pos",
                    "actual_game_speed_p95": "Actual P95",
                    "expected_traditional_game_speed_p95": "Pred P95",
                    "athletic_alpha_raw": "Alpha (yd/s)",
                    "verified_scrimmage_snaps": "Snaps (23–25)",
                }
            ).style.format({
                "Actual P95": "{:.2f} yd/s",
                "Pred P95": "{:.2f} yd/s",
                "Alpha (yd/s)": "{:.2f} yd/s",
                "Snaps (23–25)": "{:.0f}",
            }),
            use_container_width=True,
            hide_index=True,
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Orthogonality Verification Table
    st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
    st.markdown("### 🛡️ Orthogonality & Confounder Verification")
    st.markdown(
        """
        To confirm Athletic Alpha is not an artifact of opportunity, tracking sample size, or draft consensus, 
        rigorous confounding regressions were conducted in Phase 3.1:
        """
    )
    confounder_data = {
        "Potential Confounding Factor": [
            "Verified Scrimmage Snaps (Exposure)",
            "Game Tracking Frames (Volume)",
            "Overall Draft Pick Number (Scouting Consensus)",
            "Positional Macro Group (ANOVA)"
        ],
        "Sample Size": ["N = 149", "N = 149", "N = 115 (Drafted)", "N = 149"],
        "Test Statistic": ["r = -0.0317", "r = -0.0856", "r = +0.0462", "F = 0.0185"],
        "p-value": ["p = 0.7012", "p = 0.2993", "p = 0.6237", "p = 0.9966"],
        "Verdict": ["✅ Orthogonal (No Exposure Bias)", "✅ Orthogonal (No Volume Bias)", "✅ Orthogonal (No Consensus Bias)", "✅ Zero Mean Shift Across Positions"]
    }
    st.dataframe(pd.DataFrame(confounder_data), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)
