import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import joblib

# Load final dataset
df = pd.read_csv("../final_dataset.csv")

print("Preview 👇")
print(df.head())

# Convert Date → features
df["Date"] = pd.to_datetime(df["Date"])
df["Day"] = df["Date"].dt.day
df["Month"] = df["Date"].dt.month

# Encode Commodity
le = LabelEncoder()
df["Commodity"] = le.fit_transform(df["Commodity"])

# Features & Target
X = df[["Commodity", "Day", "Month", "Arrival"]]
y = df["Price"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=150)
model.fit(X_train, y_train)

# Accuracy (rough idea)
score = model.score(X_test, y_test)
print(f"Model Accuracy: {score:.2f}")

# Save model
joblib.dump(model, "price_model.pkl")
joblib.dump(le, "commodity_encoder.pkl")

print("✅ Model trained and saved!")