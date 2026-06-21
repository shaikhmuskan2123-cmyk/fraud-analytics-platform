import joblib
import pandas as pd

from services.risk_engine import (
    calculate_risk_level,
    get_recommendation
)

# ------------------------
# Load Model Once
# ------------------------

model = joblib.load(
    "models/fraud_model.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

# ------------------------
# Prediction Function
# ------------------------

def predict_transaction(
    amount,
    time,
    transactions_today,
    is_foreign,
    is_high_risk_country
):

    data = pd.DataFrame([{
        "amount": amount,
        "time": time,
        "transactions_today": transactions_today,
        "is_foreign": is_foreign,
        "is_high_risk_country": is_high_risk_country
    }])

    scaled_data = scaler.transform(data)

    prediction = model.predict(
        scaled_data
    )[0]

    probability = model.predict_proba(
        scaled_data
    )[0][1]

    risk_score = round(
        probability * 100,
        2
    )

    risk_level = calculate_risk_level(
        risk_score
    )

    recommendation = get_recommendation(
        risk_level
    )

    return {
        "prediction": int(prediction),
        "risk_score": risk_score,
        "risk_level": risk_level,
        "recommendation": recommendation
    }