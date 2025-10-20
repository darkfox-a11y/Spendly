from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.budget_schema import (
    BudgetCreate,
    BudgetUpdate,
    BudgetResponse,
    BudgetSummary
)
from app.services.budget_service import (
    create_budget,
    get_budget,
    update_budget,
    delete_budget,
    get_budget_summary
)
from app.services.auth_service import get_current_user
from app.core.rate_limiter import limiter  # Use this instead
from app.db.models import User, Budget
from fastapi import HTTPException


router = APIRouter(prefix="/budget", tags=["Budget"])

# ---------- CREATE ----------
@router.post("/", response_model=BudgetResponse, status_code=status.HTTP_201_CREATED)
@limiter.limit("3/minute")
def add_budget(
    request: Request,
    budget_data: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_budget(db, current_user, budget_data)

# ---------- READ ----------
@router.get("/", response_model=BudgetResponse)
@limiter.limit("10/minute")
def read_budget(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_budget(db, current_user.id)

# ---------- UPDATE ----------
@router.put("/", response_model=BudgetResponse)
@limiter.limit("5/minute")
def modify_budget(
    request: Request,
    budget_data: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_budget(db, current_user.id, budget_data)

# ---------- DELETE ----------
@router.delete("/", status_code=status.HTTP_200_OK)
@limiter.limit("3/minute")
def remove_budget(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_budget(db, current_user.id)

# ---------- SUMMARY ----------
@router.get("/summary", response_model=None)
@limiter.limit("10/minute")
def budget_summary(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_budget_summary(db, current_user.id)

#------------TOGGLE ALLOW OVER LIMIT -----------
@router.patch("/toggle-overlimit")
def toggle_over_limit(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    budget = db.query(Budget).filter(Budget.user_id == current_user.id).first()
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    budget.allow_over_limit = not budget.allow_over_limit
    db.commit()
    db.refresh(budget)
    return {"allow_over_limit": budget.allow_over_limit}

