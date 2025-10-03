"""
Review model for the HBnB application.
Defines the Review entity with validation and relationships.
"""

from app.models.base_model import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates, relationship
from sqlalchemy import ForeignKey


class Review(BaseModel):
    """
    Review class for managing review entities in the application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        text (str): Content of the review (required)
        rating (int): Rating from 1 to 5 (required)
        place_id (str): ID of the place being reviewed (required)
        user_id (str): ID of the user who wrote the review (required)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
        place: Relationship to Place (many-to-one)
        user: Relationship to User (many-to-one)
    """
    
    __tablename__ = 'reviews'
    
    text = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), ForeignKey('users.id'), nullable=False)
    
    # Relationships
    place = relationship('Place', back_populates='reviews')
    user = relationship('User', back_populates='reviews')
    
    @validates('text')
    def validate_text(self, key, value):
        """Validate review text is not empty."""
        if not value or not isinstance(value, str) or value.strip() == "":
            raise ValueError("Review text is required and cannot be empty.")
        return value
    
    @validates('rating')
    def validate_rating(self, key, value):
        """Validate rating is between 1 and 5."""
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer.")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        return value
    
    @validates('place_id')
    def validate_place_id(self, key, value):
        """Validate place_id is present."""
        if not value or not isinstance(value, str):
            raise ValueError("Place ID is required and must be a string.")
        return value
    
    @validates('user_id')
    def validate_user_id(self, key, value):
        """Validate user_id is present."""
        if not value or not isinstance(value, str):
            raise ValueError("User ID is required and must be a string.")
        return value
