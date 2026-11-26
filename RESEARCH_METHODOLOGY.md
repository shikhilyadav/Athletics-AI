# ATHLETIX AI: Research Methodology Specification (Revised) 🔬📐

**Project**: ATHLETIX AI  
**Tagline**: *Beyond Speed. Understanding Athletic Potential.*  
**Primary Research Question**: *"Can advanced movement analytics identify NFL prospects whose athletic potential is underestimated by traditional Combine measurements?"*

---

## 1. Problem Formulation & Theoretical Framework

### 1.1 The Underestimated Athletic Potential Hypothesis
Traditional pre-draft evaluation relies on discrete scalar measurements recorded in static Combine drills:
$$\mathbf{x}_{\text{trad}} \in \mathbb{R}^{d_{\text{trad}}} = [\text{40yd}, \text{10yd split}, \text{20yd split}, \text{vert jump}, \text{broad jump}, \text{3-cone}, \text{shuttle}, \text{weight}, \text{height}]^T$$

In contrast, on-field NFL performance and career outcomes $\mathbf{y}_{\text{career}} \in \mathbb{R}$ (from `player_career_successes.csv`) and in-game tracking kinematics $\mathbf{y}_{\text{game}}$ (from `game_tracking_*.csv`) reflect functional, continuous athleticism:
$$\mathbf{y}_i = \hat{\mathbf{y}}_{\text{trad}}(\mathbf{x}_{\text{trad}, i}) + \epsilon_i$$
$$\text{Athletic Alpha}_i \equiv \epsilon_i = \mathbf{y}_i - \hat{\mathbf{y}}_{\text{trad}}(\mathbf{x}_{\text{trad}, i})$$

Where:
* $\epsilon_i \gg 0$: The player is an **underestimated athletic prospect**—their on-field performance or career trajectory systematically outstrips traditional stopwatch and jump expectations.
* $\epsilon_i \ll 0$: The player is an **overestimated athlete ("workout warrior")**—outstanding Combine metrics that fail to translate to regular-season tracking dynamics.

### 1.2 Objective
Determine whether high-frequency $10\text{ Hz}$ movement features $\mathbf{Z}_{\text{sensor}}$ extracted from `combine_tracking.csv` explain this residual $\epsilon_i$ with statistical significance, thereby identifying prospects overlooked by conventional scouting.

---

## 2. Ingestion, Integration, and Entity Resolution

### 2.1 Entity Resolution Protocol
Across `combine_tracking.csv`, `combine_results.csv`, `players.csv`, `player_play.csv`, and `player_career_successes.csv`, player keys can appear as `nfl_id`, `nflId`, or require cross-table matching:
1. **Primary Link**: Match on numeric player identifier (`nfl_id` / `nflId`).
2. **Secondary Link (Entity Disambiguation)**: If missing in pre-draft Combine records, match via `(Standardized Name, College, Draft Year)`.
3. **Data Integrity Rule**: Unresolved entities are tagged and excluded from modeling to avoid cross-player leakage.

### 2.2 Coordinate and Kinematic Harmonization
* **Standard Grid**: $X \in [0.0, 120.0]$ yards, $Y \in [0.0, 53.33]$ yards.
* **Direction Normalization**: When `play_direction == 'left'`, reflect coordinates:
  $$x_{\text{norm}} = 120.0 - x, \quad y_{\text{norm}} = 53.333 - y, \quad \theta_{\text{norm}} = (\theta + 180^\circ) \pmod{360^\circ}$$
* **Temporal Frequency**: $10.0\text{ Hz}$ ($\Delta t = 0.1\text{ s}$).

---

## 3. Strict Memory Optimization for 8 GB RAM

Because regular-season tracking spans three multi-gigabyte files (`game_tracking_2023.csv`, `game_tracking_2024.csv`, `game_tracking_2025.csv`), memory governance is critical:

1. **Lazy Execution Pipeline**:
   All heavy scanning operations utilize Polars lazy frames (`pl.scan_csv()`). Filtering, projection, and grouping are pushed down to avoid loading unnecessary rows or columns.
2. **Sequential Season Aggregation**:
   Each season file is processed individually. Intermediate aggregates (e.g. per-player 95th percentile speed, burst acceleration count) are materialized to disk as lightweight Parquet summaries before releasing memory.
3. **PyArrow Zero-Copy Ingestion**:
   When converting datasets for model training, PyArrow with snappy compression is used.

---

## 4. Biomechanical Movement Feature Engineering

From `combine_tracking.csv`, we extract:
1. **Sprint Kinematics**:
   * Peak Velocity ($v_{\max}$) and Peak Acceleration ($a_{\max}$).
   * Time to Peak Acceleration ($t_{a_{\max}}$): Burst latency.
   * Neuromuscular Jerk ($j_t = \frac{\Delta a}{\Delta t}$): Mean positive jerk during first $1.0\text{ s}$ ($\bar{j}_{0-1s}$).
   * Mono-exponential velocity curve fitting: $v(t) = v_{\max}(1 - e^{-t/\tau})$.
2. **Change of Direction (COD) Mechanics**:
   * Minimum apex velocity during 3-cone and shuttle transitions ($v_{\text{apex}}$).
   * COD Transition Efficiency Ratio: $\eta_{\text{COD}} = \frac{v_{\text{apex}}}{v_{\text{entry}}}$.
   * Deceleration-to-reacceleration latency ($\Delta t_{\text{trans}}$).

---

## 5. Statistical Modeling, Validation & Leakage Controls

### 5.1 Prospective Time-Split Cross-Validation
* **Leakage Prevention**: Features extracted from `combine_tracking.csv` and `combine_results.csv` are strictly pre-draft.
* Game tracking and career success outcomes are strictly prospective.
* Cross-validation is grouped by `draft_year` or rookie season (e.g. Train on 2023, Test on 2024/2025) to simulate real-world draft decision-making.

### 5.2 Controlling for Confounding Factors
1. **Playing Time Minimums**:
   Players with insufficient NFL snaps ($< 50$ offensive/defensive snaps in `player_play.csv`) cannot produce stable tracking percentiles and are excluded from speed-percentile modeling.
2. **Positional Stratification**:
   Because biomechanical demands differ radically by position, all analyses are stratified by positional cohorts.
3. **Correlation vs. Causation**:
   High tracking metrics indicate athletic efficiency, not football mastery. Findings are reported as correlational enablers, not causal determinism.

---

## 6. Model Explainability via TreeSHAP

We apply TreeSHAP to the gradient-boosted movement models:
$$\hat{f}(x) = \phi_0 + \sum_{j=1}^M \phi_j(x)$$
* **Global Summary**: Ranks which micro-sensor features carry higher predictive power than stopwatch 40-yard times.
* **Local Waterfall**: Explains specific outlier athletes whose traditional Combine numbers were mediocre, but whose high-jerk acceleration curves propelled them to elite NFL tracking performance.
