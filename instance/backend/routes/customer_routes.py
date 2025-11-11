from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity
from ..database import db
from ..models import User, Customer, Driver, Order, OrderStatus, Payment
from ..utils.security import role_required
from ..utils.validators import require_fields, validate_lat_lng
from ..utils.pricing import haversine_km, compute_fare
from flask_mail import Message
import logging
from datetime import datetime
import random
import string

customer_bp = Blueprint('customer', __name__)

# Add chatbot endpoint
@customer_bp.post('/chat')
@role_required('customer')
def customer_chat():
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
            subject=f"Customer Support Chat - {user.email}",
            recipients=['swiftlogixindia@gmail.com'],
            body=f"""
Customer: {user.name} ({user.email})
Message: {message}

This message was sent from the customer support chatbot.
            """
        )
        mail.send(msg)
        logging.info(f"Chat message sent from customer {user.email}")
    except Exception as e:
        current_app.logger.error(f"Failed to send chat message email: {str(e)}")
    
    return jsonify({"message": "Message sent successfully"}), 200

@customer_bp.post('/orders')
@role_required('customer')
def create_order():
    try:
        # Handle both JSON and form data for file uploads
        material_photo_url = None
        material_description = None
        
        # Check if request contains file data
        if request.form:
            # Get data from form
            data = {
                "pickup_lat": request.form.get("pickup_lat"),
                "pickup_lng": request.form.get("pickup_lng"),
                "drop_lat": request.form.get("drop_lat"),
                "drop_lng": request.form.get("drop_lng"),
                "pickup_address": request.form.get("pickup_address"),
                "drop_address": request.form.get("drop_address"),
                "material_type": request.form.get("material_type"),
                "weight_kg": request.form.get("weight_kg"),
                "material_description": request.form.get("material_description")
            }
            
            # Handle photo upload (in a real app, you would save the file)
            # For now, we'll just store a placeholder URL
            if 'material_photo' in request.files:
                material_photo = request.files['material_photo']
                if material_photo.filename != '':
                    # In a real implementation, you would save the file and generate a URL
                    # For now, we'll just store the filename as a placeholder
                    material_photo_url = f"/uploads/{material_photo.filename}"
        else:
            # Handle JSON data
            data = request.get_json() or {}
        
        required = [
            "pickup_lat","pickup_lng","drop_lat","drop_lng",
            "pickup_address","drop_address","material_type","weight_kg"
        ]
        ok, err = require_fields(data, required)
        if not ok:
            return jsonify({"message": err}), 400

        # Validate coordinates
        try:
            # Check if all required fields are present and not None
            for field in required:
                if data.get(field) is None or data.get(field) == '':
                    return jsonify({"message": f"Missing required field: {field}"}), 400
                    
            # Convert to float with proper validation
            pickup_lat_str = data['pickup_lat']
            pickup_lng_str = data['pickup_lng']
            drop_lat_str = data['drop_lat']
            drop_lng_str = data['drop_lng']
            weight_kg_str = data['weight_kg']
            
            # Ensure they are strings before converting
            if not isinstance(pickup_lat_str, (str, int, float)):
                return jsonify({"message": "Invalid pickup_lat value"}), 400
            if not isinstance(pickup_lng_str, (str, int, float)):
                return jsonify({"message": "Invalid pickup_lng value"}), 400
            if not isinstance(drop_lat_str, (str, int, float)):
                return jsonify({"message": "Invalid drop_lat value"}), 400
            if not isinstance(drop_lng_str, (str, int, float)):
                return jsonify({"message": "Invalid drop_lng value"}), 400
            if not isinstance(weight_kg_str, (str, int, float)):
                return jsonify({"message": "Invalid weight_kg value"}), 400
                
            pickup_lat = float(pickup_lat_str)
            pickup_lng = float(pickup_lng_str)
            drop_lat = float(drop_lat_str)
            drop_lng = float(drop_lng_str)
            weight_kg = float(weight_kg_str)
        except (ValueError, TypeError) as e:
            return jsonify({"message": f"Invalid numeric values provided: {str(e)}"}), 400

        if not (validate_lat_lng(pickup_lat, pickup_lng) and validate_lat_lng(drop_lat, drop_lng)):
            return jsonify({"message": "Invalid coordinates"}), 400

        # Get user ID from JWT identity (now a string)
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        customer = user.customer_profile
        
        if not customer:
            return jsonify({"message": "Customer profile not found"}), 404

        distance = haversine_km(pickup_lat, pickup_lng, drop_lat, drop_lng)
        total, driver_share, commission = compute_fare(distance, weight_kg)

        # Create the order object
        order = Order()
        order.customer_id = customer.id
        order.pickup_address = data['pickup_address']
        order.pickup_lat = pickup_lat
        order.pickup_lng = pickup_lng
        order.drop_address = data['drop_address']
        order.drop_lat = drop_lat
        order.drop_lng = drop_lng
        order.material_type = data['material_type']
        order.weight_kg = weight_kg
        order.distance_km = round(distance, 2)
        order.fare_total = total
        order.driver_share = driver_share
        order.company_commission = commission
        order.status = OrderStatus.PENDING.value
        order.material_photo_url = material_photo_url
        order.material_description = data.get('material_description')
        
        db.session.add(order)
        db.session.commit()

        # Update customer stats
        customer.total_orders += 1
        customer.total_spent += total
        customer.last_order_date = datetime.utcnow()
        db.session.commit()

        return jsonify({"order_id": order.id, "fare_total": total, "distance_km": round(distance,2) }), 201
        
    except Exception as e:
        # Log the error for debugging
        current_app.logger.error(f"Error creating order: {str(e)}")
        return jsonify({"message": f"Error creating order: {str(e)}"}), 500

