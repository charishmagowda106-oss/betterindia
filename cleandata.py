import pandas as pd

df = pd.read_csv("rawdata.csv", skiprows=2)

print("Preview 👇")
print(df.head())

# Remove unnamed columns
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

# Strip spaces from column names
df.columns = df.columns.str.strip()

print("Cleaned Columns 👇")
print(df.columns)

# Convert numeric columns safely
for col in df.columns:
    if "Price" in col or "Arrival" in col:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop missing rows
df = df.dropna()

# Save cleaned data
df.to_csv("cleaned_data.csv", index=False)

print("✅ Cleaned data saved!")