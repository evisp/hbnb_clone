"""
Amenity API endpoints.
Handles CRUD operations for amenities.
"""

from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from app.services import facade


# Create namespace
api = Namespace('amenities', description='Amenity operations')

# Initialize facade
# facade = HBnBFacade()

# Define amenity model for validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    """Handles operations on the amenity collection."""

    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data or duplicate amenity')
    def post(self):
        """Register a new amenity."""
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
        """Retrieve a list of all amenities."""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name
            }
            for amenity in amenities
        ], 200


@api.route('/<amenity_id>')
@api.param('amenity_id', 'The amenity unique identifier')
class AmenityResource(Resource):
    """Handles operations on a specific amenity."""

    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID."""
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
    @api.response(400, 'Invalid input data or duplicate name')
    def put(self, amenity_id):
        """Update an amenity's information."""
        amenity_data = api.payload

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {'message': 'Amenity updated successfully'}, 200

        except ValueError as e:
            return {'error': str(e)}, 400
