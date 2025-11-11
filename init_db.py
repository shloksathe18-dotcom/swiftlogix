from backend.app import create_app
from backend.database import db
from backend import models
# Import all model classes explicitly
from backend.models import User, Customer, Driver, Order, Payment

app = create_app()

with app.app_context():
    # Drop all tables first to ensure clean schema
    db.drop_all()
    print("Existing tables dropped successfully!")
    
    # Create all tables with the correct schema
    db.create_all()
    print("Database tables created successfully!")
    
    # List all tables to verify
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables in database:")
    for table in tables:
        print(f"  - {table}")
        
    # Show table columns for user table to verify
    columns = inspector.get_columns('user')
    print("\nUser table columns:")
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")