# DEP Data Engineering Cohort 1

## Author

**Mark Cabael**

# Milestone M1 Submission

## Project Title

**BahaPredict: Building an Automated Regional Weather Data Pipeline in the Philippines**

# 1. Research Question

**Which Philippine regions experience the highest frequency of extreme daily rainfall events, and during which months do periods of elevated rainfall historically occur that may contribute to increased localized flood risk?**

# 2. Stakeholders

## Primary Stakeholders

- Local Disaster Risk Reduction and Management Offices (LDRRMOs)
- Local Government Units (LGUs)
- Regional Planning and Development Offices

## Secondary Stakeholders

- Farmers and agricultural agencies
- Infrastructure planners
- Environmental researchers
- Emergency response teams

# 3. Why This Matters

Many government agencies, researchers, and planners rely on historical weather data to better understand long-term rainfall patterns. However, weather datasets are often obtained from multiple sources and require manual downloading, cleaning, and preparation before they can be analyzed.

This project aims to automate the collection, storage, and preparation of historical rainfall data into a structured dataset that supports regional rainfall analysis across the Philippines.

The resulting dataset can help stakeholders:

- Identify regions that consistently experience higher frequencies of extreme rainfall events.
- Determine months when unusually heavy rainfall has historically occurred.
- Support disaster preparedness and planning by providing historical rainfall insights that may contribute to localized flood risk assessments.
- Assist agricultural planning by understanding seasonal rainfall patterns.
- Provide a reusable and automated data pipeline for future weather and environmental analyses.

> **Note:** This project analyzes historical rainfall patterns only. Rainfall is one of several factors that influence flooding and should be interpreted as a potential indicator rather than a direct measurement or prediction of flood risk.

# 4. Data Source & Ingestion

## Overview

The ingestion pipeline automatically retrieves historical daily rainfall data from the **Open-Meteo Historical Weather API** using Python and stores the original API response without modification.

The pipeline is designed to be repeatable, allowing the latest data to be downloaded whenever the script is executed.

## Data Source

- **Source:** Open-Meteo Historical Weather API
- **Data Format:** JSON
- **Access Method:** HTTP GET request using the Python `requests` library

## Raw Data Storage

The original API response is stored in the following directory:

```text
data/
└── raw/
```

Each execution creates timestamped files to preserve every ingestion run.

Example:

```text
data/raw/
├── rainfall_20260726_061500.json
└── rainfall_20260726_061500_metadata.json
```

## Metadata

Alongside each raw JSON file, a metadata file is generated containing:

- Data source
- API request URL
- Retrieval timestamp
- File format

This ensures every downloaded dataset is traceable and reproducible.

## Running the Ingestion Script

From the project root, execute:

```bash
python scripts/ingest.py
```

The script will:

1. Send a request to the Open-Meteo Historical Weather API.
2. Download the historical rainfall data.
3. Save the raw JSON response in `data/raw/`.
4. Save a metadata file containing the source URL and retrieval timestamp.

## Repeatability

The ingestion process is fully repeatable. Running the script multiple times generates new timestamped raw data and metadata files without overwriting previous ingestions.



## Primary Data Source

- **Name:** Open-Meteo Historical Weather API
- **Website:** https://open-meteo.com/
- **API Documentation:** https://open-meteo.com/en/docs/historical-weather-api
- **Direct API Endpoint:** `https://archive-api.open-meteo.com/v1/archive`

### Example API Request

https://archive-api.open-meteo.com/v1/archive?latitude=14.2117&longitude=121.1653&start_date=2026-01-01&end_date=2026-06-30&daily=precipitation_sum&timezone=Asia/Manila

### Data Format

- JSON (REST API response)

### Coverage & Scope

#### Geographic Scope

The ETL pipeline covers all **17 administrative regions of the Philippines**. Historical weather data will initially be retrieved using the latitude and longitude coordinates of one representative location within each region. These representative coordinates serve as sampling points for regional comparison and are not intended to capture the full spatial variability of rainfall across an entire region.

Future iterations of the project may incorporate multiple observation points or gridded weather datasets to provide a more comprehensive representation of regional rainfall patterns.

