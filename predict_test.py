from services.predictor import predict_transaction

print("=== Normal Transaction ===")

normal = predict_transaction(
    amount=500,
    time=14,
    transactions_today=1,
    is_foreign=0,
    is_high_risk_country=0
)

print(normal)

print("\n=== Fraud Transaction ===")

fraud = predict_transaction(
    amount=25000,
    time=2,
    transactions_today=12,
    is_foreign=1,
    is_high_risk_country=1
)

print(fraud)