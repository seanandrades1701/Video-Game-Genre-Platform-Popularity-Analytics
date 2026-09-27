import pandas as pd
from pathlib import Path

# ============================================================
# TOP VIDEO GAMES SALES ANALYSIS
# ============================================================

print("=" * 70)
print("TOP 10 VIDEO GAMES BY GLOBAL SALES")
print("=" * 70)

# ------------------------------------------------------------
# 1. Project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"
output_path = project_root / "results" / "top_games_analysis.csv"

output_path.parent.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("\nLoading transformed dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")
print(f"Total records: {len(df)}")


# ------------------------------------------------------------
# 3. Sort by global sales
# ------------------------------------------------------------

top_games = df.sort_values(
    by="Global_Sales",
    ascending=False
).head(10)


# ------------------------------------------------------------
# 4. Select useful columns
# ------------------------------------------------------------

top_games = top_games[
    [
        "Rank",
        "Name",
        "Platform",
        "Year",
        "Genre",
        "Publisher",
        "NA_Sales",
        "EU_Sales",
        "JP_Sales",
        "Other_Sales",
        "Global_Sales"
    ]
]


# ------------------------------------------------------------
# 5. Save results
# ------------------------------------------------------------

top_games.to_csv(
    output_path,
    index=False
)


# ------------------------------------------------------------
# 6. Display results
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("TOP 10 GAMES")
print("=" * 70)

print("\n")
print(top_games.to_string(index=False))


# ------------------------------------------------------------
# 7. Summary
# ------------------------------------------------------------

top_game = top_games.iloc[0]

print("\n" + "=" * 70)
print("TOP GAME SUMMARY")
print("=" * 70)

print(f"\nGame: {top_game['Name']}")
print(f"Platform: {top_game['Platform']}")
print(f"Year: {int(top_game['Year'])}")
print(f"Genre: {top_game['Genre']}")
print(f"Publisher: {top_game['Publisher']}")
print(f"Global Sales: {top_game['Global_Sales']} million")

print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 70)
print("TOP GAMES ANALYSIS COMPLETED")
print("=" * 70)