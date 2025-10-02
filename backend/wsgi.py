"""
WSGI entry point for the SwiftLogix application.
This file makes it easier for Gunicorn to find and run the app.
"""
import sys
import os

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import the application
from backend.app import app

# For Gunicorn
application = app

# For compatibility
app = application