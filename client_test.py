import requests

url = "http://127.0.0.1:5000/predict"

payload = {
    "amount": 18000,
    "time": 3,
    "transactions_today": 9,
    "is_foreign": 1,
    "is_high_risk_country": 1
}

response = requests.post(
    url,
    json=payload
)

print(response.json())