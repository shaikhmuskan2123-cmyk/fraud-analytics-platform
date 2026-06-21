from database.db import *

print("Transactions:", get_total_transactions())
print("Frauds:", get_total_frauds())
print("Average Risk:", get_average_risk())