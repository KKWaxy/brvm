"""
Authentication routes.
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session

from app.auth import (
    create_access_token,
    hash_password,
    verify_password,
    verify_token,
)
from app.config import settings
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, TokenResponse, LoginRequest

router = APIRouter(tags=["Auth"])


@router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    
    **Request body:**
    - `email`: User email (must be unique)
    - `username`: Username (3-100 chars, must be unique)
    - `password`: Password (min 8 chars)
    - `full_name`: Optional full name
    """
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered",
        )
    
    # Create new user
    hashed_password = hash_password(user_data.password)
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_password,
        full_name=user_data.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Create access token
    access_token_expires = timedelta(hours=settings.jwt_expiration_hours)
    access_token = create_access_token(
        data={"sub": str(db_user.id)},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": db_user,
    }


@router.post("/auth/login", response_model=TokenResponse)
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    """
    Login with email and password.
    
    **Request body:**
    - `email`: User email
    - `password`: User password
    """
    user = db.query(User).filter(User.email == login_data.email).first()
    
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Create access token
    access_token_expires = timedelta(hours=settings.jwt_expiration_hours)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires,
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user,
    }


@router.get("/auth/me", response_model=UserResponse)
async def get_me(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    """
    Get current authenticated user information.
    
    **Headers:**
    - `Authorization`: `Bearer <token>`
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        from uuid import UUID
        
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise ValueError("Invalid authorization header format")
        
        token = parts[1]
        payload = verify_token(token)
        user_id_str = payload.get("sub")
        
        if not user_id_str:
            raise ValueError("No sub in token")
        
        # Convert string ID to UUID
        user_id = UUID(user_id_str)
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            raise ValueError("User not found")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
