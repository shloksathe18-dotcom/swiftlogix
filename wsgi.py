import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Also add the backend directory to Python path
backend_path = os.path.join(project_root, 'backend')
sys.path.insert(0, backend_path)

# Import the app from backend
from backend.app import app

if __name__ == "__main__":
    app.run()