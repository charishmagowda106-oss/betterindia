import os
import pandas as pd
import joblib

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "data", "price_model.joblib")
DATA_PATH = os.path.join(BASE_DIR, "data", "final_dataset.csv")

_model = joblib.load(MODEL_PATH)
_data = pd.read_csv(DATA_PATH)

VALID_COMMODITIES = sorted(_data["Commodity"].unique().tolist())


def predict_price(commodity, day, month, arrival):
    """
    Predicts price using a linear regression trained on Commodity + Arrival.
    Note: day/month are accepted for API compatibility but the current
    dataset only spans 3 dates, so they aren't used as model features yet.
    Add more historical data to make date-based seasonality meaningful.
    """
    if commodity not in VALID_COMMODITIES:
        raise ValueError(
            f"Unknown commodity '{commodity}'. Valid options: {VALID_COMMODITIES}"
        )

    X = pd.DataFrame([{"Commodity": commodity, "Arrival": arrival}])
    pred = _model.predict(X)[0]
    return max(pred, 5)


def get_mandi_data(commodity, transport_cost):
    """
    Returns top mandi-like rows for a commodity, ranked by profit after
    transport cost. Current dataset has no real 'mandi' column, so each
    row (one per date) is treated as a market snapshot.
    """
    df = _data[_data["Commodity"] == commodity]

    if df.empty:
        raise ValueError(
            f"Unknown commodity '{commodity}'. Valid options: {VALID_COMMODITIES}"
        )

    results = []
    for _, row in df.iterrows():
        profit = row["Price"] - transport_cost
        results.append({
            "mandi": f"Market snapshot ({row['Date']})",
            "price": row["Price"],
            "arrival": row["Arrival"],
            "profit": round(profit, 2)
        })

    results = sorted(results, key=lambda x: x["profit"], reverse=True)
    return results[:3]