| Region                          | Representative Location        | Latitude | Longitude |
| ------------------------------- | ------------------------------ | -------- | --------- |
| NCR                             | Manila                         | 14.5995  | 120.9842  |
| CAR                             | Baguio City                    | 16.4023  | 120.5960  |
| Region I (Ilocos)               | San Fernando, La Union         | 16.6159  | 120.3209  |
| Region II (Cagayan Valley)      | Tuguegarao City                | 17.6132  | 121.7269  |
| Region III (Central Luzon)      | City of San Fernando, Pampanga | 15.0343  | 120.6845  |
| Region IV-A (CALABARZON)        | Calamba City                   | 14.2117  | 121.1653  |
| MIMAROPA                        | Calapan City                   | 13.4115  | 121.1803  |
| Region V (Bicol)                | Legazpi City                   | 13.1391  | 123.7438  |
| Region VI (Western Visayas)     | Iloilo City                    | 10.7202  | 122.5621  |
| Region VII (Central Visayas)    | Cebu City                      | 10.3157  | 123.8854  |
| Region VIII (Eastern Visayas)   | Tacloban City                  | 11.2440  | 125.0037  |
| Region IX (Zamboanga Peninsula) | Pagadian City                  | 7.8257   | 123.4370  |
| Region X (Northern Mindanao)    | Cagayan de Oro                 | 8.4542   | 124.6319  |
| Region XI (Davao Region)        | Davao City                     | 7.1907   | 125.4553  |
| Region XII (SOCCSKSARGEN)       | Koronadal City                 | 6.5007   | 124.8464  |
| Region XIII (Caraga)            | Butuan City                    | 8.9475   | 125.5406  |
| BARMM                           | Cotabato City                  | 7.2232   | 124.2464  |

#### Temporal Coverage

The project analyzes approximately **20 years of historical rainfall data (2006–2025)** to identify long-term rainfall patterns and seasonal variations across Philippine regions. The API request shown above is provided as a sample request to demonstrate data access.

# 5. Definition of Extreme Rainfall

For this project, an **extreme rainfall event** is defined as a day with **50 millimeters (mm) or more of total daily precipitation**.

This threshold is used for analytical purposes to identify unusually heavy rainfall events across regions and support consistent comparisons. It is intended as a project-specific definition and may be refined in future iterations using meteorological standards or official guidance from PAGASA.

## Backup Data Source

- **Name:** NASA POWER (Prediction of Worldwide Energy Resources) API
- **Website:** https://power.larc.nasa.gov/
- **API Documentation:** https://power.larc.nasa.gov/docs/services/api/
- **Direct API Endpoint:** `https://power.larc.nasa.gov/api/temporal/daily/point`

### Example API Request

https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG&latitude=14.2117&longitude=121.1653&start=20260101&end=20260630&format=JSON

### Data Format

- JSON (REST API response)

### Purpose

The NASA POWER API serves as the project's backup data source. If the Open-Meteo API becomes unavailable or returns incomplete data, the ETL pipeline will retrieve historical precipitation data using the same representative regional coordinates.

# 6. Planned Ingestion Method

## Method

Automated HTTP GET requests using Python (`requests` library).

## Ingestion Strategy

- Load a coordinate mapping file containing representative locations for all 17 Philippine administrative regions.
- Iterate through each representative location and submit API requests using its latitude and longitude.
- Extract historical weather data in manageable yearly batches to improve reliability and reduce request failures.
- Store the original API responses in a raw landing zone before performing any transformations.
- Transform the raw data into structured datasets for downstream analysis and database loading.

# 7. Project Scope

This project focuses on building an automated data engineering pipeline that collects, stores, and prepares historical rainfall data for analysis.

The project does **not** attempt to predict flooding or estimate flood probability. Instead, it analyzes historical rainfall patterns that may contribute to localized flood risk when considered alongside other environmental and geographic factors.

The primary objective is to produce reliable, reproducible, and analysis-ready rainfall datasets that can support future environmental and disaster-related studies.

# 8. Project Limitations

This project uses one representative geographic coordinate for each Philippine administrative region to simplify data collection and enable regional comparisons. Because rainfall can vary significantly within a region, these representative locations should not be interpreted as fully representing rainfall conditions across the entire region.

Additionally, this project analyzes historical rainfall data only. Flood occurrence is influenced by many other factors, including topography, river systems, drainage infrastructure, land use, soil conditions, and tidal conditions. Therefore, the results should be interpreted as indicators of historical rainfall intensity rather than direct measurements or predictions of flood risk.

# Repository Status

- Public repository created
- Research question defined
- Stakeholders identified
- Project rationale completed
- Primary data source documented
- Backup data source documented
- API access paths documented
- Geographic and temporal coverage documented
- Definition of extreme rainfall established
- Planned ingestion strategy documented
- Project scope and limitations documented
- README documentation completed