"""
Flask extensions initialization.
Extensions are initialized here to avoid circular imports.
"""

from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

bcrypt = Bcrypt()
jwt = JWTManager()
