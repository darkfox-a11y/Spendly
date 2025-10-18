from datetime import timedelta, datetime,timezone
from jose import JWTError, jwt
from app.core.config import settings
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""Security utilities for password hashing and JWT token management."""
def hash_password(password:str)->str:
    return pwd_context.hash(password)

"""Verify a plain password against its hashed version."""
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password, hashed_password)

"""Create a JWT access token with an optional expiration time."""
def create_access_token(data:dict,expires_delta:timedelta|None = None)->str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp":expire})   
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

"""Verify and decode a JWT access token."""
def verify_access_token(token:str)->dict|None:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None
