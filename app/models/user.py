"""
User model - represents users in the database
This defines the structure of user data
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    """
    User model for storing user information
    Base is the parent class that makes this a database table
    """
    __tablename__ = "users"  # Name of the table in database
    
    # Define columns (fields) in the users table
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each user
    email = Column(String, unique=True, index=True, nullable=False)  # User's email
    username = Column(String, unique=True, index=True, nullable=False)  # Username
    hashed_password = Column(String, nullable=False)  # Encrypted password
    full_name = Column(String)  # User's full name
    is_active = Column(Boolean, default=True)  # Is account active?
    is_admin = Column(Boolean, default=False)  # Is user an admin?
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # When created
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())  # When last updated