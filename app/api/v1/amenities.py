"""
Amenity API endpoints.
Handles CRUD operations for amenities.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

# Create namespace
api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """Handles operations on the amenities collection."""

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def post(self):
        """Create a new amenity (Admin only)."""
        # Check if user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities (Public endpoint)."""
        amenities = facade.get_all_amenities()
        return [
            {'id': amenity.id, 'name': amenity.name}
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
@api.param('amenity_id', 'The amenity unique identifier')
class AmenityResource(Resource):
    """Handles operations on a specific amenity."""

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID (Public endpoint)."""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)."""
        # Check if user is admin
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {'message': 'Amenity updated successfully'}, 200

        except ValueError as e:
            return {'error': str(e)}, 400
