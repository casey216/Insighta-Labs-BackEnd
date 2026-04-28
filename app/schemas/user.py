from enum import StrEnum

from pydantic import BaseModel, EmailStr


class RoleEnum(StrEnum):
    ADMIN = "admin"
    ANALYST = "analyst"


class UserCreate(BaseModel):
    github_id: str
    username: str
    email: EmailStr
    avatar_url: str
    role: RoleEnum
    is_active: bool


class UserOut(BaseModel):
    id: str
    github_id: str
    username: str
    email: EmailStr
    avatar_url: str
    role: str
    is_active: str
    last_login_at: str
    created_at: str


class UserUpdate(BaseModel):
    github_id: str
    username: str
    email: EmailStr
    avatar_url: str
    role: RoleEnum
    is_active: bool
