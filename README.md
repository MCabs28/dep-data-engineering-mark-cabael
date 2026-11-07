# DEP Data Engineering Cohort 1

## Author

Mark Cabael

# Milestone M5 Submission

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

The ingestion pipeline automatically retrieves historical daily rainfall data from the Open-Meteo Historical Weather API using Python and stores the original API responses without modification.

The pipeline retrieves rainfall data for representative locations across all 17 Philippine administrative regions.

The pipeline is repeatable, allowing historical rainfall data to be downloaded again whenever the script is executed.

## Data Source

- Source: Open-Meteo Historical Weather API
- Data Format: JSON
- Access Method: HTTP GET request using the Python `requests` library
- Daily Variable: `precipitation_sum`
- Timezone: Asia/Manila

## Raw Data Storage

The original API responses are stored in:

```text
data/
└── raw/
```

Each execution creates timestamped files to preserve individual ingestion runs.

Example:

```text
data/raw/

├── rainfall_ncr_20261108_153448.json
├── rainfall_ncr_20261108_153448_metadata.json
├── rainfall_car_20261108_153450.json
├── rainfall_car_20261108_153450_metadata.json
└── ...
```

## Metadata

Alongside each raw JSON file, a metadata file is generated containing:

- Data source
- API request URL
- Retrieval timestamp
- File format
- Region
- Representative location
- Latitude and longitude
- Start and end dates

This ensures that every downloaded dataset is traceable and reproducible.

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
https://archive-api.open-meteo.com/v1/archive?latitude=14.2117&longitude=121.1653&start_date=2026-01-01&end_date=2026-10-31&daily=precipitation_sum&timezone=Asia/Manila
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

The project analyzes historical daily rainfall data across the 17 representative regional locations.

The current processed dataset covers:

**January 1, 2026 – October 31, 2026**

This provides 304 daily observations for each representative location, resulting in 5,168 observations across all 17 locations.

