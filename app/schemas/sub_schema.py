from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class SubscriptionBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    renewal_date: str
    category: Optional[str] = None


class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    renewal_date: Optional[str] = None
    category: Optional[str] = None


class SubscriptionResponse(SubscriptionBase):
    id: int
    owner_id: int

    # ✅ The only correct way in Pydantic v2
    model_config = ConfigDict(from_attributes=True)
