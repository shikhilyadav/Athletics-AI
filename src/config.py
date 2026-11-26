"""
ATHLETIX AI: Configuration and Global Constants
==============================================
Central configuration module for paths, official competition files,
tracking standards, field geometry, and 8 GB RAM memory optimization settings.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
MODELS_DIR = PROJECT_ROOT / "models"
SAVED_MODELS_DIR = MODELS_DIR / "saved"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"

# Ensure directories exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR, MODELS_DIR, SAVED_MODELS_DIR, NOTEBOOKS_DIR, REPORTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Official Competition Files Specification
OFFICIAL_COMPETITION_FILES = {
    "combine_tracking": "combine_tracking.csv",
    "combine_results": "combine_results.csv",
    "game_tracking_2023": "game_tracking_2023.csv",
    "game_tracking_2024": "game_tracking_2024.csv",
    "game_tracking_2025": "game_tracking_2025.csv",
    "player_play": "player_play.csv",
    "player_career_successes": "player_career_successes.csv",
    "players": "players.csv",
    "games": "games.csv",
}

GAME_TRACKING_FILES = [
    "game_tracking_2023.csv",
    "game_tracking_2024.csv",
    "game_tracking_2025.csv",
]

# Memory Optimization Guidelines for 8 GB RAM
MAX_RAM_GB = 8.0
SAFE_MEMORY_FRACTION = 0.6  # Target maximum memory usage ~4.8 GB
CHUNK_SIZE_ROWS = 100_000   # For chunked pandas/arrow streaming if needed

# NFL Field Coordinates & Physical Bounds
FIELD_X_MIN = 0.0
FIELD_X_MAX = 120.0  # Including endzones (10 yds each)
FIELD_Y_MIN = 0.0
FIELD_Y_MAX = 53.33  # Standard NFL field width (53 1/3 yards)
TRACKING_FREQUENCY_HZ = 10.0  # Zebra / NGS RFID frequency (10 frames per second)
FRAME_INTERVAL_SEC = 0.1  # 1 / 10.0

# Physical Plausibility Thresholds for Quality Control
MAX_PLAUSIBLE_SPEED_YPS = 13.0  # ~26.6 mph (Fastest recorded NFL speed ~23.24 mph)
MAX_PLAUSIBLE_ACCEL_YPS2 = 12.0  # Sensor spikes above this typically indicate noise

# Common Identifier Names across NFL & Combine data
PLAYER_ID_CANDIDATES = ["nfl_id", "nflId", "player_id", "playerId", "smartabase_id", "combineId"]
GAME_ID_CANDIDATES = ["game_id", "gameId"]
PLAY_ID_CANDIDATES = ["play_id", "playId"]

# Positional Groupings
POSITION_GROUPS = {
    "SKILL_OFFENSE": ["WR", "RB", "FB", "TE"],
    "LINE_OFFENSE": ["T", "G", "C", "OT", "OG"],
    "DEFENSIVE_FRONT": ["DE", "DT", "NT", "EDGE", "DL"],
    "LINEBACKERS": ["ILB", "OLB", "MLB", "LB"],
    "DEFENSIVE_BACKS": ["CB", "FS", "SS", "DB", "S"],
}

RANDOM_SEED = 42
