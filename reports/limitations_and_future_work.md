# ATHLETIX AI — Scientific Limitations & Future Research Directions

**Competition:** NFL Big Data Bowl 2027  
**Category:** Research Integrity & Future Roadmap  

---

## 1. Explicit Scientific Limitations

Every data-driven sports analytics project has strict boundary conditions. In ATHLETIX AI, we explicitly document six scientific limitations:

### 1.1 Single-Season Regular-Season Data
- **Limitation:** The official competition dataset provides regular-season tracking exclusively for the 2023 NFL season.
- **Impact:** We cannot observe longitudinal multi-year development curves (e.g., rookie to year 2/3 translation), career longevity, or year-over-year athletic decline.

### 1.2 Small Sample Size in Rare Positional Roles
- **Limitation:** Requiring $\ge 50$ verified regular-season scrimmage snaps yielded $N = 149$ eligible prospects.
- **Impact:** Certain positions contain very few observations (e.g., Nose Tackle $N = 3$, Center $N = 7$). While macro-position stratification groups these into broader defensive front and offensive line buckets, position-specific linear models cannot be isolated without severe overfitting.

### 1.3 High Multicollinearity Between Stopwatches and Kinematics
- **Limitation:** 10 Hz sensor velocities and 40-yard dash stopwatch times measure the same physical phenomenon (straight-line displacement over time).
- **Impact:** Variance Inflation Factors exceed $10.0$ for 7 kinematic features ($VIF = 24.2$ for peak sensor velocity). In small samples ($N = 149$), adding highly collinear features inflates estimation variance, causing the Hybrid model to underperform the simpler baseline ($\Delta \text{RMSE} = +0.021\text{ yd/s}, p = 0.0069$).

### 1.4 Multiple Testing & Exploratory Correlation Status
- **Limitation:** Testing 11 sensor features against Athletic Alpha requires False Discovery Rate (FDR) adjustments.
- **Impact:** After applying the Benjamini-Hochberg procedure, global correlations yield $q > 0.86$, and skill sub-cohort correlations yield $q \approx 0.14$. These results are hypothesis-generating, not statistically confirmatory ($q < 0.05$).

### 1.5 Non-Causal Nature of Athletic Alpha
- **Limitation:** Athletic Alpha is an empirical out-of-fold linear regression residual ($\alpha = y - \hat{y}$).
- **Impact:** A high Athletic Alpha does not prove intrinsic hidden talent, and a low Athletic Alpha does not denote a draft bust. Residuals reflect complex in-game factors including offensive scheme, play calling, defensive coverage matchups, ball-in-hand opportunities, and pursuit geometry.

### 1.6 Physical Distinction of Speed Preservation Ratio
- **Limitation:** Change-of-direction performance is captured as $\text{SPR} = v_{\text{exit}} / v_{\text{entry}}$.
- **Impact:** This is a dimensionless kinematic velocity ratio. It cannot be referred to as "kinetic energy" because body mass is not multiplied quadratically ($E_k = \frac{1}{2}m v^2$).

---

## 2. Future Research Directions

### 2.1 Non-Linear Deep Kinematic Encoders
While linear Ridge regression suffered from multicollinearity, future research could explore 1D-Convolutional Neural Networks (1D-CNN) or Recurrent Transformer encoders trained directly on the raw 10 Hz velocity/acceleration time-series curves. Such models could learn latent movement representations that bypass handcrafted collinear features.

### 2.2 Contextual Game-Speed Normalization
In-game 95th percentile speed does not account for the role an athlete plays on specific snaps (e.g., deep route runner vs. shallow crosser, boundary cornerback vs. slot defender). Linking player-play tracking with route taxonomy and coverage assignments would enable game-context-normalized Athletic Alpha.

### 2.3 Longitudinal Multi-Season Tracking
When future tracking datasets (2024–2026) become accessible, researchers can evaluate whether Combine sensor metrics predict career durability, injury resilience, or contract value over multi-year horizons.
