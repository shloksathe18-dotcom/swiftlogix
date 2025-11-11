"""
WSGI entry point for the SwiftLogix application.
This file makes it easier for Gunicorn to find and run the app.
"""
import sys
import os

# Get the project root directory (parent of backend)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Debug information (can be removed later)
print("Project root:", project_root)
print("Python path:", sys.path)

# Import the application
try:
    from backend.app import app
    application = app
except ImportError as e:
    print(f"Import error: {e}")
    # Alternative import method
    sys.path.insert(0, os.path.join(project_root, 'backend'))
    from app import app
    application = app

# For compatibility
app = application