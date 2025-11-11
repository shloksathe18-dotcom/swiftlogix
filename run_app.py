import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app factory function
from backend.app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True) 
    
    
