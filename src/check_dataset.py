import pandas as pd

# Load dataset
df = pd.read_csv("../dataset/vgsales.csv")

# Display basic information
print("=" * 60)
print("VIDEO GAME SALES DATASET")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nDataset Information:")
print(df.info())