import pandas as pd

df = pd.read_csv("cleaned_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

print("Columns 👇")
print(df.columns)

# Find price columns
price_cols = [col for col in df.columns if "Price on" in col]

# Find arrival columns
arrival_cols = [col for col in df.columns if "Arrival on" in col]

# Melt price
price_df = df.melt(
    id_vars=["Commodity"],
    value_vars=price_cols,
    var_name="Date",
    value_name="Price"
)

# Melt arrival
arrival_df = df.melt(
    id_vars=["Commodity"],
    value_vars=arrival_cols,
    var_name="Date",
    value_name="Arrival"
)

# Clean dates
price_df["Date"] = price_df["Date"].str.replace("Price on ", "")
arrival_df["Date"] = arrival_df["Date"].str.replace("Arrival on ", "")

# Merge both
df_final = pd.merge(price_df, arrival_df, on=["Commodity", "Date"])

# Convert date
df_final["Date"] = pd.to_datetime(df_final["Date"], errors='coerce')

# Drop missing
df_final = df_final.dropna()

# Save
df_final.to_csv("final_dataset.csv", index=False)

print("✅ Final dataset ready!")
print(df_final.head())