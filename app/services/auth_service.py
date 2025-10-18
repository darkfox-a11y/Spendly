from fastapi import HTTPException, status
from jose import JWTError, jwt
from app.core.config import settings
from app.db.models import User
from app.core.security import verify_password,hash_password,create_access_token,verify_access_token
from sqlalchemy.orm import Session
from datetime import timedelta
from app.schemas.user_schema import UserResponse

def register_user(db:Session,username:str,email:str,password:str)->UserResponse:
    """register a new user with hashed password."""
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
            )
    
    hashed_pwd = hash_password(password)
    new_user = User(
        username=username,
        email=email,
        hashed_password=hashed_pwd
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }

def login_user(db:Session,email:str,password:str):
    """Authenticate user and return JWT token."""

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate":"Bearer"},
        )

    if not verify_password(password,hashed_password=user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate":"Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data = {"sub":user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token":access_token,
        "token_type":"bearer"
    }


def get_current_user(db:Session,token:str):
    """Retrieve current user based on JWT token."""
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    email = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email
    )

