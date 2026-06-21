from services.report_generator import (
    generate_transaction_report
)

file = generate_transaction_report(
    transaction_id=1,
    amount=25000,
    time=2,
    transactions_today=12,
    is_foreign=1,
    is_high_risk_country=1,
    prediction="FRAUD",
    risk_score=96.4,
    risk_level="CRITICAL",
    recommendation="Immediate fraud investigation required."
)

print(file)