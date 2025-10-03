"""
Review API endpoints.
Handles CRUD operations for reviews and listing reviews by place.
"""

from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation (without user_id, auto-set from token)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def post(self):
        """Create a new review (Authentication required)."""
        current_user = get_jwt_identity()
        review_data = api.payload

        # Automatically set user_id from authenticated user
        review_data['user_id'] = current_user

        place_id = review_data.get('place_id')

        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        # Check if user is trying to review their own place
        if place.owner_id == current_user:
            return {'error': 'You cannot review your own place'}, 400

        # Check if user has already reviewed this place
        existing_review = facade.get_review_by_user_and_place(current_user, place_id)
        if existing_review:
            return {'error': 'You have already reviewed this place'}, 400

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews (Public endpoint)."""
        reviews = facade.get_all_reviews()
        result = [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }
            for review in reviews
        ]
        return result, 200


@api.route('/<review_id>')
@api.param('review_id', 'The review unique identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID (Public endpoint)."""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def put(self, review_id):
        """Update a review (Authentication required, author or admin only)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)
        
        review_data = api.payload

        # Get the review
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404

        # Check ownership (admins can bypass this check)
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # Ensure user_id and place_id remain unchanged
        review_data['user_id'] = review.user_id
        review_data['place_id'] = review.place_id

        try:
            updated_review = facade.update_review(review_id, review_data)
            return {'message': 'Review updated successfully'}, 200

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(401, 'Unauthorized - Authentication required')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review (Authentication required, author or admin only)."""
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Get the review
        review = facade.get_review(review_id)
        
        if not review:
            return {'error': 'Review not found'}, 404

        # Check ownership (admins can bypass this check)
        if not is_admin and review.user_id != current_user_id:
            return {'error': 'Unauthorized action'}, 403

        # Delete the review (we already validated it exists and user has permission)
        facade.delete_review(review_id)
        
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'The unique identifier of the place')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place (Public endpoint)."""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            result = [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id
                }
                for review in reviews
            ]
            return result, 200

        except ValueError as e:
            return {'error': str(e)}, 404

