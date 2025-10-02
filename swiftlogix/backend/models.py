from datetime import datetime
from enum import Enum
from .database import db

class UserRole(str, Enum):
    CUSTOMER = "customer"
    DRIVER = "driver"
    ADMIN = "admin"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer_profile = db.relationship('Customer', backref='user', uselist=False)
    driver_profile = db.relationship('Driver', backref='user', uselist=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)
    is_verified = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)

class OrderStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    PICKED = "picked"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))

    pickup_address = db.Column(db.String(255))
    pickup_lat = db.Column(db.Float)
    pickup_lng = db.Column(db.Float)
    drop_address = db.Column(db.String(255))
    drop_lat = db.Column(db.Float)
    drop_lng = db.Column(db.Float)

    material_type = db.Column(db.String(120))
    weight_kg = db.Column(db.Float, default=0)
    distance_km = db.Column(db.Float, default=0)

    fare_total = db.Column(db.Float, default=0)
    driver_share = db.Column(db.Float, default=0)
    company_commission = db.Column(db.Float, default=0)

    status = db.Column(db.String(20), default=OrderStatus.PENDING.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = db.relationship('Customer', backref='orders')
    driver = db.relationship('Driver', backref='orders')

class PaymentStatus(str, Enum):
    INITIATED = "initiated"
    PAID = "paid"
    FAILED = "failed"

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    provider = db.Column(db.String(50), default="sandbox")
    status = db.Column(db.String(20), default=PaymentStatus.INITIATED.value)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref='payment')
