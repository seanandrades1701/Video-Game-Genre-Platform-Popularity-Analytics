import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME YEAR & DECADE TREND ANALYSIS
# ============================================================

print("=" * 70)
print("VIDEO GAME YEAR & DECADE TREND ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"

year_output = project_root / "results" / "year_analysis.csv"
decade_output = project_root / "results" / "decade_analysis.csv"

year_output.parent.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("\nLoading transformed dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")
print(f"Total records: {len(df)}")


# ============================================================
# PART A — YEAR-WISE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("YEAR-WISE ANALYSIS")
print("=" * 70)

year_analysis = (
    df.groupby("Year")
    .agg(
        Number_of_Games=("Name", "count"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Average_Global_Sales=("Global_Sales", "mean")
    )
    .reset_index()
)

year_analysis = year_analysis.sort_values("Year")

year_analysis["Total_Global_Sales"] = (
    year_analysis["Total_Global_Sales"].round(2)
)

year_analysis["Average_Global_Sales"] = (
    year_analysis["Average_Global_Sales"].round(2)
)

year_analysis.to_csv(year_output, index=False)

print("\nFirst 10 years:")
print(year_analysis.head(10).to_string(index=False))

print("\nLast 10 years:")
print(year_analysis.tail(10).to_string(index=False))


# ============================================================
# PART B — DECADE-WISE ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("DECADE-WISE ANALYSIS")
print("=" * 70)

decade_analysis = (
    df.groupby("Decade")
    .agg(
        Number_of_Games=("Name", "count"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Average_Global_Sales=("Global_Sales", "mean")
    )
    .reset_index()
)

decade_analysis = decade_analysis.sort_values("Decade")

decade_analysis["Total_Global_Sales"] = (
    decade_analysis["Total_Global_Sales"].round(2)
)

decade_analysis["Average_Global_Sales"] = (
    decade_analysis["Average_Global_Sales"].round(2)
)

decade_analysis.to_csv(decade_output, index=False)

print("\n")
print(decade_analysis.to_string(index=False))


# ============================================================
# PART C — HIGHEST SALES YEAR
# ============================================================

highest_sales_year = year_analysis.loc[
    year_analysis["Total_Global_Sales"].idxmax()
]


# ============================================================
# PART D — HIGHEST SALES DECADE
# ============================================================

highest_sales_decade = decade_analysis.loc[
    decade_analysis["Total_Global_Sales"].idxmax()
]


# ============================================================
# PART E — MOST ACTIVE YEAR
# ============================================================

most_games_year = year_analysis.loc[
    year_analysis["Number_of_Games"].idxmax()
]


# ============================================================
# PART F — MOST ACTIVE DECADE
# ============================================================

most_games_decade = decade_analysis.loc[
    decade_analysis["Number_of_Games"].idxmax()
]


# ============================================================
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    f"\nYear with highest total sales: "
    f"{int(highest_sales_year['Year'])}"
)

print(
    f"Total global sales: "
    f"{highest_sales_year['Total_Global_Sales']} million"
)

print(
    f"\nDecade with highest total sales: "
    f"{int(highest_sales_decade['Decade'])}s"
)

print(
    f"Total global sales: "
    f"{highest_sales_decade['Total_Global_Sales']} million"
)

print(
    f"\nYear with the most game releases: "
    f"{int(most_games_year['Year'])}"
)

print(
    f"Number of games: "
    f"{int(most_games_year['Number_of_Games'])}"
)

print(
    f"\nDecade with the most game releases: "
    f"{int(most_games_decade['Decade'])}s"
)

print(
    f"Number of games: "
    f"{int(most_games_decade['Number_of_Games'])}"
)

print("\nResults saved to:")
print(year_output)
print(decade_output)

print("\n" + "=" * 70)
print("YEAR & DECADE ANALYSIS COMPLETED")
print("=" * 70)