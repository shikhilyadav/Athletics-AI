# ATHLETIX AI — Technical Methodology Specification

**Competition:** NFL Big Data Bowl 2027  
**Target:** Engineering, Biomechanics, and Machine Learning Architecture  

---

## 1. System Architecture

```
[Raw Competition Data (data/raw/)]
   ├── combine_results.csv (510 attendees)
   ├── combine_tracking.csv (1.48M rows, 6,310 trials @ 10 Hz)
   ├── game_tracking_2023.csv (3.66M rows @ 10 Hz)
   ├── player_play.csv (50,462 plays)
   └── players.csv & games.csv
          │
          ▼
[Phase 2 Feature Extraction (src/features/)]
   ├── kinematics.py: v_max, a_init, jerk, mono-exponential sprint curve fitting
   ├── cod_metrics.py: circular angle wrapping, apex speed, speed preservation ratio
   └── tracking_aggregators.py: 95th/99th percentile speed, snap filtering
          │
          ▼
[Processed Parquet Layer (data/processed/)]
   ├── combine_player_master.parquet (510 rows, 48 cols)
   ├── combine_kinematic_features.parquet (6,310 rows, 23 cols)
   ├── combine_cod_features.parquet (6,310 rows, 18 cols)
   └── game_tracking_features_2023.parquet (156 rows, 14 cols)
          │
          ▼
[Phase 3 & 3.1 Modeling & Audit (src/models/)]
   ├── 10-Repeat 5-Fold Stratified Cross-Validation (50 folds)
   ├── Nested CV with Inner Hyperparameter Grid Search (α ∈ [0.1, 1000.0])
   ├── Player-Level Non-Parametric Bootstrap (B = 2,000 iterations)
   └── Benjamini-Hochberg False Discovery Rate (FDR) Multi-Testing Correction
          │
          ▼
[Phase 4 Interactive Dashboard (src/dashboard/)]
   └── Modular Streamlit App (app.py, data_loader, metrics, components, charts, 6 pages)
```

---

## 2. Mathematical Formulations

### 2.1 Mono-Exponential Sprint Velocity Curve
For straight-line sprints (40-yard dash):
$$v(t) = v_{\max} \left(1 - e^{-t/\tau}\right)$$
- Fitting Method: Non-linear least squares (`scipy.optimize.curve_fit`) with bounds $v_{\max} \in [5, 14]\text{ yd/s}$, $\tau \in [0.1, 3.0]\text{ s}$.
- Goodness-of-Fit:
  $$R^2 = 1 - \frac{\sum (v_i - \hat{v}_i)^2}{\sum (v_i - \bar{v})^2}$$
  Empirical mean across 2023 Combine sprint trials: **$R^2 = 0.9899$**.

### 2.2 Circular Change-of-Direction Curvature
To handle the $0^\circ / 360^\circ$ circular discontinuity in orientation ($\theta$) and direction ($\phi$):
$$\Delta \theta = \text{atan2}(\sin(\theta_{t} - \theta_{t-1}), \cos(\theta_{t} - \theta_{t-1}))$$
- **Kinematic Speed Preservation Ratio:**
  $$\text{SPR} = \frac{v_{\text{exit}}}{v_{\text{entry}}}$$
  where $v_{\text{entry}}$ is speed 0.5 s prior to turn apex, and $v_{\text{exit}}$ is speed 0.5 s post-apex.

### 2.3 Athletic Alpha Residual Formulation
$$\text{Athletic Alpha}_i = y_i - \hat{y}_{i, \text{Model A}}$$
where:
$$\hat{y}_{i, \text{Model A}} = \frac{1}{10} \sum_{r=1}^{10} \hat{y}_{i, r}$$
is the out-of-fold prediction averaged across 10 cross-validation repeats.

---

## 3. Regularization & Cross-Validation Strategy

- **Pipeline Isolation:** Median imputation and standard scaling are fitted strictly inside each training fold:
  ```python
  Pipeline([
      ("imputer", SimpleImputer(strategy="median")),
      ("scaler", StandardScaler()),
      ("regressor", Ridge(alpha=alpha))
  ])
  ```
- **Nested CV:** Outer 5-fold CV splits data into 80% train, 20% test. Inner 5-fold CV on the training split selects $\alpha^* = \arg\min_{\alpha} \text{MSE}_{\text{val}}(\alpha)$. The chosen $\alpha^*$ is refit on the outer train set and evaluated on the holdout test set.
- **Uncertainty Estimation:** Player-level non-parametric bootstrap ($B = 2,000$ iterations) resamples the $N = 149$ player vector with replacement to generate empirical 95% confidence intervals for $R^2$, $\text{RMSE}$, and paired differences ($\Delta \text{RMSE}$).
