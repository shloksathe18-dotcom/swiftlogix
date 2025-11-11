from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Global extensions

db = SQLAlchemy()
migrate = Migrate()
