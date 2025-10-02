"""
HBnB Facade module.
Provides a unified interface for interacting with the business logic layer.
"""

from app.persistence.repository import InMemoryRepository
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
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

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
        
        # Create new user (validation happens in User model)
        user = User(**user_data)
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
        return self.user_repo.get_by_attribute('email', email)

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
        
        # Update other user fields (validation happens in User model via property setters)
        self.user_repo.update(user_id, user_data)
        return user


    # =====================
    # Place-related methods
    # =====================
    def create_place(self, place_data):
        """
        Create a new place.
        
        Args:
            place_data (dict): Dictionary containing place information
                - title, description, price, latitude, longitude, owner_id, amenities
        
        Returns:
            Place: The created place instance
        """
        # Validate that owner exists
        owner_id = place_data.get('owner_id')
        if not owner_id or not self.get_user(owner_id):
            raise ValueError("Invalid owner_id")
        
        # Process amenities (convert IDs to Amenity objects)
        amenity_ids = place_data.pop('amenities', [])
        place = Place(**place_data)
        
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.add_amenity(amenity)
        
        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        """
        Retrieve place by ID including owner and amenities.

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
                title, description, price, latitude, longitude,
                owner_id, amenities (list of amenity IDs)

        Returns:
            Place: Updated Place instance or None if not found

        Raises:
            ValueError: If validation fails or invalid owner/amenities
        """
        place = self.get_place(place_id)
        if not place:
            return None

        # Owner update handling
        if 'owner_id' in place_data:
            new_owner_id = place_data['owner_id']
            new_owner = self.user_repo.get(new_owner_id)
            if not new_owner:
                raise ValueError("Owner not found")
            place.owner = new_owner
            place_data.pop('owner_id')

        # Amenities update handling
        if 'amenities' in place_data:
            new_amenity_ids = place_data['amenities']
            new_amenities = []
            for aid in new_amenity_ids:
                amenity = self.amenity_repo.get(aid)
                if not amenity:
                    raise ValueError(f"Amenity with id '{aid}' not found")
                new_amenities.append(amenity)
            # Replace existing amenities with new list
            place.amenities = new_amenities
            place_data.pop('amenities')

        # Update rest of the fields via repository update which triggers property setters
        self.place_repo.update(place_id, place_data)

        return place
    
    # =====================
    # Review-related methods (Placeholders for now)
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

        # Create review with IDs (no need to remove them anymore)
        review = Review(**review_data)
        
        # Add review to place's reviews list for relationship tracking
        place.add_review(review)
        
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
        
        # Return all reviews associated with this place
        return place.reviews
    
    def get_review_by_user_and_place(self, user_id, place_id):
        """
        Check if a user has already reviewed a specific place.
        
        Args:
            user_id (str): User UUID
            place_id (str): Place UUID
        
        Returns:
            Review instance if found, None otherwise
        """
        # Get all reviews for the place
        place = self.place_repo.get(place_id)
        if not place:
            return None
        
        # Check if any review is by this user
        for review in place.reviews:
            if review.user_id == user_id:
                return review
        
        return None




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
            # user_id will be updated below

        # Validate place if place_id provided
        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            # place_id will be updated below

        # Update the review using the repository
        self.review_repo.update(review_id, review_data)
        return review


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
        
        # Remove review from place's reviews list
        place = self.place_repo.get(review.place_id)
        if place and review in place.reviews:
            place.reviews.remove(review)
        
        # Delete the review from repository
        return self.review_repo.delete(review_id)


    # =====================
    # Amenity-related methods (Placeholders for now)
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

        # Check duplicate by name (optional uniqueness)
        existing = next((a for a in self.amenity_repo.get_all() if a.name == name), None)
        if existing:
            raise ValueError("Amenity with this name already exists")

        # Create and add new amenity
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
            # Check duplicate name
            existing = next((a for a in self.amenity_repo.get_all() if a.name == amenity_data['name']), None)
            if existing:
                raise ValueError("Amenity with this name already exists")

        # Update using repository method (which calls instance update)
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity