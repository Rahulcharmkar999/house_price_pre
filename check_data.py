import pandas as pd

# Dataset load
data = pd.read_csv("Scraped_Data.csv")

print("Dataset Shape:")
print(data.shape)

print("\nColumns:")
print(data.columns)

print("\nFirst 5 Rows:")
print(data.head())

print("\nMissing Values:")
print(data.isnull().sum())