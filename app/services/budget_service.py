# app/services/budget_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Budget, User,Subscription
from app.schemas.budget_schema import BudgetCreate, BudgetUpdate
from decimal import Decimal

def create_budget(db: Session, user: User, budget_data: BudgetCreate):
    """
    Create a new budget for the authenticated user.
    Ensures one-budget-per-user.
    """
    # Check if budget already exists by querying directly
    existing_budget = db.query(Budget).filter(Budget.user_id == user.id).first()
    
    if existing_budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this user."
        )

    # Create new budget
    new_budget = Budget(
        monthly_limit=budget_data.monthly_limit,
        current_spent=Decimal("0.00"),
        user_id=user.id  # Use user_id directly instead of user relationship
    )

    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return new_budget


def get_budget(db: Session, user_id: int):
    budget = db.query(Budget).filter(Budget.user_id == user_id).first()
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found for this user."
        )
    return budget


def update_budget(db: Session, user_id: int, budget_data: BudgetUpdate):
    budget = db.query(Budget).filter(Budget.user_id == user_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    # ✅ Preserve current_spent unless explicitly passed
    update_data = budget_data.model_dump(exclude_unset=True)

    if "current_spent" not in update_data:
        update_data["current_spent"] = budget.current_spent

    for field, value in update_data.items():
        setattr(budget, field, value)

    db.commit()
    db.refresh(budget)
    return budget



def delete_budget(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()

    if not user or not user.budget:
        raise HTTPException(status_code=404, detail="Budget not found")

    # ✅ Delete all subscriptions for this user first
    db.query(Subscription).filter(Subscription.owner_id == user_id).delete()

    # ✅ Then delete the budget itself
    db.delete(user.budget)
    db.commit()

    return {"message": "Budget and all related subscriptions deleted successfully"}



def get_budget_summary(db: Session, user_id: int):
    budget = get_budget(db, user_id)

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found for this user."
        )
    
    monthly_limit = Decimal(budget.monthly_limit or 0)
    current_spent = Decimal(budget.current_spent or 0)
    remaining = monthly_limit - current_spent   
    limit_exceeded = current_spent > monthly_limit

    return {
        "monthly_limit": monthly_limit,
        "current_spent": current_spent,
        "remaining": max(remaining, Decimal("0.00")),
        "limit_exceeded": limit_exceeded,
        "allow_over_limit": budget.allow_over_limit,
        "status": ("Over Limit" if limit_exceeded else "Within Limit"),
        "insight": (
            "You have exceeded your monthly budget. Consider reviewing subscriptions."
            if limit_exceeded and not budget.allow_over_limit else
            "You are over your limit but overspending is allowed."
            if limit_exceeded and budget.allow_over_limit else
            "You are spending within your set budget. Keep it up!"
        )

    }
