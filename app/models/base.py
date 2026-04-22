import uuid
from datetime import date, datetime
from typing import Any

from sqlalchemy import inspect
from sqlalchemy.orm import Mapper


def _mapper(obj: object) -> Mapper:
    """Returns the mapper for a model instance"""
    return inspect(obj, raiseerr=True).mapper


def _serialize(value: Any) -> Any:
    """Coerce non-JSON-native types to serializable equivalents."""
    if isinstance(value, uuid.UUID):
        return str(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    return value


class ReprMixin:
    """Adds a helpful __repr__ to any SQLAlchemy model."""

    def __repr__(self) -> str:
        mapper = _mapper(self)
        pk_names = [col.key for col in mapper.primary_key if col.key is not None]
        pk_pairs = ", ".join(
            f"{name}={getattr(self, name)!r}" for name in pk_names
        )
        return f"<{self.__class__.__name__}({pk_pairs})"
    

class ToDictMixin:
    """Adss a to_dict() method to any SQLAlchemy model."""

    def to_dict(self, exclude: set[str] | None = None) -> dict[str, Any]:
        """
        Serialize mapped columns to a plain dict.
        
        Args:
            exclude: Optional set of columns to omit (e.g. {"password"}).
            
        Returns:
            A dict of {column_name: value} for all mapped columns.
        """
        exclude = exclude or set()
        mapper = _mapper(self)
        return {
            col.key: getattr(self, col.key)
            for col in mapper.column_attrs
            if col.key is not None and col.key not in exclude
        }
    

class ModelMixin(ReprMixin, ToDictMixin):
    pass