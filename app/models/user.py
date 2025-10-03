"""
User model for the HBnB application.
Defines the User entity with validation for user attributes.
"""

from app.models.base_model import BaseModel
from app.extensions import bcrypt
from app.extensions import db
from sqlalchemy.orm import validates


class User(BaseModel):
    """
    User class for managing user entities in the application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        first_name (str): First name of the user (max 50 chars, required)
        last_name (str): Last name of the user (max 50 chars, required)
        email (str): Email address (required, must be valid format, unique)
        password (str): Hashed password
        is_admin (bool): Admin privileges flag (defaults to False)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """
    
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)


    @validates('first_name')
    def validate_first_name(self, key, value):
        """Validate first name length and requirement."""
        self.validate_string_length(value, "First name", 50, required=True)
        return value


    @validates('last_name')
    def validate_last_name(self, key, value):
        """Validate last name length and requirement."""
        self.validate_string_length(value, "Last name", 50, required=True)
        return value


    @validates('email')
    def validate_email_format(self, key, value):
        """Validate email format."""
        if not value or not self.validate_email(value):
            raise ValueError("Invalid email format.")
        return value


    def hash_password(self, password):
        """
        Hashes the password before storing it.
        
        Args:
            password (str): Plain text password to hash
        """
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


    def verify_password(self, password):
        """
        Verifies if the provided password matches the hashed password.
        
        Args:
            password (str): Plain text password to verify
            
        Returns:
            bool: True if password matches, False otherwise
        """
        return bcrypt.check_password_hash(self.password, password)
