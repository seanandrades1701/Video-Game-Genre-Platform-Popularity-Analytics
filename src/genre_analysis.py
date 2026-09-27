import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME GENRE POPULARITY ANALYSIS
# ============================================================

print("=" * 70)
print("VIDEO GAME GENRE POPULARITY ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"
output_path = project_root / "results" / "genre_analysis.csv"


# ------------------------------------------------------------
# 2. Create results directory if it doesn't exist
# ------------------------------------------------------------

output_path.parent.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 3. Load dataset
# ------------------------------------------------------------

print("\nLoading transformed dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")

print(f"Total records: {len(df)}")


# ------------------------------------------------------------
# 4. Genre analysis
# ------------------------------------------------------------

genre_analysis = (
    df.groupby("Genre")
    .agg(
        Number_of_Games=("Name", "count"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Average_Global_Sales=("Global_Sales", "mean"),
        Maximum_Global_Sales=("Global_Sales", "max")
    )
    .reset_index()
)


# ------------------------------------------------------------
# 5. Sort by total global sales
# ------------------------------------------------------------

genre_analysis = genre_analysis.sort_values(
    by="Total_Global_Sales",
    ascending=False
)


# ------------------------------------------------------------
# 6. Round numerical values
# ------------------------------------------------------------

genre_analysis["Total_Global_Sales"] = (
    genre_analysis["Total_Global_Sales"].round(2)
)

genre_analysis["Average_Global_Sales"] = (
    genre_analysis["Average_Global_Sales"].round(2)
)

genre_analysis["Maximum_Global_Sales"] = (
    genre_analysis["Maximum_Global_Sales"].round(2)
)


# ------------------------------------------------------------
# 7. Save results
# ------------------------------------------------------------

genre_analysis.to_csv(output_path, index=False)


# ------------------------------------------------------------
# 8. Display results
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("GENRE ANALYSIS RESULTS")
print("=" * 70)

print("\n")
print(genre_analysis.to_string(index=False))


# ------------------------------------------------------------
# 9. Summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

highest_sales_genre = genre_analysis.iloc[0]

print(
    f"\nHighest total global sales genre: "
    f"{highest_sales_genre['Genre']}"
)

print(
    f"Total global sales: "
    f"{highest_sales_genre['Total_Global_Sales']} million"
)

print(
    f"Number of games: "
    f"{int(highest_sales_genre['Number_of_Games'])}"
)

print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 70)
print("GENRE ANALYSIS COMPLETED")
print("=" * 70)
