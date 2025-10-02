"""
Place model for the HBnB application.
Defines the Place entity with validation and relationships.
"""

from app.models.base_model import BaseModel


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
        reviews (list): List of Review instances associated with the place
        amenities (list): List of Amenity instances associated with the place
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """

    def __init__(self, title, description, price, latitude, longitude, owner_id):
        """
        Initialize a new Place instance.
        
        Args:
            title (str): Title of the place
            description (str): Detailed description (can be empty)
            price (float): Price per night
            latitude (float): Latitude coordinate
            longitude (float): Longitude coordinate
            owner_id (str): ID of the user who owns the place
            
        Raises:
            ValueError: If validation fails
        """
        super().__init__()
        
        # Use property setters for validation
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        
        # Initialize relationship lists
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        """Get the place title."""
        return self._title

    @title.setter
    def title(self, value):
        """Set the place title with validation."""
        self.validate_string_length(value, "Title", 100, required=True)
        self._title = value

    @property
    def description(self):
        """Get the place description."""
        return self._description

    @description.setter
    def description(self, value):
        """Set the place description (optional, no length limit)."""
        self._description = value if value else ""

    @property
    def price(self):
        """Get the price per night."""
        return self._price

    @price.setter
    def price(self, value):
        """Set the price with validation (must be positive)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Price must be a number.")
        if value <= 0:
            raise ValueError("Price must be a positive value.")
        self._price = float(value)

    @property
    def latitude(self):
        """Get the latitude coordinate."""
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        """Set the latitude with range validation (-90.0 to 90.0)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Latitude must be a number.")
        self.validate_number_range(value, "Latitude", -90.0, 90.0)
        self._latitude = float(value)

    @property
    def longitude(self):
        """Get the longitude coordinate."""
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        """Set the longitude with range validation (-180.0 to 180.0)."""
        if not isinstance(value, (int, float)):
            raise ValueError("Longitude must be a number.")
        self.validate_number_range(value, "Longitude", -180.0, 180.0)
        self._longitude = float(value)

    @property
    def owner_id(self):
        """Get the owner's user ID."""
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value):
        """Set the owner ID with validation."""
        if not value or not isinstance(value, str):
            raise ValueError("Owner ID is required and must be a string.")
        self._owner_id = value

    def add_review(self, review):
        """
        Add a review to the place.
        
        Args:
            review (Review): Review instance to add
            
        Raises:
            TypeError: If review is not a Review instance
        """
        from app.models.review import Review
        if not isinstance(review, Review):
            raise TypeError("Only Review instances can be added.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """
        Add an amenity to the place.
        
        Args:
            amenity (Amenity): Amenity instance to add
            
        Raises:
            TypeError: If amenity is not an Amenity instance
            ValueError: If amenity is already added
        """
        from app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Only Amenity instances can be added.")
        if amenity in self.amenities:
            raise ValueError("Amenity already exists in this place.")
        self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """
        Remove an amenity from the place.
        
        Args:
            amenity (Amenity): Amenity instance to remove
            
        Raises:
            ValueError: If amenity is not in the list
        """
        if amenity not in self.amenities:
            raise ValueError("Amenity not found in this place.")
        self.amenities.remove(amenity)
