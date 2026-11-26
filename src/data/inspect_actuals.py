"""
ATHLETIX AI: Phase 1 Empirical Dataset Inspection
================================================
Inspects the 7 actual competition datasets in data/raw/ using Polars lazy frames.
Guaranteed memory-safe for 8 GB RAM machines.
"""

import json
from pathlib import Path
import polars as pl
import pandas as pd
import numpy as np

DATA_DIR = Path("data/raw")
REPORTS_DIR = Path("reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

FILES = [
    "combine_results.csv",
    "combine_tracking.csv",
    "games.csv",
    "game_tracking_2023.csv",
    "players.csv",
    "player_career_successes.csv",
    "player_play.csv",
]


def inspect_all():
    summary_results = {}
    
    print("=" * 80)
    print("PHASE 1A: DATASET INSPECTION")
    print("=" * 80)
    
    for fname in FILES:
        fpath = DATA_DIR / fname
        if not fpath.exists():
            print(f"ERROR: {fname} missing!")
            continue
            
        size_bytes = fpath.stat().st_size
        size_mb = size_bytes / (1024 * 1024)
        
        # Polars lazy scan
        lf = pl.scan_csv(fpath, ignore_errors=True)
        schema = lf.collect_schema()
        cols = schema.names()
        dtypes = {c: str(t) for c, t in schema.items()}
        
        row_count = lf.select(pl.len()).collect().item()
        
        # Missing values
        null_exprs = [pl.col(c).null_count().alias(c) for c in cols]
        null_counts = lf.select(null_exprs).collect().to_dict(as_series=False)
        null_dict = {c: int(null_counts[c][0]) for c in cols}
        
        # Unique players if player identifier column exists
        player_col = None
        for cand in ["nfl_id", "nflId", "player_id", "playerId", "smartabase_id", "combineId"]:
            if cand in cols:
                player_col = cand
                break
                
        unique_players = None
        if player_col:
            unique_players = lf.select(pl.col(player_col).drop_nulls().n_unique()).collect().item()
            
        # Sample duplicates: check row duplicate count
        # For small files, collect; for big files, check on key columns if available
        dup_count = 0
        if size_mb < 20:
            df_full = lf.collect()
            dup_count = df_full.height - df_full.unique().height
            del df_full
        else:
            # check key duplicates
            key_cols = [c for c in cols if c in ["nfl_id", "nflId", "game_id", "gameId", "play_id", "playId", "frame_id", "frameId", "drill_name", "time", "timestamp"]]
            if key_cols:
                n_unique_keys = lf.select(pl.struct(key_cols).n_unique()).collect().item()
                dup_count = row_count - n_unique_keys

        summary_results[fname] = {
            "size_mb": round(size_mb, 4),
            "row_count": row_count,
            "col_count": len(cols),
            "columns": cols,
            "dtypes": dtypes,
            "null_dict": null_dict,
            "player_col": player_col,
            "unique_players": unique_players,
            "dup_count": dup_count,
        }
        
        print(f"\n[{fname}] - Size: {size_mb:.2f} MB | Rows: {row_count:,} | Cols: {len(cols)}")
        print(f"Columns: {cols}")
        print(f"Player ID col: {player_col} (Unique: {unique_players})")
        print(f"Duplicates: {dup_count}")
        print("Null counts top:", {k: v for k, v in null_dict.items() if v > 0})

    return summary_results


if __name__ == "__main__":
    results = inspect_all()
    with open(REPORTS_DIR / "raw_inspection_cache.json", "w") as f:
        json.dump(results, f, indent=2)
