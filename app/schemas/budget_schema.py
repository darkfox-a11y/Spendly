# app/schemas/budget_schema.py
from pydantic import BaseModel

class BudgetBase(BaseModel):
    monthly_limit: float

class BudgetCreate(BudgetBase):
    pass

class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    current_spent: float

    class Config:
        orm_mode = True
