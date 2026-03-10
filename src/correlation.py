import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import matplotlib.patches as mpatches

# Load dataset
df = pd.read_csv("Transformed_TouristDestinations.csv")

# ------ Corelation (Origin, Destination, Repeat visitation)

# Get destination columns and chosen destination
dest_cols = [c for c in df.columns if "tourist_destination_do_you_prefer" in c.lower()]
df[dest_cols] = df[dest_cols].apply(pd.to_numeric, errors="coerce").fillna(0)
df["Destination"] = df[dest_cols].idxmax(axis=1).str.replace(
    "what_specific_phillippine_tourist_destination_do_you_prefer_","", regex=False
)

# Variables
data = {
    "Origin": df["home_address:_region"],
    "Destination": df["Destination"],
    "Repeat Visit": df["have_you_visited_this_tourist_destination_before"]
}

# Cramer's V
def cramers_v(x, y):
    t = pd.crosstab(x, y)
    chi2 = chi2_contingency(t)[0]
    n = t.values.sum()
    r, k = t.shape
    return np.sqrt(chi2 / (n * (min(r-1, k-1))))
    
# Correlation matrix
labels = list(data)
matrix = pd.DataFrame([[1 if i==j else cramers_v(data[i], data[j]) 
                        for j in labels] for i in labels],
                        index=labels, columns=labels)
print(matrix)

# Heatmap
plt.figure(figsize=(6,5))
sns.heatmap(matrix, annot=True, cmap="coolwarm_r", vmin=0, vmax=1,
            cbar_kws={"label":"Correlation Strength"})
plt.title("Correlation Matrix of Origin, Destination, and Repeat Visit")
plt.tight_layout()
plt.show()
