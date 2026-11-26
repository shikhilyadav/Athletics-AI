# ATHLETIX AI — Phase 3.1 Confidence Interval & Uncertainty Audit

**Auditor:** Statistical Quality Assurance  
**Status:** **PASS WITH LIMITATIONS (Corrected)**  
**Audit Target:** Out-of-fold performance uncertainty, 95% Confidence Intervals, Model Paired Comparison

---

## 1. Audit Problem Statement: The Pseudo-Replication Fallacy

In Phase 3, the reported 95% confidence intervals for out-of-fold metrics were computed as:
$$\text{CI}_{95\%} = \bar{M}_{\text{folds}} \pm 1.96 \times \frac{\text{std}(M_{\text{folds}})}{\sqrt{K}}$$
where $K = 50$ (the 50 folds produced by 10-repeat 5-fold cross-validation).

**Statistical Limitation:**
Treating 50 repeated folds as 50 independent samples violates the fundamental assumption of independent and identically distributed (i.i.d.) observations. In a 5-fold cross-validation scheme, any two folds from different repeats share approximately $80\%$ of their training instances ($1 - \frac{1}{k} = 0.80$). This heavy overlap introduces substantial positive covariance among fold metrics. Consequently:
- Treating $N_{\text{folds}} = 50$ as degrees of freedom artificially deflates the standard error.
- The resulting confidence intervals are spuriously narrow, overstating confidence.

---

## 2. Corrected Uncertainty Estimation: Player-Level Bootstrap

To obtain scientifically defensible confidence intervals that account for correlated folds and repeated measurements, the audit implemented a **non-parametric player-level bootstrap** with $B = 2,000$ iterations.

### Methodology:
1. Aggregate the 10 repeated out-of-fold predictions into a single vector of player-level predictions $\hat{\mathbf{y}}_A$ and $\hat{\mathbf{y}}_C$, paired with actual values $\mathbf{y}$ for all $N = 149$ prospects.
2. For $b = 1, \dots, 2000$:
   - Sample $N = 149$ player indices with replacement: $\{i_1^*, \dots, i_N^*\}$.
   - Compute bootstrap $R^2(b)$, $\text{RMSE}(b)$, and paired difference $\Delta \text{RMSE}(b) = \text{RMSE}_C(b) - \text{RMSE}_A(b)$.
3. Obtain empirical 95% confidence intervals from the 2.5th and 97.5th percentiles of the bootstrap distribution.

---

## 3. Comparative Results

### Table 3.1: Original vs. Corrected Uncertainty Estimates

| Metric | Model Architecture | Original Phase 3 (Fold-SEM) | Corrected Phase 3.1 (Player Bootstrap B=2,000) |
| :--- | :--- | :--- | :--- |
| **Out-of-Fold $R^2$** | Model A (Traditional) | $0.9372 \pm 0.0071$ $[0.9301, 0.9443]$ | **$0.9372$ $[0.9171, 0.9526]$** |
| | Model B (Sensor) | $0.9168 \pm 0.0102$ $[0.9066, 0.9270]$ | **$0.9168$ $[0.8874, 0.9389]$** |
| | Model C (Hybrid) | $0.9307 \pm 0.0084$ $[0.9223, 0.9391]$ | **$0.9307$ $[0.9083, 0.9477]$** |
| **Out-of-Fold $\text{RMSE}$** (yd/s) | Model A (Traditional) | $0.3860 \pm 0.0210$ $[0.3650, 0.4070]$ | **$0.3860$ $[0.3340, 0.4352]$** |
| | Model B (Sensor) | $0.4435 \pm 0.0264$ $[0.4171, 0.4699]$ | **$0.4435$ $[0.3892, 0.5041]$** |
| | Model C (Hybrid) | $0.4055 \pm 0.0241$ $[0.3814, 0.4296]$ | **$0.4055$ $[0.3540, 0.4578]$** |

### Table 3.2: Paired Model Comparison (Model C vs. Model A)

| Comparative Statistic | Bootstrap Estimate | Interpretation |
| :--- | :--- | :--- |
| **Mean $\Delta R^2 (C - A)$** | **$-0.0066$** | Hybrid model accounts for slightly less variance than Traditional baseline |
| **95% Bootstrap CI for $\Delta R^2$** | **$[-0.0130, -0.0001]$** | Strictly below zero (does not cross 0.0) |
| **Mean $\Delta \text{RMSE} (C - A)$** | **$+0.0194$ yd/s** | Hybrid model incurs higher error than Traditional baseline |
| **95% Bootstrap CI for $\Delta \text{RMSE}$** | **$[+0.0003, +0.0373]$** | Strictly positive (error increase is statistically robust) |
| **$P(\text{Model C} < \text{Model A in RMSE})$** | **$2.4\%$** | Only a 2.4% probability that Model C achieves superior accuracy |

---

## 4. Audit Verdict & Remediation

**Verdict: PASS WITH LIMITATIONS**  
The original confidence intervals understated uncertainty by roughly $2.2\times$ due to treating repeated cross-validation folds as independent. The corrected player-level bootstrap confidence intervals faithfully represent the empirical uncertainty of the $N = 149$ sample.

**Remediation in Phase 4 / Final Publications:**
- All reported confidence intervals must report the player-level non-parametric bootstrap intervals ($B \ge 2,000$).
- Discontinue all reporting of fold-based standard error approximations.
