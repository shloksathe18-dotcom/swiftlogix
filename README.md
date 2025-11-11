# Logistics App

A Flask-based web application for an Online Logistics Project with user registration, approval workflow, and email notifications.

## Features

1. **Database**:
   - SQLite database with users table
   - Fields: id, email, role, is_approved
   - Automatic approval for drivers and customers
   - Manual approval required for admins

2. **Registration**:
   - POST `/register` endpoint
   - Role-based approval workflow
   - Email notifications to admin

3. **Approval**:
   - GET `/approve` endpoint
   - Manual approval for admin users

4. **Login**:
   - POST `/login` endpoint
   - Approval status checking

5. **Email Integration**:
   - Gmail SMTP integration
   - Notifications for all registration and approval events

## Project Structure

```
swiftlogix/
├── app.py              # Flask routes and application
├── models.py           # Database logic
├── email_utils.py      # Email functions
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Gmail**:
   - Create an App Password for your Gmail account
   - Set the `GMAIL_APP_PASSWORD` environment variable:
     ```bash
     export GMAIL_APP_PASSWORD="your-app-password-here"
     ```
   - On Windows:
     ```cmd
     set GMAIL_APP_PASSWORD=your-app-password-here
     ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   - The app will be available at http://localhost:5000

## API Endpoints

### Register a new user
```http
POST /register
Content-Type: application/json

{
  "email": "user@example.com",
  "role": "admin"  // or "driver" or "customer"
}
```

### Login
```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com"
}
```

### Approve an admin user
```http
GET /approve?email=user@example.com
```

## Database Schema

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('admin', 'driver', 'customer')),
  is_approved INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Approval Workflow

1. **Admin Registration**:
   - User registers with role "admin"
   - User is saved with `is_approved = 0`
   - Email sent to admin (swiftlogixindia@gmail.com) with approval link
   - User cannot login until approved

2. **Driver/Customer Registration**:
   - User registers with role "driver" or "customer"
   - User is automatically saved with `is_approved = 1`
   - Email sent to admin for notification
   - User can immediately login

3. **Approval Process**:
   - Admin clicks the approval link
   - User's `is_approved` is set to 1
   - Email sent to admin confirming approval
   - User can now login

## Environment Variables

- `GMAIL_APP_PASSWORD`: App Password for the Gmail account (required for email functionality)

## Requirements

- Python 3.10+
- Flask 3.0+