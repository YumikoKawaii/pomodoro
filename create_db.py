"""
Database initialization script
Run this to create all tables in the database
"""
from app.core.database import engine
from app.db.models import Base

def create_database():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_database()