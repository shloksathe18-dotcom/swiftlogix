import requests
import json

# Test the base page HTML content
print("Testing base page HTML content...")
try:
    response = requests.get('http://127.0.0.1:5000/')
    print(f"Base page status: {response.status_code}")
    
    # Check the actual HTML content
    content = response.text
    
    print("Checking for UI elements:")
    if 'id="userInfo"' in content:
        # Check if it's hidden or visible
        if 'style="display: none;"' in content and 'id="userInfo"' in content:
            print("  - User info section: Hidden (correct for non-logged-in user)")
        else:
            print("  - User info section: Visible (incorrect for non-logged-in user)")
    
    if 'id="loginLink"' in content:
        if 'style="display: none;"' in content and 'id="loginLink"' in content:
            print("  - Login link: Hidden (incorrect for non-logged-in user)")
        else:
            print("  - Login link: Visible (correct for non-logged-in user)")
            
    if 'id="registerLink"' in content:
        if 'style="display: none;"' in content and 'id="registerLink"' in content:
            print("  - Register link: Hidden (incorrect for non-logged-in user)")
        else:
            print("  - Register link: Visible (correct for non-logged-in user)")
            
    if 'id="logoutLink"' in content:
        if 'style="display: none;"' in content and 'id="logoutLink"' in content:
            print("  - Logout link: Hidden (correct for non-logged-in user)")
        else:
            print("  - Logout link: Visible (incorrect for non-logged-in user)")
            
    # Check alert messages
    if 'id="welcomeAlert"' in content:
        if 'style="display: none;"' in content and 'id="welcomeAlert"' in content:
            print("  - Welcome alert: Hidden (incorrect for non-logged-in user)")
        else:
            print("  - Welcome alert: Visible (correct for non-logged-in user)")
            
    if 'id="loggedInAlert"' in content:
        if 'style="display: none;"' in content and 'id="loggedInAlert"' in content:
            print("  - Logged-in alert: Hidden (correct for non-logged-in user)")
        else:
            print("  - Logged-in alert: Visible (incorrect for non-logged-in user)")
        
except Exception as e:
    print(f"Error testing base page: {e}")

print("\n" + "="*50 + "\n")

# Test with logged in user
print("Testing with logged in user...")
# First, login to get a token
login_data = {
    'email': 'shloksathe18@gmail.com',
    'password': 'shlok@2116'
}

try:
    login_response = requests.post('http://127.0.0.1:5000/api/auth/login', 
                                  json=login_data, 
                                  headers={'Content-Type': 'application/json'})
    
    if login_response.status_code == 200:
        result = login_response.json()
        token = result['token']
        
        # Test admin dashboard HTML content
        print("Testing admin dashboard HTML content...")
        headers = {'Authorization': f'Bearer {token}'}
        dashboard_response = requests.get('http://127.0.0.1:5000/admin', headers=headers)
        print(f"Admin dashboard status: {dashboard_response.status_code}")
        
        if dashboard_response.status_code == 200:
            dashboard_content = dashboard_response.text
            
            print("Checking dashboard UI elements:")
            if 'id="userInfo"' in dashboard_content:
                if 'style="display: none;"' in dashboard_content and 'id="userInfo"' in dashboard_content:
                    print("  - User info section: Hidden (incorrect for logged-in user)")
                else:
                    print("  - User info section: Visible (correct for logged-in user)")
            
            if 'id="loginLink"' in dashboard_content:
                if 'style="display: none;"' in dashboard_content and 'id="loginLink"' in dashboard_content:
                    print("  - Login link: Hidden (correct for logged-in user)")
                else:
                    print("  - Login link: Visible (incorrect for logged-in user)")
                    
            if 'id="registerLink"' in dashboard_content:
                if 'style="display: none;"' in dashboard_content and 'id="registerLink"' in dashboard_content:
                    print("  - Register link: Hidden (correct for logged-in user)")
                else:
                    print("  - Register link: Visible (incorrect for logged-in user)")
                    
            if 'id="logoutLink"' in dashboard_content:
                if 'style="display: none;"' in dashboard_content and 'id="logoutLink"' in dashboard_content:
                    print("  - Logout link: Hidden (incorrect for logged-in user)")
                else:
                    print("  - Logout link: Visible (correct for logged-in user)")
                    
            # Check alert messages
            if 'id="welcomeAlert"' in dashboard_content:
                if 'style="display: none;"' in dashboard_content and 'id="welcomeAlert"' in dashboard_content:
                    print("  - Welcome alert: Hidden (correct for logged-in user)")
                else:
                    print("  - Welcome alert: Visible (incorrect for logged-in user)")
                    
            if 'id="loggedInAlert"' in dashboard_content:
                if 'style="display: none;"' in dashboard_content and 'id="loggedInAlert"' in dashboard_content:
                    print("  - Logged-in alert: Hidden (incorrect for logged-in user)")
                else:
                    print("  - Logged-in alert: Visible (correct for logged-in user)")
        else:
            print("Failed to access admin dashboard")
    else:
        print(f"Login failed with status code: {login_response.status_code}")
        
except Exception as e:
    print(f"Error during logged-in user test: {e}")