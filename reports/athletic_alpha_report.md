# ATHLETIX AI: Athletic Alpha Residual Evaluation Report 🎯⚡

**Date**: November 2026  
**Definition**:
$$\text{Athletic Alpha}_i = Y_{\text{actual}, i} - \hat{Y}_{\text{OOF, Model A}, i}$$
$$\text{Alpha Z-Score}_i = \frac{\text{Athletic Alpha}_i - \mu_{\alpha}}{\sigma_{\alpha}}$$

Where $Y_{\text{actual}, i}$ is the verified 2023 regular-season 95th percentile game speed ($v_{\text{game, p95}}$) and $\hat{Y}_{\text{OOF, Model A}, i}$ is the **Out-Of-Fold** prediction from the traditional Combine baseline model.

---

## 1. Top Underestimated Prospects (Highest Athletic Alpha)

These prospects systematically outperformed traditional stopwatch and jump expectations once playing regular-season NFL football:

| Rank | Player Name | Position | Actual $v_{\text{p95}}$ | Traditional Exp $v_{\text{p95}}$ | Athletic Alpha Raw | Alpha Z-Score | Scrimmage Snaps | Draft Pick |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | **Cam Smith** | CB | $7.74\text{ yd/s}$ | $6.50\text{ yd/s}$ | **$+1.2356\text{ yd/s}$** | **$+3.19$** | $268$ | Round 2 (Pick 51) |
| **2** | **John Ojukwu** | T | $6.44\text{ yd/s}$ | $5.21\text{ yd/s}$ | **$+1.2297\text{ yd/s}$** | **$+3.18$** | $453$ | UDFA |
| **3** | **Jose Ramirez** | OLB | $7.15\text{ yd/s}$ | $6.03\text{ yd/s}$ | **$+1.1235\text{ yd/s}$** | **$+2.90$** | $145$ | Round 6 (Pick 196) |
| **4** | **Tashawn Manning** | G | $5.95\text{ yd/s}$ | $5.11\text{ yd/s}$ | **$+0.8448\text{ yd/s}$** | **$+2.18$** | $312$ | UDFA |
| **5** | **Tre Tucker** | WR | $7.85\text{ yd/s}$ | $7.09\text{ yd/s}$ | **$+0.7607\text{ yd/s}$** | **$+1.97$** | $581$ | Round 3 (Pick 100) |
| **6** | **Blake Whiteheart** | TE | $6.75\text{ yd/s}$ | $6.01\text{ yd/s}$ | **$+0.7381\text{ yd/s}$** | **$+1.91$** | $390$ | UDFA |
| **7** | **DJ Turner** | CB | $7.85\text{ yd/s}$ | $7.15\text{ yd/s}$ | **$+0.6974\text{ yd/s}$** | **$+1.80$** | $792$ | Round 2 (Pick 60) |
| **8** | **Mazi Smith** | DT | $6.33\text{ yd/s}$ | $5.64\text{ yd/s}$ | **$+0.6865\text{ yd/s}$** | **$+1.78$** | $502$ | Round 1 (Pick 26) |

---

## 2. Bottom "Workout Warriors" (Lowest Athletic Alpha)

These prospects recorded elite testing numbers in shorts and t-shirts at the Combine that failed to translate into proportional functional game speed:

| Rank | Player Name | Position | Actual $v_{\text{p95}}$ | Traditional Exp $v_{\text{p95}}$ | Athletic Alpha Raw | Alpha Z-Score | Scrimmage Snaps | Draft Pick |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **145** | **Demario Douglas** | WR | $6.87\text{ yd/s}$ | $7.56\text{ yd/s}$ | **$-0.6948\text{ yd/s}$** | **$-1.79$** | $514$ | Round 6 (Pick 210) |
| **146** | **Jammie Robinson** | SS | $6.13\text{ yd/s}$ | $6.87\text{ yd/s}$ | **$-0.7398\text{ yd/s}$** | **$-1.91$** | $259$ | Round 5 (Pick 145) |
| **147** | **Ricky Stromberg** | C | $4.67\text{ yd/s}$ | $5.48\text{ yd/s}$ | **$-0.8047\text{ yd/s}$** | **$-2.08$** | $178$ | Round 3 (Pick 97) |
| **148** | **Tyler Steen** | G | $4.70\text{ yd/s}$ | $5.56\text{ yd/s}$ | **$-0.8580\text{ yd/s}$** | **$-2.21$** | $401$ | Round 3 (Pick 65) |
| **149** | **Braeden Daniels** | G | $4.90\text{ yd/s}$ | $5.56\text{ yd/s}$ | **$-0.6654\text{ yd/s}$** | **$-1.72$** | $112$ | Round 4 (Pick 118) |

---

## 3. Residual Distribution & Statistical Tests

* **Sample Size**: $N = 149$
* **Mean Residual**: $\mu = -0.00102\text{ yd/s}$ (Centered at zero, verifying unbiased OOF predictions).
* **Standard Deviation**: $\sigma = 0.38712\text{ yd/s}$.
* **Median Residual**: $-0.0333\text{ yd/s}$.
* **Skewness**: $+0.5409$ (Moderate positive skewness—a subset of prospects exhibit substantial positive athletic alpha).
* **Kurtosis**: $+0.5911$.
* **Shapiro-Wilk Normality Test**: $W = 0.9798, p = 0.02745$.
  * *Result*: Residuals are **not strictly Gaussian** ($p < 0.05$), exhibiting heavier tails driven by high outperforming outliers.

---

## 4. What Movement Features Drive Athletic Alpha?

Correlating Athletic Alpha residuals against continuous Combine sensor tracking features reveals the biomechanical drivers of unexpected on-field speed:

| Sensor Feature | Spearman $r_s$ | $p$-value | Pearson $r$ | Empirical Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **`combine_mean_speed_preservation_ratio`** | **$+0.1744$** | **$0.03345$** | $+0.1170$ | **Statistically Significant**. Prospects who maintain speed through cuts outperform stopwatch baselines. |
| **`combine_mean_cod_apex_speed`** | **$+0.1742$** | **$0.03364$** | $+0.1563$ | **Statistically Significant**. Minimum velocity at direction-change apex directly predicts positive alpha. |
| **`combine_mean_speed`** | **$+0.1694$** | **$0.03892$** | $+0.1480$ | **Statistically Significant**. Average continuous velocity across drill trajectories. |
| **`combine_max_speed`** | $+0.1486$ | $0.07050$ | $+0.1500$ | Positive trend with in-drill peak velocity. |
| **`combine_mean_turning_efficiency`**| $+0.1348$ | $0.10120$ | $+0.1204$ | Turning efficiency index ($v_{\text{apex}} \cdot \Delta \theta / \Delta t$). |
| **`combine_initial_accel_mean`** | $+0.1278$ | $0.12047$ | $+0.1297$ | Initial burst acceleration during first 1.0s. |

> **Scientific Finding**: Traditional Combine stopwatch numbers capture straight-line sprint decay. They completely miss **kinetic energy preservation during lateral transitions**. Sensor-tracked agility preservation ratio and apex velocity explain why prospects like Cam Smith, Tre Tucker, and John Ojukwu generate positive Athletic Alpha.
