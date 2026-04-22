import uuid
from datetime import datetime, timezone
from uuid_extensions import uuid7

from sqlalchemy import UUID, String, Float, Integer, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base
from .base import ModelMixin


class BaseModel(Base, ModelMixin):
    """
    Project base class — all models inherit __repr__ and to_dict()
    automatically just by extending Base.
    """
    
    __abstract__ = True


class Profile(BaseModel):
    __tablename__ = "profiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid7)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    gender: Mapped[str] = mapped_column(String(100))
    gender_probability: Mapped[float] = mapped_column(Float)
    age: Mapped[float] = mapped_column(Integer)
    age_group: Mapped[str] = mapped_column(String(100))
    country_id: Mapped[str] = mapped_column(String(2))
    country_name: Mapped[str] = mapped_column(String(100))
    country_probability: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())