import requests
import time
import sqlite3
import os

# Base URL for the Flask app
BASE_URL = "http://localhost:5000"

def clear_database():
    """Clear the database before running tests"""
    db_path = 'logistics.db'
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users')
        conn.commit()
        conn.close()
        print("Database cleared.")
    else:
        print("Database does not exist, will be created on first request.")

def test_register_admin():
    """Test registering an admin user"""
    print("Testing admin registration...")
    response = requests.post(f"{BASE_URL}/register", json={
        "email": "admin@test.com",
        "role": "admin"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_register_driver():
    """Test registering a driver user"""
    print("Testing driver registration...")
    response = requests.post(f"{BASE_URL}/register", json={
        "email": "driver@test.com",
        "role": "driver"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_register_customer():
    """Test registering a customer user"""
    print("Testing customer registration...")
    response = requests.post(f"{BASE_URL}/register", json={
        "email": "customer@test.com",
        "role": "customer"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login_approved_user():
    """Test logging in an approved user"""
    print("Testing login for approved user (driver)...")
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "driver@test.com"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_login_unapproved_user():
    """Test logging in an unapproved user"""
    print("Testing login for unapproved user (admin)...")
    response = requests.post(f"{BASE_URL}/login", json={
        "email": "admin@test.com"
    })
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    print("Testing Logistics App API")
    print("=" * 30)
    
    # Clear database before running tests
    clear_database()
    
    # Test registrations
    test_register_admin()
    time.sleep(1)  # Small delay between requests
    
    test_register_driver()
    time.sleep(1)
    
    test_register_customer()
    time.sleep(1)
    
    # Test logins
    test_login_approved_user()
    time.sleep(1)
    
    test_login_unapproved_user()
    
    print("Test completed. Check email for notifications.")
    print("To approve the admin user, visit: http://localhost:5000/approve?email=admin@test.com")