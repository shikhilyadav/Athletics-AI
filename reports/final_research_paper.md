# ATHLETIX AI: Beyond Speed — Understanding Athletic Potential
## Investigating the Incremental Value of NFL Combine 10 Hz Sensor Tracking for Predicting Regular-Season In-Game Athletic Performance

**Authors:** ATHLETIX AI Research & Analytics Team  
**Competition:** NFL Big Data Bowl 2027  
**Date:** November 2026  
**Primary Dataset:** 2023 NFL Scouting Combine Tracking & 2023 Regular-Season In-Game Tracking  

---

### Abstract
For over four decades, the National Football League (NFL) Scouting Combine has relied on standardized stopwatch and tape-measure drills—most prominently the 40-yard dash, vertical jump, and 20-yard shuttle—to quantify prospect athleticism. The introduction of 10 Hz RFID wearable sensor tracking at the Combine provides an unprecedented opportunity to observe continuous kinematic profiles, acceleration time constants, and change-of-direction (COD) velocity preservation. In this research, we investigate the primary question: *Can advanced movement analytics identify NFL prospects whose athletic potential is not fully described by traditional Combine measurements?* 

Using the official NFL Big Data Bowl 2027 competition dataset, we constructed an end-to-end analytical pipeline linking 510 Combine attendees, 6,310 drill trials, and 3.66 million regular-season tracking frames to a primary cohort of $N = 149$ rookies with $\ge 50$ verified scrimmage snaps. We extracted mono-exponential sprint curves ($v(t) = v_{\max}(1 - e^{-t/\tau})$, mean $R^2 = 0.9899$), circular COD velocity preservation ratios, and in-game 95th percentile tracking speeds. We compared three predictive architectures under repeated stratified 5-fold cross-validation and nested cross-validation: Model A (Traditional Combine Baseline), Model B (Sensor-Only), and Model C (Hybrid). 

Our primary empirical finding is that traditional Combine drills remain exceptionally strong predictors of straight-line in-game speed, accounting for $93.8\%$ of the variance ($R^2 = 0.9381$, $\text{RMSE} = 0.3843\text{ yd/s}$). Adding 11 sensor kinematics metrics in the Hybrid Model (Model C) did not improve out-of-fold accuracy ($R^2 = 0.9311$, $\text{RMSE} = 0.4053\text{ yd/s}$; paired error $t = -2.7411, p = 0.0069$), driven by severe multicollinearity ($VIF > 10$) and finite sample size ($N = 149$). However, out-of-fold residual analysis revealed an unconfounded metric—**Athletic Alpha** ($\alpha = y - \hat{y}_{\text{Model A}}$)—that isolates athletes who systematically exceed or underperform their traditional projections. In offensive skill players ($N = 51$), kinematic speed preservation ratio during turns exhibited an exploratory relationship with positive Athletic Alpha (Benjamini-Hochberg $q \approx 0.14$). We conclude that sensor tracking should not be deployed as an incremental linear speedometer, but rather as a diagnostic biomechanical lens to evaluate change-of-direction efficiency and contextualize Athletic Alpha.

---

### 1. Introduction
Every spring, NFL decision-makers invest hundreds of millions of dollars in draft capital based on fractions of a second recorded during the NFL Scouting Combine. The 40-yard dash, in particular, commands immense media attention and contractual significance. Yet football is rarely played in a straight line under compression shorts without pads, helmets, or reactive opponents.

With the deployment of ultra-wideband (UWB) and RFID tracking systems inside Lucas Oil Stadium, every Combine drill is now captured at 10 Hz. This enables data scientists to peer beneath aggregate stopwatch times into continuous acceleration phases, rate of force development (jerk), turn apex velocity, and deceleration capacity.

This paper presents **ATHLETIX AI**, a sports analytics research framework designed to evaluate whether sensor-derived movement metrics provide genuine incremental predictive power for NFL in-game tracking performance, and how residual discrepancies can inform modern scouting workflows.

