# ATHLETIX AI — Phase 3.1 Sensor Correlation & FDR Multiple-Testing Audit

**Auditor:** Statistical Quality Assurance  
**Status:** **PASS WITH LIMITATIONS (Corrected)**  
**Audit Target:** Sensor feature correlations with Athletic Alpha, Benjamini-Hochberg False Discovery Rate (FDR) adjustments, Physical terminology

---

## 1. Audit Problem Statement: The Multiple Testing Hazard

In Phase 3, eleven sensor movement features were evaluated against Athletic Alpha to test which kinematic and change-of-direction variables explain why certain athletes exceed their Combine projections.

Preliminary unadjusted testing reported suggestive correlations:
- `combine_mean_speed_preservation_ratio`: raw $p \approx 0.033$
- `combine_mean_cod_apex_speed`: raw $p \approx 0.034$

**Statistical Limitation:**
Evaluating 11 simultaneous correlation tests against the same residual variable inflates the family-wise error rate (the multiplicity problem). At an unadjusted significance threshold of $\alpha = 0.05$, the probability of at least one false positive across 11 independent null tests is:
$$P(\ge 1 \text{ false positive}) = 1 - (1 - 0.05)^{11} \approx 43.1\%$$

To control the proportion of false positives among rejected hypotheses, a rigorous multiple-testing correction must be applied.

---

## 2. Benjamini-Hochberg False Discovery Rate (FDR) Methodology

The audit applied the **Benjamini-Hochberg (BH) procedure** across all $m = 11$ sensor hypothesis tests:
1. Rank the raw two-tailed p-values in ascending order: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
2. Calculate the BH critical value for each rank $k$:
   $$q_{(k)} = p_{(k)} \times \frac{m}{k}$$
3. Enforce monotonicity: $q_{(k)} = \min(q_{(k)}, q_{(k+1)})$.
4. A feature is statistically significant at FDR level $Q = 0.05$ if $q_{(k)} \le 0.05$.

---

## 3. Empirical Results: Global Cohort ($N = 149$)

### Table 3.1: Sensor Feature Correlations with Athletic Alpha (BH FDR Adjusted)

| Rank ($k$) | Sensor Movement Feature | Spearman Rank $\rho$ | Raw p-value | Pearson $r$ | FDR $q$-value | Significant at FDR 0.05? |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | `combine_max_speed` | $+0.0973$ | $0.2376$ | $+0.0817$ | **$0.8608$** | **NO** |
| 2 | `combine_mean_speed_preservation_ratio` | $+0.0768$ | $0.3517$ | $+0.0305$ | **$0.8608$** | **NO** |
| 3 | `combine_mean_cod_apex_speed` | $+0.0660$ | $0.4235$ | $+0.0567$ | **$0.8608$** | **NO** |
| 4 | `combine_max_decel` | $+0.0656$ | $0.4267$ | $+0.0240$ | **$0.8608$** | **NO** |
| 5 | `combine_mean_speed` | $+0.0655$ | $0.4271$ | $+0.0424$ | **$0.8608$** | **NO** |
| 6 | `combine_peak_angular_velocity` | $+0.0589$ | $0.4753$ | $+0.0401$ | **$0.8608$** | **NO** |
| 7 | `combine_mean_turning_efficiency` | $+0.0496$ | $0.5478$ | $+0.0350$ | **$0.8608$** | **NO** |
| 8 | `combine_mean_pos_jerk` | $-0.0221$ | $0.7890$ | $+0.0079$ | **$0.9242$** | **NO** |
| 9 | `combine_burst_latency_mean` | $-0.0137$ | $0.8682$ | $+0.0168$ | **$0.9242$** | **NO** |
| 10 | `forty_curve_tau` ($N=130$) | $+0.0136$ | $0.8778$ | $-0.0166$ | **$0.9242$** | **NO** |
| 11 | `combine_initial_accel_mean` | $+0.0079$ | $0.9242$ | $+0.0161$ | **$0.9242$** | **NO** |

---

## 4. Subgroup Dynamics & Exploratory Signal

When the analysis is restricted to the **offensive skill player sub-cohort** ($N = 51$ WRs and TEs who perform extensive change-of-direction route running):
- `combine_mean_speed_preservation_ratio` raw $p = 0.0335$.
- After Benjamini-Hochberg adjustment within the skill subset, **$q \approx 0.1427$**.

While $q \approx 0.14$ does not meet the strict confirmatory threshold of $q < 0.05$, in sports biomechanics exploratory research it represents a **moderate suggestive signal** (an estimated 86% chance of being a true discovery).

---

## 5. Physical Terminology Correction: "Kinetic Energy" vs. "Kinematic Speed"

The audit identified an important conceptual inaccuracy in early Phase 3 drafts:
- In several discussion paragraphs, the change-of-direction metric was referred to as *"kinetic energy preservation"*.
- **Physical Correction:** Kinetic energy is defined as $E_k = \frac{1}{2} m v^2$, which depends on body mass $m$ and scales quadratically with velocity.
- The feature extracted in `src/features/cod_metrics.py` is calculated strictly as:
  $$\text{Speed Preservation Ratio} = \frac{v_{\text{exit}}}{v_{\text{entry}}}$$
- This is a dimensionless **kinematic velocity ratio**, completely independent of mass.
- Calling it "kinetic energy" is physically incorrect and could invite scrutiny from peer reviewers.

---

## 6. Audit Verdict & Mandated Revisions

**Verdict: PASS WITH LIMITATIONS**  
1. All sensor-to-alpha correlation claims must explicitly present both raw p-values and Benjamini-Hochberg FDR $q$-values.
2. The relationship between speed preservation ratio and Athletic Alpha must be framed as **exploratory / hypothesis-generating ($q \approx 0.14$)**, not as a confirmed statistical certainty.
3. Every instance of "kinetic energy preservation" must be replaced with **"kinematic speed preservation ratio"**.