The current implementation focuses on the 2026 reporting period. A longer historical analysis covering 2006–2025 is not included in the current processed dataset.

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
https://power.larc.nasa.gov/api/temporal/daily/point?parameters=PRECTOTCORR&community=AG&latitude=14.2117&longitude=121.1653&start=20260101&end=20261031&format=JSON
```

## Data Format

* JSON (REST API response)

## Purpose

The NASA POWER API serves as the project's backup data source. If the Open-Meteo API becomes unavailable or returns incomplete data, the ETL pipeline can retrieve historical precipitation data using the representative regional coordinates.

# 6. Ingestion Method

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

- 17 Philippine administrative regions
- 17 representative locations
- 5,168 daily rainfall observations
- 304 observations per representative location
- Date range: January 1, 2026 – October 31, 2026

The processed dataset passed the validation checks:

- 0 missing precipitation values
- 0 negative precipitation values
- 0 duplicate observations
- 304 unique observation dates for each representative location

All required fields passed validation.

# 9. M3 Business Questions

The processed dataset is used to answer three initial business questions.

The SQL queries are stored in:

```text
sql/business_questions.sql
```

The queries are executed using DuckDB.

### Business Question 1: Which representative locations recorded the highest number of extreme daily rainfall events?

An extreme rainfall event is defined in this project as daily precipitation equal to or greater than 50 mm.

| Region | Representative Location | Extreme Rainfall Days |
|---|---|---:|
| CAR | Baguio City | 15 |
| Region I | San Fernando, La Union | 12 |
| Region VIII | Tacloban City | 4 |
| MIMAROPA | Calapan City | 3 |
| Region XI | Davao City | 3 |
| BARMM | Cotabato City | 2 |
| Region III | City of San Fernando, Pampanga | 2 |
| Region V | Legazpi City | 2 |
| Region VI | Iloilo City | 2 |
| Region VII | Cebu City | 2 |
| Region X | Cagayan de Oro City | 2 |
| Region XIII | Butuan City | 2 |
| NCR | Manila | 1 |
| Region II | Tuguegarao City | 1 |
| Region XII | Koronadal City | 1 |
| Region IV-A | Calamba City | 0 |
| Region IX | Pagadian City | 0 |

**Key Finding:**

Baguio City recorded the highest number of extreme rainfall days, with 15 observations. San Fernando, La Union followed with 12. These results identify the two representative locations with the highest frequency of project-defined extreme rainfall events during the reporting period.

### Business Question 2: During which months was average daily rainfall highest across the representative locations?

The monthly average represents the mean daily rainfall across all available representative-location observations for each month.

| Month | Average Daily Rainfall (mm) |
|---|---:|
| January | 4.44 |
| February | 6.92 |
| March | 2.08 |
| April | 1.55 |
| May | 5.44 |
| June | 5.96 |
| July | 9.13 |
| August | 12.15 |
| September | 8.38 |
| October | 7.13 |

**Key Finding:**

August recorded the highest average daily rainfall at 12.15 mm, followed by July at 9.13 mm. April recorded the lowest average at 1.55 mm. The results show an increase in average rainfall from May through August, followed by a decline in September and October.

### Business Question 3: Which representative locations recorded the highest total rainfall during the reporting period?

| Representative Location | Total Rainfall (mm) |
|---|---:|
| Baguio City | 3,762.3 |
| San Fernando, La Union | 2,484.0 |
| Davao City | 2,230.8 |
| Pagadian City | 2,210.7 |
| Tacloban City | 1,917.7 |
| Cebu City | 1,881.5 |
| Cotabato City | 1,843.4 |
| Manila | 1,826.7 |
| Calapan City | 1,788.6 |
| Cagayan de Oro City | 1,779.9 |
| Iloilo City | 1,779.3 |
| Koronadal City | 1,771.4 |
| City of San Fernando, Pampanga | 1,729.7 |
| Legazpi City | 1,701.4 |
| Butuan City | 1,440.4 |
| Calamba City | 1,395.5 |
| Tuguegarao City | 1,140.7 |

**Key Finding:**

Baguio City recorded the highest total rainfall at 3,762.3 mm, followed by San Fernando, La Union at 2,484.0 mm and Davao City at 2,230.8 mm. Tuguegarao City recorded the lowest total rainfall at 1,140.7 mm among the representative locations.

### M3 Summary

The three business questions provide an initial overview of extreme rainfall frequency, monthly rainfall patterns, and total rainfall across the 17 representative locations.

The results highlight Baguio City and San Fernando, La Union as locations with the highest number of project-defined extreme rainfall observations. August recorded the highest average daily rainfall across the dataset.

These findings are based on representative locations and the January–October 2026 reporting period. They should not be interpreted as complete measurements of rainfall across entire Philippine regions.

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

This project uses one representative geographic coordinate for each of the 17 Philippine administrative regions to simplify data collection and enable regional comparisons.

Because rainfall can vary significantly within a region, these representative locations should not be interpreted as fully representing rainfall conditions across the entire region.

The current processed dataset covers January 1, 2026 to October 31, 2026. This ten-month reporting period is insufficient to establish long-term historical climate patterns or fully characterize seasonal rainfall variability.

The planned 2006–2025 historical analysis is not currently included in the processed dataset.

The project also analyzes rainfall data only. Flood occurrence is influenced by many other factors, including:

- Topography
- River systems
- Drainage infrastructure
- Land use
- Soil conditions
- Tidal conditions
- Other environmental and geographic factors

The 50 mm/day extreme rainfall threshold is a project-defined analytical threshold and is not presented as an official PAGASA classification.

Therefore, the results should be interpreted as indicators of historical rainfall patterns rather than direct measurements or predictions of flood risk.

## 13. Project Structure

```text
BahaPredict/
│
├── data/
│   ├── raw/
│   │   ├── Original API response JSON files
│   │   └── Metadata files
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
├── notebooks/
│   ├── m4_initial_insights.ipynb
│   └── m5_rainfall_distribution.ipynb
│
├── output/
│   ├── analysis/
│   │   ├── high_extreme_rainfall_by_location.csv
│   │   ├── monthly_stakeholder_kpis.csv
│   │   ├── rainfall_category_by_location.csv
│   │   ├── rainfall_descriptive_statistics.csv
│   │   └── stakeholder_rainfall_kpis.csv
│   │
│   └── figures/
│       ├── 01_extreme_rainfall_days.png
│       ├── 02_average_rainfall_by_month.png
│       ├── 03_total_rainfall_by_location.png
│       ├── 04_rainfall_distribution_by_location.png
│       ├── 05_mean_vs_median_rainfall.png
│       ├── 06_rainfall_category_composition.png
│       ├── 07_monthly_total_rainfall.png
│       └── 08_monthly_extreme_rainfall.png
│
├── dashboard/
├── requirements.txt
├── .gitignore
└── README.md
```

## 14. How to Run Pipeline

### 1. Clone the Repository
```bash
 git clone https://github.com/MCabs28/dep-data-engineering-mark-cabael.git
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
```

For macOS/Linux:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Data Ingestion Script

```bash
python scripts/ingest.py
```

This retrieves historical daily rainfall data from Open-Meteo for all 17 representative locations.

### 5. Transform the Raw Data

```bash
python scripts/transform.py
```

This processes the raw API responses, validates the rainfall records, and generates:

```text
data/processed/rainfall_clean.csv
```

### 6. Run the M3 Business Queries

```bash
python scripts/run_queries.py
```

This executes the three SQL business questions using DuckDB.

### 7. Run the M4 and M5 Analysis Notebooks

Launch Jupyter Notebook or JupyterLab:

```bash
jupyter notebook
```

Open the following notebooks:

- `notebooks/m4_initial_insights.ipynb`
- `notebooks/m5_rainfall_distribution.ipynb`

Run the notebook cells to reproduce the visualizations, descriptive statistics, rainfall segmentation, stakeholder KPIs, and analysis outputs.

### Expected Dataset

After a successful transformation, the processed dataset should contain:

- 17 representative locations
- 304 daily observations per location
- 5,168 total observations
- Reporting period: January 1, 2026 – October 31, 2026

The generated CSV analysis files are saved in `output/analysis/`, while visualization images are saved in `output/figures/`.


### 15. Run the Complete Pipeline

To execute the complete data pipeline in sequence, run:

```bash
python scripts/run_pipeline.py
```

This script runs the following steps:

1. Ingest rainfall data from the Open-Meteo API.
2. Transform and validate the raw rainfall data.
3. Execute the SQL business questions.



## 16. Repository Status

The BahaPredict project has completed the initial data engineering pipeline, exploratory analysis, and stakeholder-focused rainfall analysis milestones.

### Completed Milestones

**M1 — Project Planning**
- Defined the research question and project objectives.
- Identified target stakeholders and their information needs.
- Established the initial project scope.

**M2 — Data Source and Requirements**
- Selected Open-Meteo Historical Weather API as the primary data source.
- Identified 17 representative locations across the Philippine administrative regions.
- Defined the required dataset fields and data dictionary.

**M3 — Data Ingestion, Transformation, and SQL Analysis**
- Implemented automated rainfall data ingestion using Python.
- Stored raw API responses and retrieval metadata.
- Created a cleaned dataset containing 5,168 observations.
- Validated missing values, negative rainfall values, duplicate observations, and date coverage.
- Developed three SQL business questions using DuckDB.

**M4 — Initial Data Analysis and Visualization**
- Explored extreme rainfall frequency across representative locations.
- Analyzed monthly average rainfall patterns.
- Compared total rainfall across locations.
- Generated three initial visualizations and documented key findings.

**M5 — Rainfall Distribution and Stakeholder Analysis**
- **M5.1:** Calculated descriptive statistics and analyzed rainfall distributions.
- **M5.2:** Segmented rainfall observations into project-defined rainfall categories.
- **M5.3:** Developed location-level and monthly stakeholder KPIs.
- **M5.4:** Prepared a stakeholder brief summarizing findings, operational implications, recommendations, and limitations.

### Current Dataset Status

- Reporting period: January 1 – October 31, 2026
- Representative locations: 17
- Observations per location: 304
- Total observations: 5,168
- Missing precipitation values: 0
- Duplicate observations: 0
- Extreme rainfall observations (>=50 mm): 54

### Project Direction

The project follows a descriptive and stakeholder-focused analytical approach rather than developing a predictive machine learning model.
This approach is appropriate for the current dataset because its temporal coverage and geographic representation are limited.

