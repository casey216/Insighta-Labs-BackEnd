import os
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.server import app
from app.db.database import init_db, get_db, Base, engine


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Initializes in-memory test DB once for the whole test session"""
    init_db(test=True)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """Yields a DB session that rolls back after each test"""
    with engine.connect() as connection:
        transaction = connection.begin()

        with Session(connection) as session:
            yield session

        transaction.rollback()


@pytest.fixture(scope="function")
def client(db_session):
    """FASTApi Test client with DB dependency overridden."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()