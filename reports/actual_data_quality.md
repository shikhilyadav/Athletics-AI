# ATHLETIX AI: Empirical Data Quality & Integrity Report 🔍📊

**Date**: November 2026  
**Subject**: Empirical inspection of the 7 official competition CSV datasets in `data/raw/`.  
**Memory Architecture**: Verified under strict $8\text{ GB RAM}$ budget via Polars lazy execution (`pl.scan_csv`).

---

## 1. Executive Summary of Datasets

All 7 CSV datasets have been thoroughly ingested and empirically profiled:

| Dataset | Size | Rows | Columns | Unique Players | Primary Key / Entity | Missingness Format |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `combine_results.csv` | $41\text{ KB}$ | $510$ | $18$ | $510$ | `nfl_id` | String `'NA'` in unattempted drills |
| `combine_tracking.csv` | $79.91\text{ MB}$ | $463,189$ | $14$ | $510$ | `(nfl_id, event_id, time)` | Zero nulls |
| `games.csv` | $43\text{ KB}$ | $1,002$ | $7$ | N/A | `game_id` | Zero nulls |
| `game_tracking_2023.csv` | $319.92\text{ MB}$ | $3,665,443$ | $12$ | $156$ | `(game_id, play_id, nfl_id, time)` | Zero nulls |
| `players.csv` | $47\text{ KB}$ | $510$ | $10$ | $510$ | `nfl_id` | String `'NA'` for undrafted players |
| `player_career_successes.csv` | $14\text{ KB}$ | $510$ | $9$ | $510$ | `nfl_id` | Zero nulls |
| `player_play.csv` | $140.07\text{ MB}$ | $314,197$ | $64$ | $497$ | `(game_id, play_id, nfl_id)` | Contextual nulls |

---

## 2. Key Empirical Findings & Data Quality Discoveries

### Discovery A: String `"NA"` Encoding for Null Values
* In `combine_results.csv` and `players.csv`, missing values were recorded as literal strings (`"NA"`) rather than empty fields.
* Standard CSV parsers without explicit null string declaration parse columns like `forty`, `three_cone`, `short_shuttle`, and `bench_reps` as string dtypes instead of numeric floats.
* **Correction Implemented**: All loaders and scanning pipelines now pass `null_values=['NA', 'null', '']`.

### Discovery B: Severe Opt-Out Bias in Traditional Combine Benchmarks
Empirical missingness analysis in `combine_results.csv` exposes massive non-participation in traditional agility and strength drills:
* **3-Cone Drill**: $330$ out of $510$ prospects missing ($64.7\%$ opt-out rate).
* **20-Yard Short Shuttle**: $309$ out of $510$ prospects missing ($60.6\%$ opt-out rate).
* **Bench Press**: $318$ out of $510$ prospects missing ($62.4\%$ opt-out rate).
* **40-Yard Dash**: $86$ prospects missing ($16.9\%$ opt-out rate).
* **Vertical Jump**: $72$ prospects missing ($14.1\%$ opt-out rate).
* **Broad Jump**: $87$ prospects missing ($17.1\%$ opt-out rate).

> **Crucial Research Implication**: Traditional scouting numbers possess severe missingness bias. In sharp contrast, `combine_tracking.csv` captures sensor movement for **all 510 prospects ($100\%$)** across positional drills and route trees! Advanced movement tracking completely resolves this missingness blindspot.

### Discovery C: Football Entity in Combine Tracking
* In `combine_tracking.csv`, there are two entity types:
  * `entity_type == 'PLAYER'`: $431,094$ frames ($93.1\%$).
  * `entity_type == 'BALL'`: $32,095$ frames ($6.9\%$).
* The raw maximum velocity in `combine_tracking.csv` is $25.79\text{ yd/s}$ (approx $52.7\text{ mph}$).
* **Empirical Verification**: This peak speed belongs exclusively to the thrown football. When filtered strictly to `PLAYER`, the maximum speed is $10.73\text{ yd/s}$ ($21.95\text{ mph}$) and peak acceleration is $10.72\text{ yd/s}^2$—both entirely physiologically sound.

### Discovery D: Unsigned Acceleration Representation
* In both `combine_tracking.csv` and `game_tracking_2023.csv`, the minimum acceleration value is $a_{\min} = 0.00$.
* This confirms that acceleration $a$ in the telemetry feed represents the **magnitude of acceleration** (Euclidean norm $\|\mathbf{a}\|$), rather than signed linear acceleration ($+a$ for speeding up, $-a$ for braking).
* **Biomechanical Adaptation**: Deceleration and braking capacity must be derived via numerical backward differences of speed:
  $$a_{\text{tangential}}(t) = \frac{s(t) - s(t - \Delta t)}{\Delta t}$$

### Discovery E: Sampling Frequency & Timestamps
* Both `combine_tracking.csv` and `game_tracking_2023.csv` exhibit uniform, unjittered frame increments:
  $$\Delta t = 0.100\text{ seconds} \quad (10.0\text{ Hz})$$
* Zero missing timestamps or duplicate frame sequences were identified.

### Discovery F: Field Coordinates & Boundary Run-Outs
* `combine_tracking.csv`: $X \in [1.30, 103.90]$, $Y \in [-11.46, 66.28]$.
* `game_tracking_2023.csv`: $X \in [-5.89, 126.73]$, $Y \in [-7.29, 61.24]$.
* Negative coordinates and coordinates beyond $120\text{ yards}$ (X) or outside $[0, 53.33]$ (Y) represent players finishing sprints into the endzone buffer or running out of bounds past the sideline. These are legitimate tracking frames and should not be deleted.
