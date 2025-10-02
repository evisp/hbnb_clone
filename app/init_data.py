"""
Initialize default data on app startup.
"""

from app.services import facade


def init_default_admin():
    """Create default admin user if it doesn't exist."""
    
    admin_email = "admin@hbnb.com"
    admin_password = "admin123"
    
    # Check if admin already exists
    existing_admin = facade.get_user_by_email(admin_email)
    
    if not existing_admin:
        print("Creating default admin user...")
        
        try:
            admin_data = {
                'first_name': 'Admin',
                'last_name': 'User',
                'email': admin_email,
                'password': admin_password
            }
            
            admin_user = facade.create_user(admin_data)
            admin_user._is_admin = True
            
            print(f"✓ Admin user created")
            print(f"  Email: {admin_email}")
            print(f"  Password: {admin_password}")
            print(f"  ID: {admin_user.id}")
        except Exception as e:
            print(f"✗ Failed to create admin: {e}")
    else:
        # Ensure admin flag is set
        if not existing_admin.is_admin:
            existing_admin._is_admin = True
            print(f"✓ Admin user promoted: {admin_email}")