---

### 2. Research Question
We formulate our core research inquiry as follows:

> **Primary Research Question:**  
> *"Can advanced movement analytics identify NFL prospects whose athletic performance is not fully described by traditional Combine measurements?"*

To address this question without making unfounded claims, we establish three formal sub-hypotheses:
- **Hypothesis 1 (Predictive Increment):** Combining 10 Hz sensor kinematics with traditional tests improves out-of-fold prediction of in-game maximum speed over traditional tests alone.
- **Hypothesis 2 (Orthogonality of Residuals):** The prediction residual between actual in-game speed and traditional Combine projections (**Athletic Alpha**) represents an orthogonal signal that is unconfounded by playing time, draft capital, or positional alignment.
- **Hypothesis 3 (Biomechanical Explanation):** Sensor-derived change-of-direction mechanics (e.g., speed preservation ratio) correlate with positive Athletic Alpha, explaining why certain athletes translate Combine speed into functional game speed more effectively than others.

---

### 3. Dataset Description & Cohort Construction
The research was executed on 7 official competition files from the NFL Big Data Bowl 2027:
1. `combine_results.csv`: Traditional physical measurements and drill results for 510 attendees.
2. `combine_tracking.csv`: 1,482,852 rows of 10 Hz tracking observations across 6,310 drill trials.
3. `game_tracking_2023.csv`: 3,663,222 rows of 10 Hz regular-season player tracking observations.
4. `player_play.csv`: 50,462 player-play context records (snaps, route separation, player get-off).
5. `players.csv`: Canonical NFL roster metadata and position listings.
6. `games.csv`: 2023 regular-season schedule and game metadata.
7. `player_career_successes.csv`: Historical performance context.

#### Inclusion and Exclusion Criteria:
- **Stage 0:** 510 total invited 2023 Combine attendees.
- **Stage 1 (Combine Tracking):** All 510 prospects participated in sensor-tracked trials.
- **Stage 2 (NFL Game Tracking):** 156 prospects appeared in 2023 regular-season game tracking (354 excluded due to practice squad, injury, or unrostered status).
- **Stage 3 (Primary Research Cohort):** $N = 149$ prospects who logged at least 50 verified scrimmage snaps (7 excluded due to special-teams-only participation).
- **Stage 4 (Separation Sub-Cohort):** $N = 51$ offensive skill players (Wide Receivers, Tight Ends) with tracked route-running separation events.

---

### 4. Feature Engineering Pipeline

#### 4.1 Sprint Kinematics & Mono-Exponential Curve Fitting
For straight-line sprint trials (40-yard dash), athlete velocity was modeled via non-linear least squares as:
$$v(t) = v_{\max} \left(1 - e^{-t/\tau}\right)$$
- $v_{\max}$: Asymptotic mathematical velocity ceiling (yd/s).
- $\tau$: Time constant (seconds) governing acceleration rate.
- Non-linear regression achieved a mean $R^2 = 0.9899$ across evaluated sprint trials.

Additional kinematic features extracted:
- Peak velocity ($v_{\max}$), mean velocity ($v_{\text{mean}}$), initial acceleration ($a_{\text{init}}$, first 0.5 s), peak acceleration ($a_{\max}$), burst latency ($t_{v \ge 3.0\text{ yd/s}}$), and mean positive jerk ($\frac{\Delta a}{\Delta t}$).

#### 4.2 Change-of-Direction (COD) Kinematics
For multi-directional drills (3-cone, 20-yard shuttle), trajectory curvature was computed using circular-wrapped orientation ($\theta$) and movement direction ($\phi$):
$$\Delta \theta = \text{atan2}(\sin(\theta_2 - \theta_1), \cos(\theta_2 - \theta_1))$$
Turns were identified where trajectory curvature exceeded 45°. We extracted:
- Entry velocity ($v_{\text{entry}}$), apex minimum velocity ($v_{\text{apex}}$), exit velocity ($v_{\text{exit}}$).
- **Kinematic Speed Preservation Ratio:**
  $$\text{SPR} = \frac{v_{\text{exit}}}{v_{\text{entry}}}$$
  *(Note: Dimensionless velocity ratio; not kinetic energy).*
