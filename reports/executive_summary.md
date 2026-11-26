# ATHLETIX AI — Executive Summary
## Beyond Speed: Understanding Athletic Potential
**Competition:** NFL Big Data Bowl 2027  
**Target Audience:** NFL Front Offices, Analytics Directors, Lead Scouts  

---

### The Executive Problem
Every spring, NFL franchises commit premium draft capital based on Combine stopwatch times. However, front offices frequently encounter two painful outcomes:
1. **The Straight-Line Phantom:** A prospect with elite 4.38s speed whose athleticism fails to translate into functional game speed against NFL pursuit.
2. **The Hidden Athlete:** A prospect with modest 4.55s speed who consistently plays with blazing game speed, separating on routes and tracking down ball-carriers.

**The Core Question:** *Can 10 Hz RFID sensor tracking from the Combine explain this divergence and identify undervalued athletic potential?*

---

### Key Research Findings

1. **Stopwatches Still Rule Straight-Line Speed ($R^2 = 0.938$):**  
   Traditional Combine measurements (40-yard dash, splits, jumps, height, weight) predict 93.8% of the variance in maximum in-game speed. Adding sensor kinematics to a linear prediction model does **not** improve accuracy ($p = 0.0069$) due to high feature collinearity. Sensor tracking should not be used as an incremental straight-line speedometer.

2. **Athletic Alpha Unlocks Residual Translation:**  
   By subtracting model predictions from actual in-game tracking speed ($\alpha = y - \hat{y}$), we isolated **Athletic Alpha**. Athletic Alpha is completely independent of draft capital ($r = 0.046, p = 0.62$), scrimmage snaps ($r = -0.032, p = 0.70$), and position alignment ($p = 0.996$). It measures pure in-game over- or under-performance.

3. **Change-of-Direction Mechanics Matter for Skill Prospects:**  
   In offensive skill players ($N = 51$), the **Kinematic Speed Preservation Ratio** during cuts showed an exploratory relationship with positive Athletic Alpha ($q \approx 0.14$). Prospects who maintain velocity through the apex of cuts translate Combine speed to the field far more effectively than those who rely strictly on straight-line acceleration.

---

### Front Office Recommendations

| Traditional Approach | ATHLETIX AI Modern Scouting Approach |
| :--- | :--- |
| Draft decisions anchored to 40-yard dash times | Use 40-yard dash as baseline, but evaluate **Athletic Alpha** and **Speed Preservation Ratio** |
| Assume straight-line speed translates uniformly to game speed | Diagnose turn apex deceleration and angular velocity from 10 Hz sensor tracking |
| Label prospects with slow 40s as unathletic | Identify prospects with elite mono-exponential acceleration constants ($\tau$) who reach top speed rapidly |

---

### Deliverable: ATHLETIX AI Platform
We built a production-grade, interactive Streamlit analytics platform enabling scouts and analysts to:
- Explore all 510 prospects with complete physical and sensor profiles.
- Review out-of-fold Athletic Alpha leaderboards and position distributions.
- Inspect mono-exponential sprint curves ($v(t) = v_{\max}(1 - e^{-t/\tau})$) and Change-of-Direction dynamics.
- Access fully documented methodology and empirical test results.
