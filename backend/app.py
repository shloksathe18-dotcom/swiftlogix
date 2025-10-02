from flask import Flask, render_template
from flask_cors import CORS
from flask_mail import Mail
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from .config import DevelopmentConfig, ProductionConfig
from .database import db, migrate
from .utils.security import bcrypt, jwt
from .routes.auth_routes import auth_bp
from .routes.customer_routes import customer_bp
from .routes.driver_routes import driver_bp
from .routes.admin_routes import admin_bp
from . import models  # ensure models are imported for migrations


def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "static"),
        template_folder=os.path.join(os.path.dirname(__file__), "..", "frontend", "templates"),
        instance_relative_config=False,
    )
    
    # Use ProductionConfig if in production environment
    if os.getenv('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    CORS(app, supports_credentials=True)

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Initialize Flask-Mail
    mail = Mail(app)
    app.extensions['mail'] = mail

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(customer_bp, url_prefix="/api/customer")
    app.register_blueprint(driver_bp, url_prefix="/api/driver")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route('/')
    def index():
        return render_template('index.html')

    # Authentication pages
    @app.route('/login')
    def login_page():
        return render_template('auth/login.html')

    @app.route('/register')
    def register_page():
        return render_template('auth/register.html')

    @app.route('/reset-password')
    def reset_password_page():
        return render_template('auth/reset_password.html')

    # Basic page routes to demonstrate UIs
    @app.route('/customer')
    def customer_home():
        return render_template('customer/dashboard.html')

    @app.route('/customer/create_order')
    def customer_create_order_page():
        return render_template('customer/create_order.html')

    @app.route('/customer/track_order')
    def customer_track_order_page():
        return render_template('customer/track_order.html')

    @app.route('/driver')
    def driver_home():
        return render_template('driver/dashboard.html')

    @app.route('/driver/orders')
    def driver_orders_page():
        return render_template('driver/orders.html')

    @app.route('/admin')
    def admin_home():
        return render_template('admin/dashboard.html')

    @app.route('/admin/manage_users')
    def admin_manage_users_page():
        return render_template('admin/manage_users.html')

    return app

# For flask run discovery
app = create_app()