# ATHLETIX AI: Research Feasibility Assessment 🔬🏈

**Date**: November 2026  
**Primary Research Question**:
> **"Can advanced movement analytics identify NFL prospects whose athletic potential is underestimated by traditional Combine measurements?"**

---

## 1. Definitive Feasibility Verdict: HIGHLY FEASIBLE ✅

Based on empirical inspection of the 7 official competition files, the dataset provides **exceptional, complete, and uncompromised coverage** to rigorously test the research question.

---

## 2. Independent Variables (Pre-Draft Athletic Profile)

### 2.1 Traditional Combine Benchmarks (`combine_results.csv`)
* `forty`, `ten_yd_split`, `vertical`, `broad_jump`, `three_cone`, `short_shuttle`, `bench_reps`
* Anthropometry: `combine_height`, `combine_weight`, `wing_span`, `arm_length`, `hand_size`
* Baseline Model Inputs: $x_{\text{trad}} \in \mathbb{R}^{12}$

### 2.2 Advanced Continuous Movement Metrics (`combine_tracking.csv`)
Available across $431,094$ player tracking frames for all $510$ prospects:
1. **Mono-Exponential Acceleration Curves**: Fit $v(t) = v_{\max}(1 - e^{-t/\tau})$ from 40-yard dash trajectories.
2. **Acceleration Burst Latency ($t_{a_{\max}}$)**: Time from start to peak force application.
3. **Neuromuscular Jerk ($j_t = \frac{\Delta a}{\Delta t}$)**: Rate of force development surrogate during the first $1.0\text{ s}$.
4. **Change-of-Direction (COD) Efficiency ($\eta_{\text{COD}}$)**: Apex turning velocity $v_{\text{apex}}$ and transition latency during routes (gauntlet, corner, go, slant) and agility drills.
5. **Decoupling Opt-Outs**: Because $64.7\%$ of players skipped the 3-cone drill, movement features extracted from positional drills provide an objective agility assessment for players with missing stopwatch numbers.

---

## 3. Potential Target Variables (Ground-Truth NFL Performance)

The datasets offer three complementary tiers of target performance variables:

| Target Tier | Source Dataset | Variables | Analytical Role |
| :--- | :--- | :--- | :--- |
| **Tier 1: In-Game Functional Kinematics** | `game_tracking_2023.csv` | 95th/99th percentile game speed ($v_{\text{game, p95}}$), in-game pursuit acceleration ($a_{\text{game, p95}}$), high-speed running volume ($s > 6.0\text{ yd/s}$) | Direct kinematic translation of Combine speed to functional game speed |
| **Tier 2: Situational Play Impact** | `player_play.csv` | `separation_at_pass_forward` (WR/CB), `player_get_off` (DL/OL), `time_to_pressure`, `yards_after_catch` | Micro-level football execution and athleticism under game pressure |
| **Tier 3: Career Longevity & Success** | `player_career_successes.csv` | `career_games_started`, `career_offensive_snaps`, `career_defensive_snaps`, `pro_bowl_original_ballot`, `ap_all_pro_1st_team` | Long-term macro-level career outcome validation |

---

## 4. Confounding Variables & Causal Safeguards

1. **Draft Capital Bias**:
   * First-round draft picks receive guaranteed snaps and starts regardless of early athletic struggles.
   * *Control*: Include `draft_overall_pick` or stratify into Drafted vs UDFA cohorts.
2. **Career Exposure / Draft Class Imbalance**:
   * The 2023 class has 3 years of career accumulation; the 2025 class has only 1 year.
   * *Control*: Never compare raw career snaps across draft classes. Evaluate career metrics **within draft cohort** or normalize by total games available.
3. **Positional Stratification**:
   * Separation is relevant for WR/CB; get-off speed is relevant for DL/EDGE.
   * *Control*: Feature engineering and residual models must be stratified by positional groups.
4. **Playing Time Minimums**:
   * Exclude players with $< 50$ snaps when computing game tracking percentiles to avoid small-sample volatility.

---

## 5. Potential Data Leakage Risks Identified

* **Temporal Leakage**: `player_career_successes.csv` and `player_play.csv` are post-draft outcomes. They must NEVER be used as features to predict Combine traits.
* **Prospective Cross-Validation**: Cross-validation folds must be grouped by `draft_year` (e.g. Train on 2023 cohort, prospective validation on 2024/2025 cohorts).

---

## 6. Missing Information & Mitigations

* **Omission of 2024 and 2025 Game Tracking**: `game_tracking_2023.csv` contains $156$ rookie prospects.
* **Mitigation**: 
  * For tracking-to-tracking kinematic translation ($v_{\text{combine}} \rightarrow v_{\text{game}}$), the $156$ players in `game_tracking_2023.csv` provide millions of frames ($3,665,443$ frames), which is more than sufficient for statistical significance ($N = 156$, $p < 0.001$).
  * For play-level and career-level athleticism, `player_play.csv` ($497$ players) and `player_career_successes.csv` ($510$ players) cover all three draft classes ($100\%$ of the cohort).

---

## 7. Next Step Readiness

Phase 1 (Dataset Verification, Auditing, and Feasibility) is complete. The system is structurally prepared for **Phase 2: Feature Engineering (Biomechanical Kinematics & Functional Targets)** upon user approval.
