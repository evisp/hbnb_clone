"""
Base model class for all entities in the HBnB application.
Provides common attributes and methods for ID generation, timestamps, and updates.
"""

import uuid
from datetime import datetime
import re


class BaseModel:
    """
    Base class for all business logic entities.
    
    Attributes:
        id (str): Unique identifier (UUID) for the entity
        created_at (datetime): Timestamp when the entity was created
        updated_at (datetime): Timestamp when the entity was last updated
    """

    def __init__(self):
        """Initialize a new BaseModel instance with UUID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary.
        
        Args:
            data (dict): Dictionary containing attribute names and new values
            
        Note:
            Only updates attributes that already exist on the object.
            Automatically updates the updated_at timestamp.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

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
