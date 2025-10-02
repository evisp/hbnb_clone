"""
User API endpoints.
Handles CRUD operations for users.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

# Create namespace
api = Namespace('users', description='User operations')

# Input model with password (for registration)
user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

# Update model without email and password (for regular user updates)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user')
})

# Admin update model with all fields (for admin updates)
admin_user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'password': fields.String(description='Password of the user')
})

# Output model (without password)
user_output_model = api.model('UserOutput', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status')
})


@api.route('/')
class UserList(Resource):
    """Handles operations on the user collection."""

    @api.expect(user_input_model, validate=True)
    @api.response(201, 'User successfully created', user_output_model)
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user (Public endpoint)."""
        user_data = api.payload

        try:
            # Create user via facade (email uniqueness checked there)
            new_user = facade.create_user(user_data)
            
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'is_admin': new_user.is_admin
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of users retrieved successfully', [user_output_model])
    def get(self):
        """Retrieve a list of all users (Public endpoint)."""
        users = facade.get_all_users()
        
        return [
            {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'is_admin': user.is_admin
            }
            for user in users
        ], 200


@api.route('/<user_id>')
@api.param('user_id', 'The user unique identifier')
class UserResource(Resource):
    """Handles operations on a specific user."""

    @api.response(200, 'User details retrieved successfully', user_output_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (Public endpoint)."""
        user = facade.get_user(user_id)
        
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, 200

    @api.expect(user_update_model)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def put(self, user_id):
        """Update user information.
        
        Regular users: Can only update their own profile (first_name, last_name)
        Admins: Can update any user including email and password
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        user_data = api.payload

        # Check permissions
        if not is_admin and user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # Regular user restrictions
        if not is_admin:
            # Regular users cannot modify email or password
            if 'email' in user_data or 'password' in user_data:
                return {'error': 'You cannot modify email or password'}, 400

        # Admin capabilities
        if is_admin:
            # Validate email uniqueness if email is being changed
            if 'email' in user_data:
                existing_user = facade.get_user_by_email(user_data['email'])
                if existing_user and existing_user.id != user_id:
                    return {'error': 'Email already in use'}, 400

        try:
            # Update user via facade
            updated_user = facade.update_user(user_id, user_data)
            
            if not updated_user:
                return {'error': 'User not found'}, 404
            
            return {
                'message': 'User updated successfully'
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
