# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr

# ---------- USER BASE ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr

# ---------- USER CREATE ----------
class UserCreate(UserBase):
    password: str  # only for registration

# ---------- USER RESPONSE ----------
class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True
