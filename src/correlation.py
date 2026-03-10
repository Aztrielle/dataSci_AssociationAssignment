import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Transformed_TouristDestinations.csv")

# ----- Correlation (Origin, Destination, Repeat Visitation)------

# One-hot encode Origin (Home Address Region)
region_dummy = pd.get_dummies(df["home_address:_region"])

# Extract and format Destination columns
dest_cols = [c for c in df.columns if "what_specific_phillippine_tourist_destination_do_you_prefer" in c.lower()]
df[dest_cols] = df[dest_cols].apply(pd.to_numeric, errors="coerce").fillna(0)

# Clean up destination names for better display
rename_dict = {
    c: c.replace("what_specific_phillippine_tourist_destination_do_you_prefer_", "").replace("_", " ").title()
    for c in dest_cols
}
df = df.rename(columns=rename_dict)
clean_dest_cols = list(rename_dict.values())

# Create a binary Series for Repeat Visit
repeat_yes = (df["have_you_visited_this_tourist_destination_before"].str.strip().str.lower() == 'yes').astype(int)
repeat_yes.name = "Repeat_Visit_Yes"

# --- Calculate Correlations ---
corr_origin_dest = region_dummy.apply(lambda x: df[clean_dest_cols].corrwith(x))
corr_dest_repeat = df[clean_dest_cols].corrwith(repeat_yes).rename("Repeat_Visit_Yes")

# --- Print Formatted Terminal Output ---
output_str = ""
for region in region_dummy.columns:
    output_str += f"{'Destination':<60} {region:<45} {'Repeat Visit (Yes)':<20}\n"
    output_str += "-" * 130 + "\n"
    for dest in clean_dest_cols:
        output_str += f"{dest:<60} {corr_origin_dest.loc[dest, region]:<45.6f} {corr_dest_repeat.loc[dest]:<20.6f}\n"
    output_str += "\n"
print(output_str)

# --- Plot the Heatmap ---
combined_corr = pd.concat([corr_origin_dest, corr_dest_repeat], axis=1)
plt.figure(figsize=(14, 10))
sns.heatmap(combined_corr, annot=True, fmt=".3f", cmap="viridis", center=0,
            vmin=-0.3, vmax=0.3, linewidths=0.5, cbar_kws={"label": "Pearson Correlation"})
plt.title("Correlation of Tourist Destinations with Origin Regions and Repeat Visits", fontsize=14, pad=15)
plt.ylabel("Tourist Destinations", fontsize=12)
plt.xlabel("Origin Regions & Repeat Visit", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Save the visualization
plt.savefig("Correlation_Heatmap (Origin, Destination, Repeat Visitation.png")
