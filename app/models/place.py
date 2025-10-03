"""
Place model for the HBnB application.
Defines the Place entity with validation and relationships.
"""

from app.models.base_model import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey


class Place(BaseModel):
    """
    Place class for managing place listings in the application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        title (str): Title of the place (max 100 chars, required)
        description (str): Detailed description (optional)
        price (float): Price per night (must be positive)
        latitude (float): Latitude coordinate (-90.0 to 90.0)
        longitude (float): Longitude coordinate (-180.0 to 180.0)
        owner_id (str): ID of the user who owns the place (required)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
        owner: Relationship to User (many-to-one)
        reviews: Relationship to Review (one-to-many)
        amenities: Relationship to Amenity (many-to-many)
    """
    
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    owner = relationship('User', back_populates='places')
    reviews = relationship('Review', back_populates='place', lazy='select', cascade='all, delete-orphan')
    amenities = relationship('Amenity', secondary='place_amenity', back_populates='places', lazy='select')
    
    @validates('title')
    def validate_title(self, key, value):
        """Validate title length and requirement."""
        self.validate_string_length(value, "Title", 100, required=True)
        return value
    
    @validates('price')
    def validate_price_value(self, key, value):
        """Validate price is positive."""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number.")
        if value <= 0:
            raise ValueError("Price must be a positive value.")
        return float(value)
    
    @validates('latitude')
    def validate_latitude_range(self, key, value):
        """Validate latitude range (-90.0 to 90.0)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number.")
        self.validate_number_range(value, "Latitude", -90.0, 90.0)
        return float(value)
    
    @validates('longitude')
    def validate_longitude_range(self, key, value):
        """Validate longitude range (-180.0 to 180.0)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number.")
        self.validate_number_range(value, "Longitude", -180.0, 180.0)
        return float(value)
    
    @validates('owner_id')
    def validate_owner_id(self, key, value):
        """Validate owner_id is present."""
        if not value or not isinstance(value, str):
            raise ValueError("Owner ID is required and must be a string.")
        return value
