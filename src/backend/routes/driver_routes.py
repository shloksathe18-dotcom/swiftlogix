from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from ..database import db
from ..models import User, Customer, Driver, Order, OrderStatus
from ..utils.security import role_required
from ..utils.validators import validate_lat_lng
from flask_mail import Message
import logging

driver_bp = Blueprint('driver', __name__)

@driver_bp.get('/profile')
@role_required('driver')
def get_profile():
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    driver = user.driver_profile
    
    if not driver:
        return jsonify({"message": "Driver profile not found"}), 404

    profile_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "driver_id": driver.driver_id,  # 9-digit ID
        "phone": driver.phone,
        "license_number": driver.license_number,
        "vehicle_type": driver.vehicle_type,
        "vehicle_number": driver.vehicle_number,
        "total_deliveries": driver.total_deliveries,
        "total_earnings": driver.total_earnings,
        "is_available": driver.is_available,
        "rating": driver.rating,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
    
    return jsonify(profile_data)

@driver_bp.put('/profile')
@role_required('driver')
def update_profile():
    data = request.get_json() or {}
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    driver = user.driver_profile
    
    if not driver:
        return jsonify({"message": "Driver profile not found"}), 404

    # Update user information
    if "name" in data:
        user.name = data["name"]
    
    # Update driver information
    if "phone" in data:
        driver.phone = data["phone"]
    if "license_number" in data:
        driver.license_number = data["license_number"]
    if "vehicle_type" in data:
        driver.vehicle_type = data["vehicle_type"]
    if "vehicle_number" in data:
        driver.vehicle_number = data["vehicle_number"]

    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully"})

@driver_bp.get('/orders/available')
@role_required('driver')
def available_orders():
    # simple: list pending orders
    orders = Order.query.filter_by(status=OrderStatus.PENDING.value).all()
    return jsonify([{ "id": order.id, "pickup": [order.pickup_lat, order.pickup_lng], "drop": [order.drop_lat, order.drop_lng], "fare_total": order.fare_total } for order in orders] )

@driver_bp.get('/orders')
@role_required('driver')
def all_orders():
    # Get all orders assigned to this driver
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    driver = user.driver_profile
    
    if not driver:
        return jsonify({"message": "Driver profile not found"}), 404

    orders = Order.query.filter_by(driver_id=driver.id).all()
    return jsonify([{
        "id": order.id,
        "status": order.status,
        "pickup_address": order.pickup_address,
        "drop_address": order.drop_address,
        "distance_km": order.distance_km,
        "fare_total": order.fare_total,
        "driver_share": order.driver_share,
        "created_at": order.created_at.isoformat() if order.created_at else None
    } for order in orders])

@driver_bp.post('/orders/<int:order_id>/accept')
@role_required('driver')
def accept_order(order_id):
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    driver = user.driver_profile
    
    if not driver:
        return jsonify({"message": "Driver profile not found"}), 404

    order = Order.query.get_or_404(order_id)
    if order.status != OrderStatus.PENDING.value:
        return jsonify({"message": "Order not available"}), 400
    order.driver_id = driver.id
    order.status = OrderStatus.ASSIGNED.value
    db.session.commit()
    return jsonify({"message": "Accepted", "order_id": order.id})

@driver_bp.post('/location')
@role_required('driver')
def update_location():
    data = request.get_json() or {}
    if not validate_lat_lng(data.get('lat'), data.get('lng')):
        return jsonify({"message": "Invalid coordinates"}), 400
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    driver = user.driver_profile
    
    if not driver:
        return jsonify({"message": "Driver profile not found"}), 404
    driver.current_lat = float(data['lat'])
    driver.current_lng = float(data['lng'])
    db.session.commit()
    return jsonify({"message": "Location updated"})

@driver_bp.post('/orders/<int:order_id>/status')
@role_required('driver')
def update_status(order_id):
    data = request.get_json() or {}
    status = data.get('status')
    if status not in [s.value for s in OrderStatus]:
        return jsonify({"message": "Invalid status"}), 400
    order = Order.query.get_or_404(order_id)
    order.status = status
    db.session.commit()
    return jsonify({"message": "Status updated"})

@driver_bp.get('/earnings')
@role_required('driver')
def earnings():
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    driver = user.driver_profile
    
    if not driver:
        return jsonify({"message": "Driver profile not found"}), 404
    delivered = [o for o in driver.orders if o.status == OrderStatus.DELIVERED.value]
    total = sum(o.driver_share for o in delivered)
    return jsonify({"delivered_count": len(delivered), "total_earnings": round(total,2)})

@driver_bp.post('/chat')
@role_required('driver')
def driver_chat():
    data = request.get_json() or {}
    message = data.get('message')
    
    if not message:
        return jsonify({"message": "Message is required"}), 400
    
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    # Send message to admin email
    try:
        mail = current_app.extensions['mail']
        msg = Message(
            subject=f"Driver Support Chat - {user.email}",
            recipients=['swiftlogixindia@gmail.com'],
            body=f"""
Driver: {user.name} ({user.email})
Message: {message}

This message was sent from the driver support chatbot.
            """
        )
        mail.send(msg)
        logging.info(f"Chat message sent from driver {user.email}")
    except Exception as e:
        current_app.logger.error(f"Failed to send chat message email: {str(e)}")
    
    return jsonify({"message": "Message sent successfully"}), 200