import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from flask import Flask
from flask_mail import Mail
from backend.utils.email_utils import send_new_user_notification
from backend.models import User
from datetime import datetime

# Create a simple test app
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'swiftlogixindia@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
app.config['MAIL_DEFAULT_SENDER'] = 'swiftlogixindia@gmail.com'

mail = Mail(app)
app.extensions = {'mail': mail}

# Create a test user
test_user = User()
test_user.id = 1
test_user.name = "Test User"
test_user.email = "test@example.com"
test_user.role = "customer"
test_user.created_at = datetime.now()

# Test the email function
with app.app_context():
    try:
        send_new_user_notification(test_user)
        print("Email notification sent successfully!")
    except Exception as e:
        print(f"Failed to send email notification: {str(e)}")