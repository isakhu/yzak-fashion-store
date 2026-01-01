"""
Database configuration and setup
This file handles the database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# Create database engine
# Engine is like the "connection factory" to your database
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Create session factory
# Sessions are used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all database models
Base = declarative_base()

def get_db():
    """
    Dependency function to get database session
    This ensures each request gets its own database session
    """
    db = SessionLocal()
    try:
        yield db  # Provide the session to the request
    finally:
        db.close()  # Always close the session when done