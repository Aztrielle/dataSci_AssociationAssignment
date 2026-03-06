import pandas as pd

input_file = 'src\Copy of Team06-TouristDestinations.csv'
df = pd.read_csv(input_file)

semicolon_columns = []

for col in df.columns:
    if df[col].astype(str).str.contains(';').any():
        semicolon_columns.append(col)
        
print("Columns with multi-select values:")
print(semicolon_columns)

for col in semicolon_columns:
    dummies = df[col].str.get_dummies(sep=';')
    dummies = dummies.add_prefix(col + "_")
    df = pd.concat([df, dummies], axis=1)
    
df.drop(columns=semicolon_columns, inplace=True)

output_file = 'Transformed_TouristDestinations.csv'
df.to_csv(output_file, index=False)

print("\nProcessing complete.")
print("Encoded dataset saved as:", output_file)