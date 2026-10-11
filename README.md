# DEP Data Engineering Cohort 1

## Author

Mark Cabael

# Milestone M3 Submission

## Project Title

BahaPredict: Building an Automated Regional Weather Data Pipeline in the Philippines

# 1. Research Question

Which Philippine regions experience the highest frequency of extreme daily rainfall events, and during which months do periods of elevated rainfall historically occur that may contribute to increased localized flood risk?

# 2. Stakeholders

## Primary Stakeholders

* Local Disaster Risk Reduction and Management Offices (LDRRMOs)
* Local Government Units (LGUs)
* Regional Planning and Development Offices

## Secondary Stakeholders

* Farmers and agricultural agencies
* Infrastructure planners
* Environmental researchers
* Emergency response teams

# 3. Why This Matters

Many government agencies, researchers, and planners rely on historical weather data to better understand rainfall patterns. However, weather datasets are often obtained from multiple sources and require manual downloading, cleaning, and preparation before they can be analyzed.

This project aims to automate the collection, storage, transformation, and preparation of historical rainfall data into a structured dataset that supports regional rainfall analysis across the Philippines.

The resulting dataset can help stakeholders:

* Identify regions that experience higher frequencies of extreme rainfall events.
* Determine months when higher average rainfall occurs.
* Support disaster preparedness and planning by providing historical rainfall insights that may contribute to localized flood risk assessments.
* Assist agricultural planning by understanding seasonal rainfall patterns.
* Provide a reusable and automated data pipeline for future weather and environmental analyses.

Note: This project analyzes historical rainfall patterns only. Rainfall is one of several factors that influence flooding and should be interpreted as a potential indicator rather than a direct measurement or prediction of flood risk.

# 4. Data Source & Ingestion

## Overview

The ingestion pipeline automatically retrieves historical daily rainfall data from the Open-Meteo Historical Weather API using Python and stores the original API response without modification.

The pipeline retrieves rainfall data for representative locations across all 17 Philippine administrative regions.

The pipeline is repeatable, allowing the data to be downloaded again whenever the script is executed.

## Data Source

* Source: Open-Meteo Historical Weather API
* Data Format: JSON
* Access Method: HTTP GET request using the Python `requests` library

## Raw Data Storage

The original API responses are stored in:

```text
data/
└── raw/
```

Each execution creates timestamped files to preserve every ingestion run.

Example:

```text
data/raw/

├── rainfall_ncr_20260909_205355.json
├── rainfall_ncr_20260909_205355_metadata.json
├── rainfall_car_20260909_205357.json
├── rainfall_car_20260909_205357_metadata.json
└── ...
```

## Metadata

Alongside each raw JSON file, a metadata file is generated containing:

* Data source
* API request URL
* Retrieval timestamp
* File format
* Region
* Representative location
* Latitude and longitude
* Start and end dates

This ensures every downloaded dataset is traceable and reproducible.

## Running the Ingestion Script

From the project root, execute:

```bash
python scripts/ingest.py
```

The script will:

1. Iterate through the configured representative locations for all 17 Philippine regions.
2. Send requests to the Open-Meteo Historical Weather API.
3. Download the historical daily rainfall data.
4. Save each raw API response in `data/raw/`.
5. Save metadata for each regional response.

A successful ingestion run processes all 17 regions.

## Repeatability

The ingestion process is repeatable. Each execution creates new timestamped raw files without overwriting previous ingestion results.

# Primary Data Source

* Name: Open-Meteo Historical Weather API
* Website: https://open-meteo.com/
* API Documentation: https://open-meteo.com/en/docs/historical-weather-api
* Direct API Endpoint: `https://archive-api.open-meteo.com/v1/archive`

## Example API Request

```text
https://archive-api.open-meteo.com/v1/archive?latitude=14.2117&longitude=121.1653&start_date=2026-01-01&end_date=2026-08-31&daily=precipitation_sum&timezone=Asia/Manila
```

## Data Format

* JSON (REST API response)

## Coverage & Scope

### Geographic Scope

The ETL pipeline covers all 17 administrative regions of the Philippines.

