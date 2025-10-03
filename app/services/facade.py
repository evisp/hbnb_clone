"""
HBnB Facade module.
Provides a unified interface for interacting with the business logic layer.
"""

from app.persistence.repository import InMemoryRepository
from app.persistence.user_repository import UserRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.review_repository import ReviewRepository

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity


class HBnBFacade:
    """
    Facade class to handle business logic operations.
    Provides a unified interface between the presentation and business logic layers.
    """

    def __init__(self):
        """Initialize repositories for each entity."""
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()


    # =====================
    # User-related methods
    # =====================

    def create_user(self, user_data):
        """
        Create a new user.
        
        Args:
            user_data (dict): Dictionary containing user information
                - first_name (str): User's first name
                - last_name (str): User's last name
                - email (str): User's email address
                - password (str): Plain text password
                - is_admin (bool, optional): Admin status
        
        Returns:
            User: The created user instance
            
        Raises:
            ValueError: If user data is invalid or email already exists
        """
        # Check if email already exists
        existing_user = self.get_user_by_email(user_data.get('email'))
        if existing_user:
            raise ValueError("Email already registered")
        
        # Extract password for hashing
        password = user_data.pop('password', None)
        
        # Create new user (validation happens in User model via @validates)
        user = User(**user_data)
        
        # Hash password if provided
        if password:
            user.hash_password(password)
        
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """
        Retrieve a user by ID.
        
        Args:
            user_id (str): The user's unique identifier
            
        Returns:
            User: The user instance, or None if not found
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a user by email address.
        
        Args:
            email (str): The user's email address
            
        Returns:
            User: The user instance, or None if not found
        """
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """
        Retrieve all users.
        
        Returns:
            list: List of all user instances
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """
        Update an existing user's information.
        
        Args:
            user_id (str): The user's unique identifier
            user_data (dict): Dictionary containing fields to update
                - first_name (str, optional): User's first name
                - last_name (str, optional): User's last name
                - email (str, optional): User's email address
                - password (str, optional): User's new password
        
        Returns:
            User: The updated user instance, or None if user not found
            
        Raises:
            ValueError: If update data is invalid or email is already taken
        """
        user = self.get_user(user_id)
        if not user:
            return None
        
        # Check email uniqueness if email is being updated
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = self.get_user_by_email(user_data['email'])
            if existing_user:
                raise ValueError("Email already registered")
        
        # Handle password separately (needs hashing)
        if 'password' in user_data:
            user.hash_password(user_data['password'])
            # Remove password from user_data so it's not set as plain text
            user_data = {k: v for k, v in user_data.items() if k != 'password'}
        
        # Update other user fields (validation happens in User model via @validates)
        updated_user = self.user_repo.update(user_id, user_data)
        return updated_user

    # =====================
    # Place-related methods
    # =====================

    def create_place(self, place_data):
        """
        Create a new place.
        
        Args:
            place_data (dict): Dictionary containing place information
                - title, description, price, latitude, longitude, owner_id
                - amenities (list, optional): Will be ignored until relationships implemented
        
        Returns:
            Place: The created place instance
            
        Note:
            Amenities are accepted but not persisted yet (relationships task).
        """
        # Validate that owner exists
        owner_id = place_data.get('owner_id')
        if not owner_id or not self.get_user(owner_id):
            raise ValueError("Invalid owner_id")
        
        # Remove amenities from place_data (not persisted yet)
        place_data.pop('amenities', [])
        
        # Create place with validated data
        place = Place(**place_data)
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        """
        Retrieve place by ID.

        Args:
            place_id (str): Place ID

        Returns:
            Place or None
        """
        return self.place_repo.get(place_id)


    def get_all_places(self):
        """
        Retrieve all places.

        Returns:
            list of Place instances
        """
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        """
        Update an existing place.

        Args:
            place_id (str): Place ID
            place_data (dict): Fields to update; can include
                title, description, price, latitude, longitude, owner_id
                - amenities: Will be ignored until relationships implemented

        Returns:
            Place: Updated Place instance or None if not found

        Raises:
            ValueError: If validation fails or invalid owner
            
        Note:
            Amenities are accepted but not persisted yet (relationships task).
        """
        place = self.get_place(place_id)
        if not place:
            return None

        # Validate owner if owner_id is being updated
        if 'owner_id' in place_data:
            new_owner_id = place_data['owner_id']
            new_owner = self.user_repo.get(new_owner_id)
            if not new_owner:
                raise ValueError("Owner not found")
            # owner_id will be updated below

        # Remove amenities from update data (not persisted yet)
        place_data.pop('amenities', None)

        # Update place fields via repository
        updated_place = self.place_repo.update(place_id, place_data)
        return updated_place


    def delete_place(self, place_id):
        """
        Delete a place.
        
        Args:
            place_id (str): Place UUID
        
        Returns:
            bool: True if deleted, False if not found
        """
        place = self.get_place(place_id)
        if not place:
            return False
        
        # Delete the place from repository
        self.place_repo.delete(place_id)
        return True
    
    def add_amenity_to_place(self, place_id, amenity_id):
        """
        Add an amenity to a place (many-to-many relationship).
        
        Args:
            place_id (str): Place UUID
            amenity_id (str): Amenity UUID
        
        Raises:
            ValueError: If place or amenity not found, or amenity already associated
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        # Check if amenity is already associated
        if amenity in place.amenities:
            raise ValueError("Amenity already associated with this place")
        
        # Add amenity to place using SQLAlchemy relationship
        place.amenities.append(amenity)
        self.place_repo.update(place_id, {})  # Triggers commit
        
    
    def remove_amenity_from_place(self, place_id, amenity_id):
        """
        Remove an amenity from a place (many-to-many relationship).
        
        Args:
            place_id (str): Place UUID
            amenity_id (str): Amenity UUID
        
        Raises:
            ValueError: If place or amenity not found, or amenity not associated
        """
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found")
        
        # Check if amenity is associated
        if amenity not in place.amenities:
            raise ValueError("Amenity not associated with this place")
        
        # Remove amenity from place using SQLAlchemy relationship
        place.amenities.remove(amenity)
        self.place_repo.update(place_id, {})  # Triggers commit

    
    # =====================
    # Amenity-related methods 
    # =====================

    def create_amenity(self, amenity_data):
        """
        Create a new amenity.
        
        Args:
            amenity_data (dict): Dictionary with 'name' key
        
        Returns:
            Amenity: Created Amenity instance
        
        Raises:
            ValueError: If validation fails or duplicate name exists
        """
        name = amenity_data.get('name')
        
        # Check duplicate by name using repository method
        existing = self.amenity_repo.get_amenity_by_name(name)
        if existing:
            raise ValueError("Amenity with this name already exists")
        
        # Create and add new amenity (validation happens via @validates)
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity


    def get_amenity(self, amenity_id):
        """
        Retrieve amenity by ID.
        
        Args:
            amenity_id (str): Amenity UUID
        
        Returns:
            Amenity or None
        """
        return self.amenity_repo.get(amenity_id)


    def get_all_amenities(self):
        """
        Retrieve a list of all amenities.
        
        Returns:
            List of Amenity instances
        """
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an amenity by ID.
        
        Args:
            amenity_id (str): Amenity UUID
            amenity_data (dict): Data containing keys to update, typically 'name'
        
        Returns:
            Amenity: The updated Amenity instance, or None if not found
        
        Raises:
            ValueError: If validation fails or duplicate name exists
        """
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        
        if 'name' in amenity_data and amenity_data['name'] != amenity.name:
            # Check duplicate name using repository method
            existing = self.amenity_repo.get_amenity_by_name(amenity_data['name'])
            if existing:
                raise ValueError("Amenity with this name already exists")
        
        # Update using repository method (returns updated amenity)
        updated_amenity = self.amenity_repo.update(amenity_id, amenity_data)
        return updated_amenity



    # =====================
    # Review-related methods 
    # =====================

    def create_review(self, review_data):
        """
        Create a new review.

        Args:
            review_data (dict): Data containing 'text', 'rating', 'user_id' and 'place_id'.

        Returns:
            Review: Created Review instance.

        Raises:
            ValueError: If validation fails or referenced user/place don't exist.
        """
        user_id = review_data.get('user_id')
        place_id = review_data.get('place_id')

        # Validate user exists
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        # Validate place exists
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        # Create review with validated data
        review = Review(**review_data)
        self.review_repo.add(review)
        return review


    def get_review(self, review_id):
        """
        Retrieve review by ID.

        Args:
            review_id (str): Review UUID.

        Returns:
            Review or None.
        """
        return self.review_repo.get(review_id)


    def get_all_reviews(self):
        """
        Retrieve all reviews.

        Returns:
            List[Review]
        """
        return self.review_repo.get_all()


    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.

        Args:
            place_id (str): Place UUID.

        Returns:
            List[Review]

        Raises:
            ValueError: If place not found.
        """
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        
        # Use repository method to get reviews by place_id
        return self.review_repo.get_reviews_by_place(place_id)


    def get_review_by_user_and_place(self, user_id, place_id):
        """
        Check if a user has already reviewed a specific place.
        
        Args:
            user_id (str): User UUID
            place_id (str): Place UUID
        
        Returns:
            Review instance if found, None otherwise
        """
        return self.review_repo.get_review_by_user_and_place(user_id, place_id)


    def update_review(self, review_id, review_data):
        """
        Update a review.

        Args:
            review_id (str): Review UUID.
            review_data (dict): Fields to update: text, rating, user_id, place_id.

        Returns:
            Review instance or None if not found.

        Raises:
            ValueError: If validation fails or user/place don't exist.
        """
        review = self.get_review(review_id)
        if not review:
            return None

        # Validate user if user_id provided
        if 'user_id' in review_data:
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError("User not found")

        # Validate place if place_id provided
        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")

        # Update the review using the repository
        updated_review = self.review_repo.update(review_id, review_data)
        return updated_review


    def delete_review(self, review_id):
        """
        Delete a review.
        
        Args:
            review_id (str): Review UUID
        
        Returns:
            bool: True if deleted, False if not found
        """
        review = self.get_review(review_id)
        if not review:
            return False
        
        # Delete the review from repository
        self.review_repo.delete(review_id)
        return True
