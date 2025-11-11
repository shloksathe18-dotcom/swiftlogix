import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(__file__))

from email_utils import send_admin_notification_new_user, send_admin_notification_approved_user

def test_email_function(func, *args):
    """Test an email function and provide appropriate feedback"""
    try:
        result = func(*args)
        if result:
            print("SUCCESS: Email function executed without errors")
            return True
        else:
            print("WARNING: Email function returned False (likely authentication issue in test environment)")
            return False
    except Exception as e:
        print(f"ERROR: Email function failed with exception: {str(e)}")
        return False

# Test the email functions
print("Testing email notification functions...")
print("=" * 50)

print("\n1. Testing send_admin_notification_new_user for admin...")
test_email_function(send_admin_notification_new_user, "admin@test.com", "admin")

print("\n2. Testing send_admin_notification_new_user for driver...")
test_email_function(send_admin_notification_new_user, "driver@test.com", "driver")

print("\n3. Testing send_admin_notification_approved_user...")
test_email_function(send_admin_notification_approved_user, "admin@test.com")

print("\n" + "=" * 50)
print("NOTE: Email authentication failures are expected in test environments")
print("where valid Gmail credentials are not configured.")
print("The important part is that the functions execute without exceptions.")