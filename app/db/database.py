"""The Database Module"""
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from app.core.settings import settings, BASE_DIR


def _build_database_url(test: bool = False) -> tuple[str, dict]:
    """
    Construct the database URL and engine connection args based on config.
    Returns (URL, connect_args).
    """
    connect_args = {}

    if test:
        return "sqlite:///:memory:", {"check_same_thread": False}
    
    if settings.DB_TYPE == "sqlite":
        url = f"sqlite:///{BASE_DIR}/{settings.DB_NAME}.db"
        connect_args["check_same_thread"] = False
        return url, connect_args

    if settings.DB_TYPE == "vercel":
        url = "sqlite:////tmp/db.sqlite3"
        connect_args["check_same_thread"] = False
        return url, connect_args
    
    if settings.DB_TYPE == "postgresql":
        url = (
            f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        )
        return url, connect_args
    
    raise ValueError(f"Unsupported DB type: {settings.DB_TYPE}")
    

def get_db_engine(test: bool = False):
    url, connect_args = _build_database_url(test=test)

    kwargs: dict[str, Any] = {"connect_args": connect_args} if connect_args else {}

    if not url.startswith("sqlite"):
        kwargs.update(
            {
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": True,
                "pool_recycle": 1800,
            }
        )

    return create_engine(url, echo=False, **kwargs)


class Base(DeclarativeBase):
    pass

engine = None
SessionLocal: sessionmaker[Session] | None = None

def init_db(test: bool = False) -> None:
    """Init the database engine and factory session.
    Create all tables defined in the ORM.
    """
    global engine, SessionLocal

    if SessionLocal is not None:
        return
    
    engine = get_db_engine(test=test)
    SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)



def get_db():
    """FastAPI dependency that yields a database session."""
    if SessionLocal is None:
        raise RuntimeError("Database not initialized. Run init_db() first.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
