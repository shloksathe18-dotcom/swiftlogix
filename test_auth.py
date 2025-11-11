import requests
import json

# Test registration
print("Testing registration...")
reg_data = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "role": "customer",
    "phone": "1234567890"
}

try:
    response = requests.post('http://127.0.0.1:5000/api/auth/register', 
                             json=reg_data,
                             headers={'Content-Type': 'application/json'})
    print(f"Registration status code: {response.status_code}")
    print(f"Registration response: {response.json()}")
except Exception as e:
    print(f"Registration error: {e}")

print("\n" + "="*50 + "\n")

# Test login
print("Testing login...")
login_data = {
    "email": "test@example.com",
    "password": "password123"
}

try:
    response = requests.post('http://127.0.0.1:5000/api/auth/login', 
                             json=login_data,
                             headers={'Content-Type': 'application/json'})
    print(f"Login status code: {response.status_code}")
    print(f"Login response: {response.json()}")
except Exception as e:
    print(f"Login error: {e}")