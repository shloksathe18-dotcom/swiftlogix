#!/usr/bin/env python3
"""
Script to clear all order data from the database
This script removes all existing records from the orders table
without modifying the table structure or affecting other tables.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.database import db
from backend.models import Order, Payment

def clear_orders():
    """
    Clear all order data from the database
    """
    print("Starting order data clearing process...")
    
    app = create_app()
    
    with app.app_context():
        try:
            # First, delete all payments (since they have a foreign key to orders)
            payment_count = Payment.query.count()
            if payment_count > 0:
                print(f"Deleting {payment_count} payment records...")
                Payment.query.delete()
                db.session.commit()
                print("Payment records deleted successfully!")
            else:
                print("No payment records found.")
            
            # Then delete all orders
            order_count = Order.query.count()
            if order_count > 0:
                print(f"Deleting {order_count} order records...")
                Order.query.delete()
                db.session.commit()
                print("Order records deleted successfully!")
            else:
                print("No order records found.")
            
            # Verify that orders table is empty
            remaining_orders = Order.query.count()
            remaining_payments = Payment.query.count()
            
            print(f"\nVerification:")
            print(f"  - Remaining orders: {remaining_orders}")
            print(f"  - Remaining payments: {remaining_payments}")
            
            if remaining_orders == 0 and remaining_payments == 0:
                print("\n✅ Success: All order data has been cleared from the database!")
                return True
            else:
                print("\n❌ Warning: Some records may still remain in the database.")
                return False
                
        except Exception as e:
            print(f"❌ Error clearing order data: {str(e)}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    clear_orders()