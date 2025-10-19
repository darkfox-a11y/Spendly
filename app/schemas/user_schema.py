# app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, ConfigDict

# ---------- USER BASE ----------
class UserBase(BaseModel):
    username: str
    email: EmailStr

# ---------- USER CREATE ----------
class UserCreate(UserBase):
    password: str  # Only for registration

# ---------- USER LOGIN ----------
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# ---------- USER RESPONSE ----------
class UserResponse(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