One representative location is used for each region as a sampling point for regional rainfall comparison. These representative locations are not intended to capture the complete spatial variability of rainfall across an entire region.

| Region                          | Representative Location        | Latitude | Longitude |
| ------------------------------- | ------------------------------ | -------: | --------: |
| NCR                             | Manila                         |  14.5995 |  120.9842 |
| CAR                             | Baguio City                    |  16.4023 |  120.5960 |
| Region I (Ilocos)               | San Fernando, La Union         |  16.6159 |  120.3209 |
| Region II (Cagayan Valley)      | Tuguegarao City                |  17.6132 |  121.7269 |
| Region III (Central Luzon)      | City of San Fernando, Pampanga |  15.0343 |  120.6845 |
| Region IV-A (CALABARZON)        | Calamba City                   |  14.2117 |  121.1653 |
| MIMAROPA                        | Calapan City                   |  13.4115 |  121.1803 |
| Region V (Bicol)                | Legazpi City                   |  13.1391 |  123.7438 |
| Region VI (Western Visayas)     | Iloilo City                    |  10.7202 |  122.5621 |
| Region VII (Central Visayas)    | Cebu City                      |  10.3157 |  123.8854 |
| Region VIII (Eastern Visayas)   | Tacloban City                  |  11.2440 |  125.0037 |
| Region IX (Zamboanga Peninsula) | Pagadian City                  |   7.8257 |  123.4370 |
| Region X (Northern Mindanao)    | Cagayan de Oro                 |   8.4542 |  124.6319 |
| Region XI (Davao Region)        | Davao City                     |   7.1907 |  125.4553 |
| Region XII (SOCCSKSARGEN)       | Koronadal City                 |   6.5007 |  124.8464 |
| Region XIII (Caraga)            | Butuan City                    |   8.9475 |  125.5406 |
| BARMM                           | Cotabato City                  |   7.2232 |  124.2464 |

### Temporal Coverage

The project is designed to analyze historical rainfall patterns across Philippine regions.

The current M3 implementation contains rainfall data for:

January 1, 2026 – August 31, 2026

for all 17 representative regional locations.

The planned 2006–2025 period represents a future historical analysis scope and is not currently included in the processed dataset.

# 5. Definition of Extreme Rainfall

For this project, an extreme rainfall event is defined as a day with 50 millimeters (mm) or more of total daily precipitation.

This threshold is used for analytical purposes to identify unusually heavy rainfall events across regions and support consistent comparisons.

It is a project-specific definition and may be refined in future iterations using meteorological standards or official guidance from PAGASA.

## Backup Data Source

* Name: NASA POWER (Prediction of Worldwide Energy Resources) API
* Website: https://power.larc.nasa.gov/
* API Documentation: https://power.larc.nasa.gov/docs/services/api/
* Direct API Endpoint: `https://power.larc.nasa.gov/api/temporal/daily/point`

## Example API Request

```text
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG&latitude=14.2117&longitude=121.1653&start=20260101&end=20260831&format=JSON
```

## Data Format

* JSON (REST API response)

## Purpose

The NASA POWER API serves as the project's backup data source. If the Open-Meteo API becomes unavailable or returns incomplete data, the ETL pipeline can retrieve historical precipitation data using the representative regional coordinates.

# 6. Planned Ingestion Method

## Method

Automated HTTP GET requests using Python (`requests` library).

## Ingestion Strategy

* Load the representative location mapping for all 17 Philippine administrative regions.
* Iterate through each representative location and submit API requests using its latitude and longitude.
* Retrieve daily historical rainfall data for the configured date range.
* Store the original API responses in a raw landing zone before transformation.
* Transform the raw data into a structured dataset for downstream analysis.
* Preserve raw responses and metadata for traceability and reproducibility.

# Milestone M3 — Clean Dataset

## 7. M3 Overview

Milestone 3 transforms the raw Open-Meteo JSON responses into a clean, structured, and analysis-ready rainfall dataset.

The transformation process is implemented in:

```text
scripts/transform.py
```

The processed dataset is saved to:

```text
data/processed/rainfall_clean.csv
```

The overall pipeline is:

