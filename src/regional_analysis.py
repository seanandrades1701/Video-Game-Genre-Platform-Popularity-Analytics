import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME REGIONAL SALES ANALYSIS
# ============================================================

print("=" * 70)
print("VIDEO GAME REGIONAL SALES ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"

regional_output = project_root / "results" / "regional_sales_analysis.csv"
genre_regional_output = project_root / "results" / "genre_regional_analysis.csv"

regional_output.parent.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("\nLoading transformed dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")
print(f"Total records: {len(df)}")


# ============================================================
# PART A — OVERALL REGIONAL SALES
# ============================================================

print("\n" + "=" * 70)
print("OVERALL REGIONAL SALES")
print("=" * 70)

regional_sales = pd.DataFrame({
    "Region": [
        "North America",
        "Europe",
        "Japan",
        "Other"
    ],
    "Total_Sales": [
        df["NA_Sales"].sum(),
        df["EU_Sales"].sum(),
        df["JP_Sales"].sum(),
        df["Other_Sales"].sum()
    ]
})

# Round values
regional_sales["Total_Sales"] = regional_sales["Total_Sales"].round(2)

# Calculate percentage
total_sales = regional_sales["Total_Sales"].sum()

regional_sales["Sales_Percentage"] = (
    regional_sales["Total_Sales"] / total_sales * 100
).round(2)

# Sort
regional_sales = regional_sales.sort_values(
    by="Total_Sales",
    ascending=False
)

print("\n")
print(regional_sales.to_string(index=False))


# ------------------------------------------------------------
# Save overall regional analysis
# ------------------------------------------------------------

regional_sales.to_csv(
    regional_output,
    index=False
)


# ============================================================
# PART B — GENRE BY REGION
# ============================================================

print("\n" + "=" * 70)
print("GENRE-WISE REGIONAL SALES")
print("=" * 70)

genre_regional = (
    df.groupby("Genre")
    .agg(
        North_America=("NA_Sales", "sum"),
        Europe=("EU_Sales", "sum"),
        Japan=("JP_Sales", "sum"),
        Other=("Other_Sales", "sum")
    )
    .reset_index()
)

# Round values
numeric_columns = [
    "North_America",
    "Europe",
    "Japan",
    "Other"
]

genre_regional[numeric_columns] = (
    genre_regional[numeric_columns].round(2)
)

print("\n")
print(genre_regional.to_string(index=False))


# ------------------------------------------------------------
# Save genre regional analysis
# ------------------------------------------------------------

genre_regional.to_csv(
    genre_regional_output,
    index=False
)


# ============================================================
# PART C — HIGHEST GENRE IN EACH REGION
# ============================================================

print("\n" + "=" * 70)
print("HIGHEST-SELLING GENRE BY REGION")
print("=" * 70)

regions = {
    "North America": "North_America",
    "Europe": "Europe",
    "Japan": "Japan",
    "Other": "Other"
}

for region_name, column_name in regions.items():

    highest_genre = genre_regional.loc[
        genre_regional[column_name].idxmax()
    ]

    print(
        f"\n{region_name}: "
        f"{highest_genre['Genre']} "
        f"({highest_genre[column_name]:.2f} million)"
    )


# ============================================================
# PART D — SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

highest_region = regional_sales.iloc[0]

print(
    f"\nRegion with highest total sales: "
    f"{highest_region['Region']}"
)

print(
    f"Total sales: "
    f"{highest_region['Total_Sales']} million"
)

print(
    f"Sales contribution: "
    f"{highest_region['Sales_Percentage']}%"
)

print("\nResults saved to:")

print(regional_output)
print(genre_regional_output)

print("\n" + "=" * 70)
print("REGIONAL ANALYSIS COMPLETED")
print("=" * 70)