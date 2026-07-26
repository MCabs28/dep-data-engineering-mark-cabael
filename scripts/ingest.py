"""
Phase 2 — Data Ingestion

Downloads historical rainfall data from the Open-Meteo Historical Weather API
and saves the raw JSON response together with metadata.
"""

import json
import os
from datetime import datetime

import requests

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def ingest():
    params = {
        "latitude": 14.2117,  # Calamba City (Month of June 2026 for the available and latest data)
        "longitude": 121.1653,
        "start_date": "2026-01-01",
        "end_date": "2026-06-30",
        "daily": "precipitation_sum",
        "timezone": "Asia/Manila",
    }

    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()

    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    raw_filename = f"rainfall_{timestamp}.json"
    metadata_filename = f"rainfall_{timestamp}_metadata.json"

    raw_path = os.path.join(RAW_DATA_DIR, raw_filename)
    metadata_path = os.path.join(RAW_DATA_DIR, metadata_filename)

    # Save raw API response
    with open(raw_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    # Save metadata
    metadata = {
        "source": "Open-Meteo Historical Weather API",
        "source_url": response.url,
        "retrieved_at": datetime.now().isoformat(),
        "format": "JSON",
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=4)

    print(f"Saved raw data: {raw_filename}")
    print(f"Saved metadata: {metadata_filename}")


if __name__ == "__main__":
    os.makedirs(RAW_DATA_DIR, exist_ok=True)
    ingest()
    print("Ingestion complete. Check data/raw/ for output.")
