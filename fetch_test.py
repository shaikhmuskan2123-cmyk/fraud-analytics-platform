from database.db import *

rows = get_all_transactions()

for row in rows:
    print(row)