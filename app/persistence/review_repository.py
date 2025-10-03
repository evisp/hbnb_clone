"""
Review repository for handling review-specific database operations.
"""

from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """
    Repository for Review entity with review-specific query methods.
    """
    
    def __init__(self):
        """Initialize ReviewRepository with Review model."""
        super().__init__(Review)
    
    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.
        
        Args:
            place_id (str): The place's ID
            
        Returns:
            list: List of Review instances for the place
        """
        return self.model.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        """
        Retrieve all reviews written by a specific user.
        
        Args:
            user_id (str): The user's ID
            
        Returns:
            list: List of Review instances by the user
        """
        return self.model.query.filter_by(user_id=user_id).all()
    
    def get_review_by_user_and_place(self, user_id, place_id):
        """
        Retrieve a review by a specific user for a specific place.
        
        Args:
            user_id (str): The user's ID
            place_id (str): The place's ID
            
        Returns:
            Review: Review instance or None if not found
        """
        return self.model.query.filter_by(user_id=user_id, place_id=place_id).first()
