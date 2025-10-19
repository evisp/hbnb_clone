from flask import Flask
from flask_restx import Api
from flask_cors import CORS
from app.extensions import bcrypt, jwt, db
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns
import os


def create_app(config_class="config.DevelopmentConfig"):
    # Get the project root directory (parent of app/)
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(
        __name__,
        static_folder=os.path.join(basedir, 'static'),
        static_url_path='/static',
        template_folder=os.path.join(basedir, 'templates')
    )
    
    app.config.from_object(config_class)

    # Enable CORS for all routes
    CORS(app)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Register PRAGMA hook after db.init_app
    from sqlalchemy import event
    from sqlalchemy.engine import Engine

    @event.listens_for(Engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        try:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()
        except Exception:
            pass

    # Register frontend blueprint FIRST
    from app.frontend import frontend_bp
    app.register_blueprint(frontend_bp)

    # API configuration - doc only at /api/v1/
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/doc')

    # Register API namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')

    # CLI commands
    from app import commands
    commands.init_app(app)

    # Create tables and seed default admin once app context is active
    with app.app_context():
        db.create_all()
        from app.init_data import init_default_admin
        init_default_admin()

    return app
