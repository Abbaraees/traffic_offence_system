from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash

def create_admin():
    app = create_app()
    with app.app_context():
        # Check if the admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin is None:
            # Create the admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123', method='sha256'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists.")

if __name__ == '__main__':
    create_admin()