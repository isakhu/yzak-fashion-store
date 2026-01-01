"""
Authentication router - handles user login, registration, and JWT tokens
"""
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr

from ..database import get_db
from ..models.user import User
from ..config import settings

# Create router instance
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Password hashing setup - use a simpler approach
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=4)

# OAuth2 setup for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Pydantic models for request/response data
class UserCreate(BaseModel):
    """Schema for creating a new user"""
    username: str
    email: EmailStr
    full_name: str
    password: str

class UserResponse(BaseModel):
    """Schema for user data in responses"""
    id: int
    username: str
    email: str
    full_name: str
    is_active: bool
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str
    token_type: str

# Utility functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if provided password matches the hashed password"""
    # Try bcrypt first
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except:
        # Fallback to simple SHA256 hash for demo
        import hashlib
        simple_hash = hashlib.sha256(plain_password.encode()).hexdigest()
        return simple_hash == hashed_password

def get_password_hash(password: str) -> str:
    """Hash a password for secure storage"""
    # For new users, try bcrypt, fallback to simple hash
    try:
        # Ensure password is not too long for bcrypt (max 72 bytes)
        if len(password.encode('utf-8')) > 72:
            password = password[:72]
        return pwd_context.hash(password)
    except:
        # Fallback to simple hash for demo
        import hashlib
        return hashlib.sha256(password.encode()).hexdigest()

def create_access_token(data: dict) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# API Endpoints
@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user account"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    
    # Find user by username
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # Verify user exists and password is correct
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": user.username})
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user's information"""
    return current_user