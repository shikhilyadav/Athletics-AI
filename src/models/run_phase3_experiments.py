"""
ATHLETIX AI: Phase 3 Experiments & Statistical Modeling Runner
=============================================================
Executes Model A (Traditional), Model B (Sensor), and Model C (Hybrid)
across repeated stratified cross-validation on the 149 eligible 2023 prospects.
Computes Out-Of-Fold Athletic Alpha, performs sprint curve quality sensitivity,
and serializes predictions, metrics, and explanations.
"""

from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np

from src.models.statistical_analysis import StatisticalCohortProfiler
from src.models.model_comparison import ModelComparisonEngine
from src.models.residual_evaluator import ResidualPotentialEvaluator
from src.models.explainability import ModelExplainer
from src.config import PROCESSED_DATA_DIR, SAVED_MODELS_DIR, REPORTS_DIR

SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def run_all_experiments():
    print("=" * 80)
    print("ATHLETIX AI: EXECUTING PHASE 3 STATISTICAL MODELING")
    print("=" * 80)

    # 1. Load Primary Cohort
    print("\n[Step 1] Loading primary research cohort (2023, >= 50 snaps)...")
    profiler = StatisticalCohortProfiler()
    inclusion_report = profiler.generate_sample_inclusion_report()
    print("  -> Sample Inclusion Pipeline:", inclusion_report)

    master_df = profiler.df.filter(
        (pl.col("draft_year") == 2023) & (pl.col("is_eligible_50_snaps") == True)
    ).to_pandas()
    print(f"  -> Verified Cohort Size: N = {len(master_df)} players")

    # 2. Sprint Curve Quality Audit
    print("\n[Step 2] Sprint Curve Quality Audit...")
    curve_audit = profiler.audit_sprint_curve_quality()
    print("  -> Sprint Curve Quality Breakdown:", curve_audit)

    # 3. Target Distribution Analysis
    print("\n[Step 3] Target Distribution Analysis (Primary: game_speed_p95)...")
    target_summary = profiler.analyze_research_targets()
    print(target_summary[["target_variable", "n_obs", "mean", "std", "skewness", "is_normally_distributed"]])

    # 4. Multicollinearity Check
    print("\n[Step 4] Checking Multicollinearity (VIF)...")
    vif_features = [
        "forty", "ten_yd_split", "vertical", "broad_jump", "combine_height", "combine_weight",
        "combine_max_speed", "combine_initial_accel_mean", "combine_mean_pos_jerk", "combine_max_decel",
        "combine_mean_speed_preservation_ratio"
    ]
    vif_df = ModelExplainer.compute_vif(master_df, vif_features)
    print("  -> Top VIF scores:\n", vif_df.head(6))
    vif_df.to_csv(SAVED_MODELS_DIR / "vif_analysis.csv", index=False)

    # 5. Model Training & Cross-Validation Comparison
    print("\n[Step 5] Running Repeated Stratified 5-Fold Cross-Validation (10 repeats = 50 folds)...")
    engine = ModelComparisonEngine(master_df, target_col="game_speed_p95")
    comparison_results = engine.run_complete_model_comparison()

    metrics_rows = []
    oof_df = master_df[["nfl_id", "display_name", "nfl_position", "game_speed_p95"]].copy()

    for model_name, res in comparison_results.items():
        metrics_rows.append({
            "model_name": model_name,
            "oof_r2": res["oof_r2"],
            "oof_rmse": res["oof_rmse"],
            "oof_mae": res["oof_mae"],
            "oof_spearman": res["oof_spearman"],
            "mean_fold_r2": res["mean_fold_r2"],
            "std_fold_r2": res["std_fold_r2"],
            "ci_95_r2_low": res["ci_95_r2"][0],
            "ci_95_r2_high": res["ci_95_r2"][1],
            "n_features": res["n_features"],
        })
        oof_df[f"oof_pred_{model_name}"] = np.round(res["oof_predictions"], 4)

    metrics_df = pd.DataFrame(metrics_rows).sort_values(by="oof_r2", ascending=False).reset_index(drop=True)
    print("\n--- MODEL COMPARISON RESULTS (Repeated 5-Fold CV) ---")
    print(metrics_df[["model_name", "oof_r2", "oof_rmse", "oof_spearman", "ci_95_r2_low", "ci_95_r2_high"]])
    metrics_df.to_csv(SAVED_MODELS_DIR / "model_comparison_metrics.csv", index=False)
    oof_df.to_csv(SAVED_MODELS_DIR / "oof_predictions.csv", index=False)

    # 6. Complete-Case Sensitivity Analysis
    print("\n[Step 6] Running Complete-Case Sensitivity Analysis...")
    cc_sensitivity = engine.run_complete_case_sensitivity()
    print("  -> Complete-case results:", cc_sensitivity)

    # 7. Low-Quality Curve Sensitivity Analysis
    print("\n[Step 7] Running Sprint Curve Sensitivity Analysis (excluding R^2 < 0.85)...")
    high_curve_df = master_df[master_df["forty_curve_r2"] >= 0.85].copy()
    engine_high_curve = ModelComparisonEngine(high_curve_df, target_col="game_speed_p95")
    sens_res = engine_high_curve.evaluate_model_cv(
        engine.TRADITIONAL_FEATURES + engine.POSITION_DUMMIES, model_type="ridge", alpha=10.0
    )
    print(f"  -> Sensitivity (N={len(high_curve_df)} high/acceptable curves): OOF R^2 = {sens_res['oof_r2']}, RMSE = {sens_res['oof_rmse']}")

    # 8. Athletic Alpha Residual Analysis
    print("\n[Step 8] Evaluating Athletic Alpha Out-Of-Fold Residuals from Model A (Traditional Baseline)...")
    actual_y = master_df["game_speed_p95"].values
    oof_trad = comparison_results["Model_A_Ridge_Traditional"]["oof_predictions"]

    alpha_df = ResidualPotentialEvaluator.compute_athletic_alpha(
        master_df, actual_y, oof_trad, metric_name="game_speed_p95"
    )
    print("  -> Top 5 Underestimated Prospects (Highest Athletic Alpha):")
    print(alpha_df[["display_name", "nfl_position", "actual_game_speed_p95", "expected_traditional_game_speed_p95", "athletic_alpha_raw", "athletic_alpha_zscore"]].head(5))
    print("  -> Bottom 5 Workout Warriors (Lowest Athletic Alpha):")
    print(alpha_df[["display_name", "nfl_position", "actual_game_speed_p95", "expected_traditional_game_speed_p95", "athletic_alpha_raw", "athletic_alpha_zscore"]].tail(5))
    alpha_df.to_csv(SAVED_MODELS_DIR / "athletic_alpha_residuals.csv", index=False)

    # Residual Distribution Tests
    res_dist = ResidualPotentialEvaluator.analyze_residual_distribution(alpha_df["athletic_alpha_raw"].values)
    print("  -> Residual Distribution Stats:", res_dist)

    # Position Profiling
    pos_alpha = ResidualPotentialEvaluator.profile_by_position(alpha_df)
    print("  -> Athletic Alpha by Position:\n", pos_alpha.head(6))

    # Correlation with Sensor Features
    print("\n[Step 9] Correlating Athletic Alpha with Sensor Features...")
    sensor_corrs = ResidualPotentialEvaluator.correlate_with_sensor_features(
        alpha_df, master_df, engine.SENSOR_FEATURES
    )
    print("  -> Top Sensor Features Correlated with Athletic Alpha:\n", sensor_corrs.head(6))
    sensor_corrs.to_csv(SAVED_MODELS_DIR / "sensor_alpha_correlations.csv", index=False)

    # 9. Explainability & Permutation Importance
    print("\n[Step 10] Running Permutation Feature Importance & SHAP on Hybrid Model...")
    hybrid_feats = list(dict.fromkeys(engine.TRADITIONAL_FEATURES + engine.SENSOR_FEATURES + engine.POSITION_DUMMIES))
    hybrid_pipeline = engine.build_pipeline(model_type="ridge", alpha=10.0)
    hybrid_pipeline.fit(engine.df[hybrid_feats].values, actual_y)

    perm_imp = ModelExplainer.compute_permutation_importance(
        hybrid_pipeline, engine.df[hybrid_feats].values, actual_y, hybrid_feats
    )
    print("  -> Top Permutation Feature Importances:\n", perm_imp.head(8))
    perm_imp.to_csv(SAVED_MODELS_DIR / "feature_importance.csv", index=False)

    print("\nPhase 3 Statistical Modeling Pipeline Successfully Executed!")
    return {
        "metrics_df": metrics_df,
        "alpha_df": alpha_df,
        "inclusion_report": inclusion_report,
        "curve_audit": curve_audit,
        "cc_sensitivity": cc_sensitivity,
        "sensor_corrs": sensor_corrs,
        "perm_imp": perm_imp,
    }


if __name__ == "__main__":
    run_all_experiments()
