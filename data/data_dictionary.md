# BahaPredict Data Dictionary

This data dictionary describes the fields contained in the weather dataset retrieved from the Open-Meteo Historical Weather API.

## Weather Dataset

| Field                           | Data Type     | Description                                                                                                                              |
| ------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `latitude`                      | Float         | Latitude of the location returned by the Open-Meteo API.                                                                                 |
| `longitude`                     | Float         | Longitude of the location returned by the Open-Meteo API.                                                                                |
| `generationtime_ms`             | Float         | Time required by the API to generate the response, measured in milliseconds.                                                             |
| `utc_offset_seconds`            | Integer       | UTC offset of the requested timezone in seconds.                                                                                         |
| `timezone`                      | String        | Timezone used for the returned weather data.                                                                                             |
| `timezone_abbreviation`         | String        | Abbreviated timezone name.                                                                                                               |
| `elevation`                     | Float         | Elevation of the location in meters above sea level.                                                                                     |
| `daily_units`                   | Object        | Contains the units and date format used by the daily weather fields.                                                                     |
| `daily`                         | Object        | Contains the daily weather observations.                                                                                                 |
| `daily_units.time`              | String        | Format of the dates returned in the `daily.time` field.                                                                                  |
| `daily_units.precipitation_sum` | String        | Unit of measurement for daily precipitation. The value is `mm`.                                                                          |
| `daily.time`                    | Array[String] | List of dates for each daily weather observation in `YYYY-MM-DD` format.                                                                 |
| `daily.precipitation_sum`       | Array[Float]  | Total precipitation for each day, measured in millimeters (mm). Each value corresponds to the date at the same position in `daily.time`. |

## Data Source

* **Source:** Open-Meteo Historical Weather API
* **Format:** JSON
* **Weather variable:** `precipitation_sum`
* **Unit:** millimeters (mm)
* **Current geographic scope:** Calamba City, CALABARZON
* **Current date range:** January 1, 2026 – June 30, 2026

## Notes

* The API response is stored in `data/` without modification.
* `daily.time` and `daily.precipitation_sum` are positionally related. For example, `daily.time[0]` corresponds to `daily.precipitation_sum[0]`.
* The current ingestion implementation retrieves rainfall data for the CALABARZON representative location.
* The dataset may be expanded to additional Philippine regions and longer historical periods in future ingestion runs.
