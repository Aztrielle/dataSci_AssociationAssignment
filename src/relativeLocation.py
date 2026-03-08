import pandas as pd
import matplotlib.pyplot as plt

# -------- LOAD DATA --------
df = pd.read_csv("Transformed_TouristDestinations.csv")
origin_col = "Home Address: Region"
repeat_col = "Have you visited this tourist destination before?"
dest_cols = [c for c in df.columns if "tourist destination do you prefer" in c.lower()]

# -------- RELATIVE LOCATION FUNCTION --------
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
dest_freq.index = dest_freq.index.str.split("_", n=1).str[-1]  # clean names
dest_table, dest_q, dest_d, dest_p = rel_loc(dest_freq)

# -------- FUNCTION TO PLOT TABLE + QUARTILES AS IMAGE --------
def plot_summary(title, table, quartiles):
    fig, ax = plt.subplots(figsize=(12, len(table)*0.25 + 2))
    ax.axis('off')
    
    text = f"--- {title} ---\n\n{table.to_string()}\n\n" \
           f"25% : {quartiles['Q1_cat']}\n" \
           f"50% (Median) : {quartiles['Q2_cat']}\n" \
           f"75% : {quartiles['Q3_cat']}"
    
    ax.text(0, 1, text, va='top', family='monospace', fontsize=10)
    plt.tight_layout()
    plt.show()

# -------- PLOT RESULTS --------
plot_summary("ORIGIN", origin_table, origin_q)
plot_summary("REPEAT VISIT", repeat_table, repeat_q)
plot_summary("DESTINATIONS", dest_table, dest_q)