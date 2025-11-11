import requests
import json

# Test the base page to see if authentication UI works
print("Testing base page...")
try:
    response = requests.get('http://127.0.0.1:5000/')
    print(f"Base page status: {response.status_code}")
    
    # Check if the page contains the expected elements
    content = response.text
    if 'Login' in content and 'Register' in content:
        print("✓ Login and Register links are visible (expected for non-logged-in user)")
    else:
        print("✗ Login/Register links not found")
        
    if 'Welcome' in content:
        print("✗ Welcome message found (should not be visible for non-logged-in user)")
    else:
        print("✓ Welcome message correctly hidden for non-logged-in user")
        
except Exception as e:
    print(f"Error testing base page: {e}")

print("\n" + "="*50 + "\n")

# Test login
print("Testing login...")
login_data = {
    'email': 'shloksathe18@gmail.com',
    'password': 'shlok@2116'
}

try:
    response = requests.post('http://127.0.0.1:5000/api/auth/login', 
                             json=login_data, 
                             headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        result = response.json()
        token = result['token']
        user = result['user']
        print(f"✓ Login successful for {user['name']} ({user['role']})")
        
        # Test admin dashboard
        print("\nTesting admin dashboard...")
        headers = {'Authorization': f'Bearer {token}'}
        dashboard_response = requests.get('http://127.0.0.1:5000/admin', headers=headers)
        print(f"Admin dashboard status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            dashboard_content = dashboard_response.text
            if 'Logout' in dashboard_content:
                print("✓ Logout option is visible in admin dashboard")
            else:
                print("✗ Logout option not found in admin dashboard")
                
            if 'Login' in dashboard_content or 'Register' in dashboard_content:
                print("✗ Login/Register options still visible in admin dashboard")
            else:
                print("✓ Login/Register options correctly hidden in admin dashboard")
        else:
            print("✗ Failed to access admin dashboard")
    else:
        print(f"✗ Login failed with status code: {response.status_code}")
        print(response.json())
        
except Exception as e:
    print(f"Error during login test: {e}")