import pandas as pd

# -------- LOAD DATA --------
df = pd.read_csv("Transformed_TouristDestinations.csv")

# -------- RELATIVE LOCATION (origin, destination, repeat visitatin)--------
origin_col = "home_address:_region"
repeat_col = "have_you_visited_this_tourist_destination_before"
dest_cols = [c for c in df.columns if "tourist_destination_do_you_prefer" in c.lower()]

def rel_loc(freq):
    """Compute frequency table, quartiles, deciles, and selected percentiles."""
    freq = freq.sort_values(ascending=False)
    cf = freq.cumsum()
    n = freq.sum()
    percent = (freq / n * 100).round(2)
    cum_percent = (cf / n * 100).round(2)
    
    table = pd.DataFrame({"f": freq, "cf": cf, "Percent": percent, "Cum %": cum_percent})
    
    get_cat = lambda p: cf[cf >= p].index[0] if any(cf >= p) else None
    
    quartiles = {"Q1_cat": get_cat(0.25*n), "Q2_cat": get_cat(0.5*n), "Q3_cat": get_cat(0.75*n)}
    deciles = {f"D{i} ({i*10}%)": get_cat(i*0.1*n) for i in range(1,10)}
    percentiles = {f"P{i}": get_cat(i*0.01*n) for i in [5,10,90,95]}
    
    return table, quartiles, deciles, percentiles

# -------- COMPUTE TABLES --------
origin_table, origin_q, origin_d, origin_p = rel_loc(df[origin_col].value_counts())
repeat_table, repeat_q, repeat_d, repeat_p = rel_loc(df[repeat_col].value_counts())

dest_freq = df[dest_cols].sum()
dest_freq.index = dest_freq.index.str.replace("what_specific_phillippine_tourist_destination_do_you_prefer_", "", regex=False).str.replace("_", " ").str.title()
dest_table, dest_q, dest_d, dest_p = rel_loc(dest_freq)

print("\n--- ORIGIN ---")
print(origin_table)
print(f"\n25% of respondents are from: {origin_q['Q1_cat']}")
print(f"50% (Median) are from:       {origin_q['Q2_cat']}")
print(f"75% of respondents are from: {origin_q['Q3_cat']}")

print("\n--- REPEAT VISIT ---")
print(repeat_table)
print(f"\n25% of respondents: {repeat_q['Q1_cat']}")
print(f"50% (Median):       {repeat_q['Q2_cat']}")
print(f"75% of respondents: {repeat_q['Q3_cat']}")

print("\n--- DESTINATIONS ---")
print(dest_table)
print(f"\n25% of preferences: {dest_q['Q1_cat']}")
print(f"50% (Median):       {dest_q['Q2_cat']}")
print(f"75% of preferences: {dest_q['Q3_cat']}")
