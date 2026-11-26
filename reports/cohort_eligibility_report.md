# ATHLETIX AI: Cohort Eligibility & Research Controls Report 📋🏈

**Date**: November 2026  
**Scope**: Cohort segregation, playing opportunity thresholds, and data leakage controls.

---

## 1. Multi-Year Draft Cohort Partitioning

The master analytical dataset (`combine_player_master.parquet`) tracks all **$510$ prospects** across three distinct draft classes:

| Draft Year | Total Prospects | Combine Tracking Available | 2023 Game Tracking Status | Research Cohort Classification |
| :--- | :--- | :--- | :--- | :--- |
| **2023** | $160$ | $160$ ($100.0\%$) | $156$ active ($4$ inactive) | **Primary Prospective Evaluation Cohort** |
| **2024** | $177$ | $177$ ($100.0\%$) | $0$ (Season unreleased in 2023 tracking) | **Future Prospective Cohort (Holdout)** |
| **2025** | $173$ | $173$ ($100.0\%$) | $0$ (Season unreleased in 2023 tracking) | **Future Prospective Cohort (Holdout)** |
| **Total** | **$510$** | **$510$ ($100.0\%$)** | **$156$** | — |

> **Critical Research Control**: In `combine_player_master.parquet`, players from the 2024 and 2025 cohorts are explicitly assigned `game_target_cohort_status = FUTURE_COHORT_2024_UNAVAILABLE` and `FUTURE_COHORT_2025_UNAVAILABLE`. They are **never treated as having missing 2023 data**, preventing false zero or missing-data imputation artifacts.

---

## 2. Verified Scrimmage Snap Eligibility ($\ge 50$ Snaps)

### Counting Methodology
A verified scrimmage snap is defined as any distinct `(game_id, play_id)` in `player_play.csv` where:
$$\text{play\_nullified\_by\_penalty} \neq \text{'Y'}$$

### Eligibility Breakdown for 2023 Rookie Cohort:
* **Total 2023 Prospects**: $160$
* **Tracked in 2023 Games**: $156$
* **Eligible ($\ge 50$ Scrimmage Snaps)**: **$149$ ($95.5\%$)**
* **Ineligible ($< 50$ Scrimmage Snaps)**: **$7$ ($4.5\%$)**
  * Average snaps for ineligible group: $14.2$ snaps.
  * *Reason for exclusion*: Small sample sizes in tracking frames cause extreme volatility in $95\text{th}$ and $99\text{th}$ percentile game speeds. Filtering them ensures research validity.

---

## 3. Position Group Distribution of Eligible 2023 Rookies

The $149$ verified eligible 2023 prospects span all major NFL positional groupings:

| Position Group | Count of Eligible Prospects | Avg 2023 Scrimmage Snaps | Avg Combine $v_{\max}$ | Avg In-Game $v_{\text{p95}}$ |
| :--- | :--- | :--- | :--- | :--- |
| **Wide Receivers (WR)** | $31$ | $612.4$ | $10.42\text{ yd/s}$ | $7.15\text{ yd/s}$ |
| **Cornerbacks (CB)** | $20$ | $748.1$ | $10.41\text{ yd/s}$ | $7.18\text{ yd/s}$ |
| **Offensive Tackles (T)** | $17$ | $921.3$ | $9.38\text{ yd/s}$ | $5.32\text{ yd/s}$ |
| **Defensive Tackles (DT)** | $14$ | $514.8$ | $9.56\text{ yd/s}$ | $5.64\text{ yd/s}$ |
| **Tight Ends (TE)** | $12$ | $638.2$ | $10.08\text{ yd/s}$ | $6.48\text{ yd/s}$ |
| **Defensive Ends (DE)** | $11$ | $592.5$ | $9.92\text{ yd/s}$ | $6.21\text{ yd/s}$ |
| **Safeties (SS/FS)** | $10$ | $704.6$ | $10.35\text{ yd/s}$ | $7.02\text{ yd/s}$ |
| **Other Positions** | $34$ | $710.2$ | $10.12\text{ yd/s}$ | $6.41\text{ yd/s}$ |

---

## 4. Scientific Safeguards & Data Leakage Prevention

1. **Temporal Pre-Draft Segregation**:
   All kinematic and COD features derived from `combine_tracking.csv` represent pre-draft movement. They contain zero post-draft regular-season information.
2. **Post-Combine Outcomes Isolated as Targets**:
   In-game speed percentiles (`game_speed_p95`, `game_speed_p99`) and career outcomes (`career_games_started`, `pro_bowl_original_ballot`) exist strictly as target variables and are quarantined from the feature space.
3. **No Synthetic Imputation**:
   Prospects with missing traditional agility numbers (e.g. 3-cone opt-outs) retain true `null` values in the traditional columns, while their continuous sensor features provide complete empirical coverage.
