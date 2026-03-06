import pandas as pd

# Load dataset
file_path = "Transformed_TouristDestinations.csv"
df = pd.read_csv(file_path)

print("\nCount of '1' values per column\n")

for col in df.columns:
    
    # Count how many times 1 appears in the column
    count_ones = (df[col] == 1).sum()
    print(f"{col}: {count_ones}")