import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME SALES DATA TRANSFORMATION
# ============================================================

print("=" * 70)
print("VIDEO GAME SALES DATA TRANSFORMATION")
print("=" * 70)

# ------------------------------------------------------------
# 1. Define paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales_cleaned.csv"
output_path = project_root / "dataset" / "vgsales_transformed.csv"


# ------------------------------------------------------------
# 2. Load cleaned dataset
# ------------------------------------------------------------

print("\nLoading cleaned dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")

print("\nDataset Shape:")
print(df.shape)


# ------------------------------------------------------------
# 3. Create Decade column
# ------------------------------------------------------------

df["Decade"] = (df["Year"] // 10 * 10).astype(int)

print("\nDecade column created.")


# ------------------------------------------------------------
# 4. Create Sales Category
# ------------------------------------------------------------

def classify_sales(sales):

    if sales < 1:
        return "Low"

    elif sales < 5:
        return "Medium"

    elif sales < 10:
        return "High"

    else:
        return "Very High"


df["Sales_Category"] = df["Global_Sales"].apply(classify_sales)

print("Sales_Category column created.")


# ------------------------------------------------------------
# 5. Calculate total regional sales
# ------------------------------------------------------------

df["Regional_Total"] = (
    df["NA_Sales"]
    + df["EU_Sales"]
    + df["JP_Sales"]
    + df["Other_Sales"]
)

print("Regional_Total column created.")


# ------------------------------------------------------------
# 6. Calculate regional percentages
# ------------------------------------------------------------

df["NA_Percentage"] = (
    df["NA_Sales"] / df["Regional_Total"] * 100
)

df["EU_Percentage"] = (
    df["EU_Sales"] / df["Regional_Total"] * 100
)

df["JP_Percentage"] = (
    df["JP_Sales"] / df["Regional_Total"] * 100
)

df["Other_Percentage"] = (
    df["Other_Sales"] / df["Regional_Total"] * 100
)

print("Regional percentage columns created.")


# ------------------------------------------------------------
# 7. Save transformed dataset
# ------------------------------------------------------------

df.to_csv(output_path, index=False)

print("\nTransformed dataset saved to:")
print(output_path)


# ------------------------------------------------------------
# 8. Display results
# ------------------------------------------------------------

print("\nFinal Dataset Shape:")
print(df.shape)

print("\nFinal Columns:")
print(df.columns.tolist())

print("\nSales Category Distribution:")
print(df["Sales_Category"].value_counts())

print("\nDecade Distribution:")
print(df["Decade"].value_counts().sort_index())

print("\nFirst 5 Transformed Records:")
print(df.head())


print("\n" + "=" * 70)
print("DATA TRANSFORMATION COMPLETED")
print("=" * 70)