# ATHLETIX AI: Official Dataset Guide & Ingestion Protocol 📊

This document provides the definitive specification of the official competition datasets for **ATHLETIX AI**, correcting initial assumptions regarding file structures, outcome labels, and memory constraints.

---

## 1. Official Competition Datasets (9 Files)

The project operates exclusively on the 9 official competition files:

| # | Official File Name | Core Scope & Description | Target Memory Strategy (8 GB RAM) |
|---|---|---|---|
| 1 | `combine_tracking.csv` | Pre-draft Combine RFID sensor tracking ($10\text{ Hz}$). | Polars lazy scan (`scan_csv`) / Parquet conversion. |
| 2 | `combine_results.csv` | Official pre-draft Combine measurements (40yd, splits, vertical/broad jump, 3-cone, shuttle, bench, measurements). | In-memory Pandas/Polars dataframe. |
| 3 | `game_tracking_2023.csv` | Regular-season on-field tracking for the 2023 season ($10\text{ Hz}$). | **Process independently.** Never co-load with 2024/2025. |
| 4 | `game_tracking_2024.csv` | Regular-season on-field tracking for the 2024 season ($10\text{ Hz}$). | **Process independently.** Never co-load with 2023/2025. |
| 5 | `game_tracking_2025.csv` | Regular-season on-field tracking for the 2025 season ($10\text{ Hz}$). | **Process independently.** Never co-load with 2023/2024. |
| 6 | `player_play.csv` | Situational player involvement and performance per play. | Lazy scan or chunked processing. |
| 7 | `player_career_successes.csv`| Ground-truth career outcome metrics and milestone achievements. | In-memory Pandas/Polars dataframe. |
| 8 | `players.csv` | Master player biographical registry. | In-memory lookup table. |
| 9 | `games.csv` | Schedule, weather, venue, and score metadata. | In-memory lookup table. |

---

## 2. Dataset Schemas & Key Identifiers

### Identifier Resolution Protocol
* **Player Identifier**: May be named `nfl_id` or `nflId` depending on the file format. The ingestion layer dynamically handles snake_case and camelCase column aliases.
* **Game Identifier**: `game_id` / `gameId`.
* **Play Identifier**: `play_id` / `playId`.

### File Details:

#### 1. `combine_tracking.csv`
* **Sampling Rate**: $10.0\text{ Hz}$ ($\Delta t = 0.10\text{ s}$).
* **Variables**: `nfl_id` (or `nflId`/`combine_id`), `displayName`, `drill_name`, `frame_id`, `time`, `x`, `y`, `s` (velocity), `a` (acceleration), `dis` (displacement), `o` (orientation), `dir` (direction of movement), `event`.

#### 2. `combine_results.csv`
* **Traditional Scouting Metrics**: `nfl_id`, `player_name`, `college`, `position`, `draft_year`, `forty_yard`, `ten_yard`, `twenty_yard`, `vertical_jump`, `broad_jump`, `three_cone`, `twenty_yard_shuttle`, `bench_press`, `height`, `weight`.

#### 3. `game_tracking_2023.csv`, `game_tracking_2024.csv`, `game_tracking_2025.csv`
* **Granular Coordinate Feeds**: `game_id`, `play_id`, `nfl_id`, `frame_id`, `time`, `x`, `y`, `s`, `a`, `dis`, `o`, `dir`, `event`, `play_direction`.

#### 4. `player_play.csv`
* **Contextual Play Impact**: Links players to play-specific outcomes, snap participation, pre-snap alignment, routes run, pass rushes, or tackles.

#### 5. `player_career_successes.csv`
* **Ground-Truth Career Outcomes**: Contains multi-year performance indicators (e.g. career EPA contributions, starts, Pro Bowl selections, second contract value, or cumulative approximate value). Serves as an objective target to evaluate whether Combine movement features predict long-term NFL success.

#### 6. `players.csv` & `games.csv`
* Reference and join tables for biographical demographics and game-level conditions.

---

## 3. Strict Memory Management Protocol (8 GB RAM Laptop)

Tracking files easily exceed 4–10 GB when uncompressed. To prevent Out-Of-Memory (OOM) crashes:

1. **Polars Lazy Scanning**:
   Use `polars.scan_csv()` or `polars.scan_parquet()` to construct query execution plans without materializing the dataset in RAM.
2. **PyArrow Parquet Partitioning**:
   Raw CSV files should be converted into compressed columnar Parquet files (`snappy` or `zstd`) partitioned by season and week.
3. **Strict Sequential Season Execution**:
   ```
   [2023 Season Engine] -> Aggregate Player Features -> Write to Disk -> Garbage Collect
   [2024 Season Engine] -> Aggregate Player Features -> Write to Disk -> Garbage Collect
   [2025 Season Engine] -> Aggregate Player Features -> Write to Disk -> Garbage Collect
   ```
   **NEVER load multiple game tracking seasons simultaneously.**
4. **Chunked Extraction**:
   When parsing with Pandas, enforce `chunksize=100_000` and accumulate summary statistics rather than raw data frames.

---

## 4. File Placement Guide

Place all 9 CSV files in `data/raw/`:

```
d:\Athletics ai\data\raw\
├── combine_tracking.csv
├── combine_results.csv
├── game_tracking_2023.csv
├── game_tracking_2024.csv
├── game_tracking_2025.csv
├── player_play.csv
├── player_career_successes.csv
├── players.csv
└── games.csv
```
