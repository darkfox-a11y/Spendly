from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Subscription

def create_subscription(db: Session, user, sub_data):
    """
    Create a new subscription for the authenticated user.
    Uses ORM relationship (owner=user) instead of raw FK (owner_id).
    """
    new_sub = Subscription(
        **sub_data.dict(),
        owner=user  # ORM relationship usage
    )
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)
    return new_sub


def get_subscriptions(db: Session, user_id: int):
    return db.query(Subscription).filter(Subscription.owner_id == user_id).all()


def get_subscription_by_id(db: Session, sub_id: int, user_id: int):
    sub = db.query(Subscription).filter(
        Subscription.id == sub_id,
        Subscription.owner_id == user_id
    ).first()
    if not sub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    return sub


def update_subscription(db: Session, sub_id: int, user_id: int, sub_data):
    sub = get_subscription_by_id(db, sub_id, user_id)
    for field, value in sub_data.dict(exclude_unset=True).items():
        setattr(sub, field, value)
    db.commit()
    db.refresh(sub)
    return sub


def delete_subscription(db: Session, sub_id: int, user_id: int):
    sub = get_subscription_by_id(db, sub_id, user_id)
    db.delete(sub)
    db.commit()
    return {"message": "Subscription deleted successfully"}


def get_subscription_by_name(db: Session, name: str, user_id: int):
    sub = db.query(Subscription).filter(
        Subscription.owner_id == user_id,
        Subscription.name.ilike(f"%{name}%")  # case-insensitive partial match
    ).all()

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No subscriptions found matching '{name}'"
        )
    return sub
