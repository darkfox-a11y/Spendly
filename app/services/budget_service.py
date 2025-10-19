# app/services/budget_service.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Budget, User
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
    budget = db.query(Budget).filter(Budget.user_id == user_id).first()
    if not budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")

    db.delete(budget)
    db.commit()
    return {"message": "Budget deleted successfully"}


def get_budget_summary(db: Session, user_id: int):
    budget = get_budget(db, user_id)
    remaining = budget.monthly_limit - budget.current_spent
    return {
        "monthly_limit": budget.monthly_limit,
        "current_spent": budget.current_spent,
        "remaining": remaining
    }