import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME SALES CATEGORY ANALYSIS
# ============================================================

print("=" * 70)
print("VIDEO GAME SALES CATEGORY ANALYSIS")
print("=" * 70)

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_transformed.csv"
output_path = project_root / "results" / "sales_category_analysis.csv"

output_path.parent.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(input_path)

print("\nDataset loaded successfully.")
print(f"Total records: {len(df)}")


# ------------------------------------------------------------
# Sales category analysis
# ------------------------------------------------------------

sales_category = (
    df.groupby("Sales_Category")
    .agg(
        Number_of_Games=("Name", "count"),
        Total_Global_Sales=("Global_Sales", "sum"),
        Average_Global_Sales=("Global_Sales", "mean")
    )
    .reset_index()
)


# ------------------------------------------------------------
# Calculate percentage of games
# ------------------------------------------------------------

total_games = sales_category["Number_of_Games"].sum()

sales_category["Percentage_of_Games"] = (
    sales_category["Number_of_Games"] / total_games * 100
).round(2)


# ------------------------------------------------------------
# Sort categories logically
# ------------------------------------------------------------

category_order = ["Low", "Medium", "High", "Very High"]

sales_category["Sales_Category"] = pd.Categorical(
    sales_category["Sales_Category"],
    categories=category_order,
    ordered=True
)

sales_category = sales_category.sort_values("Sales_Category")


# Round values
sales_category["Total_Global_Sales"] = (
    sales_category["Total_Global_Sales"].round(2)
)

sales_category["Average_Global_Sales"] = (
    sales_category["Average_Global_Sales"].round(2)
)


# Save
sales_category.to_csv(output_path, index=False)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("SALES CATEGORY RESULTS")
print("=" * 70)

print(
    sales_category.to_string(index=False)
)


print("\nResults saved to:")
print(output_path)

print("\n" + "=" * 70)
print("SALES CATEGORY ANALYSIS COMPLETED")
print("=" * 70)