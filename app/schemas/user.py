from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    firebase_id: str
    role: UserRole.USER
    organization_name: str | None = None

class UserUpdate(BaseModel):
    username: str | None = None
    role: UserRole | None = None
    organization_name: str | None = None

class UserResponse(UserBase):
    id: int
    firebase_id: str
    role: UserRole
    organization_name: str | None = None
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)