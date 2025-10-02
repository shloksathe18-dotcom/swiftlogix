from functools import wraps
from flask import request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

bcrypt = Bcrypt()
jwt = JWTManager()


def hash_password(password: str) -> str:
    return bcrypt.generate_password_hash(password).decode('utf-8')


def check_password(password: str, pw_hash: str) -> bool:
    return bcrypt.check_password_hash(pw_hash, password)


def make_access_token(identity: dict) -> str:
    return create_access_token(identity=identity)


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            ident = get_jwt_identity()
            if not ident or ident.get('role') not in allowed_roles:
                return jsonify({"message": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
