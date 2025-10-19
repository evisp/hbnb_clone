from flask import render_template
from app.frontend import frontend_bp


@frontend_bp.route('/')
def index():
    """Render the main page with list of places"""
    return render_template('index.html')


@frontend_bp.route('/login')
def login():
    """Render the login page"""
    return render_template('login.html')


@frontend_bp.route('/place/<place_id>')
def place_detail(place_id):
    """Render the place details page"""
    return render_template('place.html', place_id=place_id)


@frontend_bp.route('/add-review/<place_id>')
def add_review(place_id):
    """Render the add review page"""
    return render_template('add_review.html', place_id=place_id)
