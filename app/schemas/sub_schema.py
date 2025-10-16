# app/schemas/sub_schema.py
from pydantic import BaseModel
from datetime import date

class SubscriptionBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    renewal_date: date

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionResponse(SubscriptionBase):
    id: int
    category: str
    owner_id: int

    class Config:
        orm_mode = True
