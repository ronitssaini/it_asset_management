from backend.database.session import SessionLocal
from backend.models.user import User
from backend.auth.security import get_password_hash

# --- EDIT THESE VALUES ---
USERNAME = "admin"
EMAIL = "admin@example.com"
PASSWORD = "admin123"
ROLE = "admin"  # or "manager"
# ------------------------

def create_user():
    db = SessionLocal()
    try:
        # Check if user already exists
        existing = db.query(User).filter((User.username == USERNAME) | (User.email == EMAIL)).first()
        if existing:
            print(f"User with username '{USERNAME}' or email '{EMAIL}' already exists.")
            return
        hashed_password = get_password_hash(PASSWORD)
        user = User(
            username=USERNAME,
            email=EMAIL,
            hashed_password=hashed_password,
            role=ROLE,
            is_active=True
        )
        db.add(user)
        db.commit()
        print(f"User '{USERNAME}' created successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_user() 