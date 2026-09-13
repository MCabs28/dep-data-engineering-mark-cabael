"""
Phase 2 — Data Ingestion

Downloads historical rainfall data for all 17 Philippine administrative
regions from the Open-Meteo Historical Weather API and saves the raw
JSON responses together with metadata.
"""

import json
import os
import re
import time
from datetime import datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ============================================================
# Configuration
# ============================================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "data", "raw"))

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

START_DATE = "2026-01-01"
END_DATE = "2026-08-31"


# ============================================================
# Philippine Regions
# ============================================================

REGIONS = [
    {
        "region": "NCR",
        "location": "Manila",
        "latitude": 14.5995,
        "longitude": 120.9842,
    },
    {
        "region": "CAR",
        "location": "Baguio City",
        "latitude": 16.4023,
        "longitude": 120.5960,
    },
    {
        "region": "Region I (Ilocos)",
        "location": "San Fernando, La Union",
        "latitude": 16.6159,
        "longitude": 120.3209,
    },
    {
        "region": "Region II (Cagayan Valley)",
        "location": "Tuguegarao City",
        "latitude": 17.6132,
        "longitude": 121.7269,
    },
    {
        "region": "Region III (Central Luzon)",
        "location": "City of San Fernando, Pampanga",
        "latitude": 15.0343,
        "longitude": 120.6845,
    },
    {
        "region": "Region IV-A (CALABARZON)",
        "location": "Calamba City",
        "latitude": 14.2117,
        "longitude": 121.1653,
    },
    {
        "region": "MIMAROPA",
        "location": "Calapan City",
        "latitude": 13.4115,
        "longitude": 121.1803,
    },
    {
        "region": "Region V (Bicol)",
        "location": "Legazpi City",
        "latitude": 13.1391,
        "longitude": 123.7438,
    },
    {
        "region": "Region VI (Western Visayas)",
        "location": "Iloilo City",
        "latitude": 10.7202,
        "longitude": 122.5621,
    },
    {
        "region": "Region VII (Central Visayas)",
        "location": "Cebu City",
        "latitude": 10.3157,
        "longitude": 123.8854,
    },
    {
        "region": "Region VIII (Eastern Visayas)",
        "location": "Tacloban City",
        "latitude": 11.2440,
        "longitude": 125.0037,
    },
    {
        "region": "Region IX (Zamboanga Peninsula)",
        "location": "Pagadian City",
        "latitude": 7.8257,
        "longitude": 123.4370,
    },
    {
        "region": "Region X (Northern Mindanao)",
        "location": "Cagayan de Oro",
        "latitude": 8.4542,
        "longitude": 124.6319,
    },
    {
        "region": "Region XI (Davao Region)",
        "location": "Davao City",
        "latitude": 7.1907,
        "longitude": 125.4553,
    },
    {
        "region": "Region XII (SOCCSKSARGEN)",
        "location": "Koronadal City",
        "latitude": 6.5007,
        "longitude": 124.8464,
    },
    {
        "region": "Region XIII (Caraga)",
        "location": "Butuan City",
        "latitude": 8.9475,
        "longitude": 125.5406,
    },
    {
        "region": "BARMM",
        "location": "Cotabato City",
        "latitude": 7.2232,
        "longitude": 124.2464,
    },
]


# ============================================================
# HTTP Session
# ============================================================


def build_session():
    """
    Creates a shared HTTP session with retry handling
    for temporary API/network failures.
    """

    session = requests.Session()

    retry_strategy = Retry(
        total=5,
        connect=5,
        read=5,
        status=5,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)

    session.mount("https://", adapter)
    session.mount("http://", adapter)

    return session


# ============================================================
# Filename Helper
# ============================================================


def sanitize_filename(name):
    """
    Converts region names into safe lowercase filenames.
    """

    return re.sub(r"[^\w]+", "_", name).strip("_").lower()


# ============================================================
# Region Ingestion
# ============================================================


def ingest_region(session, region_info):
    """
    Downloads rainfall data for one region and saves:
    1. Raw API response
    2. Metadata
    """

    params = {
        "latitude": region_info["latitude"],
        "longitude": region_info["longitude"],
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": "precipitation_sum",
        "timezone": "Asia/Manila",
    }

    print(f"\nFetching {region_info['region']} " f"({region_info['location']})...")

    response = session.get(
        BASE_URL,
        params=params,
        timeout=(30, 180),
    )

    response.raise_for_status()

    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    region_slug = sanitize_filename(region_info["region"])

    raw_filename = f"rainfall_{region_slug}_{timestamp}.json"

    metadata_filename = f"rainfall_{region_slug}_{timestamp}_metadata.json"

    raw_path = os.path.join(RAW_DATA_DIR, raw_filename)

    metadata_path = os.path.join(RAW_DATA_DIR, metadata_filename)

    # --------------------------------------------------------
    # Save raw API response
    # --------------------------------------------------------

    with open(raw_path, "w", encoding="utf-8") as file:

        json.dump(data, file, indent=4)

    # --------------------------------------------------------
    # Save metadata
    # --------------------------------------------------------

    metadata = {
        "source": "Open-Meteo Historical Weather API",
        "source_url": response.url,
        "retrieved_at": datetime.now().isoformat(),
        "format": "JSON",
        "region": region_info["region"],
        "location": region_info["location"],
        "latitude": region_info["latitude"],
        "longitude": region_info["longitude"],
        "start_date": START_DATE,
        "end_date": END_DATE,
    }

    with open(metadata_path, "w", encoding="utf-8") as file:

        json.dump(metadata, file, indent=4)

    print(f"✔ Saved {region_info['region']}: " f"{raw_filename}")


# ============================================================
# Main Ingestion Process
# ============================================================


def ingest():

    os.makedirs(RAW_DATA_DIR, exist_ok=True)

    session = build_session()

    successful_regions = []
    failed_regions = []

    print("=" * 60)
    print("BahaPredict — Rainfall Data Ingestion")
    print("=" * 60)

    print(f"Date range: {START_DATE} to {END_DATE}")

    print(f"Regions: {len(REGIONS)}")

    print("=" * 60)

    for index, region in enumerate(REGIONS, start=1):

        print(f"\n[{index}/{len(REGIONS)}] " f"{region['region']}")

        try:

            ingest_region(session, region)

            successful_regions.append(region["region"])

            # Small delay between requests
            time.sleep(2)

        except requests.exceptions.RequestException as error:

            failed_regions.append(region["region"])

            print(f"✖ Failed {region['region']}: " f"{error}")

            # Continue with the next region
            continue

        except ValueError as error:

            failed_regions.append(region["region"])

            print(f"✖ Invalid API response for " f"{region['region']}: {error}")

            continue

    # ========================================================
    # Summary
    # ========================================================

    print("\n" + "=" * 60)
    print("INGESTION SUMMARY")
    print("=" * 60)

    print(f"Successful regions: " f"{len(successful_regions)}/{len(REGIONS)}")

    print(f"Failed regions: " f"{len(failed_regions)}/{len(REGIONS)}")

    if successful_regions:
        print("\nSuccessful:")
        for region in successful_regions:
            print(f"  ✔ {region}")

    if failed_regions:
        print("\nFailed:")
        for region in failed_regions:
            print(f"  ✖ {region}")

    print("=" * 60)

    if len(successful_regions) == len(REGIONS):

        print(
            "Ingestion complete. " f"All {len(REGIONS)} regions processed successfully."
        )

    else:

        print("Ingestion completed with failures.")

        print("Run the script again to retry " "the failed regions.")


# ============================================================
# Entry Point
# ============================================================

if __name__ == "__main__":
    ingest()
