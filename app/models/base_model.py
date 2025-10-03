"""
Base model class for all entities in the HBnB application.
Provides common attributes and methods for ID generation, timestamps, and validation utilities.
"""

import uuid
from datetime import datetime
import re
from app.extensions import db


class BaseModel(db.Model):
    """
    Base class for all business logic entities (SQLAlchemy model).
    
    Attributes:
        id (str): Unique identifier (UUID) for the entity
        created_at (datetime): Timestamp when the entity was created
        updated_at (datetime): Timestamp when the entity was last updated
    """
    
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


    @staticmethod
    def validate_email(email):
        """
        Validate email format using simple regex.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            bool: True if email is valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


    @staticmethod
    def validate_string_length(value, field_name, max_length, required=True):
        """
        Validate string length constraints.
        
        Args:
            value (str): The string value to validate
            field_name (str): Name of the field being validated (for error messages)
            max_length (int): Maximum allowed length
            required (bool): Whether the field is required
            
        Raises:
            ValueError: If validation fails
        """
        if required and (value is None or value.strip() == ""):
            raise ValueError(f"{field_name} is required and cannot be empty.")
        
        if value and len(value) > max_length:
            raise ValueError(f"{field_name} must not exceed {max_length} characters.")


    @staticmethod
    def validate_number_range(value, field_name, min_value=None, max_value=None):
        """
        Validate that a number falls within a specified range.
        
        Args:
            value (float/int): The number to validate
            field_name (str): Name of the field being validated
            min_value (float/int, optional): Minimum allowed value
            max_value (float/int, optional): Maximum allowed value
            
        Raises:
            ValueError: If validation fails
        """
        if min_value is not None and value < min_value:
            raise ValueError(f"{field_name} must be at least {min_value}.")
        
        if max_value is not None and value > max_value:
            raise ValueError(f"{field_name} must not exceed {max_value}.")
