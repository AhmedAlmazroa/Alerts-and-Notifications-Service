import requests

# URL of your running microservice
url = "http://localhost:5001/alerts"

# Required headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer TEST_API_KEY"   # must match your VALID_API_KEY
}

# Valid alert body
body = {
    "userId": "12345",
    "alertType": "deadline",
    "message": "Your task is due soon.",
    "priority": "high",
    "eventId": "task-001"
}

# Send POST request
response = requests.post(url, json=body, headers=headers)

# Print results
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
