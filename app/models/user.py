import uuid
from datetime import datetime
from uuid_extensions import uuid7

from sqlalchemy import UUID, String, DateTime, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid7)
    github_id: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, index=True)
    avatar_url: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String, default="analyst")
    is_active: Mapped[bool] = mapped_column(Boolean)
    last_login_at: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
