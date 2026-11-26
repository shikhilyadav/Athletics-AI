# ATHLETIX AI: Empirical Player Matching & Entity Resolution Report 🔗

**Date**: November 2026  
**Subject**: Cross-table entity resolution across the 7 competition datasets.

---

## 1. Universal Player Identifier

The canonical identifier across all datasets is **`nfl_id`** (snake_case, 64-bit integer, range: $55867$ to $59278$).

### Cross-Dataset Linkage Matrix:

| Target Dataset | Total Unique Players | Linkage to `players.csv` | Match Rate | Unmatched Count | Reason for Non-Match |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `combine_results.csv` | $510$ | $510$ | **$100.0\%$** | $0$ | Perfect 1-to-1 correspondence |
| `combine_tracking.csv` | $510$ | $510$ | **$100.0\%$** | $0$ | Perfect 1-to-1 correspondence |
| `player_career_successes.csv` | $510$ | $510$ | **$100.0\%$** | $0$ | Perfect 1-to-1 correspondence |
| `player_play.csv` | $497$ | $497$ | **$97.5\%$** | $13$ | 13 prospects never played an official NFL scrimmage snap |
| `game_tracking_2023.csv` | $156$ | $156$ | **$97.5\%$ (of 2023 cohort)** | $4$ | 4 rookies in the 2023 class had zero active tracking snaps |

---

## 2. Draft Class Cohort Distribution

The 510 prospects in `players.csv` are partitioned across three consecutive draft years:

| Draft Year | Total Prospects | Drafted Players | Undrafted (UDFA) | UDFA Rate |
| :--- | :--- | :--- | :--- | :--- |
| **2023** | $160$ | $121$ | $39$ | $24.4\%$ |
| **2024** | $177$ | $132$ | $45$ | $25.4\%$ |
| **2025** | $173$ | $130$ | $43$ | $24.9\%$ |
| **Total** | **$510$** | **$383$** | **$127$** | **$24.9\%$** |

* **Undrafted Free Agents**: Exactly $127$ prospects ($24.9\%$) have null `draft_round`, `draft_pick_within_round`, and `draft_overall_pick`.
* **Positional Breakdown**:
  * Wide Receivers (WR): $106$
  * Cornerbacks (CB): $60$
  * Offensive Tackles (T): $50$
  * Defensive Tackles (DT): $47$
  * Tight Ends (TE): $42$
  * Defensive Ends (DE): $36$
  * Strong Safeties (SS): $28$
  * Other positions (ILB, MLB, RB): $141$

---

## 3. Career Success Linkage & Active Play Status

Analysis of `player_career_successes.csv` linked directly to `players.csv`:
* **Active in $\ge 1$ NFL Regular Season Game**: $422$ / $510$ prospects ($82.7\%$).
* **Started in $\ge 1$ NFL Regular Season Game**: $302$ / $510$ prospects ($59.2\%$).
* **Snaps Recorded**:
  * Offensive Snaps $> 0$: $213$ prospects.
  * Defensive Snaps $> 0$: $193$ prospects.
  * Special Teams Snaps $> 0$: $402$ prospects.
* **Pro Bowl Honors**: $14$ total selections across the cohort ($9$ in 2023 class, $4$ in 2024, $1$ in 2025).

---

## 4. Entity Resolution Integrity Assessment
* **No Fuzzy Matching Required**: Because `nfl_id` is populated in $100\%$ of rows across all tables, complex string/name matching is unnecessary, completely eliminating name collision or false-linkage errors.
* **Referential Integrity**: Every `nfl_id` in tracking and performance files is a valid foreign key to `players.csv`.
