"""
Flask CLI commands for administrative tasks.
"""

import click
from flask.cli import with_appcontext
from app.services import facade


@click.command('create-admin')
@click.argument('email')
@click.argument('password')
@with_appcontext
def create_admin_command(email, password):
    """Create an admin user."""
    
    # Check if user already exists
    existing_user = facade.get_user_by_email(email)
    
    if existing_user:
        click.echo(f"User {email} already exists. Promoting to admin...")
        existing_user._is_admin = True
        click.echo(f"✓ User promoted to admin")
        click.echo(f"  ID: {existing_user.id}")
        click.echo(f"  Email: {existing_user.email}")
        click.echo(f"  Is Admin: {existing_user.is_admin}")
    else:
        # Create new user
        click.echo(f"Creating admin user: {email}")
        
        user_data = {
            'first_name': 'Admin',
            'last_name': 'User',
            'email': email,
            'password': password
        }
        
        try:
            new_user = facade.create_user(user_data)
            # Promote to admin
            new_user._is_admin = True
            
            click.echo(f"✓ Admin user created successfully")
            click.echo(f"  ID: {new_user.id}")
            click.echo(f"  Email: {new_user.email}")
            click.echo(f"  Is Admin: {new_user.is_admin}")
            
        except ValueError as e:
            click.echo(f"✗ Error: {str(e)}", err=True)


def init_app(app):
    """Register CLI commands with Flask app."""
    app.cli.add_command(create_admin_command)
