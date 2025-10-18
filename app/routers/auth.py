# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.auth_service import register_user, login_user, get_current_user
from app.core.security import verify_access_token
from app.db.models import User
from app.main import limiter

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

oauth2scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")



@router.post("/register", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(user_data:UserCreate, db:Session = Depends(get_db)):
    """Endpoint to register a new user."""
    new_user = register_user(db, user_data.username, user_data.email, user_data.password)
    return new_user




@router.post("/login", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
def login(user_data:UserLogin, db:Session = Depends(get_db)):
    """Endpoint to login a user and return JWT token."""
    token_data = login_user(db, user_data.email, user_data.password)
    return token_data   





@router.get("/me", response_model=UserResponse)
@limiter.limit("15/minute")
def read_current_user(db:Session = Depends(get_db), token:str = Depends(oauth2scheme)):
    """Endpoint to get the current logged-in user."""
    curr_user = get_current_user(db, token)
    if not curr_user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"},
        )
    return curr_user