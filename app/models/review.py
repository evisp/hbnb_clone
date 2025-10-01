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
        place (Place): Place being reviewed (required)
        user (User): User who wrote the review (required)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """

    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review instance.
        
        Args:
            text (str): Content of the review
            rating (int): Rating between 1 and 5
            place (Place): Place instance being reviewed
            user (User): User instance who wrote the review
            
        Raises:
            ValueError: If validation fails
            TypeError: If place or user are not proper instances
        """
        super().__init__()
        
        # Use property setters for validation
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

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
    def place(self):
        """Get the place being reviewed."""
        return self._place

    @place.setter
    def place(self, value):
        """Set the place with validation (must be a Place instance)."""
        from app.models.place import Place
        if not isinstance(value, Place):
            raise TypeError("Place must be a Place instance.")
        self._place = value

    @property
    def user(self):
        """Get the user who wrote the review."""
        return self._user

    @user.setter
    def user(self, value):
        """Set the user with validation (must be a User instance)."""
        from app.models.user import User
        if not isinstance(value, User):
            raise TypeError("User must be a User instance.")
        self._user = value
