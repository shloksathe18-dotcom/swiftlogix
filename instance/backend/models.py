from datetime import datetime
from enum import Enum
from .database import db
import random

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
    # Add a field to track if user is blacklisted
    is_blacklisted = db.Column(db.Boolean, default=False)
    blacklist_reason = db.Column(db.String(255))

    customer_profile = db.relationship('Customer', backref='user', uselist=False)
    driver_profile = db.relationship('Driver', backref='user', uselist=False)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add 9-digit customer ID
    customer_id = db.Column(db.BigInteger, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    zip_code = db.Column(db.String(10))
    country = db.Column(db.String(100), default='India')
    total_orders = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    loyalty_points = db.Column(db.Integer, default=0)
    last_order_date = db.Column(db.DateTime)
    
    def __init__(self, **kwargs):
        super(Customer, self).__init__(**kwargs)
        # Generate a unique 9-digit customer ID if not provided
        if not self.customer_id and 'customer_id' not in kwargs:
            self.customer_id = self.generate_unique_customer_id()
    
    def generate_unique_customer_id(self):
        # Generate a 9-digit number
        # We'll use a simpler approach to avoid context issues
        import time
        # Use timestamp + random to create a unique ID
        timestamp_part = int(time.time()) % 100000
        random_part = random.randint(10000, 99999)
        candidate = int(f"{timestamp_part:05d}{random_part:05d}")
        # Ensure it's 9 digits
        if candidate < 100000000:
            candidate += 100000000
        elif candidate > 999999999:
            candidate = candidate % 1000000000
            if candidate < 100000000:
                candidate += 100000000
        return candidate

class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Add 9-digit driver ID
    driver_id = db.Column(db.BigInteger, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    current_lat = db.Column(db.Float)
    current_lng = db.Column(db.Float)
    is_verified = db.Column(db.Boolean, default=False)
    is_available = db.Column(db.Boolean, default=True)
    phone = db.Column(db.String(20))
    license_number = db.Column(db.String(50))
    vehicle_type = db.Column(db.String(50))
    vehicle_number = db.Column(db.String(20))
    total_deliveries = db.Column(db.Integer, default=0)
    total_earnings = db.Column(db.Float, default=0.0)
    rating = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    
    def __init__(self, **kwargs):
        super(Driver, self).__init__(**kwargs)
        # Generate a unique 9-digit driver ID if not provided
        if not self.driver_id and 'driver_id' not in kwargs:
            self.driver_id = self.generate_unique_driver_id()
    
    def generate_unique_driver_id(self):
        # Generate a 9-digit number
        # We'll use a simpler approach to avoid context issues
        import time
        # Use timestamp + random to create a unique ID
        timestamp_part = int(time.time()) % 100000
        random_part = random.randint(10000, 99999)
        candidate = int(f"{timestamp_part:05d}{random_part:05d}")
        # Ensure it's 9 digits
        if candidate < 100000000:
            candidate += 100000000
        elif candidate > 999999999:
            candidate = candidate % 1000000000
            if candidate < 100000000:
                candidate += 100000000
        return candidate

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
    
    # Add photo upload fields
    material_photo_url = db.Column(db.String(500))
    material_description = db.Column(db.Text)

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