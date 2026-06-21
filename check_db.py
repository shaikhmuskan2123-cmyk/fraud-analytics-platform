from database.db import get_all_transactions

rows = get_all_transactions()

for row in rows:
    print(row)