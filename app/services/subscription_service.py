from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Subscription, User
from decimal import Decimal


def create_subscription(db: Session, user: User, sub_data):
    """
    Create a new subscription for the authenticated user.
    Updates user's budget current_spent if a budget exists.
    """
    # ✅ Ensure the user still exists
    user_in_db = db.query(User).filter(User.id == user.id).first()
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # ✅ Check if user has a budget before adding subscription
    if not user_in_db.budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must create a budget before adding subscriptions."
        )

    # ✅ Normalize and create subscription
    data = sub_data.model_dump()
    data["price"] = Decimal(str(data["price"]))  # ensure Decimal precision

    new_sub = Subscription(**data, owner=user_in_db)
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    # ✅ Update budget spending
    user_in_db.budget.current_spent += new_sub.price
    db.commit()
    db.refresh(user_in_db.budget)

    return new_sub


def get_subscriptions(db: Session, user_id: int):
    """
    Retrieve all subscriptions for a given user.
    """
    return db.query(Subscription).filter(Subscription.owner_id == user_id).all()


def get_subscription_by_id(db: Session, sub_id: int, user_id: int):
    """
    Retrieve a specific subscription by its ID for the given user.
    """
    sub = db.query(Subscription).filter(
        Subscription.id == sub_id,
        Subscription.owner_id == user_id
    ).first()

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found."
        )

    return sub


def update_subscription(db: Session, sub_id: int, user_id: int, sub_data):
    """
    Update an existing subscription's details.
    """
    sub = get_subscription_by_id(db, sub_id, user_id)

    for field, value in sub_data.model_dump(exclude_unset=True).items():
        setattr(sub, field, value)

    db.commit()
    db.refresh(sub)
    return sub


def delete_subscription(db: Session, sub_id: int, user_id: int):
    """
    Delete a subscription for a user and adjust budget spending if a budget exists.
    """
    sub = db.query(Subscription).filter(
        Subscription.id == sub_id,
        Subscription.owner_id == user_id
    ).first()

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found."
        )

    # ✅ Ensure user still exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # ✅ Ensure user has a budget before adjusting spending
    if not user.budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify spending — no budget found for this user."
        )

    # ✅ Deduct spending safely (never negative)
    new_value = user.budget.current_spent - sub.price
    if new_value < 0:
        new_value = Decimal("0.00")

    user.budget.current_spent = new_value
    db.commit()
    db.refresh(user.budget)

    # ✅ Delete the subscription
    db.delete(sub)
    db.commit()

    return {"message": "Subscription deleted successfully"}


def get_subscription_by_name(db: Session, name: str, user_id: int):
    """
    Retrieve subscriptions by name (case-insensitive partial match).
    """
    subs = db.query(Subscription).filter(
        Subscription.owner_id == user_id,
        Subscription.name.ilike(f"%{name}%")
    ).all()

    if not subs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No subscriptions found matching '{name}'."
        )

    return subs
