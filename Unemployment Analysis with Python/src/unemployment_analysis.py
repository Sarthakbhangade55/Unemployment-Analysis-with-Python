# ==============================================================
# OASIS INFOBYTE INTERNSHIP - TASK 2
# Unemployment Analysis with Python
# Author: Sarthak Bhangade
# ==============================================================

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")


# ==============================================================
# 1. PROJECT PATHS
# ==============================================================

DATA_PATH = "data/Unemployment in India.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================
# 2. LOAD DATASET
# ==============================================================

print("=" * 70)
print("UNEMPLOYMENT ANALYSIS WITH PYTHON")
print("=" * 70)

print("\nLoading dataset...")

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")


# ==============================================================
# 3. CLEAN COLUMN NAMES
# ==============================================================

df.columns = df.columns.str.strip()

print("\nColumn Names:")
print(df.columns.tolist())


# ==============================================================
# 4. BASIC DATA INSPECTION
# ==============================================================

print("\n" + "=" * 70)
print("DATASET INFORMATION")
print("=" * 70)

print(f"\nDataset Shape: {df.shape}")
print(f"Rows: {df.shape[0]}")
print(f"Columns: {df.shape[1]}")

print("\nFirst 5 Records:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())


# ==============================================================
# 5. DATA CLEANING
# ==============================================================

print("\n" + "=" * 70)
print("DATA CLEANING")
print("=" * 70)

# Remove extra spaces from text columns
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].str.strip()

# Convert Date column to datetime
df["Date"] = pd.to_datetime(
    df["Date"],
    format="%d-%m-%Y",
    errors="coerce"
)

# Convert numerical columns
numeric_columns = [
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove rows with missing important values
df.dropna(
    subset=[
        "Region",
        "Date",
        "Estimated Unemployment Rate (%)",
        "Estimated Employed",
        "Estimated Labour Participation Rate (%)"
    ],
    inplace=True
)

# Sort by date
df.sort_values("Date", inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)

print("\nData cleaning completed.")

print(f"Clean Dataset Shape: {df.shape}")


# ==============================================================
# 6. DESCRIPTIVE STATISTICS
# ==============================================================

print("\n" + "=" * 70)
print("DESCRIPTIVE STATISTICS")
print("=" * 70)

print(df.describe())


# ==============================================================
# 7. REGION-WISE AVERAGE UNEMPLOYMENT RATE
# ==============================================================

print("\n" + "=" * 70)
print("REGION-WISE AVERAGE UNEMPLOYMENT RATE")
print("=" * 70)

region_average = (
    df.groupby("Region")["Estimated Unemployment Rate (%)"]
    .mean()
    .sort_values(ascending=False)
)

print(region_average.round(2))


# Save region averages
region_average.to_csv(
    os.path.join(OUTPUT_DIR, "region_average_unemployment.csv")
)


# ==============================================================
# 8. MONTH-WISE UNEMPLOYMENT TREND
# ==============================================================

df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%B")

month_order = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

month_average = (
    df.groupby("Month_Name")["Estimated Unemployment Rate (%)"]
    .mean()
    .reindex(month_order)
)

print("\n" + "=" * 70)
print("MONTH-WISE AVERAGE UNEMPLOYMENT RATE")
print("=" * 70)

print(month_average.round(2))


# ==============================================================
# 9. MONTH-WISE BAR CHART
# ==============================================================

plt.figure(figsize=(12, 6))

sns.barplot(
    x=month_average.index,
    y=month_average.values
)

plt.title("Month-wise Average Unemployment Rate in India")
plt.xlabel("Month")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "01_month_wise_unemployment.png"),
    dpi=300
)

plt.close()


# ==============================================================
# OBSERVATION 1
# ==============================================================

highest_month = month_average.idxmax()
lowest_month = month_average.idxmin()

print("\nObservation:")
print(
    f"The highest average unemployment rate occurred in {highest_month} "
    f"({month_average.max():.2f}%), while the lowest occurred in "
    f"{lowest_month} ({month_average.min():.2f}%)."
)


