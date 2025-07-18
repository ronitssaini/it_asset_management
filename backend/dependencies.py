from sqlalchemy.orm import Session
from backend.database.session import SessionLocal

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()     