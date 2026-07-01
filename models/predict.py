import joblib
import pandas as pd
import os

# Get current file directory
BASE_DIR = os.path.dirname(__file__)

# Load model + encoder
model = joblib.load(os.path.join(BASE_DIR, "price_model.pkl"))
le = joblib.load(os.path.join(BASE_DIR, "commodity_encoder.pkl"))

def predict_price(commodity, day, month, arrival):
    try:
        # Encode commodity
        commodity_encoded = le.transform([commodity])[0]

        # Create input
        input_data = pd.DataFrame([{
            "Commodity": commodity_encoded,
            "Day": day,
            "Month": month,
            "Arrival": arrival
        }])

        # Predict
        prediction = model.predict(input_data)

        return round(prediction[0], 2)

    except Exception as e:
        return f"Error: {str(e)}"


# 🔥 Test it
if __name__ == "__main__":
    result = predict_price("Maize", 30, 3, 3000)
    print("Predicted Price:", result)