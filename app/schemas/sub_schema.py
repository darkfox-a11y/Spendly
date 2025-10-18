from pydantic import BaseModel
from typing import Optional

# ---------- BASE ----------
class SubscriptionBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    renewal_date: str
    category: str

# ---------- CREATE ----------
class SubscriptionCreate(SubscriptionBase):
    pass  # same as base, but allows future extension

# ---------- UPDATE ----------
class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    renewal_date: Optional[str] = None
    category: Optional[str] = None

# ---------- RESPONSE ----------
class SubscriptionResponse(SubscriptionBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True
