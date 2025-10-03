"""
Amenity repository for handling amenity-specific database operations.
"""

from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """
    Repository for Amenity entity with amenity-specific query methods.
    """
    
    def __init__(self):
        """Initialize AmenityRepository with Amenity model."""
        super().__init__(Amenity)
    
    def get_amenity_by_name(self, name):
        """
        Retrieve an amenity by name.
        
        Args:
            name (str): The amenity's name
            
        Returns:
            Amenity: The amenity instance, or None if not found
        """
        return self.model.query.filter_by(name=name).first()