@customer_bp.post('/orders/simple')
@role_required('customer')
def create_simple_order():
    try:
        # Get form data
        pickup_location = request.form.get('pickup_location')
        drop_location = request.form.get('drop_location')
        pickup_lat = request.form.get('pickup_lat')
        pickup_lng = request.form.get('pickup_lng')
        drop_lat = request.form.get('drop_lat')
        drop_lng = request.form.get('drop_lng')
        material_type = request.form.get('material_type')
        material_description = request.form.get('material_description')
        material_weight = request.form.get('material_weight')
        distance_km = request.form.get('distance_km')
        fare_total = request.form.get('fare_total')
        
        # Validate required fields
        if not pickup_location:
            return jsonify({"message": "Pickup location is required"}), 400
        if not drop_location:
            return jsonify({"message": "Drop location is required"}), 400
        if not pickup_lat or not pickup_lng:
            return jsonify({"message": "Pickup coordinates are required"}), 400
        if not drop_lat or not drop_lng:
            return jsonify({"message": "Drop coordinates are required"}), 400
        if not material_type:
            return jsonify({"message": "Material type is required"}), 400
        if not material_weight:
            return jsonify({"message": "Material weight is required"}), 400
        if not distance_km:
            return jsonify({"message": "Distance is required"}), 400
        if not fare_total:
            return jsonify({"message": "Price is required"}), 400
            
        # Validate coordinates are numbers
        try:
            pickup_lat_float = float(pickup_lat)
            pickup_lng_float = float(pickup_lng)
            drop_lat_float = float(drop_lat)
            drop_lng_float = float(drop_lng)
            distance_km_float = float(distance_km)
            fare_total_float = float(fare_total)
        except ValueError:
            return jsonify({"message": "Coordinates, distance, and price must be valid numbers"}), 400
            
        # Validate weight is a number
        try:
            weight_kg = float(material_weight)
            if weight_kg <= 0:
                return jsonify({"message": "Material weight must be greater than 0"}), 400
        except ValueError:
            return jsonify({"message": "Material weight must be a valid number"}), 400
            
        # Validate distance and fare
        if distance_km_float < 0:
            return jsonify({"message": "Distance cannot be negative"}), 400
        if fare_total_float < 0:
            return jsonify({"message": "Price cannot be negative"}), 400
            
        # Generate a unique order ID
        order_id = generate_unique_order_id()
        
        # Get user ID from JWT identity
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"message": "User not found"}), 404
            
        customer = user.customer_profile
        
        if not customer:
            return jsonify({"message": "Customer profile not found"}), 404
            
        # Handle photo upload (in a real app, you would save the file)
        material_photo_url = None
        if 'material_photo' in request.files:
            material_photo = request.files['material_photo']
            if material_photo.filename != '':
                # In a real implementation, you would save the file and generate a URL
                # For now, we'll just store the filename as a placeholder
                material_photo_url = f"/uploads/{material_photo.filename}"
        
        # Create the order object with simplified data
        order = Order()
        order.customer_id = customer.id
        order.pickup_address = pickup_location
        order.pickup_lat = pickup_lat_float
        order.pickup_lng = pickup_lng_float
        order.drop_address = drop_location
        order.drop_lat = drop_lat_float
        order.drop_lng = drop_lng_float
        order.material_type = material_type
        order.material_description = material_description
        order.material_photo_url = material_photo_url
        order.weight_kg = weight_kg
        order.distance_km = distance_km_float
        order.fare_total = fare_total_float
        order.status = OrderStatus.PENDING.value
        order.driver_share = 0  # Will be calculated when assigned to driver
        order.company_commission = 0  # Will be calculated when assigned to driver
        
        db.session.add(order)
        db.session.commit()

        # Update customer stats
        customer.total_orders += 1
        customer.total_spent += fare_total_float
        customer.last_order_date = datetime.utcnow()
        db.session.commit()

        return jsonify({
            "order_id": f"ORD{order_id}",
            "distance_km": distance_km_float,
            "material_weight": weight_kg,
            "fare_total": fare_total_float,
            "message": "Order created successfully!"
        }), 201
        
    except Exception as e:
        # Log the error for debugging
        current_app.logger.error(f"Error creating simple order: {str(e)}")
        return jsonify({"message": f"Error creating order: {str(e)}"}), 500

