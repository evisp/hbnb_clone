"""
Review model for the HBnB application.
Defines the Review entity with validation and relationships.
"""

from app.models.base_model import BaseModel


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
    """

    def __init__(self, text, rating, place_id, user_id):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): Content of the review
            rating (int): Rating between 1 and 5
            place_id (str): ID of the place being reviewed
            user_id (str): ID of the user who wrote the review
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Use property setters for validation
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @property
    def text(self):
        """Get the review text."""
        return self._text

    @text.setter
    def text(self, value):
        """Set the review text with validation (required)."""
        if not value or not isinstance(value, str) or value.strip() == "":
            raise ValueError("Review text is required and cannot be empty.")
        self._text = value

    @property
    def rating(self):
        """Get the review rating."""
        return self._rating

    @rating.setter
    def rating(self, value):
        """Set the rating with validation (must be between 1 and 5)."""
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer.")
        if value < 1 or value > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self._rating = value

    @property
    def place_id(self):
        """Get the place ID."""
        return self._place_id

    @place_id.setter
    def place_id(self, value):
        """Set the place ID with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Place ID is required and must be a string.")
        self._place_id = value

    @property
    def user_id(self):
        """Get the user ID."""
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        """Set the user ID with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("User ID is required and must be a string.")
        self._user_id = value
