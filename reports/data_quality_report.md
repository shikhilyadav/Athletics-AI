# ATHLETIX AI: Data Quality & Integrity Audit Report 🔍

Generated automatically by `src/data/dataset_audit.py`.

## 1. Executive Summary

- **Total Official Files Expected**: 9
- **Files Discovered on Disk**: 0 / 9
- **Memory Strategy**: 8 GB RAM target — Polars streaming & lazy scanning enabled.

## 2. File-by-File Quality Audit

| Filename | Status | Size (MB) | Rows | Identified Player ID | Quality Flags |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `combine_tracking.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `combine_results.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `game_tracking_2023.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `game_tracking_2024.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `game_tracking_2025.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `player_play.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `player_career_successes.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `players.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |
| `games.csv` | ❌ MISSING | 0.0 | 0 | `N/A` | FILE_NOT_FOUND_ON_DISK |

## 3. Discovered Columns and Data Types

### `combine_tracking.csv` (Status: MISSING)
> **Action Required**: Place `combine_tracking.csv` into `data/raw/`.

### `combine_results.csv` (Status: MISSING)
> **Action Required**: Place `combine_results.csv` into `data/raw/`.

### `game_tracking_2023.csv` (Status: MISSING)
> **Action Required**: Place `game_tracking_2023.csv` into `data/raw/`.

### `game_tracking_2024.csv` (Status: MISSING)
> **Action Required**: Place `game_tracking_2024.csv` into `data/raw/`.

### `game_tracking_2025.csv` (Status: MISSING)
> **Action Required**: Place `game_tracking_2025.csv` into `data/raw/`.

### `player_play.csv` (Status: MISSING)
> **Action Required**: Place `player_play.csv` into `data/raw/`.

### `player_career_successes.csv` (Status: MISSING)
> **Action Required**: Place `player_career_successes.csv` into `data/raw/`.

### `players.csv` (Status: MISSING)
> **Action Required**: Place `players.csv` into `data/raw/`.

### `games.csv` (Status: MISSING)
> **Action Required**: Place `games.csv` into `data/raw/`.

## 4. Methodological Safeguards for Phase 1

1. **No Data Fabrication**: This report reflects only verified files on disk.
2. **Memory Guard**: Three-year game tracking files are audited in isolation.
3. **Entity Resolution Guard**: Join keys will only be established against observed schemas.
