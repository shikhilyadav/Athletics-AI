"""
ATHLETIX AI — Dashboard View 6: Research Methodology
Editorial research paper format with minimalist light-grey background,
white rounded cards, lime accents (#C8F45A), and deep black typography (#171917).
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import load_dataset_inventory, load_fdr_correlations
from src.dashboard.components import (
    render_editorial_header,
    render_scientific_banner,
)


def render_page():
    render_editorial_header(
        title="Scientific Research Methodology",
        subtitle="Empirical protocols, entity resolution, cross-validation, and boundary conditions.",
        tag="RESEARCH SPECIFICATION",
    )
    
    inv_df = load_dataset_inventory()
    fdr_df = load_fdr_correlations()

    # Prominent "What This Research Does Not Prove" Section
    st.markdown(
        """
        <div class="athletix-card-dark">
            <div style="font-size: 0.78rem; font-weight: 700; color: #C8F45A; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">
                SCIENTIFIC BOUNDARY SPECIFICATION
            </div>
            <div style="font-size: 1.4rem; font-weight: 800; color: #FFFFFF; margin-bottom: 12px;">
                ⚠️ What This Research Does Not Prove
            </div>
            <div style="color: #A3A8A4; font-size: 0.9rem; line-height: 1.65;">
                <p><strong>1. Sensor Features Did NOT Improve Straight-Line Speed Prediction:</strong> The traditional Combine baseline (40-yard dash, vertical jump, height, weight, position) achieved R² = 0.9381 in nested cross-validation, outperforming the hybrid model (R² = 0.9311; paired error p = 0.0069). Adding 11 collinear sensor velocity metrics to an N = 149 sample inflated model variance without improving generalization.</p>
                <p><strong>2. Global Sensor Correlations Did NOT Survive False Discovery Rate (FDR) Correction:</strong> While unadjusted p-values for change-of-direction speed preservation showed weak signals (p ≈ 0.03), applying Benjamini-Hochberg correction across all 11 sensor features produced q &gt; 0.86 globally and q ≈ 0.14 in skill subsets. These correlations are strictly exploratory hypotheses, not proven causal laws.</p>
                <p><strong>3. Athletic Alpha is NOT Proven 'Hidden Athletic Potential':</strong> Athletic Alpha is an out-of-fold linear regression residual (α = y - ŷ). It measures the empirical delta between a player's actual in-game top speed and a traditional linear model's projection. It does NOT prove intrinsic talent, 'guaranteed draft steals', or future career longevity.</p>
                <p><strong>4. Single-Season Data Limitation:</strong> The official competition dataset provides regular-season tracking exclusively for the 2023 season. Multi-year trajectory tracking (2024–2025) is unavailable, precluding longitudinal career development modeling.</p>
                <p><strong>5. Small Sample Size in Rare Positional Roles:</strong> With N = 149 eligible scrimmage players, rare positions such as Nose Tackle (N = 3) cannot support independent statistical models.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "Dataset Inventory", "Cross-Validation & Bootstrap", "FDR Multi-Testing Control", "Cohort Construction Lineage"
    ])

    with tab1:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("#### 1. Official Competition Datasets (NFL Big Data Bowl 2027)")
        st.markdown("Empirically verified files discovered in `data/raw/`:")
        if not inv_df.empty:
            st.dataframe(
                inv_df.rename(
                    columns={
                        "filename": "Filename",
                        "file_size_mb": "File Size (MB)",
                        "row_count": "Row Count",
                        "column_count": "Columns",
                    }
                ).style.format({
                    "File Size (MB)": "{:.2f} MB",
                    "Row Count": "{:,}",
                }),
                use_container_width=True,
                hide_index=True,
            )
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("#### 2. Cross-Validation & Bootstrap Uncertainty Methodology")
        st.markdown(
            r"""
            - **Repeated Stratified 5-Fold Cross-Validation:** 10 repeats $\times$ 5 folds = 50 total model fits.
            - **Zero Leakage:** Imputation (`SimpleImputer(strategy='median')`) and standardization (`StandardScaler()`) are encapsulated inside `sklearn.pipeline.Pipeline`, strictly fitted on training splits only.
            - **Player-Level Non-Parametric Bootstrap ($B = 2,000$):**  
              Treating 50 repeated folds as 50 independent samples introduces pseudo-replication (folds share 80% training data). 
              Player-level bootstrap resampling provides genuine empirical 95% confidence intervals and paired delta distributions ($\Delta \text{RMSE} = \text{RMSE}_C - \text{RMSE}_A$).
            - **Nested Cross-Validation:** Outer 5-fold CV evaluates out-of-fold generalization, while inner 5-fold CV optimizes Ridge regularization strength $\alpha \in [0.1, 1.0, 10.0, 100.0, 1000.0]$.
            """
        )
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("#### 3. Multiple Testing & Benjamini-Hochberg FDR Control")
        st.markdown(
            """
            Evaluating 11 simultaneous sensor features against Athletic Alpha requires controlling the False Discovery Rate:  
            $$q_{(k)} = p_{(k)} \\times \\frac{m}{k}$$
            """
        )
        if not fdr_df.empty:
            st.dataframe(
                fdr_df.rename(
                    columns={
                        "sensor_feature": "Sensor Feature",
                        "spearman_r": "Spearman ρ",
                        "spearman_raw_p": "Raw p-value",
                        "pearson_r": "Pearson r",
                        "fdr_q_value": "BH FDR q-value",
                        "is_significant_fdr_0.05": "FDR < 0.05?",
                    }
                ).style.format({
                    "Spearman ρ": "{:.4f}",
                    "Raw p-value": "{:.4f}",
                    "Pearson r": "{:.4f}",
                    "BH FDR q-value": "{:.4f}",
                }),
                use_container_width=True,
                hide_index=True,
            )
            st.caption("All 11 features yield q > 0.05 globally across the 149-player cohort, confirming signals are exploratory.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab4:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("#### 4. Cohort Construction & Lineage Lineage")
        lineage_table = {
            "Stage": [
                "Stage 0: Combine Attendees",
                "Stage 1: Combine Sensor Tracked",
                "Stage 2: Regular-Season Game Tracked",
                "Stage 3: Verified Scrimmage Snaps (≥50)",
                "Stage 4: Route Separation Sub-Cohort"
            ],
            "Count (N)": ["510", "510", "156", "149", "51"],
            "Exclusion Criterion": [
                "All invited 2023 Combine prospects",
                "Zero excluded (All 510 attendees tracked)",
                "354 excluded (No regular-season 2023 game tracking)",
                "7 excluded (< 50 verified scrimmage snaps)",
                "98 excluded (Non-route running trench/defense players)"
            ],
            "File Source": [
                "data/raw/combine_results.csv",
                "data/processed/combine_kinematic_features.parquet",
                "data/processed/game_tracking_features_2023.parquet",
                "models/saved/oof_predictions.csv",
                "reports/phase3/03_model_comparison_report.md"
            ]
        }
        st.dataframe(pd.DataFrame(lineage_table), use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
