-- ============================================================
-- BahaPredict — M3 Business Questions
-- ============================================================
-- Dataset:
-- data/processed/rainfall_clean.csv
--
-- Analysis period:
-- January 1, 2026 – August 31, 2026
--
-- Extreme rainfall threshold:
-- 50 mm or more per day
-- ============================================================


-- ============================================================
-- Business Question 1
-- Which Philippine regions experienced the highest number
-- of extreme rainfall days?
-- ============================================================

SELECT
    region,
    location,
    SUM(
        CASE
            WHEN is_extreme = TRUE THEN 1
            ELSE 0
        END
    ) AS extreme_rainfall_days
FROM read_csv_auto('data/processed/rainfall_clean.csv')
GROUP BY
    region,
    location
ORDER BY
    extreme_rainfall_days DESC,
    region;


-- ============================================================
-- Business Question 2
-- Which months had the highest average daily rainfall
-- across the 17 Philippine regions?
-- ============================================================

SELECT
    EXTRACT(MONTH FROM CAST(date AS DATE)) AS month,
    ROUND(AVG(precipitation_mm), 2) AS average_rainfall_mm
FROM read_csv_auto('data/processed/rainfall_clean.csv')
WHERE precipitation_missing = FALSE
GROUP BY
    month
ORDER BY
    average_rainfall_mm DESC;


-- ============================================================
-- Business Question 3
-- Which Philippine regions recorded the highest total
-- rainfall during the analysis period?
-- ============================================================

SELECT
    region,
    location,
    ROUND(SUM(precipitation_mm), 2) AS total_rainfall_mm
FROM read_csv_auto('data/processed/rainfall_clean.csv')
WHERE precipitation_missing = FALSE
GROUP BY
    region,
    location
ORDER BY
    total_rainfall_mm DESC;