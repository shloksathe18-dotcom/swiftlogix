from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity
from ..database import db
from ..models import User, Customer, Driver, Order, OrderStatus
from ..utils.security import role_required
from ..utils.validators import validate_lat_lng

driver_bp = Blueprint('driver', __name__)

@driver_bp.get('/orders/available')
@role_required('driver')
def available_orders():
    # simple: list pending orders
    orders = Order.query.filter_by(status=OrderStatus.PENDING.value).all()
    return jsonify([{ "id": o.id, "pickup": [o.pickup_lat, o.pickup_lng], "drop": [o.drop_lat, o.drop_lng], "fare_total": o.fare_total }] )

@driver_bp.post('/orders/<int:order_id>/accept')
@role_required('driver')
def accept_order(order_id):
    ident = get_jwt_identity()
    user = User.query.get(ident['id'])
    driver = user.driver_profile

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
    ident = get_jwt_identity()
    user = User.query.get(ident['id'])
    driver = user.driver_profile
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
    ident = get_jwt_identity()
    user = User.query.get(ident['id'])
    driver = user.driver_profile
    delivered = [o for o in driver.orders if o.status == OrderStatus.DELIVERED.value]
    total = sum(o.driver_share for o in delivered)
    return jsonify({"delivered_count": len(delivered), "total_earnings": round(total,2)})
