import json
import pytest
from backend.app import create_app
from backend.database import db

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'JWT_SECRET_KEY': 'test',
        'SECRET_KEY': 'test'
    })
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


def register(client, name, email, password, role):
    return client.post('/api/auth/register', json={"name": name, "email": email, "password": password, "role": role})


def login(client, email, password):
    return client.post('/api/auth/login', json={"email": email, "password": password})


def test_auth_and_order_flow(client):
    # Register customer
    r = register(client, 'Alice', 'alice@example.com', 'pass123', 'customer')
    assert r.status_code == 201
    token = r.get_json()['token']

    # Create order
    headers = { 'Authorization': f'Bearer {token}' }
    order = client.post('/api/customer/orders', json={
        "pickup_address": "A", "pickup_lat": 28.6, "pickup_lng": 77.2,
        "drop_address": "B", "drop_lat": 28.61, "drop_lng": 77.21,
        "material_type": "Docs", "weight_kg": 2
    }, headers=headers)
    assert order.status_code == 201
