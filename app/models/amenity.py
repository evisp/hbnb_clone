"""
Amenity model for the HBnB application.
Defines the Amenity entity with validation.
"""

from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """
    Amenity class for managing amenity entities in the application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        name (str): Name of the amenity (max 50 chars, required)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """

    def __init__(self, name):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): Name of the amenity (e.g., "Wi-Fi", "Parking")
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        self.name = name  

    @property
    def name(self):
        """Get the amenity name."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the amenity name with validation."""
        self.validate_string_length(value, "Amenity name", 50, required=True)
        self._name = value
