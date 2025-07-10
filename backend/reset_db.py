from backend.database.session import Base, engine
from backend.models.asset import Asset

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

print("Database tables dropped and recreated successfully.")
