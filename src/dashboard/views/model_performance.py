"""
ATHLETIX AI — Dashboard View 3: Model Analytics
Model A vs. Model B vs. Model C comparison with nested cross-validation,
bootstrap uncertainty, and clean minimalist card containers.
"""

import streamlit as st
import pandas as pd
from src.dashboard.data_loader import (
    load_model_metrics,
    load_nested_cv_metrics,
    load_oof_predictions,
    load_feature_importance,
    load_vif_analysis,
)
from src.dashboard.charts import (
    plot_model_comparison_bars,
    plot_actual_vs_predicted,
    plot_residuals,
    plot_feature_importance,
    plot_vif_bars,
)
from src.dashboard.components import (
    render_editorial_header,
    render_scientific_banner,
)


def render_page():
    render_editorial_header(
        title="Predictive Modeling & Statistical Evaluation",
        subtitle="Evaluating whether 10 Hz sensor tracking provides incremental predictive power for NFL in-game speed.",
        tag="MACHINE LEARNING BENCHMARK",
    )
    
    oof_df = load_oof_predictions()
    phase3_metrics = load_model_metrics()
    nested_metrics = load_nested_cv_metrics()
    feat_df = load_feature_importance()
    vif_df = load_vif_analysis()

    # Scientific Caution Banner
    render_scientific_banner(
        "Methodological Integrity Notice",
        "The Traditional Combine Baseline (Model A, R² = 0.9381) statistically outperforms the Hybrid Model (Model C, R² = 0.9311) "
        "in out-of-fold generalization (paired error test: t = -2.74, p = 0.0069). Adding 11 sensor kinematics metrics to traditional tests "
        "inflates model variance without improving global speed prediction due to severe feature multicollinearity. Sensor features do not outperform traditional stopwatches."
    )

    tab1, tab2, tab3 = st.tabs(["Nested CV (Tuned)", "Phase 3 Baseline CV", "Multicollinearity & Weights"])

    with tab1:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("### 1. Nested Cross-Validation with Inner Regularization Grid Search")
        st.caption("Outer Loop: 5-Fold Stratified CV | Inner Loop: 5-Fold Grid Search on Ridge Regularizer α ∈ [0.1, 1.0, 10.0, 100.0, 1000.0]")
        
        if not nested_metrics.empty:
            c1, c2 = st.columns([3, 2])
            with c1:
                st.dataframe(
                    nested_metrics.rename(
                        columns={
                            "model": "Model Architecture",
                            "oof_r2": "Tuned Outer OOF R²",
                            "oof_rmse": "Tuned Outer RMSE (yd/s)",
                            "oof_mae": "Tuned Outer MAE (yd/s)",
                            "spearman": "Spearman Rank ρ",
                        }
                    ).style.format({
                        "Tuned Outer OOF R²": "{:.4f}",
                        "Tuned Outer RMSE (yd/s)": "{:.4f}",
                        "Tuned Outer MAE (yd/s)": "{:.4f}",
                        "Spearman Rank ρ": "{:.4f}",
                    }),
                    use_container_width=True,
                    hide_index=True,
                )
            with c2:
                st.markdown(
                    """
                    <div style="background: #1B222D; border: 1px solid #C8F45A; border-radius: 14px; padding: 1.1rem 1.3rem; box-shadow: 0 0 15px rgba(200, 244, 90, 0.15);">
                        <div style="font-size: 0.76rem; font-weight: 700; color: #C8F45A; text-transform: uppercase; margin-bottom: 4px; letter-spacing: 0.06em;">PAIRED ERROR COMPARISON</div>
                        <div style="font-size: 1.25rem; font-weight: 800; color: #FFFFFF;">ΔRMSE = +0.0210 yd/s</div>
                        <div style="font-size: 0.84rem; color: #94A3B8; margin-top: 6px; line-height: 1.5;">
                            • Paired Error t-test: <strong style="color:#FFFFFF;">t = -2.7411</strong> (p = 0.0069)<br>
                            • Wilcoxon Signed-Rank: <strong style="color:#FFFFFF;">W = 4,218</strong> (p = 0.0084)<br>
                            • Conclusion: <span style="color:#C8F45A; font-weight:700;">Model A is statistically superior to Model C.</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            
            bar_col1, bar_col2 = st.columns(2)
            with bar_col1:
                st.plotly_chart(plot_model_comparison_bars(nested_metrics, metric_col="oof_r2"), use_container_width=True)
            with bar_col2:
                st.plotly_chart(plot_model_comparison_bars(nested_metrics, metric_col="oof_rmse"), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
                
        # Corrected Bootstrap Uncertainty Table
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("#### Corrected Uncertainty Estimates (Player-Level Bootstrap, B=2,000)")
        bootstrap_data = {
            "Model Architecture": [
                "Model A: Traditional Baseline (Ridge)",
                "Model B: Sensor Kinematics (Ridge)",
                "Model C: Hybrid Traditional + Sensor",
                "Paired Delta: Model C minus Model A"
            ],
            "Empirical Mean R²": ["0.9372", "0.9168", "0.9307", "Δ = -0.0066"],
            "95% Bootstrap CI (R²)": ["[0.9171, 0.9526]", "[0.8874, 0.9389]", "[0.9083, 0.9477]", "[-0.0130, -0.0001]"],
            "Empirical Mean RMSE": ["0.3860 yd/s", "0.4435 yd/s", "0.4055 yd/s", "Δ = +0.0194 yd/s"],
            "95% Bootstrap CI (RMSE)": ["[0.3340, 0.4352]", "[0.3892, 0.5041]", "[0.3540, 0.4578]", "[+0.0003, +0.0373]"],
        }
        st.dataframe(pd.DataFrame(bootstrap_data), use_container_width=True, hide_index=True)
        st.caption("Note: 50 repeated folds share 80% of training data and cannot be treated as 50 independent observations. Player-level bootstrap accurately reflects true uncertainty.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("### 2. Original Phase 3 Cross-Validation Comparison")
        st.caption("10-Repeat 5-Fold Stratified Cross-Validation (50 Folds, Fixed α=10.0)")
        
        if not phase3_metrics.empty:
            st.dataframe(
                phase3_metrics.rename(
                    columns={
                        "model_name": "Model",
                        "oof_r2": "Mean OOF R²",
                        "oof_rmse": "Mean OOF RMSE",
                        "oof_mae": "Mean OOF MAE",
                        "ci_95_r2_low": "Fold CI Low",
                        "ci_95_r2_high": "Fold CI High",
                        "n_features": "Features (P)",
                    }
                ).style.format({
                    "Mean OOF R²": "{:.4f}",
                    "Mean OOF RMSE": "{:.4f}",
                    "Mean OOF MAE": "{:.4f}",
                    "Fold CI Low": "{:.4f}",
                    "Fold CI High": "{:.4f}",
                }),
                use_container_width=True,
                hide_index=True,
            )

        if not oof_df.empty:
            st.markdown("#### Out-of-Fold Actual vs. Predicted Visualizations")
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.plotly_chart(
                    plot_actual_vs_predicted(oof_df, "oof_pred_Model_A_Ridge_Traditional"),
                    use_container_width=True
                )
            with p_col2:
                st.plotly_chart(
                    plot_actual_vs_predicted(oof_df, "oof_pred_Model_C_Ridge_Hybrid"),
                    use_container_width=True
                )
                
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                st.plotly_chart(
                    plot_residuals(oof_df, "oof_pred_Model_A_Ridge_Traditional"),
                    use_container_width=True
                )
            with r_col2:
                st.plotly_chart(
                    plot_residuals(oof_df, "oof_pred_Model_C_Ridge_Hybrid"),
                    use_container_width=True
                )
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="athletix-card">', unsafe_allow_html=True)
        st.markdown("### 3. Multicollinearity Diagnostics & Feature Importance")
        
        vif_col, feat_col = st.columns(2)
        with vif_col:
            st.markdown("#### Variance Inflation Factor (VIF)")
            st.markdown(
                """
                A VIF value exceeding **10.0** indicates severe collinearity. Combining 40-yard dash time with 
                tracking kinematics (`combine_max_speed`, `combine_mean_speed`, `forty_curve_tau`) creates high 
                redundancy that destabilizes linear estimation.
                """
            )
            if not vif_df.empty:
                st.plotly_chart(plot_vif_bars(vif_df), use_container_width=True)
                
        with feat_col:
            st.markdown("#### Model C Standardized Coefficients")
            st.markdown(
                """
                Position dummy controls and traditional sprint drills dominate the model weights. Sensor kinematics 
                receive dampened coefficients due to Ridge penalty shrinking collinear weights.
                """
            )
            if not feat_df.empty:
                st.plotly_chart(plot_feature_importance(feat_df), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