```text
Open-Meteo Historical Weather API
                ↓
        scripts/ingest.py
                ↓
          data/raw/*.json
                ↓
       scripts/transform.py
                ↓
     data/processed/rainfall_clean.csv
                ↓
          SQL analysis
```

## 8. M3 Data Transformation

The transformation script performs the following operations:

1. Loads the raw Open-Meteo rainfall JSON files from `data/raw/`.
2. Identifies the region and representative location associated with each raw file.
3. Extracts the nested `daily.time` and `daily.precipitation_sum` arrays.
4. Converts the nested daily data into one row per observation.
5. Converts rainfall values into numeric values.
6. Converts observation dates into date values.
7. Adds the representative region and location metadata.
8. Flags missing precipitation values using `precipitation_missing`.
9. Removes observations with invalid dates.
10. Removes duplicate observations based on `date`, `latitude`, and `longitude`.
11. Calculates `is_extreme` using the project's 50 mm/day threshold.
12. Sorts the processed observations by region and date.
13. Saves the resulting dataset to `data/processed/rainfall_clean.csv`.

### Missing Value Handling

Missing precipitation values are flagged rather than automatically replaced with zero.

This decision avoids interpreting an unknown rainfall measurement as zero rainfall.

The `precipitation_missing` field allows missing observations to be identified during downstream analysis.

## Validation Results

The latest transformation successfully processed:

* 17 regions
* 4,131 records
* 243 records per region
* Date range: January 1, 2026 – August 31, 2026

All required fields passed validation, with 0 missing values in the processed dataset.

# 9. M3 Business Questions

The processed dataset is used to answer three initial business questions.

The SQL queries are stored in:

```text
sql/business_questions.sql
```

The queries are executed using DuckDB.

## Business Question 1

Which regions experience the highest number of extreme rainfall days?

The query counts observations where daily precipitation is at least 50 mm and groups the results by region.

### Current Results

| Region                          | Representative Location        | Extreme Rainfall Days |
| ------------------------------- | ------------------------------ | --------------------: |
| CAR                             | Baguio City                    |                    13 |
| Region I (Ilocos)               | San Fernando, La Union         |                    11 |
| Region VIII (Eastern Visayas)   | Tacloban City                  |                     4 |
| MIMAROPA                        | Calapan City                   |                     3 |
| Region XI (Davao Region)        | Davao City                     |                     3 |
| BARMM                           | Cotabato City                  |                     2 |
| NCR                             | Manila                         |                     2 |
| Region III (Central Luzon)      | City of San Fernando, Pampanga |                     2 |
| Region V (Bicol)                | Legazpi City                   |                     2 |
| Region VI (Western Visayas)     | Iloilo City                    |                     2 |
| Region VII (Central Visayas)    | Cebu City                      |                     2 |
| Region X (Northern Mindanao)    | Cagayan de Oro                 |                     2 |
| Region XIII (Caraga)            | Butuan City                    |                     2 |
| Region II (Cagayan Valley)      | Tuguegarao City                |                     1 |
| Region XII (SOCCSKSARGEN)       | Koronadal City                 |                     1 |
| Region IV-A (CALABARZON)        | Calamba City                   |                     0 |
| Region IX (Zamboanga Peninsula) | Pagadian City                  |                     0 |

### Interpretation

Based on the current January–August 2026 dataset, CAR recorded the highest number of extreme rainfall days with 13, followed by Region I (Ilocos) with 11.

Region IV-A (CALABARZON) and Region IX (Zamboanga Peninsula) recorded no observations meeting the project's 50 mm/day extreme rainfall threshold during the current period.

These results represent the selected representative locations and should not be interpreted as complete rainfall measurements for entire regions.

## Business Question 2

Which months have the highest average daily rainfall across the 17 representative regional locations?

### Current Results

| Month    | Average Rainfall |
| -------- | ---------------: |
| August   |         12.15 mm |
| July     |          9.22 mm |
| February |          6.92 mm |
| June     |          5.96 mm |
| May      |          5.44 mm |
| January  |          4.44 mm |
| March    |          2.08 mm |
| April    |          1.55 mm |

### Interpretation

August recorded the highest average daily rainfall across the 17 representative locations at 12.15 mm, followed by July at 9.22 mm.