# ==============================================================
# 10. TIME-SERIES ANALYSIS
#    AT LEAST 3 MAJOR STATES
# ==============================================================

major_states = [
    "Maharashtra",
    "Tamil Nadu",
    "West Bengal"
]

available_states = [
    state for state in major_states
    if state in df["Region"].unique()
]

plt.figure(figsize=(14, 7))

for state in available_states:

    state_data = (
        df[df["Region"] == state]
        .groupby("Date")["Estimated Unemployment Rate (%)"]
        .mean()
        .sort_index()
    )

    plt.plot(
        state_data.index,
        state_data.values,
        marker="o",
        linewidth=2,
        label=state
    )

plt.title(
    "Unemployment Rate Over Time - Major Indian States"
)

plt.xlabel("Date")
plt.ylabel("Unemployment Rate (%)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "02_state_time_series.png"),
    dpi=300
)

plt.close()


# ==============================================================
# OBSERVATION 2
# ==============================================================

print("\nObservation:")
print(
    "The time-series chart shows that unemployment rates changed "
    "considerably over time. The COVID-19 period produced a strong "
    "increase in unemployment in several regions."
)


# ==============================================================
# 11. TOP 10 STATES WITH HIGHEST AVERAGE UNEMPLOYMENT
# ==============================================================

top_10_states = region_average.head(10)

print("\n" + "=" * 70)
print("TOP 10 STATES WITH HIGHEST AVERAGE UNEMPLOYMENT")
print("=" * 70)

print(top_10_states.round(2))


# Bar chart
plt.figure(figsize=(12, 7))

sns.barplot(
    x=top_10_states.values,
    y=top_10_states.index
)

plt.title(
    "Top 10 States/Regions with Highest Average Unemployment Rate"
)

plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("State / Region")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "03_top_10_states.png"),
    dpi=300
)

plt.close()


# ==============================================================
# OBSERVATION 3
# ==============================================================

print("\nObservation:")
print(
    "The top-10 analysis highlights the states/regions with the "
    "highest average unemployment rates during the period covered "
    "by the dataset."
)


# ==============================================================
# 12. CORRELATION HEATMAP
# ==============================================================

correlation_columns = [
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)"
]

correlation_matrix = df[correlation_columns].corr()

print("\n" + "=" * 70)
print("CORRELATION MATRIX")
print("=" * 70)

print(correlation_matrix.round(3))


plt.figure(figsize=(9, 7))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title(
    "Correlation: Unemployment, Employment & Labour Participation"
)

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "04_correlation_heatmap.png"),
    dpi=300
)

plt.close()


# ==============================================================
# OBSERVATION 4
# ==============================================================

print("\nObservation:")
print(
    "The correlation heatmap shows the relationship between "
    "unemployment rate, estimated employment and labour "
    "participation rate. Correlation indicates association and "
    "does not by itself prove causation."
)


# ==============================================================
# 13. PRE-COVID VS POST-COVID ANALYSIS
# ==============================================================

# COVID impact period begins around March 2020.
# We compare:
# Pre-COVID  : Before March 2020
# Post-COVID : March 2020 onwards

covid_start = pd.Timestamp("2020-03-01")

df["COVID_Period"] = np.where(
    df["Date"] < covid_start,
    "Pre-COVID",
    "Post-COVID"
)

covid_comparison = (
    df.groupby("COVID_Period")[
        [
            "Estimated Unemployment Rate (%)",
            "Estimated Labour Participation Rate (%)",
            "Estimated Employed"
        ]
    ]
    .mean()
)

print("\n" + "=" * 70)
print("PRE-COVID VS POST-COVID COMPARISON")
print("=" * 70)

print(covid_comparison.round(2))


# Save comparison
covid_comparison.to_csv(
    os.path.join(OUTPUT_DIR, "covid_comparison.csv")
)


# ==============================================================
# 14. COVID COMPARISON BAR CHART
# ==============================================================

plt.figure(figsize=(10, 6))

covid_unemployment = covid_comparison[
    "Estimated Unemployment Rate (%)"
]

