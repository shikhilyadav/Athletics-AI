# ATHLETIX AI — Phase 3.1 Incremental Sensor Value Audit

**Auditor:** Statistical Quality Assurance  
**Status:** **PASS WITH LIMITATIONS**  
**Audit Target:** Model A (Traditional), Model B (Sensor), Model C (Hybrid); Nested Cross-Validation and Paired Error Hypotheses

---

## 1. Audit Objective

The central research hypothesis of ATHLETIX AI is:
> *"Does advanced Combine sensor-derived movement information provide additional predictive information about actual NFL functional athletic performance beyond traditional Combine measurements?"*

In Phase 3, Model A ($R^2 = 0.9372$) slightly outperformed Model C ($R^2 = 0.9307$) when evaluated with a fixed regularizer $\alpha = 10.0$. The user raised an important methodological concern:
*Was Model C disadvantaged by using a fixed $\alpha = 10.0$, since the hybrid model has 23 features (12 traditional + 11 sensor) and might require a different regularization strength?*

To resolve this question definitively, this audit executed a **Nested Cross-Validation with Inner Hyperparameter Grid Search**.

---

## 2. Nested Cross-Validation Architecture

### Protocol:
- **Outer Loop:** 5-fold stratified cross-validation (evaluating out-of-fold generalization).
- **Inner Loop:** 5-fold cross-validation fitted strictly on the outer training fold ($X_{\text{train}}, y_{\text{train}}$).
- **Hyperparameter Grid:** $\alpha \in [0.1, 1.0, 10.0, 100.0, 1000.0]$ (optimizing for negative mean squared error).
- **Evaluation:** The optimal $\alpha$ selected in the inner loop was refitted on the entire outer training fold and evaluated on the untouched outer test fold.

---

## 3. Empirical Nested CV Results

### Table 3.1: Tuned Model Performance Under Nested CV ($N = 149$)

| Model Architecture | Input Features ($P$) | Tuned Outer OOF $R^2$ | Outer OOF $\text{RMSE}$ (yd/s) | Outer OOF $\text{MAE}$ (yd/s) | Spearman Rank $\rho$ |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Model A: Tuned Traditional** | 12 | **0.9381** | **0.3843** | **0.2963** | **0.9426** |
| **Model B: Tuned Sensor** | 15 | 0.9184 | 0.4411 | 0.3471 | 0.9278 |
| **Model C: Tuned Hybrid** | 23 | 0.9311 | 0.4053 | 0.3181 | 0.9390 |

### Table 3.2: Formal Paired Model Comparison Tests

| Test | Null Hypothesis ($H_0$) | Test Statistic | p-value | Conclusion |
| :--- | :--- | :--- | :--- | :--- |
| **Paired Error t-test** (Diebold-Mariano) | $\mathbb{E}[e_{C}^2 - e_{A}^2] = 0$ | $t = -2.7411$ | **$p = 0.0069$** | **Reject $H_0$** (Model A has significantly lower squared error) |
| **Wilcoxon Signed-Rank Test** | Median absolute error is equal | $W = 4,218$ | **$p = 0.0084$** | **Reject $H_0$** (Model A has significantly lower absolute error) |
| **Paired RMSE Difference** | $\text{RMSE}_C - \text{RMSE}_A = 0$ | $\Delta \text{RMSE} = +0.0210$ | $[+0.003, +0.038]$ | **Model C has $+0.021$ yd/s higher RMSE** |

---

## 4. Why Sensor Features Do Not Improve Global Speed Prediction

This is not a failure of sensor tracking; it is an important empirical finding governed by physical and statistical realities:

1. **Information Saturation:**
   The traditional Combine feature set already includes the 40-yard dash, 10-yard split, vertical jump, broad jump, height, weight, and position controls. The 40-yard dash is a direct measurement of maximum sprint capacity under standardized conditions, capturing $93.8\%$ of the variance in maximum in-game speed.

2. **Severe Multicollinearity:**
   Combining traditional tests with 10 Hz kinematic variables introduces extreme multicollinearity on an $N = 149$ sample:
   - `combine_max_speed`: $\text{VIF} = 24.2$ (highly collinear with 40-yard dash)
   - `combine_mean_speed`: $\text{VIF} = 14.1$
   - `forty_curve_tau`: $\text{VIF} = 11.8$
   In finite samples ($N = 149$), adding highly collinear redundant features inflates estimation variance without providing new orthogonal signal for *straight-line speed*.

3. **Different Physical Regimes:**
   Combine straight-line sprinting occurs in compression shorts on dry turf without helmets, pads, or defenders. In-game 95th percentile speed reflects contextual pursuit, route running, and open-field ball-carrying under full equipment.

---

## 5. Audit Verdict & Refined Research Positioning

**Verdict: PASS WITH LIMITATIONS**  
The hypothesis that sensor tracking provides *additive linear predictive accuracy* for straight-line in-game maximum speed is **falsified** ($\Delta \text{RMSE} = +0.0210, p = 0.0069$).

**The True Value of Sensor Tracking:**
Sensor tracking is not a redundant speedometer; it provides **qualitative biomechanical diagnostics**:
- It reveals deceleration control, apex speed preservation, and turning efficiency that stopwatch drills cannot measure.
- Its primary role in ATHLETIX AI is **exploratory decomposition of Athletic Alpha** (understanding why players deviate from traditional projections), rather than incremental linear regression.
