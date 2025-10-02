from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from ..database import db
from ..models import User, Customer, Driver, Order, OrderStatus, Payment
from ..utils.security import role_required
from ..utils.validators import require_fields, validate_lat_lng
from ..utils.pricing import haversine_km, compute_fare

customer_bp = Blueprint('customer', __name__)

@customer_bp.post('/orders')
@role_required('customer')
def create_order():
    data = request.get_json() or {}
    required = [
        "pickup_lat","pickup_lng","drop_lat","drop_lng",
        "pickup_address","drop_address","material_type","weight_kg"
    ]
    ok, err = require_fields(data, required)
    if not ok:
        return jsonify({"message": err}), 400

    if not (validate_lat_lng(data['pickup_lat'], data['pickup_lng']) and validate_lat_lng(data['drop_lat'], data['drop_lng'])):
        return jsonify({"message": "Invalid coordinates"}), 400

    ident = get_jwt_identity()
    user = User.query.get(ident['id'])
    customer = user.customer_profile

    distance = haversine_km(float(data['pickup_lat']), float(data['pickup_lng']), float(data['drop_lat']), float(data['drop_lng']))
    total, driver_share, commission = compute_fare(distance, float(data['weight_kg']))

    order = Order(
        customer_id=customer.id,
        pickup_address=data['pickup_address'],
        pickup_lat=float(data['pickup_lat']),
        pickup_lng=float(data['pickup_lng']),
        drop_address=data['drop_address'],
        drop_lat=float(data['drop_lat']),
        drop_lng=float(data['drop_lng']),
        material_type=data['material_type'],
        weight_kg=float(data['weight_kg']),
        distance_km=round(distance, 2),
        fare_total=total,
        driver_share=driver_share,
        company_commission=commission,
        status=OrderStatus.PENDING.value
    )
    db.session.add(order)
    db.session.commit()

    return jsonify({"order_id": order.id, "fare_total": total, "distance_km": round(distance,2) }), 201

@customer_bp.get('/orders')
@role_required('customer')
def my_orders():
    ident = get_jwt_identity()
    user = User.query.get(ident['id'])
    customer = user.customer_profile
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
