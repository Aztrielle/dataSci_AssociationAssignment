import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data & filter columns
df = pd.read_csv('Transformed_TouristDestinations.csv')

# ----- Variability (most important elements of the trip) -----
cols = [c for c in df.columns if "what_factors_are_most_important_when_planning_your_trip" in c.lower()]
f_df = df[cols]

# Calculate statistics directly into the DataFrame
stats_df = pd.DataFrame({
    'Factor': [c.split('options._')[-1].replace('_', ' ').title() for c in cols],
    'Count (Yes)': f_df.sum().values,
    'Count (No)': len(df) - f_df.sum().values,
    'Proportion (Mean)': f_df.mean().values,
    'Variance': f_df.var().values,
    'Standard Deviation': f_df.std().values
})

print("Variability of Trip Planning Factors (Sorted by Highest Variance):")
print(stats_df.sort_values('Variance', ascending=False)[['Factor', 'Proportion (Mean)', 'Variance', 'Standard Deviation']].to_string(index=False), "\n")

# Visualization
sp = stats_df.sort_values('Variance')
plt.figure(figsize=(9, 5.5))

plt.barh(sp['Factor'], sp['Count (Yes)'], color='#1f77b4', edgecolor='black', label='Selected (Yes)')
plt.barh(sp['Factor'], sp['Count (No)'], left=sp['Count (Yes)'], color='#d3d3d3', edgecolor='black', label='Not Selected (No)')

# Add Variance labels exactly on the split
bbox_props = dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.2', alpha=0.9)
for i, (c_yes, var) in enumerate(zip(sp['Count (Yes)'], sp['Variance'])):
    plt.text(c_yes, i, f'Var: {var:.3f}', va='center', ha='center', fontsize=9, fontweight='bold', bbox=bbox_props)

# Format and display
plt.title('Element Variability of Trip Planning Factors', fontsize=12, pad=12)
plt.xlabel('Number of Respondents', fontsize=10)
plt.ylabel('Trip Planning Factors (Elements)', fontsize=10)
plt.xlim(0, len(df))
plt.xticks(fontsize=9); plt.yticks(fontsize=9)
plt.grid(axis='x', linestyle='--', alpha=0.6)
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2, fontsize=9)

plt.tight_layout()
plt.show()
