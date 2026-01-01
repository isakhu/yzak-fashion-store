"""
Configuration settings for the e-commerce API
This file manages all the settings and environment variables
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings class"""
    
    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecommerce.db")
    
    # Security settings
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # Application settings
    APP_NAME = "E-Commerce API"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Create a global settings instance
settings = Settings()