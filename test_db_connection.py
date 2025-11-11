#!/usr/bin/env python3
"""
Test database connection and order creation
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

def test_database():
    """
    Test database connection and models
    """
    try:
        from backend.database import db
        from backend.models import User, Customer, Order, OrderStatus
        from backend.app import create_app
        
        print("Creating app context...")
        app = create_app()
        
        with app.app_context():
            print("Database connection successful!")
            
            # Test querying users
            users = User.query.all()
            print(f"Found {len(users)} users in the database")
            
            if users:
                print("First user:", users[0].email, users[0].role)
                
                # Try to find a customer
                customer_user = User.query.filter_by(role='customer').first()
                if customer_user:
                    print(f"Found customer: {customer_user.email}")
                    customer = customer_user.customer_profile
                    if customer:
                        print(f"Customer profile ID: {customer.id}")
                        
                        # Count existing orders
                        order_count = Order.query.filter_by(customer_id=customer.id).count()
                        print(f"Customer has {order_count} existing orders")
                    else:
                        print("Customer profile not found")
                else:
                    print("No customer found in database")
            else:
                print("No users found in database")
                
        return True
        
    except Exception as e:
        print(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_database()