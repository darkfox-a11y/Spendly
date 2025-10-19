from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.db.models import Budget, User
from app.schemas.budget_schema import BudgetCreate, BudgetUpdate
from decimal import Decimal

def create_budget(db: Session, user: User, budget_data: BudgetCreate):
    """
    Create a new budget for the authenticated user.
    Ensures the user exists, enforces one-budget-per-user,
    and uses ORM relationship (user=user) to avoid lazy-load issues.
    """
    #  Ensure the user still exists in the DB (token could be stale)
    user_in_db = db.query(User).filter(User.id == user.id).first()
    if not user_in_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    #  Enforce one budget per user
    if user_in_db.budget:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Budget already exists for this user."
        )

    #  ORM-native relationship assignment (fills user_id automatically)
    new_budget = Budget(
        monthly_limit=budget_data.monthly_limit,
        current_spent=Decimal("0.00"),
        user=user_in_db
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

    # Pydantic v2: model_dump (instead of dict)
    for field, value in budget_data.model_dump(exclude_unset=True).items():
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
