import uuid
from datetime import datetime, timedelta, timezone
from uuid_extensions import uuid7

from sqlalchemy import UUID, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = "refreshtokens"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    used: Mapped[bool] = mapped_column(Boolean)
