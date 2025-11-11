from functools import wraps
from flask import request, jsonify, current_app
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, get_jwt

bcrypt = Bcrypt()
jwt = JWTManager()


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(password: str, pw_hash: str) -> bool:
    return bcrypt.check_password_hash(pw_hash, password)


def make_access_token(identity: dict) -> str:
    # Extract user ID and role from identity dict
    user_id = identity.get("id")
    role = identity.get("role")
    
    # Create token with user_id as identity and role as additional claim
    return create_access_token(
        identity=str(user_id),
        additional_claims={"role": role}
    )


# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    print(f"Expired token: {jwt_header}, {jwt_payload}")
    return jsonify({"message": "Token has expired"}), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    print(f"Invalid token: {error}")
    return jsonify({"message": "Invalid token"}), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    print(f"Missing token: {error}")
    return jsonify({"message": "Missing token"}), 401


@jwt.needs_fresh_token_loader
def needs_fresh_token_callback(jwt_header, jwt_payload):
    print(f"Needs fresh token: {jwt_header}, {jwt_payload}")
    return jsonify({"message": "Fresh token required"}), 401


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            try:
                print(f"Checking role for {fn.__name__}")
                print(f"Allowed roles: {allowed_roles}")
                # Get user ID from JWT identity
                user_id = get_jwt_identity()
                print(f"JWT Identity (user_id): {user_id}")
                
                # Get role from additional claims
                claims = get_jwt()
                role = claims.get("role")
                print(f"User role from claims: {role}")
                
                if not user_id or not role or role not in allowed_roles:
                    print(f"Role not allowed. User role: {role if role else 'None'}")
                    return jsonify({"message": "Forbidden"}), 403
                print(f"Role check passed, calling function {fn.__name__}")
                return fn(*args, **kwargs)
            except Exception as e:
                # Log the actual error for debugging
                print(f"Error in role_required decorator: {str(e)}")
                return jsonify({"message": "Authentication error"}), 401
        return wrapper
    return decorator