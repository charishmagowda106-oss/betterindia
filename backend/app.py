from flask import Flask, request, jsonify
from flask_cors import CORS

from predictor import predict_price, get_mandi_data, VALID_COMMODITIES

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "Smart Crop Selling Advisor API is running!"


@app.route('/commodities', methods=['GET'])
def commodities():
    return jsonify(VALID_COMMODITIES)


@app.route('/predict', methods=['GET'])
def predict():
    try:
        commodity = request.args.get("commodity")
        day = int(request.args.get("day"))
        month = int(request.args.get("month"))
        arrival = float(request.args.get("arrival"))

        result = predict_price(commodity, day, month, arrival)

        return jsonify({
            "commodity": commodity,
            "day": day,
            "month": month,
            "arrival": arrival,
            "predicted_price": round(result, 2)
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/mandis', methods=['GET'])
def mandis():
    try:
        commodity = request.args.get("commodity")
        transport = float(request.args.get("transport"))

        result = get_mandi_data(commodity, transport)

        return jsonify(result)

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)