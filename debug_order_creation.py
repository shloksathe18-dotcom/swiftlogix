#!/usr/bin/env python3
"""
Debug script for order creation issues
"""

import sys
import os
import requests
import json

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_order_creation():
    """
    Test the order creation endpoint
    """
    print("Testing order creation...")
    
    # You'll need to get a valid token first by logging in
    # This is just an example of how the request should look
    
    # Example order data
    order_data = {
        "pickup_lat": "28.6139",
        "pickup_lng": "77.2090",
        "drop_lat": "28.7041",
        "drop_lng": "77.1025",
        "pickup_address": "Connaught Place, New Delhi",
        "drop_address": "Rohini, New Delhi",
        "material_type": "Electronics",
        "weight_kg": "2.5",
        "material_description": "Mobile phones and accessories"
    }
    
    print("Order data to be sent:")
    print(json.dumps(order_data, indent=2))
    
    # To actually test this, you would need:
    # 1. A valid JWT token obtained through login
    # 2. The correct endpoint URL
    # 3. Proper headers
    
    print("\nTo test this manually:")
    print("1. Log in as a customer to get a JWT token")
    print("2. Make a POST request to /api/customer/orders with the above data")
    print("3. Include the Authorization header: Bearer <your_token>")
    
    return True

if __name__ == "__main__":
    test_order_creation()