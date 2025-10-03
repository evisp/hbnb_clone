"""
Place repository for handling place-specific database operations.
"""

from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """
    Repository for Place entity with place-specific query methods.
    """
    
    def __init__(self):
        """Initialize PlaceRepository with Place model."""
        super().__init__(Place)
    
    def get_places_by_owner(self, owner_id):
        """
        Retrieve all places owned by a specific user.
        
        Args:
            owner_id (str): The owner's user ID
            
        Returns:
            list: List of Place instances owned by the user
        """
        return self.model.query.filter_by(owner_id=owner_id).all()
