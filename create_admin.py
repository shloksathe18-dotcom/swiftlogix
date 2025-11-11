from backend.app import create_app
from backend.database import db
from backend.models import User, UserRole
from backend.utils.security import hash_password

app = create_app()

with app.app_context():
    # Check if admin user already exists
    existing_user = User.query.filter_by(email="shloksathe18@gmail.com").first()
    if existing_user:
        print(f"User with email shloksathe18@gmail.com already exists with ID: {existing_user.id}")
        # Update user details
        existing_user.name = "shlok"
        if existing_user.role != UserRole.ADMIN.value:
            existing_user.role = UserRole.ADMIN.value
            print("Updated user role to admin")
        else:
            print("User is already an admin")
        db.session.commit()
        print("Updated user details")
    else:
        # Create new admin user
        admin_user = User()
        admin_user.name = "shlok"
        admin_user.email = "shloksathe18@gmail.com"
        admin_user.password_hash = hash_password("shlok@2116")
        admin_user.role = UserRole.ADMIN.value
        admin_user.is_active = True
        
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created successfully with ID: {admin_user.id}")
    
    # Verify the user
    user = User.query.filter_by(email="shloksathe18@gmail.com").first()
    if user:
        print(f"User details:")
        print(f"  ID: {user.id}")
        print(f"  Name: {user.name}")
        print(f"  Email: {user.email}")
        print(f"  Role: {user.role}")
        print(f"  Active: {user.is_active}")
    else:
        print("Failed to retrieve user")