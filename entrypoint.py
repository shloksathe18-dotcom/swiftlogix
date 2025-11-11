import sys
import os

# Debug information
print("Python path:", sys.path)
print("Current working directory:", os.getcwd())
print("Directory contents:", os.listdir('.'))

# Add current directory and backend to path
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(current_dir, 'backend')

print("Current dir:", current_dir)
print("Backend dir:", backend_dir)

sys.path.insert(0, current_dir)
sys.path.insert(0, backend_dir)

print("Updated Python path:", sys.path)

# Try to import the app
try:
    print("Attempting to import backend.app...")
    from backend.app import app
    print("Successfully imported backend.app")
except ImportError as e:
    print(f"Failed to import backend.app: {e}")
    
    # Try direct import from backend directory
    try:
        print("Attempting to import app directly...")
        from app import app
        print("Successfully imported app")
    except ImportError as e2:
        print(f"Failed to import app: {e2}")
        sys.exit(1)

# Make app available at module level for Gunicorn
application = app

if __name__ == "__main__":
    print("Running app directly...")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))