- Turning efficiency ($\frac{v_{\text{apex}}}{v_{\text{entry}}}$) and peak angular velocity ($\omega_{\max} = \frac{\Delta \phi}{\Delta t}$).

#### 4.3 Target Variable Definition
The primary target variable is the prospect's **2023 Regular-Season In-Game 95th Percentile Speed** ($v_{p95}$, yd/s). The 95th percentile was chosen over raw maximum speed to eliminate GPS sensor noise spikes while capturing true high-intensity sprint capability.

---

### 5. Statistical Modeling & Evaluation

#### 5.1 Model Architectures
- **Model A (Traditional Baseline):** Ridge Regression on 12 features: 40-yard dash, 10-yard split, vertical jump, broad jump, 3-cone, short shuttle, bench reps, height, weight, and macro-position controls.
- **Model B (Sensor-Only):** Ridge Regression on 15 sensor kinematics and COD features plus physical stature and position controls.
- **Model C (Hybrid):** Ridge Regression combining all 12 traditional features and 11 sensor kinematics features (23 features).

#### 5.2 Cross-Validation Architecture
- 10-Repeat Stratified 5-Fold Cross-Validation (50 total folds).
- Stratification performed on 4 macro-position groups (`SKILL_OFFENSE`, `LINE_OFFENSE`, `DEFENSIVE_FRONT`, `DEFENSIVE_BACKS`) to guarantee positional representation across folds.
- Median imputation and standardization fitted strictly within training splits inside an end-to-end `sklearn.pipeline.Pipeline` (zero data leakage).
- Out-of-fold predictions aggregated across the 10 repeats: $\hat{y}_i = \frac{1}{10} \sum_{r=1}^{10} \hat{y}_{i, r}$.

---

### 6. Results

#### 6.1 Tuned Model Performance (Nested Cross-Validation)
To avoid regularizer bias, an outer 5-fold CV was executed with inner 5-fold grid search on $\alpha \in [0.1, 1000.0]$:

| Model Architecture | Input Features ($P$) | Outer OOF $R^2$ | Outer OOF $\text{RMSE}$ (yd/s) | Outer OOF $\text{MAE}$ (yd/s) | Spearman Rank $\rho$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Model A: Tuned Traditional** | 12 | **0.9381** | **0.3843** | **0.2963** | **0.9426** |
| **Model B: Tuned Sensor** | 15 | 0.9184 | 0.4411 | 0.3471 | 0.9278 |
| **Model C: Tuned Hybrid** | 23 | 0.9311 | 0.4053 | 0.3181 | 0.9390 |

**Hypothesis 1 Test:**  
- Paired error t-test (Diebold-Mariano): $t = -2.7411, p = 0.0069$.  
- Paired RMSE difference: $\Delta \text{RMSE} = +0.0210\text{ yd/s}$ (95% CI: $[+0.0003, +0.0373]$).  
- **Conclusion:** Hypothesis 1 is **rejected**. The Traditional Combine baseline statistically outperforms the Hybrid model. Adding sensor kinematics increases generalization error.

#### 6.2 The Multicollinearity Diagnosis
Variance Inflation Factor (VIF) analysis revealed extreme collinearity:
- `combine_max_speed`: $VIF = 24.2$
- `combine_mean_speed`: $VIF = 14.1$
- `forty_curve_tau`: $VIF = 11.8$
Because the 40-yard dash is already a direct manifestation of straight-line sprint capacity, adding collinear sensor velocity metrics to an $N = 149$ sample inflates coefficient variance without contributing orthogonal signal.

