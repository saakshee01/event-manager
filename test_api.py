import requests
import json

url = "http://127.0.0.1:5000/api/events"
data = {
    "name": "Test Event",
    "date": "2025-07-13",
    "desc": "Sample Description",
    "location": "Delhi",
    "budget": "5000",
    "completed": False,
    "expenses": [],
    "people": [],
    "rating": 0
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))
