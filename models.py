import sqlite3
import os
from datetime import datetime

# Database file path
DB_PATH = 'logistics.db'

def init_db():
    """Initialize the database with the users table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'driver', 'customer')),
            is_approved INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def add_user(email, role):
    """
    Add a new user to the database
    Returns the user id if successful, None if email already exists
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # For admin, is_approved is 0 by default
    # For driver and customer, is_approved is 1 by default
    is_approved = 0 if role == 'admin' else 1
    
    try:
        cursor.execute('''
            INSERT INTO users (email, role, is_approved)
            VALUES (?, ?, ?)
        ''', (email, role, is_approved))
        
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return user_id
    except sqlite3.IntegrityError:
        # Email already exists
        conn.close()
        return None

def approve_user(email):
    """
    Approve a user by setting is_approved to 1
    Returns True if successful, False if user not found
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE users
        SET is_approved = 1
        WHERE email = ?
    ''', (email,))
    
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    
    return rows_affected > 0

def is_user_approved(email):
    """
    Check if a user is approved
    Returns True if approved, False if not approved, None if user not found
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT is_approved FROM users
        WHERE email = ?
    ''', (email,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return None
    return bool(result[0])

def get_user_by_email(email):
    """
    Get user details by email
    Returns user dict if found, None if not found
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, email, role, is_approved, created_at
        FROM users
        WHERE email = ?
    ''', (email,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result is None:
        return None
    
    return {
        'id': result['id'],
        'email': result['email'],
        'role': result['role'],
        'is_approved': result['is_approved'],
        'created_at': result['created_at']
    }

# Initialize the database when this module is imported
init_db()