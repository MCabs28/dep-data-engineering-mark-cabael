"""
Generate stakeholder reports and visualizations for BahaPredict.
"""

import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DATA_FILE = os.path.join(BASE_DIR, "data", "processed", "rainfall_clean.csv")

ANALYSIS_DIR = os.path.join(BASE_DIR, "output", "analysis")
FIGURE_DIR = os.path.join(BASE_DIR, "output", "figures")
EXTREME_RAINFALL_THRESHOLD = 50.0


# --------------------------------------------------
# Load processed dataset
# --------------------------------------------------


def load_data():
    """Load and validate the processed rainfall dataset."""

    if not os.path.exists(PROCESSED_DATA_FILE):
        raise FileNotFoundError(f"Processed dataset not found: {PROCESSED_DATA_FILE}")

    df = pd.read_csv(PROCESSED_DATA_FILE)

    required_columns = ["date", "region", "location", "precipitation_mm", "is_extreme"]

    missing_columns = [
        column for column in required_columns if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    df["date"] = pd.to_datetime(df["date"])
    df["precipitation_mm"] = pd.to_numeric(df["precipitation_mm"], errors="coerce")

    if df["precipitation_mm"].isna().any():
        raise ValueError("Dataset contains missing rainfall values.")

    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    os.makedirs(FIGURE_DIR, exist_ok=True)

    print("Dataset loaded successfully.")
    print(f"Total observations: {len(df)}")
    print(f"Total regions: {df['region'].nunique()}")
    print(f"Date range: {df['date'].min().date()} " f"to {df['date'].max().date()}")

    return df


def generate_location_kpis(df):
    """Generate rainfall KPIs for each representative location."""

    location_kpis = (
        df.groupby(["region", "location"])
        .agg(
            total_rainfall_mm=("precipitation_mm", "sum"),
            mean_daily_rainfall_mm=("precipitation_mm", "mean"),
            extreme_rainfall_days=("is_extreme", "sum"),
            maximum_daily_rainfall_mm=("precipitation_mm", "max"),
            rainfall_std_dev_mm=("precipitation_mm", "std"),
            observation_count=("precipitation_mm", "count"),
        )
        .reset_index()
    )

    location_kpis = location_kpis.sort_values(by="total_rainfall_mm", ascending=False)

    output_file = os.path.join(ANALYSIS_DIR, "stakeholder_rainfall_kpis.csv")

    location_kpis.to_csv(output_file, index=False)

    print("\nLocation-level KPIs generated successfully.")
    print(f"Locations analyzed: {len(location_kpis)}")
    print(f"Total rainfall: {location_kpis['total_rainfall_mm'].sum():.1f} mm")
    print(
        f"Total extreme rainfall days: "
        f"{location_kpis['extreme_rainfall_days'].sum()}"
    )
    print(f"Saved to: {output_file}")

    return location_kpis


def classify_rainfall(df):
    """Classify daily rainfall using project-defined thresholds."""

    conditions = [
        df["precipitation_mm"].eq(0),
        df["precipitation_mm"].gt(0) & df["precipitation_mm"].le(2.5),
        df["precipitation_mm"].gt(2.5) & df["precipitation_mm"].le(7.5),
        df["precipitation_mm"].gt(7.5)
        & df["precipitation_mm"].lt(EXTREME_RAINFALL_THRESHOLD),
        df["precipitation_mm"].ge(EXTREME_RAINFALL_THRESHOLD),
    ]

    labels = ["No rainfall", "Low", "Moderate", "High", "Extreme"]

    df["rainfall_category"] = np.select(conditions, labels, default="Unclassified")

    category_counts = df["rainfall_category"].value_counts()

    print("\nRainfall categories generated successfully.")
    print(category_counts.to_string())

    if (df["rainfall_category"] == "Unclassified").any():
        raise ValueError("Unclassified rainfall observations detected.")

    expected_extreme = df["precipitation_mm"].ge(EXTREME_RAINFALL_THRESHOLD)

    if not df["is_extreme"].eq(expected_extreme).all():
        raise ValueError("is_extreme values do not match the rainfall threshold.")

    return df


def generate_monthly_kpis(df):
    """Generate monthly rainfall KPIs."""

    df["month"] = df["date"].dt.to_period("M").astype(str)

    monthly_kpis = (
        df.groupby("month")
        .agg(
            total_rainfall_mm=("precipitation_mm", "sum"),
            mean_daily_rainfall_mm=("precipitation_mm", "mean"),
            extreme_rainfall_observations=("is_extreme", "sum"),
            high_extreme_observations=(
                "rainfall_category",
                lambda x: x.isin(["High", "Extreme"]).sum(),
            ),
            observation_count=("precipitation_mm", "count"),
        )
        .reset_index()
    )

    output_file = os.path.join(ANALYSIS_DIR, "monthly_stakeholder_kpis.csv")

    monthly_kpis.to_csv(output_file, index=False)

    print("\nMonthly stakeholder KPIs generated successfully.")
    print(monthly_kpis.to_string(index=False))
    print(f"\nSaved to: {output_file}")

    return monthly_kpis


def generate_descriptive_statistics(df):
    """Generate descriptive rainfall statistics by location."""

    descriptive_stats = (
        df.groupby(["region", "location"])["precipitation_mm"]
        .agg(
            mean="mean",
            median="median",
            standard_deviation="std",
            minimum="min",
            maximum="max",
            observation_count="count",
        )
        .reset_index()
    )

    descriptive_stats = descriptive_stats.sort_values(by="mean", ascending=False)

    output_file = os.path.join(ANALYSIS_DIR, "rainfall_descriptive_statistics.csv")

    descriptive_stats.to_csv(output_file, index=False)

    print("\nDescriptive statistics generated successfully.")
    print(f"Locations analyzed: {len(descriptive_stats)}")
    print(descriptive_stats.head(5).to_string(index=False))
    print(f"\nSaved to: {output_file}")

    return descriptive_stats


def generate_category_summaries(df):
    """Generate rainfall category summaries by location."""

    category_summary = df.pivot_table(
        index=["region", "location"],
        columns="rainfall_category",
        values="precipitation_mm",
        aggfunc="count",
        fill_value=0,
    ).reset_index()

    category_columns = ["No rainfall", "Low", "Moderate", "High", "Extreme"]

    for column in category_columns:
        if column not in category_summary.columns:
            category_summary[column] = 0

    category_summary = category_summary[["region", "location"] + category_columns]

    category_summary["total_observations"] = category_summary[category_columns].sum(
        axis=1
    )

    category_file = os.path.join(ANALYSIS_DIR, "rainfall_category_by_location.csv")

    category_summary.to_csv(category_file, index=False)

    high_extreme_summary = category_summary[
        ["region", "location", "High", "Extreme"]
    ].copy()

    high_extreme_summary["high_extreme_total"] = (
        high_extreme_summary["High"] + high_extreme_summary["Extreme"]
    )

    high_extreme_summary = high_extreme_summary.sort_values(
        by="high_extreme_total", ascending=False
    )

    high_extreme_file = os.path.join(
        ANALYSIS_DIR, "high_extreme_rainfall_by_location.csv"
    )

    high_extreme_summary.to_csv(high_extreme_file, index=False)

    print("\nRainfall category summaries generated successfully.")
    print(f"Locations analyzed: {len(category_summary)}")

    print("\nHigh and Extreme rainfall by location:")
    print(high_extreme_summary.head(5).to_string(index=False))

    print(f"\nSaved to: {category_file}")
    print(f"Saved to: {high_extreme_file}")

    return category_summary, high_extreme_summary


def generate_distribution_chart(df):
    """Generate rainfall distribution boxplot by location."""

    plt.figure(figsize=(16, 8))

    df.boxplot(column="precipitation_mm", by="location", rot=90, grid=False)

    plt.title("Daily Rainfall Distribution by Location")
    plt.suptitle("")
    plt.xlabel("Representative Location")
    plt.ylabel("Daily Rainfall (mm)")
    plt.tight_layout()

    output_file = os.path.join(FIGURE_DIR, "04_rainfall_distribution_by_location.png")

    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    plt.close()

    print("\nRainfall distribution chart generated.")
    print(f"Saved to: {output_file}")


def generate_mean_median_chart(descriptive_stats):
    """Compare mean and median rainfall by location."""

    chart_data = descriptive_stats.sort_values(by="mean", ascending=True)

    plt.figure(figsize=(14, 8))

    positions = np.arange(len(chart_data))

    plt.barh(positions - 0.2, chart_data["mean"], height=0.4, label="Mean")

    plt.barh(positions + 0.2, chart_data["median"], height=0.4, label="Median")

    plt.yticks(positions, chart_data["location"])

    plt.title("Mean vs. Median Daily Rainfall by Location")
    plt.xlabel("Daily Rainfall (mm)")
    plt.ylabel("Representative Location")
    plt.legend()
    plt.tight_layout()

    output_file = os.path.join(FIGURE_DIR, "05_mean_vs_median_rainfall.png")

    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    plt.close()

    print("\nMean vs. median rainfall chart generated.")
    print(f"Saved to: {output_file}")


def generate_category_chart(df):
    """Generate rainfall category composition chart."""

    category_order = ["No rainfall", "Low", "Moderate", "High", "Extreme"]

    category_counts = (
        df["rainfall_category"].value_counts().reindex(category_order, fill_value=0)
    )

    plt.figure(figsize=(10, 6))

    plt.bar(category_counts.index, category_counts.values)

    plt.title("Rainfall Category Distribution")
    plt.xlabel("Rainfall Category")
    plt.ylabel("Number of Observations")
    plt.xticks(rotation=20)
    plt.tight_layout()

    output_file = os.path.join(FIGURE_DIR, "06_rainfall_category_composition.png")

    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    plt.close()

    print("\nRainfall category composition chart generated.")
    print(f"Saved to: {output_file}")


def generate_monthly_rainfall_chart(monthly_kpis):
    """Generate monthly total rainfall chart."""

    plt.figure(figsize=(12, 6))

    plt.bar(monthly_kpis["month"], monthly_kpis["total_rainfall_mm"])

    plt.title("Total Monthly Rainfall Across 17 Locations")
    plt.xlabel("Month")
    plt.ylabel("Total Rainfall (mm)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_file = os.path.join(FIGURE_DIR, "07_monthly_total_rainfall.png")

    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    plt.close()

    print("\nMonthly total rainfall chart generated.")
    print(f"Saved to: {output_file}")


def generate_monthly_extreme_chart(monthly_kpis):
    """Generate monthly extreme rainfall observations chart."""

    plt.figure(figsize=(12, 6))

    plt.bar(monthly_kpis["month"], monthly_kpis["extreme_rainfall_observations"])

    plt.title("Monthly Extreme Rainfall Observations")
    plt.xlabel("Month")
    plt.ylabel("Number of Extreme Rainfall Observations")
    plt.xticks(rotation=45)
    plt.tight_layout()

    output_file = os.path.join(FIGURE_DIR, "08_monthly_extreme_rainfall.png")

    plt.savefig(output_file, dpi=300, bbox_inches="tight")

    plt.close()

    print("\nMonthly extreme rainfall chart generated.")
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    df = load_data()
    location_kpis = generate_location_kpis(df)
    df = classify_rainfall(df)
    monthly_kpis = generate_monthly_kpis(df)
    descriptive_stats = generate_descriptive_statistics(df)

    category_summary, high_extreme_summary = generate_category_summaries(df)
    generate_distribution_chart(df)
    generate_mean_median_chart(descriptive_stats)
    generate_category_chart(df)
    generate_monthly_rainfall_chart(monthly_kpis)
    generate_monthly_extreme_chart(monthly_kpis)
