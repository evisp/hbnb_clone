"""
Amenity model for the HBnB application.
Defines the Amenity entity with validation.
"""

from app.models.base_model import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates


class Amenity(BaseModel):
    """
    Amenity class for managing amenity entities in the application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        name (str): Name of the amenity (max 50 chars, required, unique)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """
    
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    @validates('name')
    def validate_name(self, key, value):
        """Validate amenity name length and requirement."""
        self.validate_string_length(value, "Amenity name", 50, required=True)
        return value
