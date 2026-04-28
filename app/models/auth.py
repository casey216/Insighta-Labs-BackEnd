import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = "refreshtokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc) + timedelta(minutes=5)
    )
    used: Mapped[bool] = mapped_column(Boolean)

    user: Mapped["User"] = relationship("User", back_populates="tokens")    # noqa: F821