April recorded the lowest average daily rainfall during the current January–August period at 1.55 mm.

## Business Question 3

Which Philippine regions recorded the highest total rainfall during the current period?

### Current Results

| Region                          | Representative Location        | Total Rainfall |
| ------------------------------- | ------------------------------ | -------------: |
| CAR                             | Baguio City                    |      3038.8 mm |
| Region I (Ilocos)               | San Fernando, La Union         |      2068.4 mm |
| Region XI (Davao Region)        | Davao City                     |      1849.3 mm |
| Region VIII (Eastern Visayas)   | Tacloban City                  |      1506.0 mm |
| Region IX (Zamboanga Peninsula) | Pagadian City                  |      1483.3 mm |
| BARMM                           | Cotabato City                  |      1435.0 mm |
| NCR                             | Manila                         |      1346.1 mm |
| Region XII (SOCCSKSARGEN)       | Koronadal City                 |      1331.6 mm |
| Region VII (Central Visayas)    | Cebu City                      |      1303.7 mm |
| MIMAROPA                        | Calapan City                   |      1294.9 mm |
| Region V (Bicol)                | Legazpi City                   |      1275.4 mm |
| Region X (Northern Mindanao)    | Cagayan de Oro                 |      1261.1 mm |
| Region III (Central Luzon)      | City of San Fernando, Pampanga |      1253.9 mm |
| Region XIII (Caraga)            | Butuan City                    |      1204.7 mm |
| Region VI (Western Visayas)     | Iloilo City                    |      1189.8 mm |
| Region IV-A (CALABARZON)        | Calamba City                   |       986.5 mm |
| Region II (Cagayan Valley)      | Tuguegarao City                |       866.1 mm |

### Interpretation

Based on the current January–August 2026 dataset, CAR recorded the highest total rainfall at 3038.8 mm, followed by Region I (Ilocos) at 2068.4 mm and Region XI (Davao Region) at 1849.3 mm.

Region II (Cagayan Valley) recorded the lowest total rainfall among the 17 representative locations at 866.1 mm.

These results are based on the selected representative locations and should not be interpreted as complete rainfall totals for the entire regions.

# 10. Processed Dataset

The final processed dataset is stored in:

```text
data/
└── processed/
    └── rainfall_clean.csv
```

## Dataset Grain

One row represents one daily rainfall observation for one representative geographic location.

## Logical Identifier

The logical identifier for an observation is:

```text
date + latitude + longitude
```

This allows the same date to exist for different geographic locations.

## Processed Fields

| Field                   | Data Type | Description                                                                   |
| ----------------------- | --------- | ----------------------------------------------------------------------------- |
| `date`                  | Date      | Date of the rainfall observation.                                             |
| `region`                | String    | Philippine administrative region associated with the representative location. |
| `location`              | String    | Representative location used for the weather observation.                     |
| `latitude`              | Float     | Latitude returned by Open-Meteo for the observation location.                 |
| `longitude`             | Float     | Longitude returned by Open-Meteo for the observation location.                |
| `precipitation_mm`      | Float     | Total daily precipitation measured in millimeters.                            |
| `precipitation_missing` | Boolean   | Indicates whether the precipitation value was missing during transformation.  |
| `is_extreme`            | Boolean   | Indicates whether daily precipitation is at least 50 mm.                      |

# 11. Project Scope

This project focuses on building an automated data engineering pipeline that collects, stores, transforms, validates, and prepares historical rainfall data for analysis across the 17 Philippine administrative regions.

The project does not attempt to predict flooding or estimate flood probability. Instead, it analyzes historical rainfall patterns that may contribute to localized flood risk when considered alongside other environmental and geographic factors.

The primary objective is to produce reliable, reproducible, and analysis-ready rainfall datasets that can support future environmental and disaster-related studies.

# 12. Project Limitations

This project uses one representative geographic coordinate for each Philippine administrative region to simplify data collection and enable regional comparisons.

Because rainfall can vary significantly within a region, these representative locations should not be interpreted as fully representing rainfall conditions across the entire region.

Additionally, the current dataset covers only January 1, 2026 to August 31, 2026. Therefore, the current results should not be interpreted as long-term historical climate patterns.

