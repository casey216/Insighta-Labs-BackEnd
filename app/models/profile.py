import uuid
from datetime import datetime
from uuid_extensions import uuid7

from sqlalchemy import UUID, String, Float, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel


class Profile(BaseModel):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID, primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    gender: Mapped[str] = mapped_column(String(100), index=True)
    gender_probability: Mapped[float] = mapped_column(Float)
    age: Mapped[float] = mapped_column(Integer, index=True)
    age_group: Mapped[str] = mapped_column(String(100), index=True)
    country_id: Mapped[str] = mapped_column(String(2), index=True)
    country_name: Mapped[str] = mapped_column(String(100))
    country_probability: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), index=True)
