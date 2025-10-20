from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.schemas.sub_schema import SubscriptionCreate, SubscriptionUpdate, SubscriptionResponse
from app.services.subscription_service import (
    create_subscription,
    get_subscriptions,
    get_subscription_by_id,
    update_subscription,
    delete_subscription,
    get_subscription_by_name
)
from app.services.auth_service import get_current_user
from app.core.rate_limiter import limiter
from app.db.models import User


router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])

# ---------- CREATE ----------
@router.post("/", response_model=None, status_code=status.HTTP_201_CREATED)
def create_subscription_route(
    sub_data: SubscriptionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_sub = create_subscription(db=db, user=current_user, sub_data=sub_data)
    return new_sub

# ---------- READ ALL ----------
@router.get("/", response_model=List[SubscriptionResponse])
@limiter.limit("10/minute")
def list_subscriptions(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ Added type annotation
):
    return get_subscriptions(db, current_user.id)


# ---------- SEARCH BY NAME ----------
@router.get("/search/", response_model=List[SubscriptionResponse])
@limiter.limit("10/minute")
def search_subscriptions(
    request: Request,
    name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ Added type annotation
):
    """
    Search subscriptions by name (case-insensitive, partial match).
    Example: /subscriptions/search/?name=netflix
    """
    return get_subscription_by_name(db, name, current_user.id)

# ---------- READ SINGLE ----------
@router.get("/{sub_id}", response_model=SubscriptionResponse)
@limiter.limit("10/minute")
def read_subscription(
    request: Request,
    sub_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ Added type annotation
):
    return get_subscription_by_id(db, sub_id, current_user.id)

# ---------- UPDATE ----------
@router.put("/{sub_id}", response_model=SubscriptionResponse)
@limiter.limit("5/minute")
def modify_subscription(
    request: Request,
    sub_id: int,
    sub_data: SubscriptionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ Added type annotation
):
    return update_subscription(db, sub_id, current_user.id, sub_data)

# ---------- DELETE ----------
@router.delete("/{sub_id}", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def remove_subscription(
    request: Request,
    sub_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)  # ✅ Added type annotation
):
    return delete_subscription(db, sub_id, current_user)

