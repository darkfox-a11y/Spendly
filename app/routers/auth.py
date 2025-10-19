# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import register_user, login_user, get_current_user
from app.db.models import User
from app.core.rate_limiter import limiter

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(
    request: Request,
    user_data: UserCreate, 
    db: Session = Depends(get_db)
):
    """Endpoint to register a new user."""
    new_user = register_user(db, user_data.username, user_data.email, user_data.password)
    return new_user


@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login.
    Use email in the 'username' field.
    """
    # form_data.username will contain the email
    token_data = login_user(db, form_data.username, form_data.password)
    return token_data


@router.get("/me", response_model=UserResponse)
@limiter.limit("15/minute")
def read_current_user(
    request: Request,
    current_user: User = Depends(get_current_user)
):
    """Endpoint to get the current logged-in user."""
    return current_user