"""
User model for the HBnB application.
Defines the User entity with validation for user attributes.
"""

from app.models.base_model import BaseModel


class User(BaseModel):
    """
    User class for managing user entities in the application.
    
    Attributes:
        id (str): Unique identifier (inherited from BaseModel)
        first_name (str): First name of the user (max 50 chars, required)
        last_name (str): Last name of the user (max 50 chars, required)
        email (str): Email address (required, must be valid format)
        is_admin (bool): Admin privileges flag (defaults to False)
        created_at (datetime): Creation timestamp (inherited from BaseModel)
        updated_at (datetime): Last update timestamp (inherited from BaseModel)
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User instance.
        
        Args:
            first_name (str): First name of the user
            last_name (str): Last name of the user
            email (str): Email address of the user
            is_admin (bool, optional): Admin status. Defaults to False.
            
        Raises:
            ValueError: If any validation fails
        """
        super().__init__()
        
        # Use property setters for validation
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

    @property
    def first_name(self):
        """Get the first name."""
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        """Set the first name with validation."""
        self.validate_string_length(value, "First name", 50, required=True)
        self._first_name = value

    @property
    def last_name(self):
        """Get the last name."""
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        """Set the last name with validation."""
        self.validate_string_length(value, "Last name", 50, required=True)
        self._last_name = value

    @property
    def email(self):
        """Get the email address."""
        return self._email

    @email.setter
    def email(self, value):
        """Set the email with format validation."""
        if not value or not self.validate_email(value):
            raise ValueError("Invalid email format.")
        self._email = value

    @property
    def is_admin(self):
        """Get admin status."""
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value):
        """Set admin status."""
        self._is_admin = value
