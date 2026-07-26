from pathlib import Path

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# Open-Meteo API
BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

TIMEZONE = "Asia/Manila"
