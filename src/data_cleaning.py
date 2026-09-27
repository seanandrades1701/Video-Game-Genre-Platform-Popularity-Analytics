import pandas as pd
from pathlib import Path

# ============================================================
# VIDEO GAME SALES DATA CLEANING
# ============================================================

print("=" * 70)
print("VIDEO GAME SALES DATA CLEANING")
print("=" * 70)

# ------------------------------------------------------------
# 1. Define project paths
# ------------------------------------------------------------

project_root = Path(__file__).resolve().parent.parent

input_path = project_root / "dataset" / "vgsales.csv"
output_path = project_root / "dataset" / "vgsales_cleaned.csv"


# ------------------------------------------------------------
# 2. Load dataset
# ------------------------------------------------------------

print("\nLoading dataset...")

df = pd.read_csv(input_path)

print("Dataset loaded successfully.")


# ------------------------------------------------------------
# 3. Display original dataset information
# ------------------------------------------------------------

print("\nOriginal Dataset Shape:")
print(df.shape)

print("\nOriginal Missing Values:")
print(df.isnull().sum())

print("\nOriginal Duplicate Records:")
print(df.duplicated().sum())


# ------------------------------------------------------------
# 4. Remove duplicate records
# ------------------------------------------------------------

df = df.drop_duplicates()

print("\nDuplicate records removed.")


# ------------------------------------------------------------
# 5. Remove records with missing Year
# ------------------------------------------------------------

before_year = len(df)

df = df.dropna(subset=["Year"])

removed_year = before_year - len(df)

print(f"Records removed due to missing Year: {removed_year}")


# ------------------------------------------------------------
# 6. Remove records with missing Publisher
# ------------------------------------------------------------

before_publisher = len(df)

df = df.dropna(subset=["Publisher"])

removed_publisher = before_publisher - len(df)

print(f"Records removed due to missing Publisher: {removed_publisher}")


# ------------------------------------------------------------
# 7. Convert Year to integer
# ------------------------------------------------------------

df["Year"] = df["Year"].astype(int)

print("\nYear column converted to integer.")


# ------------------------------------------------------------
# 8. Check sales columns
# ------------------------------------------------------------

sales_columns = [
    "NA_Sales",
    "EU_Sales",
    "JP_Sales",
    "Other_Sales",
    "Global_Sales"
]

print("\nChecking sales values...")

for column in sales_columns:
    invalid_count = (df[column] < 0).sum()
    print(f"{column}: {invalid_count} invalid negative values")


# ------------------------------------------------------------
# 9. Remove invalid negative sales records
# ------------------------------------------------------------

for column in sales_columns:
    df = df[df[column] >= 0]


# ------------------------------------------------------------
# 10. Reset index
# ------------------------------------------------------------

df = df.reset_index(drop=True)


# ------------------------------------------------------------
# 11. Save cleaned dataset
# ------------------------------------------------------------

df.to_csv(output_path, index=False)


# ------------------------------------------------------------
# 12. Final results
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DATA CLEANING COMPLETED")
print("=" * 70)

print("\nOriginal Dataset Shape:")
print("(16598, 11)")

print("\nCleaned Dataset Shape:")
print(df.shape)

print("\nRemaining Missing Values:")
print(df.isnull().sum())

print("\nRemaining Duplicate Records:")
print(df.duplicated().sum())

print("\nCleaned Dataset Saved To:")
print(output_path)

print("\nFirst 5 Cleaned Records:")
print(df.head())

print("\n" + "=" * 70)
