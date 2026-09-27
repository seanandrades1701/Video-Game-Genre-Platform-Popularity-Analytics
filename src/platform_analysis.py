import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME PLATFORM POPULARITY ANALYSIS
# ============================================================

print("=" * 70)
print("VIDEO GAME PLATFORM POPULARITY ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"
output_path = project_root / "results" / "platform_analysis.csv"

# Create results directory if needed
output_path.parent.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("\nLoading transformed dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")
print(f"Total records: {len(df)}")


# ------------------------------------------------------------
# 3. Platform analysis
# ------------------------------------------------------------

platform_analysis = (
    df.groupby("Platform")
    .agg(
        Number_of_Games=("Name", "count"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Average_Global_Sales=("Global_Sales", "mean"),
        Maximum_Global_Sales=("Global_Sales", "max")
    )
    .reset_index()
)


# ------------------------------------------------------------
# 4. Sort by total global sales
# ------------------------------------------------------------

platform_analysis = platform_analysis.sort_values(
    by="Total_Global_Sales",
    ascending=False
)


# ------------------------------------------------------------
# 5. Round numerical values
# ------------------------------------------------------------

platform_analysis["Total_Global_Sales"] = (
    platform_analysis["Total_Global_Sales"].round(2)
)

platform_analysis["Average_Global_Sales"] = (
    platform_analysis["Average_Global_Sales"].round(2)
)

platform_analysis["Maximum_Global_Sales"] = (
    platform_analysis["Maximum_Global_Sales"].round(2)
)


# ------------------------------------------------------------
# 6. Save results
# ------------------------------------------------------------

platform_analysis.to_csv(output_path, index=False)


# ------------------------------------------------------------
# 7. Display complete results
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("PLATFORM ANALYSIS RESULTS")
print("=" * 70)

print("\n")
print(platform_analysis.to_string(index=False))


# ------------------------------------------------------------
# 8. Top 10 platforms
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 10 PLATFORMS BY GLOBAL SALES")
print("=" * 70)

top_10 = platform_analysis.head(10)

print(
    top_10[
        [
            "Platform",
            "Number_of_Games",
            "Total_Global_Sales",
            "Average_Global_Sales"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 9. Summary
# ------------------------------------------------------------

top_platform = platform_analysis.iloc[0]

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    f"\nHighest total global sales platform: "
    f"{top_platform['Platform']}"
)

print(
    f"Total global sales: "
    f"{top_platform['Total_Global_Sales']} million"
)

print(
    f"Number of games: "
    f"{int(top_platform['Number_of_Games'])}"
)

print(
    f"Average sales per game: "
    f"{top_platform['Average_Global_Sales']} million"
)

print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 70)
print("PLATFORM ANALYSIS COMPLETED")
print("=" * 70)