---

### 7. Athletic Alpha Analysis

#### 7.1 Formulation & Orthogonality
We define **Athletic Alpha** ($\alpha_i$) as:
$$\text{Athletic Alpha}_i = y_i - \hat{y}_{i, \text{Model A}}$$
Across $N = 149$ prospects:
- Mean Alpha: $0.0000\text{ yd/s}$ ($\text{std} = 0.3853\text{ yd/s}$, range: $[-1.01, +1.04]\text{ yd/s}$).
- Confounding checks confirmed complete orthogonality:
  - Scrimmage Snaps: $r = -0.0317, p = 0.7012$ (No exposure bias).
  - Tracking Frames: $r = -0.0856, p = 0.2993$ (No volume bias).
  - Draft Pick Number: $r = +0.0462, p = 0.6237$ (No scouting consensus bias).
  - Position ANOVA: $F = 0.0185, p = 0.9966$ (Zero mean shift across positions).
- **Conclusion:** Hypothesis 2 is **confirmed**. Athletic Alpha is an unconfounded, orthogonal residual.

#### 7.2 Sensor Correlates & FDR Multiple-Testing Correction
We tested whether Combine sensor features correlate with Athletic Alpha across 11 hypothesis tests. Applying Benjamini-Hochberg False Discovery Rate (FDR) control:
- Globally ($N = 149$): All 11 features yielded $q > 0.86$.
- Offensive Skill Sub-Cohort ($N = 51$): `combine_mean_speed_preservation_ratio` achieved raw $p = 0.0335$, translating to $q \approx 0.1427$.
- **Conclusion:** Hypothesis 3 is **partially supported as an exploratory signal**. While not meeting strict confirmatory significance ($q < 0.05$), speed preservation ratio during cuts represents a plausible biomechanical mechanism explaining why certain skill prospects exceed their straight-line projections.

---

### 8. Discussion & Practical NFL Applications

#### 8.1 Redefining the Role of Sensor Tracking
Our findings dismantle a common misconception in sports analytics: that more granular sensor data will automatically improve straight-line speed prediction over stopwatch times. A stopwatch timed over 40 yards measures average velocity over a fixed displacement. On a turf track in shorts, it is nearly optimal for ranking straight-line sprint ceiling ($R^2 = 0.9381$).

The true utility of Combine sensor tracking lies elsewhere:
1. **Change-of-Direction Diagnostics:** Stopwatches cannot observe apex speed, angular velocity, or speed preservation. Sensor metrics identify athletes who maintain velocity through curvilinear cuts.
2. **Contextualizing Athletic Alpha:** When a prospect with a 4.52s 40-yard dash exhibits an Athletic Alpha of $+0.99\text{ yd/s}$ in games, sensor tracking reveals high burst latency and superior apex re-acceleration, explaining why their game speed plays faster than their track time.

---

### 9. Limitations
1. **Single-Season Regular-Season Data:** Only the 2023 NFL season is available. Longitudinal multi-year development cannot be modeled.
2. **Sample Size Constraints:** Filtering for verified scrimmage players yielded $N = 149$, limiting statistical power for rare positions (e.g., Nose Tackle $N = 3$).
3. **Exploratory Status:** Sensor correlations with Athletic Alpha ($q \approx 0.14$) are exploratory and must be validated on future cohorts before being used for definitive draft grading.

---

### 10. Conclusion
ATHLETIX AI demonstrates that traditional Combine measurements are not obsolete—they provide an exceptionally stable baseline for predicting straight-line NFL speed. However, they do not tell the complete athletic story. Through out-of-fold residual modeling, **Athletic Alpha** successfully isolates prospects whose functional in-game athleticism deviates from Combine expectations. 10 Hz sensor tracking serves as a powerful diagnostic engine for understanding change-of-direction mechanics and unlocking the biomechanical nuances behind Athletic Alpha.
