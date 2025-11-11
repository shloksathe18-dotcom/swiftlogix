from flask import Blueprint, request, jsonify, current_app, render_template
from ..database import db
from ..models import User, UserRole, Customer, Driver
from ..utils.security import hash_password, check_password, make_access_token
from ..utils.validators import require_fields
from ..utils.email_utils import send_new_user_notification, send_password_reset_email, send_password_reset_confirmation
import secrets
import string
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# In-memory storage for reset tokens (in production, use database)
reset_tokens = {}

@auth_bp.post('/register')
def register():
    data = request.get_json() or {}
    ok, err = require_fields(data, ["name","email","password","role"])
    if not ok:
        return jsonify({"message": err}), 400

    role = data["role"].lower()
    if role not in [r.value for r in UserRole]:
        return jsonify({"message": "Invalid role"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already registered"}), 409

    user = User()
    user.name = data["name"]
    user.email = data["email"]
    user.password_hash = hash_password(data["password"])
    user.role = role
    db.session.add(user)
    db.session.flush()

    if role == UserRole.CUSTOMER.value:
        customer = Customer()
        customer.user_id = user.id
        # Add additional customer fields if provided
        if "phone" in data:
            customer.phone = data["phone"]
        if "address" in data:
            customer.address = data["address"]
        if "city" in data:
            customer.city = data["city"]
        if "state" in data:
            customer.state = data["state"]
        if "zip_code" in data:
            customer.zip_code = data["zip_code"]
        db.session.add(customer)
    elif role == UserRole.DRIVER.value:
        driver = Driver()
        driver.user_id = user.id
        # Add additional driver fields if provided
        if "phone" in data:
            driver.phone = data["phone"]
        if "license_number" in data:
            driver.license_number = data["license_number"]
        if "vehicle_type" in data:
            driver.vehicle_type = data["vehicle_type"]
        if "vehicle_number" in data:
            driver.vehicle_number = data["vehicle_number"]
        db.session.add(driver)

    db.session.commit()
    
    # Send email notification to admin
    try:
        send_new_user_notification(user)
    except Exception as e:
        # Log error but don't fail the registration
        current_app.logger.error(f"Failed to send notification email: {str(e)}")

    token = make_access_token({"id": user.id, "role": user.role})
    user_data = {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    
    # Add 9-digit IDs to user data
    if role == UserRole.CUSTOMER.value:
        customer_profile = Customer.query.filter_by(user_id=user.id).first()
        if customer_profile:
            user_data["customer_id"] = customer_profile.customer_id
    elif role == UserRole.DRIVER.value:
        driver_profile = Driver.query.filter_by(user_id=user.id).first()
        if driver_profile:
            user_data["driver_id"] = driver_profile.driver_id
    
    return jsonify({"token": token, "user": user_data}), 201

@auth_bp.post('/login')
def login():
    data = request.get_json() or {}
    ok, err = require_fields(data, ["email","password"])
    if not ok:
        return jsonify({"message": err}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user or not check_password(data["password"], user.password_hash):
        return jsonify({"message": "Invalid credentials"}), 401
    if not user.is_active:
        return jsonify({"message": "User blocked"}), 403
    # Check if user is blacklisted
    if user.is_blacklisted:
        return jsonify({"message": "User is blacklisted"}), 403

    token = make_access_token({"id": user.id, "role": user.role})
    user_data = {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    
    # Add 9-digit IDs to user data
    if user.role == UserRole.CUSTOMER.value:
        customer_profile = Customer.query.filter_by(user_id=user.id).first()
        if customer_profile:
            user_data["customer_id"] = customer_profile.customer_id
    elif user.role == UserRole.DRIVER.value:
        driver_profile = Driver.query.filter_by(user_id=user.id).first()
        if driver_profile:
            user_data["driver_id"] = driver_profile.driver_id
    
    return jsonify({"token": token, "user": user_data})

@auth_bp.post('/forgot-password')
def forgot_password():
    data = request.get_json() or {}
    email = data.get('email')
    
    if not email:
        return jsonify({"message": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        # For security, we don't reveal if the email exists
        return jsonify({"message": "If the email exists, a reset link has been sent"}), 200
    
    # Check if user is blacklisted
    if user.is_blacklisted:
        return jsonify({"message": "User is blacklisted"}), 403
    
    try:
        # Generate reset token
        reset_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
        # Store token with expiration (1 hour)
        reset_tokens[reset_token] = {
            'email': email,
            'expires_at': datetime.utcnow() + timedelta(hours=1)
        }
        
        # Send password reset email with our token
        send_password_reset_email(user, reset_token)
        return jsonify({"message": "If the email exists, a reset link has been sent"}), 200
    except Exception as e:
        current_app.logger.error(f"Failed to send password reset email: {str(e)}")
        return jsonify({"message": "Failed to send reset link. Please try again later."}), 500

@auth_bp.post('/reset-password')
def reset_password():
    data = request.get_json() or {}
    token = data.get('token')
    email = data.get('email')
    password = data.get('password')
    
    if not token or not email or not password:
        return jsonify({"message": "Token, email, and password are required"}), 400
    
    # Validate token
    if token not in reset_tokens:
        return jsonify({"message": "Invalid or expired reset token"}), 400
    
    token_data = reset_tokens[token]
    if token_data['email'] != email:
        return jsonify({"message": "Invalid reset token"}), 400
    
    if token_data['expires_at'] < datetime.utcnow():
        # Remove expired token
        del reset_tokens[token]
        return jsonify({"message": "Reset token has expired"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid request"}), 400
    
    # Check if user is blacklisted
    if user.is_blacklisted:
        return jsonify({"message": "User is blacklisted"}), 403
    
    try:
        user.password_hash = hash_password(password)
        db.session.commit()
        
        # Remove used token
        del reset_tokens[token]
        
        # Send confirmation email to both user and admin
        try:
            send_password_reset_confirmation(user)
        except Exception as e:
            current_app.logger.error(f"Failed to send password reset confirmation: {str(e)}")
        
        return jsonify({"message": "Password reset successfully"}), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Failed to reset password: {str(e)}")
        return jsonify({"message": "Failed to reset password. Please try again later."}), 500

@auth_bp.get('/reset-password')
def reset_password_page():
    # Pass query parameters to template so they can be used in JavaScript
    from flask import request
    token = request.args.get('token', '')
    email = request.args.get('email', '')
    return render_template('auth/reset_password.html', token=token, email=email)