The planned 2006–2025 historical analysis is not currently included in the processed dataset.

The project also analyzes rainfall data only. Flood occurrence is influenced by many other factors, including:

* Topography
* River systems
* Drainage infrastructure
* Land use
* Soil conditions
* Tidal conditions
* Other environmental and geographic factors

Therefore, the results should be interpreted as indicators of historical rainfall intensity rather than direct measurements or predictions of flood risk.

# 13. Project Structure

```text
dep-data-engineering-mark-cabael/

│
├── data/
│   ├── raw/
│   │   ├── rainfall_*.json
│   │   └── rainfall_*_metadata.json
│   │
│   ├── processed/
│   │   └── rainfall_clean.csv
│   │
│   └── data_dictionary.md
│
├── scripts/
│   ├── ingest.py
│   ├── transform.py
│   └── run_queries.py
│
├── sql/
│   └── business_questions.sql
│
└── README.md
```

# 14. How to Run the Pipeline

The following steps allow reviewers to reproduce the ingestion, transformation, and SQL analysis workflow.

## Step 1: Install Dependencies

From the project root, activate the virtual environment and install the required Python packages:

```bash
pip install requests pandas duckdb
```

## Step 2: Run Ingestion

Run:

```bash
python scripts/ingest.py
```

This retrieves daily rainfall data for all 17 representative regional locations from the Open-Meteo Historical Weather API.

The raw JSON responses and metadata files are saved to:

```text
data/raw/
```

Expected result:

```text
Successful regions: 17/17
Failed regions: 0/17
```

## Step 3: Run Transformation

After ingestion completes, run:

```bash
python scripts/transform.py
```

This processes the raw JSON files, applies the cleaning and validation rules, and generates:

```text
data/processed/rainfall_clean.csv
```

Expected validation result:

```text
Regions processed: 17
Records processed: 4131
```

The current dataset contains 4,131 records, with 243 daily observations for each of the 17 regions.

## Step 4: Run Business Queries

After the transformation completes, run:

```bash
python scripts/run_queries.py
```

This executes the three SQL business questions using DuckDB and displays the results in the terminal.

The SQL source file is:

```text
sql/business_questions.sql
```

The three queries answer:

1. Which regions experience the highest number of extreme rainfall days?
2. Which months have the highest average daily rainfall across the 17 representative locations?
3. Which Philippine regions recorded the highest total rainfall during the current period?

## Recommended Full Pipeline

To reproduce the complete workflow from raw data collection through analysis, run the following commands in order:

```bash
pip install requests pandas duckdb

python scripts/ingest.py

python scripts/transform.py

python scripts/run_queries.py
```

## Pipeline Output

After running the complete pipeline, the main outputs are:

```text
data/raw/
    ├── rainfall_*.json
    └── rainfall_*_metadata.json

data/processed/
    └── rainfall_clean.csv
```

The terminal output from `run_queries.py` displays the results of the three business questions.

# 15. Repository Status

## M1

* Public repository created
* Research question defined
* Stakeholders identified
* Project rationale completed
* Primary data source documented
* Backup data source documented
* API access paths documented
* Geographic coverage documented
* Temporal coverage documented
* Definition of extreme rainfall established
* Planned ingestion strategy documented
* Project scope and limitations documented

## M2

* Raw Open-Meteo API ingestion implemented
* Raw JSON responses preserved
* Timestamped raw files implemented
* Metadata files implemented
* Ingestion script tested successfully
* 17 regional ingestion implemented
* Raw data stored in `data/raw/`

## M3

* Schema plan documented
* Dataset grain defined
* Logical identifier defined
* Processed dataset created
* 17 Philippine administrative regions processed
* Missing values handled and documented
* Column data types transformed appropriately
* Cleaning decisions documented
* Validation checks implemented
* Deterministic transformation implemented
* Three SQL business questions implemented
* SQL analysis executed successfully
* Processed dataset stored in `data/processed/`
* M3 data dictionary updated
* M3 README documentation updated
* Current dataset updated through August 31, 2026
* 4,131 processed records validated


## 16. M4 

