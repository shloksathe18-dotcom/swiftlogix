import csv
import io
from flask import Blueprint, jsonify, send_file
from ..database import db
from ..models import User, UserRole, Order, OrderStatus, Customer, Driver
from ..utils.security import role_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.get('/dashboard')
@role_required('admin')
def dashboard():
    customers = User.query.filter_by(role=UserRole.CUSTOMER.value).count()
    drivers = User.query.filter_by(role=UserRole.DRIVER.value).count()
    orders = Order.query.count()
    revenue = db.session.query(db.func.sum(Order.company_commission)).scalar() or 0
    active = Order.query.filter(Order.status.in_([
        OrderStatus.ASSIGNED.value,
        OrderStatus.PICKED.value,
        OrderStatus.DELIVERING.value
    ])).count()
    return jsonify({
        "customers": customers,
        "drivers": drivers,
        "orders": orders,
        "revenue": round(revenue,2),
        "active_orders": active
    })

@admin_bp.get('/users')
@role_required('admin')
def get_all_users():
    # Get all users with their roles
    users = User.query.all()
    
    user_data = []
    for user in users:
        user_info = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        
        # Add role-specific information
        if user.role == UserRole.CUSTOMER.value:
            customer = Customer.query.filter_by(user_id=user.id).first()
            if customer:
                user_info["customer_id"] = customer.id
                # Add customer-specific data here if needed
        elif user.role == UserRole.DRIVER.value:
            driver = Driver.query.filter_by(user_id=user.id).first()
            if driver:
                user_info["driver_id"] = driver.id
                user_info["is_verified"] = driver.is_verified
                user_info["is_available"] = driver.is_available
                user_info["current_lat"] = driver.current_lat
                user_info["current_lng"] = driver.current_lng
        
        user_data.append(user_info)
    
    return jsonify(user_data)

@admin_bp.get('/orders/export')
@role_required('admin')
def export_orders():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id","customer_id","driver_id","status","fare_total","commission","created_at"])
    for o in Order.query.all():
        writer.writerow([o.id, o.customer_id, o.driver_id, o.status, o.fare_total, o.company_commission, o.created_at.isoformat()])
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    return send_file(mem, mimetype='text/csv', as_attachment=True, download_name='orders.csv')
