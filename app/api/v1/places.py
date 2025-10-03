"""
Place API endpoints.
Handles CRUD operations for places.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

# Define models for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description='List of amenities ID')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def post(self):
        """Create a new place (Authentication required)."""
        current_user_id = get_jwt_identity()
        place_data = api.payload

        # Set owner_id from authenticated user
        place_data['owner_id'] = current_user_id

        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'owner_id': new_place.owner_id,
                'amenities': [amenity.id for amenity in new_place.amenities]
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
                'longitude': place.longitude,
                'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities]
            }
            for place in places
        ], 200

@api.route('/<place_id>')
@api.param('place_id', 'The place unique identifier')
class PlaceResource(Resource):
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
            'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities]
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def put(self, place_id):
        """Update a place's information (Authentication required, owner or admin only)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404

        # Check ownership (admins can bypass this check)
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        place_data = api.payload
        # Ensure owner_id doesn't change
        place_data['owner_id'] = place.owner_id

        try:
            updated_place = facade.update_place(place_id, place_data)
            return {'message': 'Place updated successfully'}, 200

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (Authentication required, owner or admin only)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Get the place
        place = facade.get_place(place_id)
        
        if not place:
            return {'error': 'Place not found'}, 404

        # Check ownership (admins can bypass this check)
        if not is_admin and place.owner_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # Delete the place
        facade.delete_place(place_id)
        
        return {'message': 'Place deleted successfully'}, 200

@api.route('/<place_id>/amenities/<amenity_id>')
@api.param('place_id', 'The place unique identifier')
@api.param('amenity_id', 'The amenity unique identifier')
class PlaceAmenityResource(Resource):
    @api.response(200, 'Amenity added to place successfully')
    @api.response(404, 'Place or amenity not found')
    @api.response(400, 'Amenity already associated with place')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def post(self, place_id, amenity_id):
        """Add an amenity to a place (Authentication required)."""
        try:
            facade.add_amenity_to_place(place_id, amenity_id)
            return {'message': 'Amenity added to place successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Place or amenity not found'}, 404

    @api.response(200, 'Amenity removed from place successfully')
    @api.response(404, 'Place or amenity not found')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def delete(self, place_id, amenity_id):
        """Remove an amenity from a place (Authentication required)."""
        try:
            facade.remove_amenity_from_place(place_id, amenity_id)
            return {'message': 'Amenity removed from place successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Place or amenity not found'}, 404
