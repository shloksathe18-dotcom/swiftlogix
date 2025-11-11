import requests
import json

# First, login to get the token
login_data = {
    'email': 'shloksathe18@gmail.com',
    'password': 'shlok@2116'
}

print("Logging in...")
response = requests.post('http://127.0.0.1:5000/api/auth/login', 
                         json=login_data, 
                         headers={'Content-Type': 'application/json'})

if response.status_code == 200:
    result = response.json()
    token = result['token']
    user = result['user']
    
    print(f"Login successful!")
    print(f"User: {user['name']} ({user['email']})")
    print(f"Role: {user['role']}")
    
    # Test accessing the admin panel
    print("\nTesting admin panel access...")
    headers = {'Authorization': f'Bearer {token}'}
    admin_response = requests.get('http://127.0.0.1:5000/admin', headers=headers)
    
    if admin_response.status_code == 200:
        print("Admin panel access: SUCCESS")
        print("Admin user can access the admin panel!")
    else:
        print(f"Admin panel access: FAILED (Status code: {admin_response.status_code})")
else:
    print(f"Login failed with status code: {response.status_code}")
    print(response.json())