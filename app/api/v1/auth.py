"""
Authentication API endpoints.
Handles user login and JWT token generation.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import facade

# Create namespace
api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})


@api.route('/login')
class Login(Resource):
    """Handles user login and JWT token generation."""

    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """
        Authenticate user and return a JWT token.
        
        Returns:
            JSON response with access_token or error message
        """
        credentials = api.payload

        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])

        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id as identity and is_admin as additional claim
        access_token = create_access_token(
            identity=str(user.id),  # Identity must be a string
            additional_claims={'is_admin': user.is_admin}  # Additional claims for other data
        )

        # Step 4: Return the JWT token to the client
        return {
            'access_token': access_token
        }, 200


@api.route('/protected')
class ProtectedResource(Resource):
    """Example of a protected endpoint that requires JWT authentication."""

    @jwt_required()
    @api.response(200, 'Access granted')
    @api.response(401, 'Missing or invalid token')
    def get(self):
        """
        A protected endpoint that requires a valid JWT token.
        
        Returns:
            JSON response with user information from the token
        """
        # Get the identity of the current user from the JWT token (this is the user_id)
        current_user_id = get_jwt_identity()
        
        # Get additional claims from the token
        claims = get_jwt()
        
        return {
            'message': f'Hello, user {current_user_id}!',
            'user_id': current_user_id,
            'is_admin': claims.get('is_admin', False)
        }, 200

