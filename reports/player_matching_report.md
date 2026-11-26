# ATHLETIX AI: Player Entity Resolution & Matching Report 🔗

## 1. Player Key Discovery & Cross-Table Linkage Plan

This report audits the join feasibility between Combine datasets, regular-season tracking, and career outcomes.

### Target Cross-Table Join Matrix

| Source Table | Target Join Table | Candidate Player Key | Fallback Match Key |
| :--- | :--- | :--- | :--- |
| `combine_results.csv` | `combine_tracking.csv` | `nfl_id` / `combine_id` | `displayName` + `drill_name` |
| `combine_results.csv` | `players.csv` | `nfl_id` / `nflId` | `displayName` + `college` + `draft_year` |
| `players.csv` | `game_tracking_*.csv` | `nfl_id` / `nflId` | `displayName` + `jerseyNumber` |
| `players.csv` | `player_play.csv` | `nfl_id` / `nflId` | Direct foreign key |
| `players.csv` | `player_career_successes.csv` | `nfl_id` / `nflId` | Direct foreign key |

## 2. Integrity Warnings on Player Matching

1. **Suffix & Name Collisions**: Generational suffixes (`Jr.`, `III`) must be stripped during fallback name matching.
2. **Undrafted / Unmatched Prospects**: Players in `combine_results.csv` who never made an active regular-season roster will not appear in `game_tracking_*.csv`. These must be preserved in Combine distributions but flagged with `has_nfl_snaps = False`.
3. **Sample Size Censoring**: Prospects with $< 50$ snaps in `player_play.csv` cannot be used to compute valid game speed percentiles.
