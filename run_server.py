#!/usr/bin/env python3
"""
Entry point for the Flask application.
This helps with deployment by providing a clear entry point.
"""
import os
import sys

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the application
try:
    from backend.app import app
    print("Successfully imported app from backend.app")
except ImportError as e:
    print(f"Failed to import app from backend.app: {e}")
    # Try alternative import
    try:
        sys.path.insert(0, 'backend')
        from app import app
        print("Successfully imported app from app (with backend in path)")
    except ImportError as e2:
        print(f"Failed to import app from app: {e2}")
        sys.exit(1)

# For Gunicorn to access the app
application = app

if __name__ == "__main__":
    # Run the app in development mode
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)