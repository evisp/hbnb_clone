"""
Places API endpoints.
Handles CRUD operations for places.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

# Create namespace
api = Namespace('places', description='Place operations')

# Define the amenity model for nested references
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

# Define the user model for owner details
user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description='List of amenities ID\'s')
})


@api.route('/')
class PlaceList(Resource):
    """Handles operations on the places collection."""

    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def post(self):
        """Create a new place (Authentication required)."""
        current_user = get_jwt_identity()
        place_data = api.payload

        # Automatically set the owner_id from the authenticated user
        place_data['owner_id'] = current_user

        try:
            # Create place via facade
            new_place = facade.create_place(place_data)
            
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places (Public endpoint)."""
        places = facade.get_all_places()
        
        return [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude
            }
            for place in places
        ], 200


@api.route('/<place_id>')
@api.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
    """Handles operations on a specific place."""

    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID (Public endpoint)."""
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404
        
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'amenities': [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities
            ]
        }, 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place successfully updated')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (Authentication required, Owner only)."""
        current_user = get_jwt_identity()
        place_data = api.payload

        # Get the place
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404

        # Check ownership - only the owner can update their place
        if place.owner_id != current_user:
            return {'error': 'Unauthorized action'}, 403

        try:
            # Update place via facade
            updated_place = facade.update_place(place_id, place_data)
            
            return {
                'message': 'Place updated successfully'
            }, 200

        except ValueError as e:
            return {'error': str(e)}, 400
