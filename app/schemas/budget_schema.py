from pydantic import BaseModel
from decimal import Decimal
from typing import Optional

# ---------- BASE ----------
class BudgetBase(BaseModel):
    monthly_limit: Decimal

# ---------- CREATE ----------
class BudgetCreate(BudgetBase):
    pass

# ---------- UPDATE ----------
class BudgetUpdate(BaseModel):
    monthly_limit: Optional[Decimal] = None

# ---------- RESPONSE ----------
class BudgetResponse(BudgetBase):
    id: int
    current_spent: Decimal

    class Config:
        from_attributes = True

# ---------- SUMMARY ----------
class BudgetSummary(BaseModel):
    monthly_limit: Decimal
    current_spent: Decimal
    remaining: Decimal
