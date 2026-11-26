"""
ATHLETIX AI: Phase 3.1 Independent Statistical Audit Script
===========================================================
Performs a rigorous audit across:
1. Cross-validation fold isolation & player-level aggregation.
2. Player-level bootstrap confidence intervals & paired model comparisons.
3. Position stratification & fold assignment counts.
4. Nested CV hyperparameter tuning to test incremental sensor value.
5. Athletic Alpha residual diagnostics against draft capital, snaps, frames, position.
6. Benjamini-Hochberg FDR correction on sensor-alpha correlations.
7. Cohort reconciliation between Phase 2 and Phase 3 reports.

Saves all audit outputs to models/saved/phase3_1_audit/.
"""

import sys
from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats.multitest import multipletests
from sklearn.linear_model import Ridge, ElasticNet, RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV

from src.config import PROCESSED_DATA_DIR, SAVED_MODELS_DIR, REPORTS_DIR, RANDOM_SEED

AUDIT_DIR = SAVED_MODELS_DIR / "phase3_1_audit"
AUDIT_DIR.mkdir(parents=True, exist_ok=True)
AUDIT_REPORTS_DIR = REPORTS_DIR / "phase3_1_audit"
AUDIT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)


def run_full_statistical_audit():
    print("=" * 80)
    print("STARTING PHASE 3.1 INDEPENDENT STATISTICAL AUDIT")
    print("=" * 80)

    # 1. Load Data
    master_path = PROCESSED_DATA_DIR / "combine_player_master.parquet"
    master_pl = pl.read_parquet(master_path)
    cohort_df = master_pl.filter(
        (pl.col("draft_year") == 2023) & (pl.col("is_eligible_50_snaps") == True)
    ).to_pandas()

    n_players = len(cohort_df)
    print(f"\n[Audit Item 1] Primary Research Cohort: N = {n_players} players (Expected: 149)")
    assert n_players == 149, f"Cohort size mismatch: {n_players} != 149"

    # Position macro grouping
    def get_macro_pos(pos):
        pos = str(pos).upper()
        if pos in ["WR", "TE", "RB", "FB"]:
            return "SKILL_OFFENSE"
        elif pos in ["T", "G", "C", "OT", "OG"]:
            return "LINE_OFFENSE"
        elif pos in ["DE", "DT", "NT", "EDGE", "DL", "OLB"]:
            return "DEFENSIVE_FRONT"
        elif pos in ["CB", "SS", "FS", "DB", "S"]:
            return "DEFENSIVE_BACKS"
        return "OTHER"

    cohort_df["macro_position"] = cohort_df["nfl_position"].apply(get_macro_pos)
    cohort_df["pos_skill"] = (cohort_df["macro_position"] == "SKILL_OFFENSE").astype(float)
    cohort_df["pos_oline"] = (cohort_df["macro_position"] == "LINE_OFFENSE").astype(float)
    cohort_df["pos_dfront"] = (cohort_df["macro_position"] == "DEFENSIVE_FRONT").astype(float)
    cohort_df["pos_dback"] = (cohort_df["macro_position"] == "DEFENSIVE_BACKS").astype(float)

    trad_features = [
        "forty", "ten_yd_split", "vertical", "broad_jump",
        "three_cone", "short_shuttle", "combine_height", "combine_weight"
    ]
    sensor_features = [
        "combine_max_speed", "combine_mean_speed", "combine_initial_accel_mean",
        "combine_burst_latency_mean", "combine_mean_pos_jerk", "combine_max_decel",
        "forty_curve_tau", "combine_mean_cod_apex_speed", "combine_mean_speed_preservation_ratio",
        "combine_peak_angular_velocity", "combine_mean_turning_efficiency"
    ]
    pos_dummies = ["pos_skill", "pos_oline", "pos_dfront", "pos_dback"]

    model_a_cols = trad_features + pos_dummies
    model_b_cols = sensor_features + pos_dummies
    model_c_cols = list(dict.fromkeys(trad_features + sensor_features + pos_dummies))

    y = cohort_df["game_speed_p95"].values
    strata = cohort_df["macro_position"].values

    # ---------------------------------------------------------
    # AUDIT ITEM 1: CROSS-VALIDATION & FOLD ISOLATION
    # ---------------------------------------------------------
    print("\n--- AUDITING REPEATED CROSS-VALIDATION & ISOLATION ---")
    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=RANDOM_SEED)

    leakage_detected = False
    fold_sizes = []
    player_test_appearances = {pid: 0 for pid in cohort_df["nfl_id"]}

    for repeat_idx in range(10):
        repeat_seen = set()
        for fold_idx, (train_idx, test_idx) in enumerate(rskf.split(cohort_df.values, strata)):
            if fold_idx // 5 != repeat_idx:
                continue
            train_set = set(cohort_df.iloc[train_idx]["nfl_id"])
            test_set = set(cohort_df.iloc[test_idx]["nfl_id"])
            
            # Check overlap within fold
            overlap = train_set & test_set
            if overlap:
                leakage_detected = True
                print(f"CRITICAL LEAKAGE: Player(s) {overlap} in both train and test!")

            # Check overlap across folds in the same repeat
            if repeat_seen & test_set:
                leakage_detected = True
                print(f"CRITICAL LEAKAGE: Player(s) tested multiple times in repeat {repeat_idx}!")
            repeat_seen.update(test_set)
            fold_sizes.append(len(test_idx))

            for pid in test_set:
                player_test_appearances[pid] += 1

    print(f"  -> Total Folds: 50 (5 splits x 10 repeats)")
    print(f"  -> Leakage Detected within Folds: {leakage_detected}")
    print(f"  -> Min Test Fold Size: {min(fold_sizes)}, Max Test Fold Size: {max(fold_sizes)}")
    test_counts = list(player_test_appearances.values())
    print(f"  -> Player OOF prediction count per model: Min={min(test_counts)}, Max={max(test_counts)}, Mean={np.mean(test_counts):.1f}")
    assert min(test_counts) == 10 and max(test_counts) == 10, "Not every player was tested exactly 10 times!"

    # ---------------------------------------------------------
    # AUDIT ITEM 2: PLAYER-LEVEL BOOTSTRAP CONFIDENCE INTERVALS
    # ---------------------------------------------------------
    print("\n--- AUDITING CONFIDENCE INTERVALS VIA PLAYER-LEVEL BOOTSTRAP ---")
    # Load original OOF predictions
    oof_df = pd.read_csv(SAVED_MODELS_DIR / "oof_predictions.csv")
    
    y_true = oof_df["game_speed_p95"].values
    y_pred_a = oof_df["oof_pred_Model_A_Ridge_Traditional"].values
    y_pred_b = oof_df["oof_pred_Model_B_Ridge_Sensor"].values
    y_pred_c = oof_df["oof_pred_Model_C_Ridge_Hybrid"].values

    B = 2000
    np.random.seed(RANDOM_SEED)
    boot_indices = np.random.randint(0, n_players, size=(B, n_players))

    boot_r2_a, boot_r2_b, boot_r2_c = [], [], []
    boot_rmse_a, boot_rmse_b, boot_rmse_c = [], [], []
    boot_delta_r2_ca = []  # Model C - Model A
    boot_delta_rmse_ca = []  # Model C - Model A

    for b in range(B):
        idx = boot_indices[b]
        yb = y_true[idx]
        pa = y_pred_a[idx]
        pb = y_pred_b[idx]
        pc = y_pred_c[idx]

        ss_tot = np.sum((yb - np.mean(yb)) ** 2)
        r2_a = 1.0 - np.sum((yb - pa) ** 2) / ss_tot
        r2_b = 1.0 - np.sum((yb - pb) ** 2) / ss_tot
        r2_c = 1.0 - np.sum((yb - pc) ** 2) / ss_tot

        rmse_a = np.sqrt(np.mean((yb - pa) ** 2))
        rmse_b = np.sqrt(np.mean((yb - pb) ** 2))
        rmse_c = np.sqrt(np.mean((yb - pc) ** 2))

        boot_r2_a.append(r2_a)
        boot_r2_b.append(r2_b)
        boot_r2_c.append(r2_c)
        boot_rmse_a.append(rmse_a)
        boot_rmse_b.append(rmse_b)
        boot_rmse_c.append(rmse_c)

        boot_delta_r2_ca.append(r2_c - r2_a)
        boot_delta_rmse_ca.append(rmse_c - rmse_a)

    ci_bootstrap = {
        "Model_A_R2_95CI": [np.percentile(boot_r2_a, 2.5), np.percentile(boot_r2_a, 97.5)],
        "Model_B_R2_95CI": [np.percentile(boot_r2_b, 2.5), np.percentile(boot_r2_b, 97.5)],
        "Model_C_R2_95CI": [np.percentile(boot_r2_c, 2.5), np.percentile(boot_r2_c, 97.5)],
        "Model_A_RMSE_95CI": [np.percentile(boot_rmse_a, 2.5), np.percentile(boot_rmse_a, 97.5)],
        "Model_B_RMSE_95CI": [np.percentile(boot_rmse_b, 2.5), np.percentile(boot_rmse_b, 97.5)],
        "Model_C_RMSE_95CI": [np.percentile(boot_rmse_c, 2.5), np.percentile(boot_rmse_c, 97.5)],
        "Delta_R2_C_minus_A_95CI": [np.percentile(boot_delta_r2_ca, 2.5), np.percentile(boot_delta_r2_ca, 97.5)],
        "Delta_RMSE_C_minus_A_95CI": [np.percentile(boot_delta_rmse_ca, 2.5), np.percentile(boot_delta_rmse_ca, 97.5)],
        "Prob_Model_C_Better_Than_A_RMSE": np.mean(np.array(boot_delta_rmse_ca) < 0),
    }
    print("  -> Player-Level Bootstrap 95% CIs:")
    print(f"     Model A R^2: [{ci_bootstrap['Model_A_R2_95CI'][0]:.4f}, {ci_bootstrap['Model_A_R2_95CI'][1]:.4f}]")
    print(f"     Model C R^2: [{ci_bootstrap['Model_C_R2_95CI'][0]:.4f}, {ci_bootstrap['Model_C_R2_95CI'][1]:.4f}]")
    print(f"     Delta R^2 (C - A): Mean={np.mean(boot_delta_r2_ca):.4f}, 95% CI=[{ci_bootstrap['Delta_R2_C_minus_A_95CI'][0]:.4f}, {ci_bootstrap['Delta_R2_C_minus_A_95CI'][1]:.4f}]")
    print(f"     Delta RMSE (C - A): Mean={np.mean(boot_delta_rmse_ca):.4f}, 95% CI=[{ci_bootstrap['Delta_RMSE_C_minus_A_95CI'][0]:.4f}, {ci_bootstrap['Delta_RMSE_C_minus_A_95CI'][1]:.4f}]")
    print(f"     Probability Model C improves on Model A (lower RMSE): {ci_bootstrap['Prob_Model_C_Better_Than_A_RMSE']*100:.1f}%")

    # ---------------------------------------------------------
    # AUDIT ITEM 3: POSITION STRATIFICATION & FOLD COUNTS
    # ---------------------------------------------------------
    print("\n--- AUDITING POSITION STRATIFICATION ---")
    pos_counts_per_fold = []
    for fold_idx, (train_idx, test_idx) in enumerate(rskf.split(cohort_df.values, strata)):
        if fold_idx >= 5:  # Inspect repeat 0
            break
        test_sub = cohort_df.iloc[test_idx]
        counts = test_sub["macro_position"].value_counts().to_dict()
        granular_counts = test_sub["nfl_position"].value_counts().to_dict()
        pos_counts_per_fold.append({
            "fold": fold_idx + 1,
            "total_players": len(test_idx),
            **counts,
        })
    pos_fold_df = pd.DataFrame(pos_counts_per_fold)
    print("  -> Fold Distribution across Macro Groups (Repeat 1):\n", pos_fold_df)

    # ---------------------------------------------------------
    # AUDIT ITEM 4: NESTED CV HYPERPARAMETER TUNING
    # ---------------------------------------------------------
    print("\n--- AUDITING INCREMENTAL SENSOR VALUE VIA NESTED CV ---")
    # Outer 5-fold CV, Inner 5-fold CV tuning Ridge alpha in [0.01, 0.1, 1.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0]
    param_grid = {"regressor__alpha": [0.01, 0.1, 1.0, 5.0, 10.0, 20.0, 50.0, 100.0, 200.0]}
    
    outer_cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=5, random_state=RANDOM_SEED)

    def run_nested_cv(feat_cols):
        X = cohort_df[feat_cols].values
        oof_preds = np.zeros((n_players, 5))
        outer_fold_idx = 0

        for train_idx, test_idx in outer_cv.split(X, strata):
            rep = outer_fold_idx // 5
            X_tr, y_tr = X[train_idx], y[train_idx]
            X_te = X[test_idx]

            pipe = Pipeline([
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
                ("regressor", Ridge(random_state=RANDOM_SEED)),
            ])
            # Inner CV strictly on training fold
            grid = GridSearchCV(pipe, param_grid, cv=5, scoring="neg_root_mean_squared_error", n_jobs=1)
            grid.fit(X_tr, y_tr)

            best_pipe = grid.best_estimator_
            oof_preds[test_idx, rep] = best_pipe.predict(X_te)
            outer_fold_idx += 1

        mean_oof = np.mean(oof_preds, axis=1)
        ss_res = np.sum((y - mean_oof) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        r2 = 1.0 - (ss_res / ss_tot)
        rmse = np.sqrt(np.mean((y - mean_oof) ** 2))
        mae = np.mean(np.abs(y - mean_oof))
        spearman, _ = stats.spearmanr(y, mean_oof)
        return mean_oof, r2, rmse, mae, spearman

    print("  -> Running Nested CV for Model A (Tuned Traditional)...")
    oof_a_opt, r2_a_opt, rmse_a_opt, mae_a_opt, sp_a_opt = run_nested_cv(model_a_cols)
    print(f"     Model A Tuned: OOF R^2 = {r2_a_opt:.4f}, RMSE = {rmse_a_opt:.4f}, MAE = {mae_a_opt:.4f}")

    print("  -> Running Nested CV for Model B (Tuned Sensor)...")
    oof_b_opt, r2_b_opt, rmse_b_opt, mae_b_opt, sp_b_opt = run_nested_cv(model_b_cols)
    print(f"     Model B Tuned: OOF R^2 = {r2_b_opt:.4f}, RMSE = {rmse_b_opt:.4f}, MAE = {mae_b_opt:.4f}")

    print("  -> Running Nested CV for Model C (Tuned Hybrid)...")
    oof_c_opt, r2_c_opt, rmse_c_opt, mae_c_opt, sp_c_opt = run_nested_cv(model_c_cols)
    print(f"     Model C Tuned: OOF R^2 = {r2_c_opt:.4f}, RMSE = {rmse_c_opt:.4f}, MAE = {mae_c_opt:.4f}")

    # Paired differences on tuned OOF predictions
    paired_rmse_diff_ca = np.sqrt(np.mean((y - oof_c_opt) ** 2)) - np.sqrt(np.mean((y - oof_a_opt) ** 2))
    paired_t_stat, paired_p_val = stats.ttest_rel((y - oof_a_opt)**2, (y - oof_c_opt)**2)
    print(f"     Paired RMSE Difference (C - A): {paired_rmse_diff_ca:.4f}")
    print(f"     Diebold-Mariano / Paired Error t-test: t = {paired_t_stat:.4f}, p = {paired_p_val:.4f}")

    # ---------------------------------------------------------
    # AUDIT ITEM 5: ATHLETIC ALPHA RESIDUAL DIAGNOSTICS
    # ---------------------------------------------------------
    print("\n--- AUDITING ATHLETIC ALPHA RESIDUALS ---")
    alpha_raw = y - oof_a_opt
    cohort_df["athletic_alpha_audit"] = alpha_raw

    # Regress alpha against position, draft capital, snaps, game tracking frames
    # Load frame count per player
    trk_pl = pl.scan_csv("data/raw/game_tracking_2023.csv").group_by("nfl_id").agg(pl.len().alias("game_tracking_frames")).collect().to_pandas()
    cohort_df = cohort_df.merge(trk_pl, on="nfl_id", how="left")

    alpha_reg_vars = ["draft_overall_pick", "verified_scrimmage_snaps", "game_tracking_frames"]
    diagnostics = []
    for var in alpha_reg_vars:
        sub = cohort_df[["athletic_alpha_audit", var]].dropna()
        r, p = stats.spearmanr(sub["athletic_alpha_audit"], sub[var])
        diagnostics.append({"variable": var, "spearman_r": round(float(r), 4), "p_value": round(float(p), 5), "n": len(sub)})
    
    # Position ANOVA
    pos_groups = [group["athletic_alpha_audit"].values for _, group in cohort_df.groupby("macro_position")]
    anova_f, anova_p = stats.f_oneway(*pos_groups)
    print("  -> Confounding Checks on Athletic Alpha:")
    for d in diagnostics:
        print(f"     {d['variable']}: r = {d['spearman_r']:.4f}, p = {d['p_value']:.5f} (N={d['n']})")
    print(f"     Position Macro Group ANOVA: F = {anova_f:.4f}, p = {anova_p:.5f}")

    # ---------------------------------------------------------
    # AUDIT ITEM 6: BENJAMINI-HOCHBERG FDR CORRECTION
    # ---------------------------------------------------------
    print("\n--- AUDITING SENSOR CORRELATIONS WITH BENJAMINI-HOCHBERG FDR ---")
    corrs_raw = []
    for col in sensor_features:
        sub = cohort_df[["athletic_alpha_audit", col]].dropna()
        if len(sub) > 10:
            sr, sp = stats.spearmanr(sub["athletic_alpha_audit"], sub[col])
            pr, pp = stats.pearsonr(sub["athletic_alpha_audit"], sub[col])
            corrs_raw.append({
                "sensor_feature": col,
                "spearman_r": round(float(sr), 4),
                "spearman_raw_p": float(sp),
                "pearson_r": round(float(pr), 4),
                "n_samples": len(sub),
            })
    corr_audit_df = pd.DataFrame(corrs_raw).sort_values(by="spearman_raw_p").reset_index(drop=True)
    
    # Apply Benjamini-Hochberg
    p_values = corr_audit_df["spearman_raw_p"].values
    reject, q_values, _, _ = multipletests(p_values, alpha=0.05, method="fdr_bh")
    corr_audit_df["fdr_q_value"] = np.round(q_values, 5)
    corr_audit_df["is_significant_fdr_0.05"] = reject
    print("  -> FDR Adjusted Correlations:\n", corr_audit_df[["sensor_feature", "spearman_r", "spearman_raw_p", "fdr_q_value", "is_significant_fdr_0.05"]])
    corr_audit_df.to_csv(AUDIT_DIR / "fdr_corrected_correlations.csv", index=False)

    # ---------------------------------------------------------
    # AUDIT ITEM 7: COHORT RECONCILIATION
    # ---------------------------------------------------------
    print("\n--- RECONCILING PHASE 2 VS PHASE 3 COHORT COUNTS ---")
    c_pos_counts = cohort_df["combine_position"].value_counts().to_dict()
    nfl_pos_counts = cohort_df["nfl_position"].value_counts().to_dict()
    print("  -> combine_position in 149 players:", c_pos_counts)
    print("  -> nfl_position in 149 players:", nfl_pos_counts)

    # Save summary audit metrics
    nested_metrics = pd.DataFrame([
        {"model": "Model_A_Tuned_Ridge", "oof_r2": r2_a_opt, "oof_rmse": rmse_a_opt, "oof_mae": mae_a_opt, "spearman": sp_a_opt},
        {"model": "Model_B_Tuned_Ridge", "oof_r2": r2_b_opt, "oof_rmse": rmse_b_opt, "oof_mae": mae_b_opt, "spearman": sp_b_opt},
        {"model": "Model_C_Tuned_Ridge", "oof_r2": r2_c_opt, "oof_rmse": rmse_c_opt, "oof_mae": mae_c_opt, "spearman": sp_c_opt},
    ])
    nested_metrics.to_csv(AUDIT_DIR / "nested_cv_model_metrics.csv", index=False)
    
    print("\nPhase 3.1 Audit Script Finished Successfully!")
    return {
        "ci_bootstrap": ci_bootstrap,
        "nested_metrics": nested_metrics,
        "corr_audit_df": corr_audit_df,
        "diagnostics": diagnostics,
        "pos_fold_df": pos_fold_df,
    }


if __name__ == "__main__":
    run_full_statistical_audit()
