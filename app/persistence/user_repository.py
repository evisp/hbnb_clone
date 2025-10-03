"""
User repository for handling user-specific database operations.
"""

from app.models.user import User
from app.persistence.repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """
    Repository for User entity with user-specific query methods.
    """
    
    def __init__(self):
        """Initialize UserRepository with User model."""
        super().__init__(User)
    
    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.
        
        Args:
            email (str): The user's email address
            
        Returns:
            User: The user instance, or None if not found
        """
        return self.model.query.filter_by(email=email).first()
