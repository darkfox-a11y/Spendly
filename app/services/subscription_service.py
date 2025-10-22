from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Subscription, User
from decimal import Decimal
from app.services.ai_categorizer import predict_category


def create_subscription(db: Session, user: User, sub_data):
    """
    Create a new subscription for the authenticated user.
    Updates user's budget current_spent if a budget exists.
    """

    # ✅ Ensure the user exists in DB
    user_in_db = db.query(User).filter(User.id == user.id).first()
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    # ✅ Require existing budget before adding subscription
    if not user_in_db.budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You must create a budget before adding subscriptions."
        )

    # ✅ Normalize and validate input
    data = sub_data.model_dump()

    try:
        data["price"] = Decimal(str(data["price"]))  # precision-safe conversion
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid price format."
        )
    

    projected_spent = (
        user_in_db.budget.current_spent or Decimal("0.00")
    ) + data["price"]
    
    # Enforce budget limit unless over-limit is allowed
    if projected_spent > user.budget.monthly_limit and not user_in_db.budget.allow_over_limit:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
             detail=f"Cannot add subscription — exceeds monthly budget limit of ₹{user_in_db.budget.monthly_limit}. "
                   f"Your projected spend would be ₹{projected_spent}."
        )
    
    # ✅ Categorize subscription if category not provided
    if not data.get("category") or data.get("category", "").lower() == "other":
        # Call categorizer and update the data dictionary
        data["category"] = predict_category(data.get("name"), data.get("description"))

    # ✅ Create subscription linked to user
    new_sub = Subscription(**data, owner=user_in_db)
    db.add(new_sub)
    db.commit()
    db.refresh(new_sub)

    # ✅ Update current_spent safely (Decimal arithmetic)
    user_in_db.budget.current_spent = (
        user_in_db.budget.current_spent or Decimal("0.00")
    ) + new_sub.price

    db.commit()
    db.refresh(user_in_db.budget)

    # ✅ Return ORM object (will serialize via from_attributes=True)
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


def delete_subscription(db: Session, sub_id: int, user: User):
    """
    Delete a subscription and update user's budget current_spent accordingly.
    """
    sub = db.query(Subscription).filter(
        Subscription.id == sub_id,
        Subscription.owner_id == user.id
    ).first()

    if not sub:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found."
        )

    user_in_db = db.query(User).filter(User.id == user.id).first()
    if not user_in_db or not user_in_db.budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User or budget not found."
        )

    # ✅ Subtract this subscription's price from current_spent
    current_spent = user_in_db.budget.current_spent or Decimal("0.00")
    user_in_db.budget.current_spent = max(
        Decimal("0.00"),
        current_spent - sub.price
    )

    db.delete(sub)
    db.commit()
    db.refresh(user_in_db.budget)

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