sns.barplot(
    x=covid_unemployment.index,
    y=covid_unemployment.values
)

plt.title("Average Unemployment Rate: Pre-COVID vs Post-COVID")
plt.xlabel("Period")
plt.ylabel("Average Unemployment Rate (%)")

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "05_pre_vs_post_covid.png"),
    dpi=300
)

plt.close()


# ==============================================================
# OBSERVATION 5
# ==============================================================

pre_covid_rate = covid_comparison.loc[
    "Pre-COVID",
    "Estimated Unemployment Rate (%)"
]

post_covid_rate = covid_comparison.loc[
    "Post-COVID",
    "Estimated Unemployment Rate (%)"
]

change = post_covid_rate - pre_covid_rate

print("\nCOVID-19 Observation:")

if change > 0:
    print(
        f"The average unemployment rate increased from "
        f"{pre_covid_rate:.2f}% before COVID-19 to "
        f"{post_covid_rate:.2f}% from March 2020 onward. "
        f"This represents an increase of approximately {change:.2f} "
        f"percentage points."
    )
else:
    print(
        f"The average unemployment rate changed from "
        f"{pre_covid_rate:.2f}% before COVID-19 to "
        f"{post_covid_rate:.2f}% from March 2020 onward."
    )


# ==============================================================
# 15. OVERALL TREND
# ==============================================================

overall_monthly = (
    df.groupby("Date")["Estimated Unemployment Rate (%)"]
    .mean()
    .sort_index()
)

plt.figure(figsize=(14, 7))

plt.plot(
    overall_monthly.index,
    overall_monthly.values,
    marker="o",
    linewidth=2
)

plt.axvline(
    covid_start,
    linestyle="--",
    linewidth=2,
    label="COVID-19 Period Begins"
)

plt.title("Overall Unemployment Rate Trend in India")
plt.xlabel("Date")
plt.ylabel("Average Unemployment Rate (%)")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "06_overall_unemployment_trend.png"),
    dpi=300
)

plt.close()


# ==============================================================
# 16. SAVE CLEANED DATA
# ==============================================================

df.to_csv(
    os.path.join(OUTPUT_DIR, "cleaned_unemployment_data.csv"),
    index=False
)


# ==============================================================
# 17. SAVE WRITTEN OBSERVATIONS
# ==============================================================

observations = f"""
UNEMPLOYMENT ANALYSIS - KEY OBSERVATIONS
=========================================

1. Dataset:
The dataset contains {df.shape[0]} cleaned records and
{df.shape[1]} columns.

2. Month-wise Trend:
The highest average unemployment rate occurred in {highest_month}
at approximately {month_average.max():.2f}%.
The lowest occurred in {lowest_month}
at approximately {month_average.min():.2f}%.

3. Regional Analysis:
The analysis identifies the states/regions with the highest
average unemployment rates during the study period.

4. Time-Series Analysis:
Unemployment rates varied considerably across states and over time.
The COVID-19 period shows a noticeable disruption in unemployment
patterns.

5. COVID-19 Impact:
Pre-COVID average unemployment rate: {pre_covid_rate:.2f}%
Post-COVID average unemployment rate: {post_covid_rate:.2f}%

Change: {change:.2f} percentage points.

6. Correlation:
The correlation heatmap shows relationships between unemployment,
employment and labour participation. Correlation should not be
interpreted as proof of causation.

7. Conclusion:
The analysis demonstrates clear temporal and regional differences
in unemployment across India. The COVID-19 period was associated
with substantial changes in unemployment patterns.
"""

with open(
    os.path.join(OUTPUT_DIR, "observations.txt"),
    "w",
    encoding="utf-8"
) as file:
    file.write(observations)


# ==============================================================
# 18. FINAL SUMMARY
# ==============================================================

print("\n" + "=" * 70)
print("PROJECT COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nGenerated output files:")

for file_name in sorted(os.listdir(OUTPUT_DIR)):
    print(f"  ✓ {file_name}")

print("\n" + "=" * 70)
print("TASK 2 - UNEMPLOYMENT ANALYSIS COMPLETED")
print("=" * 70)