# ATHLETIX AI — Phase 4 Data Mapping Specification

**Document:** Data Source and Metric Traceability Matrix  
**Author:** Research Analytics & UI/UX Engineering Team  
**Date:** November 2026  
**Status:** Complete & Verified  

---

## 1. Overview & Data Integrity Principles

This document establishes the exact traceability between every dashboard component, metric, chart, and table in Phase 4 and its underlying verified dataset or serialized model artifact.

### Core Architecture Rules:
1. **Zero Runtime CSV Heavy-Loading:** Under no circumstances will raw tracking datasets (`game_tracking_2023.csv`, 3.66M rows; `combine_tracking.csv`, 1.48M rows) be loaded into Streamlit memory during runtime. All analytics run off optimized Parquet files and serialized summary CSVs.
2. **Explicit Null Representation:** Any missing physical measurement, unattempted drill, or out-of-cohort status is presented explicitly as `"N/A"` or `"Unavailable"`. No imputation is performed for UI display.
3. **Traceable Lineage:** Every metric is backed by a deterministic column in an existing processed file.

---

## 2. Section-by-Section Data Mapping Matrix

| Dashboard Section | Component / Visualization | Source File | Required Columns | Record Count | Filters / Aggregations Applied |
| :--- | :--- | :--- | :--- | :---: | :--- |
| **1. Research Overview** | Prospect Funnel KPI Cards | `data/processed/combine_player_master.parquet` | `nfl_id`, `is_eligible_50_snaps`, `game_target_cohort_status` | 510 | 510 total Combine prospects; 156 with tracking; 149 primary cohort. |
| | Route-Separation Sub-cohort KPI | `data/processed/player_play_features.parquet` | `nfl_id`, `separation_at_pass_forward` | 50,462 plays | Filter `separation_at_pass_forward.is_not_null()` and skill positions: 51 unique players. |
| | Combine Drill Trials KPI | `data/processed/combine_kinematic_features.parquet` | `event_id`, `drill_type` | 6,310 | Total tracked drill attempts across all drills. |
| | Regular-Season Tracking Volume KPI | `reports/actual_dataset_inventory.csv` | `row_count` where file is `game_tracking_2023.csv` | 1 row | Exact count: 3,663,222 tracking frames at 10 Hz. |
| | Model Performance Summary Table | `models/saved/phase3_1_audit/nested_cv_model_metrics.csv` | `model`, `oof_r2`, `oof_rmse`, `oof_mae`, `spearman` | 3 rows | Direct load of nested CV evaluation metrics. |
| **2. Prospect Explorer** | Filterable Master Roster Table | `data/processed/combine_player_master.parquet` | `nfl_id`, `display_name`, `nfl_position`, `draft_year`, `draft_round`, `draft_overall_pick`, `forty`, `vertical`, `broad_jump`, `combine_max_speed`, `game_speed_p95`, `verified_scrimmage_snaps`, `is_eligible_50_snaps` | 510 rows | Interactive filters by position, draft round, cohort status, and search query. |
| | Prospect Detail Header & Badge Card | `data/processed/combine_player_master.parquet` | `display_name`, `nfl_position`, `combine_position`, `college_name`, `combine_height`, `combine_weight`, `draft_overall_pick` | 1 selected player | Filtered by `nfl_id`. |
| | Traditional Combine Test Card | `data/processed/combine_player_master.parquet` | `forty`, `ten_yd_split`, `vertical`, `broad_jump`, `three_cone`, `short_shuttle`, `bench_reps` | 1 selected player | Null values rendered as `"Not Attempted"`. |
| | Sensor Kinematics Card | `data/processed/combine_player_master.parquet` | `combine_max_speed`, `combine_mean_speed`, `combine_max_accel`, `combine_initial_accel_mean`, `combine_burst_latency_mean`, `combine_max_decel` | 1 selected player | Formatted with physical SI / imperial units (yd/s, yd/s²). |
| | Change-of-Direction Card | `data/processed/combine_player_master.parquet` | `combine_mean_cod_apex_speed`, `combine_mean_speed_preservation_ratio`, `combine_peak_angular_velocity`, `combine_mean_turning_efficiency` | 1 selected player | Dimensionless ratios and deg/s. |
| | Regular-Season In-Game Tracking Card | `data/processed/game_tracking_features_2023.parquet` | `game_speed_p95`, `game_speed_p99`, `game_speed_max`, `game_accel_p95`, `high_speed_running_fraction`, `verified_scrimmage_snaps` | 1 selected player | Render `"Out of Cohort / Ineligible"` if $< 50$ snaps. |
| **3. Model Performance** | Baseline Phase 3 Metrics Table | `models/saved/model_comparison_metrics.csv` | `model_name`, `oof_r2`, `oof_rmse`, `oof_mae`, `ci_95_r2_low`, `ci_95_r2_high`, `n_features` | 6 rows | Unadjusted Phase 3 fold evaluation metrics. |
| | Nested CV Metrics Table (Phase 3.1) | `models/saved/phase3_1_audit/nested_cv_model_metrics.csv` | `model`, `oof_r2`, `oof_rmse`, `oof_mae`, `spearman` | 3 rows | Rigorously tuned models with inner CV grid search. |
| | Bootstrap Uncertainty Comparison Table | `reports/phase3_1_audit/confidence_interval_audit.md` | `model`, `bootstrap_r2_ci`, `bootstrap_rmse_ci`, `delta_rmse_ci` | Markdown table | Player-level bootstrap ($B=2,000$) intervals. |
| | Actual vs. Predicted Speed Scatter Plot | `models/saved/oof_predictions.csv` | `game_speed_p95`, `oof_pred_Model_A_Ridge_Traditional`, `oof_pred_Model_B_Ridge_Sensor`, `oof_pred_Model_C_Ridge_Hybrid`, `display_name`, `nfl_position` | 149 rows | Multi-model toggle with 45° reference line ($y=x$). |
| | Model Residual Distribution Plot | `models/saved/oof_predictions.csv` | Residuals computed as $y - \hat{y}$ for Model A, B, and C | 149 rows | Histograms and box plots showing error spread. |
| | Feature Importance Chart | `models/saved/feature_importance.csv` | `feature`, `importance_mean`, `importance_std` | 23 features | Ranked bar chart of Model C coefficients. |
| | Multicollinearity Diagnostic Chart | `models/saved/vif_analysis.csv` | `feature`, `vif` | 8 key features | Horizontal bar chart highlighting $VIF > 10$ cutoff. |
| **4. Athletic Alpha Explorer** | Top Outperformer Leaderboard ($Z \ge 1.0$) | `models/saved/athletic_alpha_residuals.csv` | `display_name`, `nfl_position`, `actual_game_speed_p95`, `expected_traditional_game_speed_p95`, `athletic_alpha_raw`, `athletic_alpha_zscore`, `athletic_alpha_tier` | Filtered subset ($N \approx 24$) | Sorted descending by `athletic_alpha_raw`. |
| | Top Underperformer Leaderboard ($Z \le -1.0$) | `models/saved/athletic_alpha_residuals.csv` | (Same as above) | Filtered subset ($N \approx 25$) | Sorted ascending by `athletic_alpha_raw`. |
| | Athletic Alpha vs. Predicted Speed Scatter | `models/saved/athletic_alpha_residuals.csv` | `expected_traditional_game_speed_p95`, `actual_game_speed_p95`, `athletic_alpha_raw`, `display_name`, `nfl_position`, `athletic_alpha_tier` | 149 rows | Color-coded by tier: Outperformer, Neutral, Underperformer. |
| | Position Distribution of Alpha | `models/saved/athletic_alpha_residuals.csv` | `nfl_position`, `athletic_alpha_raw` | 149 rows | Box plot showing mean-zero calibration across positions. |
| | Confounding Factor Check Matrix | `reports/phase3_1_audit/athletic_alpha_validation.md` | Confounder name, correlation $r$, p-value | 4 checks | Orthogonality verification with snaps, frames, draft pick. |
| **5. Biomechanical Lab** | Prospect Drill Trial Selector & Metrics | `data/processed/combine_kinematic_features.parquet` & `combine_cod_features.parquet` | `nfl_id`, `drill_type`, `drill_name`, `attempt`, `v_max`, `a_max`, `mean_speed_preservation_ratio`, `peak_angular_velocity_deg_s` | 6,310 rows | Filtered by selected prospect and drill type. |
| | Mono-Exponential Sprint Curve Fitting Card | `data/processed/combine_player_master.parquet` | `forty_curve_vmax`, `forty_curve_tau`, `forty_curve_r2` | 1 selected player | Displays fitted $v(t) = v_{\max}(1 - e^{-t/\tau})$, $\tau$, asymptotic $v_{\max}$, and $R^2$ quality badge. |
| | Curve Fit Quality Distribution Chart | `data/processed/combine_player_master.parquet` | `forty_curve_r2` | 510 prospects | Categorized into: High Quality ($R^2 \ge 0.95$), Moderate, Low, or Unavailable/Skipped. |
| | COD Speed Preservation vs. Apex Speed | `data/processed/combine_cod_features.parquet` | `mean_apex_speed`, `mean_speed_preservation_ratio`, `drill_name`, `display_name` | 6,310 trials | Scatter plot illustrating turn entry vs. exit dynamics. |
| | Head-to-Head Player Comparison Radar/Bars | `data/processed/combine_player_master.parquet` | Z-scored kinematic metrics (`combine_max_speed`, `combine_max_accel`, `combine_mean_speed_preservation_ratio`, `combine_peak_angular_velocity`, `forty`) | 2 selected players | Standardized normalized comparison across biomechanical attributes. |
| **6. Research & Methodology** | Interactive Dataset Inventory Table | `reports/actual_dataset_inventory.csv` | `filename`, `file_size_mb`, `row_count`, `column_count` | 7 raw files | Summary of competition datasets. |
| | Multiple Testing FDR Correction Table | `models/saved/phase3_1_audit/fdr_corrected_correlations.csv` | `sensor_feature`, `spearman_r`, `spearman_raw_p`, `pearson_r`, `fdr_q_value`, `is_significant_fdr_0.05` | 11 tests | Displaying Benjamini-Hochberg corrected $q$-values. |
| | "What This Research Does Not Prove" Card | Static verified research synthesis | Markdown text | N/A | Clear scientific boundaries and non-claims. |

---

## 3. Data Availability & Fallback Safeguards

1. **Missing Combine Drills:** If an athlete skipped the 40-yard dash, 3-cone, or short shuttle, the UI renders `"Not Attempted (Combine DNP)"`.
2. **Missing Sprint Curve Fits:** If non-linear curve fitting did not converge or was skipped (e.g., non-sprint trials), the UI flags `"Sprint Model Not Fit: Trial Not Straight-Line Sprint"`.
3. **Ineligible In-Game Tracking:** If a prospect had $< 50$ snaps in 2023 regular season, in-game metrics show `"Ineligible for Modeling (< 50 Scrimmage Snaps)"`.
4. **Memory Guard:** All Parquet data is read using cached Polars lazy-scanning or cached Pandas readers, consuming $< 250\text{ MB}$ total application memory, fully compatible with 8 GB RAM constraints.