def generate_unique_order_id():
    """Generate a unique order ID in the format ORD20251102XXXX"""
    # Get current date in YYYYMMDD format
    date_str = datetime.now().strftime("%Y%m%d")
    
    # Generate 4 random digits
    random_digits = ''.join(random.choices(string.digits, k=4))
    
    # Combine date and random digits
    order_id = f"{date_str}{random_digits}"
    
    # Check if this ID already exists (very unlikely but good to be safe)
    # In a production environment, you might want to check against the database
    return order_id

@customer_bp.get('/orders')
@role_required('customer')
def my_orders():
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    customer = user.customer_profile
    
    if not customer:
        return jsonify({"message": "Customer profile not found"}), 404
        
    orders = [
        {
            "id": o.id,
            "status": o.status,
            "fare_total": o.fare_total,
            "driver_id": o.driver_id,
            "distance_km": o.distance_km,
            "created_at": o.created_at.isoformat()
        } for o in customer.orders
    ]
    return jsonify(orders)

@customer_bp.get('/orders/<int:order_id>/track')
@role_required('customer')
def track_order(order_id):
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    customer = user.customer_profile
    
    if not customer:
        return jsonify({"message": "Customer profile not found"}), 404
    
    order = Order.query.get_or_404(order_id)
    if not order.driver:
        return jsonify({"status": order.status, "driver": None})
    return jsonify({
        "status": order.status,
        "driver": {
            "id": order.driver.id,
            "lat": order.driver.current_lat,
            "lng": order.driver.current_lng
        }
    })

@customer_bp.get('/profile')
@role_required('customer')
def get_profile():
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    customer = user.customer_profile
    
    if not customer:
        return jsonify({"message": "Customer profile not found"}), 404

    profile_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "customer_id": customer.customer_id,  # 9-digit ID
        "phone": customer.phone,
        "address": customer.address,
        "city": customer.city,
        "state": customer.state,
        "zip_code": customer.zip_code,
        "country": customer.country,
        "total_orders": customer.total_orders,
        "total_spent": customer.total_spent,
        "loyalty_points": customer.loyalty_points,
        "last_order_date": customer.last_order_date.isoformat() if customer.last_order_date else None,
        "created_at": user.created_at.isoformat() if user.created_at else None
    }
    
    return jsonify(profile_data)

@customer_bp.put('/profile')
@role_required('customer')
def update_profile():
    data = request.get_json() or {}
    # Get user ID from JWT identity (now a string)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({"message": "User not found"}), 404
        
    customer = user.customer_profile
    
    if not customer:
        return jsonify({"message": "Customer profile not found"}), 404

    # Update user information
    if "name" in data:
        user.name = data["name"]
    
    # Update customer information
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
    if "country" in data:
        customer.country = data["country"]

    db.session.commit()
    
    return jsonify({"message": "Profile updated successfully"})