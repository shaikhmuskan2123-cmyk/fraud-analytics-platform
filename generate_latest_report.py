from database.db import (
    get_latest_transaction
)

from services.report_generator import (
    generate_transaction_report
)

record = get_latest_transaction()

if record:

    report = generate_transaction_report(
        transaction_id=record[0],
        amount=record[1],
        time=record[2],
        transactions_today=record[3],
        is_foreign=record[4],
        is_high_risk_country=record[5],
        prediction=record[6],
        risk_score=record[7],
        risk_level=record[8],
        recommendation="Automatically generated report"
    )

    print(report)

else:

    print("No transactions found")