import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME GENRE × PLATFORM ANALYSIS
# ============================================================

print("=" * 70)
print("VIDEO GAME GENRE × PLATFORM ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"

detail_output = (
    project_root / "results" / "genre_platform_analysis.csv"
)

matrix_output = (
    project_root / "results" / "genre_platform_matrix.csv"
)

detail_output.parent.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("\nLoading transformed dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")
print(f"Total records: {len(df)}")


# ============================================================
# PART A — DETAILED GENRE × PLATFORM ANALYSIS
# ============================================================

print("\n" + "=" * 70)
print("GENRE × PLATFORM ANALYSIS")
print("=" * 70)

genre_platform = (
    df.groupby(["Genre", "Platform"])
    .agg(
        Number_of_Games=("Name", "count"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Average_Global_Sales=("Global_Sales", "mean")
    )
    .reset_index()
)


# ------------------------------------------------------------
# Sort by total global sales
# ------------------------------------------------------------

genre_platform = genre_platform.sort_values(
    by="Total_Global_Sales",
    ascending=False
)


# ------------------------------------------------------------
# Round values
# ------------------------------------------------------------

genre_platform["Total_Global_Sales"] = (
    genre_platform["Total_Global_Sales"].round(2)
)

genre_platform["Average_Global_Sales"] = (
    genre_platform["Average_Global_Sales"].round(2)
)


# ------------------------------------------------------------
# Save detailed results
# ------------------------------------------------------------

genre_platform.to_csv(
    detail_output,
    index=False
)


# ------------------------------------------------------------
# Display top 20 combinations
# ------------------------------------------------------------

print("\nTOP 20 GENRE × PLATFORM COMBINATIONS")
print("-" * 70)

print(
    genre_platform.head(20).to_string(index=False)
)


# ============================================================
# PART B — CREATE MATRIX FOR HEATMAP
# ============================================================

print("\n" + "=" * 70)
print("CREATING GENRE × PLATFORM SALES MATRIX")
print("=" * 70)

genre_platform_matrix = pd.pivot_table(
    df,
    values="Global_Sales",
    index="Genre",
    columns="Platform",
    aggfunc="sum",
    fill_value=0
)


# ------------------------------------------------------------
# Round matrix values
# ------------------------------------------------------------

genre_platform_matrix = genre_platform_matrix.round(2)


# ------------------------------------------------------------
# Save matrix
# ------------------------------------------------------------

genre_platform_matrix.to_csv(
    matrix_output
)


# ------------------------------------------------------------
# Display matrix
# ------------------------------------------------------------

print("\nGenre × Platform Matrix:")
print(genre_platform_matrix)


# ============================================================
# PART C — HIGHEST COMBINATION
# ============================================================

highest_combination = genre_platform.iloc[0]


print("\n" + "=" * 70)
print("HIGHEST-SELLING GENRE × PLATFORM COMBINATION")
print("=" * 70)

print(
    f"\nGenre: {highest_combination['Genre']}"
)

print(
    f"Platform: {highest_combination['Platform']}"
)

print(
    f"Number of Games: "
    f"{int(highest_combination['Number_of_Games'])}"
)

print(
    f"Total Global Sales: "
    f"{highest_combination['Total_Global_Sales']} million"
)

print(
    f"Average Global Sales: "
    f"{highest_combination['Average_Global_Sales']} million"
)


# ============================================================
# PART D — SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print("\nDetailed analysis saved to:")
print(detail_output)

print("\nHeatmap matrix saved to:")
print(matrix_output)

print("\n" + "=" * 70)
print("GENRE × PLATFORM ANALYSIS COMPLETED")
print("=" * 70)