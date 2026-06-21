from database.db import *

create_tables()

save_transaction(
    amount=15000,
    time=2,
    transactions_today=10,
    is_foreign=1,
    is_high_risk_country=1,
    prediction=1,
    risk_score=96.4,
    risk_level="CRITICAL"
)

print("Inserted Successfully")