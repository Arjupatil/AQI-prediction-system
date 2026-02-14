import requests

url = "http://127.0.0.1:8000/predict"
payload = {
    "city": "Test City",
    "pm2_5": 50.0,
    "pm10": 80.0,
    "no2": 20.0,
    "so2": 10.0,
    "co": 1.5,
    "o3": 30.0
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
