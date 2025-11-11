from flask import Flask, request, jsonify, render_template_string, send_from_directory
import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import add_user, approve_user, is_user_approved, get_user_by_email
from email_utils import send_admin_notification_new_user, send_admin_notification_approved_user

app = Flask(__name__)

# HTML template for the approval confirmation page
APPROVAL_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>User Approval</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .success {
            color: #28a745;
        }
        .error {
            color: #dc3545;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>User Approval</h1>
        {% if success %}
            <h2 class="success">✅ Approval Successful!</h2>
            <p>The user with email <strong>{{ email }}</strong> has been successfully approved.</p>
        {% else %}
            <h2 class="error">❌ Approval Failed</h2>
            <p>{{ message }}</p>
        {% endif %}
        <a href="/" class="btn">Go to Home</a>
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    """Home page with API documentation"""
    return jsonify({
        "message": "Welcome to the Logistics App API",
        "endpoints": {
            "POST /register": "Register a new user",
            "POST /login": "Login as a user",
            "GET /approve": "Approve an admin user"
        }
    })

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    Expects JSON with 'email' and 'role' fields
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        email = data.get('email')
        role = data.get('role')
        
        if not email or not role:
            return jsonify({"error": "Email and role are required"}), 400
            
        if role not in ['admin', 'driver', 'customer']:
            return jsonify({"error": "Role must be 'admin', 'driver', or 'customer'"}), 400
        
        # Add user to database
        user_id = add_user(email, role)
        
        if user_id is None:
            return jsonify({"error": "Email already registered"}), 409
        
        # Send notification to admin
        send_admin_notification_new_user(email, role)
        
        # Return success response
        if role == 'admin':
            return jsonify({
                "message": "Admin registration successful. Awaiting approval.",
                "email": email,
                "role": role
            }), 201
        else:
            return jsonify({
                "message": "Registration successful.",
                "email": email,
                "role": role
            }), 201
            
    except Exception as e:
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500

@app.route('/approve')
def approve():
    """
    Approve an admin user
    Expects 'email' as a query parameter
    """
    try:
        email = request.args.get('email')
        
        if not email:
            return render_template_string(APPROVAL_TEMPLATE, 
                                        success=False, 
                                        message="Email parameter is required"), 400
        
        # Check if user exists
        user = get_user_by_email(email)
        if not user:
            return render_template_string(APPROVAL_TEMPLATE, 
                                        success=False, 
                                        message="User not found"), 404
        
        # Check if user is already approved
        if user['is_approved']:
            return render_template_string(APPROVAL_TEMPLATE, 
                                        success=True, 
                                        email=email), 200
        
        # Approve the user
        if approve_user(email):
            # Send notification to admin
            send_admin_notification_approved_user(email)
            
            return render_template_string(APPROVAL_TEMPLATE, 
                                        success=True, 
                                        email=email)
        else:
            return render_template_string(APPROVAL_TEMPLATE, 
                                        success=False, 
                                        message="Failed to approve user"), 500
            
    except Exception as e:
        return render_template_string(APPROVAL_TEMPLATE, 
                                    success=False, 
                                    message=f"Approval failed: {str(e)}"), 500

@app.route('/login', methods=['POST'])
def login():
    """
    Login endpoint
    Expects JSON with 'email' field
    """
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        email = data.get('email')
        
        if not email:
            return jsonify({"error": "Email is required"}), 400
        
        # Check if user exists and is approved
        approval_status = is_user_approved(email)
        
        if approval_status is None:
            return jsonify({"error": "User not found"}), 404
        elif not approval_status:
            return jsonify({"error": "Your account is not approved yet!"}), 403
        else:
            user = get_user_by_email(email)
            if user:
                return jsonify({
                    "message": f"Welcome {email}",
                    "email": email,
                    "role": user['role']
                }), 200
            else:
                return jsonify({
                    "message": f"Welcome {email}",
                    "email": email
                }), 200
            
    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500

# Add favicon route
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'frontend', 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
    # app.run(debug=True)