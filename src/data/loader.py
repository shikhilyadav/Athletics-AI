"""
ATHLETIX AI: Data Loader Module
===============================
Loads and validates official competition files using Polars and Pandas.
Supports 8 GB RAM memory optimization via Polars lazy execution and single-season tracking scans.
"""

from pathlib import Path
from typing import Dict, Optional, Union
import pandas as pd
import polars as pl
from src.config import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    OFFICIAL_COMPETITION_FILES,
    GAME_TRACKING_FILES,
)


class DataLoader:
    """Manages loading and integrity verification of competition datasets."""

    def __init__(self, base_dir: Path = RAW_DATA_DIR):
        self.base_dir = Path(base_dir)

    def find_file(self, filename: str) -> Optional[Path]:
        """Finds a file recursively in base_dir."""
        for path in self.base_dir.rglob(filename):
            if path.is_file():
                return path
        return None

    def check_dataset_availability(self) -> Dict[str, bool]:
        """Checks if expected official competition files exist on disk."""
        status = {}
        for key, fname in OFFICIAL_COMPETITION_FILES.items():
            found = self.find_file(fname)
            status[key] = found is not None
        return status

    def load_players(self) -> pd.DataFrame:
        """Loads players.csv context file."""
        file_path = self.find_file(OFFICIAL_COMPETITION_FILES["players"])
        if not file_path:
            raise FileNotFoundError(f"Missing {OFFICIAL_COMPETITION_FILES['players']}. Please see DATASET_GUIDE.md")
        return pd.read_csv(file_path)

    def load_games(self) -> pd.DataFrame:
        """Loads games.csv context file."""
        file_path = self.find_file(OFFICIAL_COMPETITION_FILES["games"])
        if not file_path:
            raise FileNotFoundError(f"Missing {OFFICIAL_COMPETITION_FILES['games']}. Please see DATASET_GUIDE.md")
        return pd.read_csv(file_path)

    def load_combine_results(self) -> pd.DataFrame:
        """Loads combine_results.csv (traditional measurements)."""
        file_path = self.find_file(OFFICIAL_COMPETITION_FILES["combine_results"])
        if not file_path:
            raise FileNotFoundError(f"Missing {OFFICIAL_COMPETITION_FILES['combine_results']}. Please see DATASET_GUIDE.md")
        return pd.read_csv(file_path)

    def load_player_career_successes(self) -> pd.DataFrame:
        """Loads player_career_successes.csv ground truth career outcomes."""
        file_path = self.find_file(OFFICIAL_COMPETITION_FILES["player_career_successes"])
        if not file_path:
            raise FileNotFoundError(f"Missing {OFFICIAL_COMPETITION_FILES['player_career_successes']}. Please see DATASET_GUIDE.md")
        return pd.read_csv(file_path)

    def scan_combine_tracking(self) -> pl.LazyFrame:
        """Returns Polars LazyFrame for combine_tracking.csv (memory-safe)."""
        file_path = self.find_file(OFFICIAL_COMPETITION_FILES["combine_tracking"])
        if not file_path:
            raise FileNotFoundError(f"Missing {OFFICIAL_COMPETITION_FILES['combine_tracking']}. Please see DATASET_GUIDE.md")
        return pl.scan_csv(file_path, ignore_errors=True)

    def scan_game_tracking(self, season: Union[int, str]) -> pl.LazyFrame:
        """
        Returns Polars LazyFrame for a single game tracking season (2023, 2024, or 2025).
        Enforces strict single-season access to safeguard 8 GB RAM.
        """
        filename = f"game_tracking_{season}.csv"
        file_path = self.find_file(filename)
        if not file_path:
            raise FileNotFoundError(f"Missing {filename}. Please see DATASET_GUIDE.md")
        return pl.scan_csv(file_path, ignore_errors=True)
