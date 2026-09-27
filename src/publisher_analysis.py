import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME PUBLISHER ANALYSIS
# ============================================================

print("=" * 70)
print("VIDEO GAME PUBLISHER ANALYSIS")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"
output_path = project_root / "results" / "publisher_analysis.csv"

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
# 3. Publisher analysis
# ------------------------------------------------------------

publisher_analysis = (
    df.groupby("Publisher")
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

publisher_analysis = publisher_analysis.sort_values(
    by="Total_Global_Sales",
    ascending=False
)


# ------------------------------------------------------------
# 5. Round numerical values
# ------------------------------------------------------------

publisher_analysis["Total_Global_Sales"] = (
    publisher_analysis["Total_Global_Sales"].round(2)
)

publisher_analysis["Average_Global_Sales"] = (
    publisher_analysis["Average_Global_Sales"].round(2)
)

publisher_analysis["Maximum_Global_Sales"] = (
    publisher_analysis["Maximum_Global_Sales"].round(2)
)


# ------------------------------------------------------------
# 6. Save complete results
# ------------------------------------------------------------

publisher_analysis.to_csv(output_path, index=False)


# ------------------------------------------------------------
# 7. Display top 20 publishers
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 20 PUBLISHERS BY GLOBAL SALES")
print("=" * 70)

print(
    publisher_analysis.head(20).to_string(index=False)
)


# ------------------------------------------------------------
# 8. Top 10 publishers
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 10 PUBLISHERS")
print("=" * 70)

top_10 = publisher_analysis.head(10)

print(
    top_10[
        [
            "Publisher",
            "Number_of_Games",
            "Total_Global_Sales",
            "Average_Global_Sales"
        ]
    ].to_string(index=False)
)


# ------------------------------------------------------------
# 9. Publisher with most games
# ------------------------------------------------------------

most_games_publisher = publisher_analysis.sort_values(
    by="Number_of_Games",
    ascending=False
).iloc[0]


# ------------------------------------------------------------
# 10. Publisher with highest total sales
# ------------------------------------------------------------

highest_sales_publisher = publisher_analysis.iloc[0]


# ------------------------------------------------------------
# 11. Summary
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

print(
    f"\nPublisher with highest total global sales: "
    f"{highest_sales_publisher['Publisher']}"
)

print(
    f"Total global sales: "
    f"{highest_sales_publisher['Total_Global_Sales']} million"
)

print(
    f"Number of games: "
    f"{int(highest_sales_publisher['Number_of_Games'])}"
)

print(
    f"\nPublisher with the most games: "
    f"{most_games_publisher['Publisher']}"
)

print(
    f"Number of games: "
    f"{int(most_games_publisher['Number_of_Games'])}"
)


print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 70)
print("PUBLISHER ANALYSIS COMPLETED")
print("=" * 70)