Milestone 4 performs exploratory analysis on the processed rainfall dataset generated during M3. The objective is to identify initial rainfall patterns across 17 representative locations in the Philippines using Python, Pandas, and Matplotlib.

The analysis is documented in the Jupyter Notebook:

`notebooks/m4_initial_insights.ipynb`

The notebook analyzes the following business questions:

1. Which representative locations recorded the highest number of extreme rainfall days?
2. Which months recorded the highest average daily rainfall across the representative locations?
3. Which representative locations recorded the highest total rainfall during the observation period?

## 17. Visualizations and Initial Findings

## 17.1 Extreme Rainfall Days by Representative Location

**Output:** `output/figures/01_extreme_rainfall_days.png`

This chart compares the number of days with daily precipitation of at least 50 mm across the 17 representative locations.

**Initial finding:** Baguio City recorded 13 extreme rainfall days, followed by San Fernando, La Union, with 11. These findings describe the selected locations during January–August 2026 and do not represent complete measurements for their entire administrative regions.

## 17.2 Average Daily Rainfall by Month

**Output:** `output/figures/02_average_rainfall_by_month.png`

This chart compares average daily rainfall across the 17 representative locations for each month from January through August 2026.

**Initial finding:** August recorded the highest average daily rainfall at approximately 12.15 mm, followed by July at 9.22 mm. April recorded the lowest average at approximately 1.55 mm.

Because the observation period covers only eight months of 2026, these results should not be interpreted as long-term seasonal trends.

## 17.3 Total Rainfall by Representative Location

**Output:** `output/figures/03_total_rainfall_by_location.png`

This chart compares cumulative daily precipitation for each representative location during the observation period.

**Initial finding:** Baguio City recorded the highest total rainfall at approximately 3,038.8 mm, followed by San Fernando, La Union, at 2,068.4 mm, and Davao City at 1,849.3 mm.

These totals represent the selected locations rather than complete regional rainfall totals.

## 18. Key Inferences

The initial analysis suggests that rainfall patterns varied across the representative locations during January–August 2026. Baguio City ranked highest in both extreme rainfall days and total rainfall, while August had the highest average daily rainfall across the selected locations.

These findings are descriptive and do not establish that rainfall caused flooding or that any location experienced a specific level of flood risk. A more complete assessment would require additional historical observations, multiple sampling locations per region, and other relevant factors such as topography, drainage, land use, and river conditions.

## 19. M4 Limitations

* The dataset covers January 1 through August 31, 2026 only.
* Each administrative region is represented by one selected location.
* Extreme rainfall is defined using the project's threshold of at least 50 mm/day.
* Rainfall observations do not directly measure flood occurrence or flood probability.
* Longer historical coverage and additional locations would improve future analysis.

## 20. How to Run the M4 Analysis

Run these commands from the project root.

## Step 1: Install Dependencies

```bash
pip install pandas matplotlib jupyter
```

## Step 2: Confirm the Processed Dataset Exists

The notebook uses:

```text
data/processed/rainfall_clean.csv
```

If this file has not been generated, run the ingestion and transformation scripts first:

```bash
python scripts/ingest.py
python scripts/transform.py
```

## Step 3: Launch Jupyter Notebook

```bash
jupyter notebook
```

Open `notebooks/m4_initial_insights.ipynb`.

In VS Code, you can also open the notebook directly from the Explorer.

## Step 4: Run the Notebook

Select **Run All** to execute the cells in order. The notebook loads the processed dataset, performs the three analyses, displays the charts, and presents the interpretations.

## Step 5: Verify the Output Figures

After successful execution, confirm that the following files exist:

```text
output/
└── figures/
    ├── 01_extreme_rainfall_days.png
    ├── 02_average_rainfall_by_month.png
    └── 03_total_rainfall_by_location.png
```

## M4 Completion Checklist

* Processed M3 dataset loaded successfully.
* Dataset overview and validation completed.
* Three charts generated with clear titles and axis labels.
* Each chart includes a written interpretation.
* Key inferences documented without unsupported causal claims.
* Project limitations documented.
* Figures saved to `output/figures/`.
* Notebook runs successfully from beginning to end.