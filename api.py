from flask import Flask, request, jsonify

from services.predictor import predict_transaction

from database.db import (
    create_tables,
    save_transaction
)

app = Flask(__name__)

# Initialize Database
create_tables()


@app.route("/")
def home():
    return jsonify({
        "message": "Fraud Analytics API Running"
    })


@app.route("/predict", methods=["POST"])
def predict():

    try:

        data = request.get_json()

        amount = float(data["amount"])
        time = int(data["time"])
        transactions_today = int(
            data["transactions_today"]
        )

        is_foreign = int(
            data["is_foreign"]
        )

        is_high_risk_country = int(
            data["is_high_risk_country"]
        )

        result = predict_transaction(
            amount,
            time,
            transactions_today,
            is_foreign,
            is_high_risk_country
        )

        save_transaction(
            amount,
            time,
            transactions_today,
            is_foreign,
            is_high_risk_country,
            result["prediction"],
            result["risk_score"],
            result["risk_level"]
        )

        return jsonify({
            "status": "success",
            "prediction": result["prediction"],
            "risk_score": result["risk_score"],
            "risk_level": result["risk_level"],
            "recommendation": result["recommendation"]
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )