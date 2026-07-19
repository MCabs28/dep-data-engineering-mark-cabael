# DEP Data Engineering Cohort 1

## Author

**Mark Cabael**

# Milestone M1 Submission

## Project Title

**BahaPredict: Building an Automated Regional Weather Data Pipeline in the Philippines**

# 1. Research Question

**Which Philippine regions experience the highest frequency of extreme daily rainfall events, and during which months do localized flood risks historically peak?**

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

Many local government agencies still rely on scattered reports, social media updates, and manually downloaded weather datasets to assess flood risks. By automating the collection, cleaning, and analysis of historical rainfall data, this project aims to provide structured and reliable insights into where and when extreme rainfall events occur most frequently.

These insights can help stakeholders:

- Identify flood-prone regions more accurately.
- Prepare drainage systems and flood-control infrastructure before high-risk months.
- Improve disaster preparedness and emergency response planning.
- Support agricultural planning and crop protection strategies.
- Allocate public resources and infrastructure budgets more effectively.


# 4. Data Source & Ingestion

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

The ETL pipeline covers all **17 administrative regions of the Philippines**. Historical weather data will be retrieved using the latitude and longitude coordinates of each region's representative capital city.

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

The project analyzes approximately **20 years of historical rainfall data (2006–2026)** to provide statistically meaningful insights into long-term rainfall patterns and seasonal flood risks. The API request shown above is a sample request used to demonstrate data access.

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

The NASA POWER API serves as the project's backup data source. If the Open-Meteo API becomes unavailable or returns incomplete data, the ETL pipeline will retrieve historical precipitation data from NASA POWER using the same regional coordinates.


# Planned Ingestion Method

### Method

Automated HTTP GET requests using Python (`requests` library).

### Ingestion Strategy

- Load a coordinate mapping file containing representative locations for all 17 Philippine administrative regions.
- Iterate through each region and submit API requests using its latitude and longitude.
- Extract historical weather data in manageable yearly batches to reduce request failures and improve pipeline reliability.
- Store raw JSON responses in a dedicated landing zone before performing any transformations.
- Transform the raw data into structured tabular datasets for downstream analysis and loading into the target database.

# Repository Status

- Public repository created
- Research question defined
- Stakeholders identified
- Project rationale completed
- Primary data source documented
- Backup data source documented
- API access paths documented
- Geographic and temporal coverage documented
- Planned ingestion strategy defined
- README documentation completed