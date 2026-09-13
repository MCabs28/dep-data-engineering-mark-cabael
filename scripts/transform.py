"""
Phase 3 — Data Transformation

Loads rainfall data for all 17 Philippine regions from raw Open-Meteo
JSON files, cleans and validates the data, and saves one combined
processed CSV dataset.
"""

import glob
import json
import os

import pandas as pd

RAW_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")

PROCESSED_DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")

OUTPUT_FILE = os.path.join(PROCESSED_DATA_DIR, "rainfall_clean.csv")

EXTREME_RAINFALL_THRESHOLD = 50.0


def transform():
    raw_files = glob.glob(os.path.join(RAW_DATA_DIR, "rainfall_*.json"))

    # Exclude metadata files
    raw_files = [file for file in raw_files if not file.endswith("_metadata.json")]

    if not raw_files:
        raise FileNotFoundError("No raw rainfall JSON files found in data/raw/")

    records = []

    for raw_file in raw_files:
        print(f"Processing: {os.path.basename(raw_file)}")

        with open(raw_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        daily = data.get("daily", {})

        dates = daily.get("time", [])
        precipitation = daily.get("precipitation_sum", [])

        if len(dates) != len(precipitation):
            raise ValueError(
                f"Date and precipitation arrays have "
                f"different lengths in {raw_file}"
            )

        # Extract region information from metadata
        metadata_file = raw_file.replace(".json", "_metadata.json")

        if not os.path.exists(metadata_file):
            raise FileNotFoundError(f"Metadata file not found for {raw_file}")

        with open(metadata_file, "r", encoding="utf-8") as f:
            metadata = json.load(f)

        region = metadata["region"]
        location = metadata["location"]

        # Use coordinates returned by the API
        latitude = data.get("latitude", metadata["latitude"])

        longitude = data.get("longitude", metadata["longitude"])

        for date, rainfall in zip(dates, precipitation):
            records.append(
                {
                    "date": date,
                    "region": region,
                    "location": location,
                    "latitude": latitude,
                    "longitude": longitude,
                    "precipitation_mm": rainfall,
                }
            )

    df = pd.DataFrame(records)

    # Convert date to datetime
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Convert rainfall to numeric
    df["precipitation_mm"] = pd.to_numeric(df["precipitation_mm"], errors="coerce")

    # Flag missing rainfall values
    df["precipitation_missing"] = df["precipitation_mm"].isna()

    # Validate dates
    if df["date"].isna().any():
        raise ValueError("Invalid date values found in dataset.")

    # Validate rainfall values
    if (df["precipitation_mm"].dropna() < 0).any():
        raise ValueError("Negative precipitation values found.")

    # Remove duplicate observations
    df = df.drop_duplicates(
        subset=[
            "date",
            "latitude",
            "longitude",
        ]
    )

    # Flag extreme rainfall
    df["is_extreme"] = df["precipitation_mm"] >= EXTREME_RAINFALL_THRESHOLD

    # Sort dataset
    df = df.sort_values(by=["region", "date"]).reset_index(drop=True)

    # Convert date to YYYY-MM-DD
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Expected columns
    expected_columns = [
        "date",
        "region",
        "location",
        "latitude",
        "longitude",
        "precipitation_mm",
        "precipitation_missing",
        "is_extreme",
    ]

    df = df[expected_columns]

    # M3 validation checks
    if df.empty:
        raise ValueError("Processed dataset is empty.")

    if df["region"].nunique() != 17:
        raise ValueError(f"Expected 17 regions, found " f"{df['region'].nunique()}.")

    if df.duplicated(subset=["region", "date"]).any():
        raise ValueError("Duplicate region/date observations found.")

    # Save processed dataset
    os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

    df.to_csv(OUTPUT_FILE, index=False)

    print("\nValidation passed.")
    print(f"Regions processed: {df['region'].nunique()}")
    print(f"Records processed: {len(df)}")
    print(f"Processed data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    transform()

    print("Transformation complete. " "Check data/processed/ for output.")
