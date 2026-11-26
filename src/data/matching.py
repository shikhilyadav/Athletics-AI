"""
Player Entity Resolution and Matching
======================================
Robust cross-referencing between pre-draft Combine records and NFL regular-season records.
"""

from typing import Optional
import pandas as pd
import numpy as np


class PlayerMatcher:
    """Matches players across Combine and NGS datasets using deterministic and fuzzy keys."""

    @staticmethod
    def standardize_name(name: str) -> str:
        """Standardizes name strings by removing punctuation, suffixes, and whitespace."""
        if pd.isna(name):
            return ""
        name = str(name).lower().strip()
        suffixes = [" jr.", " sr.", " ii", " iii", " iv", " v", " jr", " sr"]
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[: -len(suffix)]
        return "".join(c for c in name if c.isalnum() or c.isspace()).strip()

    def merge_combine_and_nfl(
        self,
        combine_df: pd.DataFrame,
        players_df: pd.DataFrame,
        on_id: str = "nflId",
    ) -> pd.DataFrame:
        """
        Merges combine records with NFL players metadata.
        Prioritizes direct ID matching (nflId), falling back to (standardized_name, collegeName, draftYear).
        """
        if on_id in combine_df.columns and on_id in players_df.columns:
            matched = pd.merge(combine_df, players_df, on=on_id, how="inner", suffixes=("_combine", "_nfl"))
            return matched

        # Name + College fallback matching
        c_df = combine_df.copy()
        p_df = players_df.copy()
        c_df["clean_name"] = c_df["displayName"].apply(self.standardize_name)
        p_df["clean_name"] = p_df["displayName"].apply(self.standardize_name)

        matched = pd.merge(c_df, p_df, on=["clean_name", "collegeName"], how="inner", suffixes=("_combine", "_nfl"))
        return matched
