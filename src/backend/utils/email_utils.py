from flask import current_app
from flask_mail import Message
import logging
import secrets
import string

def send_new_user_notification(user):
    """
    Send email notification to admin when a new user registers
    """
    try:
        mail = current_app.extensions['mail']
        
        # Create email message
        msg = Message(
            subject=f"New User Registration - {user.name}",
            recipients=[current_app.config.get('MAIL_DEFAULT_SENDER', 'swiftlogixindia@gmail.com')],
            body=f"""
A new user has registered on SwiftLogix:

Name: {user.name}
Email: {user.email}
Role: {user.role}
Registration Date: {user.created_at}

Please review this user in the admin panel.
            """,
            html=f"""
            <h2>New User Registration</h2>
            <p>A new user has registered on SwiftLogix:</p>
            <ul>
                <li><strong>Name:</strong> {user.name}</li>
                <li><strong>Email:</strong> {user.email}</li>
                <li><strong>Role:</strong> {user.role}</li>
                <li><strong>Registration Date:</strong> {user.created_at}</li>
            </ul>
            <p>Please review this user in the <a href="http://localhost:5000/admin/manage_users">admin panel</a>.</p>
            """
        )
        
        # Send email
        mail.send(msg)
        logging.info(f"New user notification sent for {user.email}")
        
    except Exception as e:
        logging.error(f"Failed to send new user notification: {str(e)}")

def send_password_reset_email(user, reset_token=None):
    """
    Send password reset email to user
    """
    try:
        mail = current_app.extensions['mail']
        
        # Use provided token or generate a new one
        if reset_token is None:
            reset_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        
        # In a real application, you would store this token in the database
        # associated with the user and set an expiration time
        
        reset_link = f"http://localhost:5000/reset-password?token={reset_token}&email={user.email}"
        
        # Create email message
        msg = Message(
            subject="Password Reset Request - SwiftLogix",
            recipients=[user.email],
            bcc=[current_app.config.get('MAIL_DEFAULT_SENDER', 'swiftlogixindia@gmail.com')],
            body=f"""
Hello {user.name},

You have requested to reset your password for your SwiftLogix account.

Please click the link below to reset your password:
{reset_link}

If you did not request this, please ignore this email.

This link will expire in 1 hour.

Thank you,
SwiftLogix Team
            """,
            html=f"""
            <h2>Password Reset Request</h2>
            <p>Hello {user.name},</p>
            <p>You have requested to reset your password for your SwiftLogix account.</p>
            <p><a href="{reset_link}" style="background-color: #667eea; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a></p>
            <p>If you did not request this, please ignore this email.</p>
            <p><strong>Note:</strong> This link will expire in 1 hour.</p>
            <br>
            <p>Thank you,<br>SwiftLogix Team</p>
            """
        )
        
        # Send email
        mail.send(msg)
        logging.info(f"Password reset email sent to {user.email}")
        
    except Exception as e:
        logging.error(f"Failed to send password reset email: {str(e)}")
        raise

def send_password_reset_confirmation(user):
    """
    Send password reset confirmation email to user and admin
    """
    try:
        mail = current_app.extensions['mail']
        
        # Create email message to user
        msg_to_user = Message(
            subject="Password Reset Confirmation - SwiftLogix",
            recipients=[user.email],
            bcc=[current_app.config.get('MAIL_DEFAULT_SENDER', 'swiftlogixindia@gmail.com')],
            body=f"""
Hello {user.name},

Your password for your SwiftLogix account has been successfully reset.

If you did not request this change, please contact our support team immediately.

Thank you,
SwiftLogix Team
            """,
            html=f"""
            <h2>Password Reset Confirmation</h2>
            <p>Hello {user.name},</p>
            <p>Your password for your SwiftLogix account has been successfully reset.</p>
            <p>If you did not request this change, please contact our support team immediately.</p>
            <br>
            <p>Thank you,<br>SwiftLogix Team</p>
            """
        )
        
        # Send email to user
        mail.send(msg_to_user)
        logging.info(f"Password reset confirmation sent to {user.email}")
        
    except Exception as e:
        logging.error(f"Failed to send password reset confirmation: {str(e)}")
        raise