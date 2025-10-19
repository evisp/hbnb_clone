from flask import Blueprint

# Don't specify static_folder or static_url_path in blueprint
# Let Flask handle static files from the root static/ folder
frontend_bp = Blueprint(
    'frontend',
    __name__,
    template_folder='../../templates'
)

from app.frontend import routes
