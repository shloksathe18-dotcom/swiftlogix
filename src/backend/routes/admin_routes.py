import csv
import io
from flask import Blueprint, jsonify, send_file, request
from ..database import db
from ..models import User, UserRole, Order, OrderStatus, Customer, Driver
from ..utils.security import role_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.get('/dashboard')
@role_required('admin')
def dashboard():
    try:
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
    except Exception as e:
        print(f"Error in admin dashboard: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@admin_bp.get('/users')
@role_required('admin')
def get_all_users():
    try:
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
                "is_blacklisted": user.is_blacklisted,
                "blacklist_reason": user.blacklist_reason,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            
            # Add role-specific information
            if user.role == UserRole.CUSTOMER.value:
                customer = Customer.query.filter_by(user_id=user.id).first()
                if customer:
                    user_info["customer_id"] = customer.customer_id  # Use 9-digit ID
                    # Get customer orders count and total spent
                    orders = Order.query.filter_by(customer_id=customer.id).all()
                    user_info["total_orders"] = len(orders)
                    user_info["total_spent"] = sum(order.fare_total for order in orders)
                    user_info["completed_orders"] = len([order for order in orders if order.status == OrderStatus.DELIVERED.value])
            elif user.role == UserRole.DRIVER.value:
                driver = Driver.query.filter_by(user_id=user.id).first()
                if driver:
                    user_info["driver_id"] = driver.driver_id  # Use 9-digit ID
                    user_info["is_verified"] = driver.is_verified
                    user_info["is_available"] = driver.is_available
                    user_info["current_lat"] = driver.current_lat
                    user_info["current_lng"] = driver.current_lng
                    # Get driver orders count and earnings
                    orders = Order.query.filter_by(driver_id=driver.id).all()
                    user_info["total_deliveries"] = len([order for order in orders if order.status == OrderStatus.DELIVERED.value])
                    user_info["total_earnings"] = sum(order.driver_share for order in orders if order.status == OrderStatus.DELIVERED.value)
            
            user_data.append(user_info)
        
        return jsonify(user_data)
    except Exception as e:
        print(f"Error in get_all_users: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@admin_bp.get('/users/<int:user_id>')
@role_required('admin')
def get_user_details(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        user_info = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "is_blacklisted": user.is_blacklisted,
            "blacklist_reason": user.blacklist_reason,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        
        # Add role-specific information
        if user.role == UserRole.CUSTOMER.value:
            customer = Customer.query.filter_by(user_id=user.id).first()
            if customer:
                user_info["customer_id"] = customer.customer_id  # Use 9-digit ID
                # Get all customer orders with details
                orders = Order.query.filter_by(customer_id=customer.id).all()
                user_info["orders"] = [{
                    "id": order.id,
                    "status": order.status,
                    "pickup_address": order.pickup_address,
                    "drop_address": order.drop_address,
                    "distance_km": order.distance_km,
                    "fare_total": order.fare_total,
                    "created_at": order.created_at.isoformat() if order.created_at else None
                } for order in orders]
                user_info["total_orders"] = len(orders)
                user_info["total_spent"] = sum(order.fare_total for order in orders)
                user_info["completed_orders"] = len([order for order in orders if order.status == OrderStatus.DELIVERED.value])
        elif user.role == UserRole.DRIVER.value:
            driver = Driver.query.filter_by(user_id=user.id).first()
            if driver:
                user_info["driver_id"] = driver.driver_id  # Use 9-digit ID
                user_info["is_verified"] = driver.is_verified
                user_info["is_available"] = driver.is_available
                user_info["current_lat"] = driver.current_lat
                user_info["current_lng"] = driver.current_lng
                # Get all driver orders with details
                orders = Order.query.filter_by(driver_id=driver.id).all()
                user_info["orders"] = [{
                    "id": order.id,
                    "status": order.status,
                    "pickup_address": order.pickup_address,
                    "drop_address": order.drop_address,
                    "distance_km": order.distance_km,
                    "driver_share": order.driver_share,
                    "created_at": order.created_at.isoformat() if order.created_at else None
                } for order in orders]
                user_info["total_deliveries"] = len([order for order in orders if order.status == OrderStatus.DELIVERED.value])
                user_info["total_earnings"] = sum(order.driver_share for order in orders if order.status == OrderStatus.DELIVERED.value)
        
        return jsonify(user_info)
    except Exception as e:
        print(f"Error in get_user_details: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500

@admin_bp.post('/users/<int:user_id>/blacklist')
@role_required('admin')
def blacklist_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        # Handle both JSON and form data
        data = request.get_json()
        if data is None:
            # Try to get data from form if JSON is not provided
            data = request.form.to_dict() or {}
        
        reason = data.get('reason', 'No reason provided')
        
        # Blacklist the user
        user.is_blacklisted = True
        user.blacklist_reason = reason
        # Also deactivate the user
        user.is_active = False
        
        db.session.commit()
        
        return jsonify({"message": f"User {user.email} has been blocked successfully"})
    except Exception as e:
        print(f"Error in blacklist_user: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@admin_bp.post('/users/<int:user_id>/block')
@role_required('admin')
def block_user(user_id):
    # Alias for blacklist_user
    return blacklist_user(user_id)

@admin_bp.post('/users/<int:user_id>/unblacklist')
@role_required('admin')
def unblacklist_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        
        # Handle request data (even though we don't use it, this prevents 422 errors)
        data = request.get_json()
        if data is None:
            # Try to get data from form if JSON is not provided
            data = request.form.to_dict() or {}
        
        # Remove blacklist status
        user.is_blacklisted = False
        user.blacklist_reason = None
        # Reactivate the user
        user.is_active = True
        
        db.session.commit()
        
        return jsonify({"message": f"User {user.email} has been unblocked successfully"})
    except Exception as e:
        print(f"Error in unblacklist_user: {str(e)}")
        db.session.rollback()
        return jsonify({"message": "Internal server error"}), 500

@admin_bp.post('/users/<int:user_id>/unblock')
@role_required('admin')
def unblock_user(user_id):
    # Alias for unblacklist_user
    return unblacklist_user(user_id)

@admin_bp.get('/orders/export')
@role_required('admin')
def export_orders():
    try:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["id","customer_id","driver_id","status","fare_total","commission","created_at"])
        for o in Order.query.all():
            writer.writerow([o.id, o.customer_id, o.driver_id, o.status, o.fare_total, o.company_commission, o.created_at.isoformat()])
        mem = io.BytesIO()
        mem.write(output.getvalue().encode('utf-8'))
        mem.seek(0)
        return send_file(mem, mimetype='text/csv', as_attachment=True, download_name='orders.csv')
    except Exception as e:
        print(f"Error in export_orders: {str(e)}")
        return jsonify({"message": "Internal server error"}), 500