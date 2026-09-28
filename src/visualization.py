import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

print("=" * 70)
print("VIDEO GAME ANALYTICS - VISUALIZATION")
print("=" * 70)

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

dataset_path = project_root / "dataset" / "vgsales_transformed.csv"
results_path = project_root / "results"
visualization_path = project_root / "visualizations"

visualization_path.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(dataset_path)

print(f"\nDataset loaded: {len(df)} records")

# ---------------------------------------------------------
# 1. GLOBAL SALES BY GENRE
# ---------------------------------------------------------

genre = (
    df.groupby("Genre")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
genre.plot(kind="bar")

plt.title("Global Sales by Genre")
plt.xlabel("Genre")
plt.ylabel("Global Sales (Millions)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    visualization_path / "global_sales_by_genre.png",
    dpi=300
)
plt.close()

print("✓ Genre visualization created")


# ---------------------------------------------------------
# 2. TOP 10 PLATFORMS
# ---------------------------------------------------------

platform = (
    df.groupby("Platform")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
platform.plot(kind="bar")

plt.title("Top 10 Platforms by Global Sales")
plt.xlabel("Platform")
plt.ylabel("Global Sales (Millions)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    visualization_path / "top_10_platforms.png",
    dpi=300
)
plt.close()

print("✓ Platform visualization created")


# ---------------------------------------------------------
# 3. TOP 10 PUBLISHERS
# ---------------------------------------------------------

publisher = (
    df.groupby("Publisher")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(11, 6))
publisher.plot(kind="bar")

plt.title("Top 10 Publishers by Global Sales")
plt.xlabel("Publisher")
plt.ylabel("Global Sales (Millions)")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig(
    visualization_path / "top_10_publishers.png",
    dpi=300
)
plt.close()

print("✓ Publisher visualization created")


# ---------------------------------------------------------
# 4. REGIONAL SALES
# ---------------------------------------------------------

regional_sales = {
    "North America": df["NA_Sales"].sum(),
    "Europe": df["EU_Sales"].sum(),
    "Japan": df["JP_Sales"].sum(),
    "Other": df["Other_Sales"].sum()
}

regional = pd.Series(regional_sales)

plt.figure(figsize=(8, 6))
regional.plot(kind="bar")

plt.title("Regional Video Game Sales")
plt.xlabel("Region")
plt.ylabel("Sales (Millions)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    visualization_path / "regional_sales.png",
    dpi=300
)
plt.close()

print("✓ Regional visualization created")

plt.title("Regional Video Game Sales")
plt.xlabel("Region")
plt.ylabel("Sales (Millions)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    visualization_path / "regional_sales.png",
    dpi=300
)
plt.close()

print("✓ Regional visualization created")


# ---------------------------------------------------------
# 5. YEARLY SALES TREND
# ---------------------------------------------------------

year_sales = (
    df.groupby("Year")["Global_Sales"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(12, 6))
plt.plot(
    year_sales.index,
    year_sales.values,
    marker="o",
    linewidth=1.5
)

plt.title("Global Video Game Sales by Year")
plt.xlabel("Year")
plt.ylabel("Global Sales (Millions)")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    visualization_path / "yearly_sales_trend.png",
    dpi=300
)
plt.close()

print("✓ Yearly trend visualization created")


# ---------------------------------------------------------
# 6. DECADE SALES
# ---------------------------------------------------------

decade_sales = (
    df.groupby("Decade")["Global_Sales"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(9, 6))
decade_sales.plot(kind="bar")

plt.title("Global Video Game Sales by Decade")
plt.xlabel("Decade")
plt.ylabel("Global Sales (Millions)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(
    visualization_path / "decade_sales.png",
    dpi=300
)
plt.close()

print("✓ Decade visualization created")


# ---------------------------------------------------------
# 7. TOP 10 GAMES
# ---------------------------------------------------------

top_games = (
    df.groupby("Name")["Global_Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

plt.figure(figsize=(10, 7))
top_games.plot(kind="barh")

plt.title("Top 10 Video Games by Global Sales")
plt.xlabel("Global Sales (Millions)")
plt.ylabel("Game")

plt.tight_layout()

plt.savefig(
    visualization_path / "top_10_games.png",
    dpi=300
)
plt.close()

print("✓ Top games visualization created")


# ---------------------------------------------------------
# 8. GENRE × PLATFORM HEATMAP
# ---------------------------------------------------------

heatmap_data = pd.pivot_table(
    df,
    values="Global_Sales",
    index="Genre",
    columns="Platform",
    aggfunc="sum",
    fill_value=0
)

# Select top 15 platforms for readability
top_platforms = (
    df.groupby("Platform")["Global_Sales"]
    .sum()
    .nlargest(15)
    .index
)

heatmap_data = heatmap_data[top_platforms]

plt.figure(figsize=(15, 7))

sns.heatmap(
    heatmap_data,
    cmap="YlOrRd",
    linewidths=0.2
)

plt.title("Genre × Platform Global Sales")
plt.xlabel("Platform")
plt.ylabel("Genre")

plt.tight_layout()

plt.savefig(
    visualization_path / "genre_platform_heatmap.png",
    dpi=300
)
plt.close()

print("✓ Genre × Platform heatmap created")


# ---------------------------------------------------------
# 9. SALES CATEGORY DISTRIBUTION
# ---------------------------------------------------------

category = (
    df["Sales_Category"]
    .value_counts()
    .reindex(
        ["Low", "Medium", "High", "Very High"]
    )
)

plt.figure(figsize=(9, 6))
category.plot(kind="bar")

plt.title("Video Game Sales Category Distribution")
plt.xlabel("Sales Category")
plt.ylabel("Number of Games")
plt.xticks(rotation=0)

plt.tight_layout()

plt.savefig(
    visualization_path / "sales_category_distribution.png",
    dpi=300
)
plt.close()

print("✓ Sales category visualization created")


# ---------------------------------------------------------
# COMPLETION
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("VISUALIZATION COMPLETED")
print("=" * 70)

print("\nCharts saved in:")
print(visualization_path)

print("\nGenerated files:")

for file in sorted(visualization_path.glob("*.png")):
    print(" -", file.name)

print("=" * 70)