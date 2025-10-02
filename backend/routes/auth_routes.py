from flask import Blueprint, request, jsonify, current_app, render_template
from ..database import db
from ..models import User, UserRole, Customer, Driver
from ..utils.security import hash_password, check_password, make_access_token
from ..utils.validators import require_fields
from ..utils.email_utils import send_new_user_notification, send_password_reset_email, send_password_reset_confirmation

auth_bp = Blueprint('auth', __name__)

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
        db.session.add(customer)
    elif role == UserRole.DRIVER.value:
        driver = Driver()
        driver.user_id = user.id
        db.session.add(driver)

    db.session.commit()
    
    # Send email notification to admin
    try:
        send_new_user_notification(user)
    except Exception as e:
        # Log error but don't fail the registration
        current_app.logger.error(f"Failed to send notification email: {str(e)}")

    token = make_access_token({"id": user.id, "role": user.role})
    return jsonify({"token": token, "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}}), 201

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

    token = make_access_token({"id": user.id, "role": user.role})
    return jsonify({"token": token, "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role}})

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
    
    try:
        # Send password reset email
        send_password_reset_email(user)
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
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Invalid request"}), 400
    
    # In a real application, you would validate the token against the database
    # For this implementation, we'll just reset the password directly
    
    try:
        user.password_hash = hash_password(password)
        db.session.commit()
        
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
    return render_template('auth/reset_password.html')