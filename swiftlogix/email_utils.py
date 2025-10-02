import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Gmail SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "swiftlogixindia@gmail.com"
# Note: In production, use environment variables for the app password
SENDER_PASSWORD = os.getenv('GMAIL_APP_PASSWORD', 'your-app-password-here')

def send_email(to_email, subject, body):
    """
    Send an email using Gmail SMTP
    """
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        # Create SMTP session
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Enable TLS encryption
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        
        # Send email
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, to_email, text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

def send_admin_notification_new_user(email, role):
    """
    Send notification to admin when a new user registers
    """
    if role == 'admin':
        subject = f"New Admin Registration - Approval Required"
        body = f"""
A new admin user has registered:
Email: {email}
Role: {role}

Please approve this user by clicking the link below:
http://localhost:5000/approve?email={email}

This is an automated message from the Logistics System.
        """
    else:
        subject = f"New {role.capitalize()} Registration"
        body = f"""
A new user has registered:
Email: {email}
Role: {role}
Auto-approved: Yes

This is an automated message from the Logistics System.
        """
    
    return send_email(SENDER_EMAIL, subject, body)

def send_admin_notification_approved_user(email):
    """
    Send notification to admin when a user is approved
    """
    subject = f"User Approved - {email}"
    body = f"""
User has been approved:
Email: {email}

This is an automated message from the Logistics System.
    """
    
    return send_email(SENDER_EMAIL, subject, body)